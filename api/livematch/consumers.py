import logging
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings
from django.db import transaction

from core.util import Move, is_livematch_id

from .models import LiveMatch
from .serializers import (
    get_client_msg_serializer,
    ErrorSerializer,
    ClientMessageType,
    LiveMatchPlayerStateSerializer,
)
from .error import ClientError, ClientErrorType

logger = logging.getLogger(settings.RPS_LOGGER_NAME)


def validate_content(content):
    # Get the message type
    try:
        msg_type = content["type"]
    except KeyError:
        raise ClientError(
            ClientErrorType.MALFORMED_MESSAGE, detail="Missing type"
        )

    # Look up the correct serializer for this type and try to deserialize
    serializer_cls = get_client_msg_serializer(msg_type)
    serializer = serializer_cls(data=content)
    if not serializer.is_valid():
        raise ClientError(
            ClientErrorType.MALFORMED_MESSAGE, detail=serializer.errors
        )
    return serializer.validated_data


class MatchConsumer(JsonWebsocketConsumer):
    """
    In general, this consumer should accept all connection and keep them open.
    Anything that goes wrong in terms of input/state/etc. should be reported
    as an error over the socket, but still left open. An actual socket error
    should indicate a bug, network error, or the like.
    """

    @property
    def channel_group_name(self):
        return f"match_{self.match_id}"

    def trigger_client_update(self):
        """
        Initiates an state update to all clients. This doesn't actuall send
        the update messages - it just triggers a group message over the Channel
        layer, which will cause an update in every consumer (including this one)
        """
        # Send the message to other consumers in the group
        async_to_sync(self.channel_layer.group_send)(
            self.channel_group_name, {"type": "match.update"}
        )

    def match_update(self, event):
        """
        Listener for match updates from other consumers on this match.

        Arguments:
            event {dict} -- The event received from the sender. Should contain
            the current match state, which will be sent to the client.
        """
        # No need to lock for read-only operation
        live_match = self.get_match(lock=False)
        self.send_json(
            LiveMatchPlayerStateSerializer(
                live_match, context={"player": self.player}
            ).data
        )

    def handle_error(self, error):
        """
        Processes the given error. An error message is send over the socket,
        but the socket is left open.

        Arguments:
            error {ClientError} -- The error
        """
        self.send_json(ErrorSerializer(error.to_dict()).data)

    def validate_match_id(self):
        """
        Checks if the match ID from the URL is valid.

        Raises:
            ClientError: If the match ID is invalid
        """
        if not is_livematch_id(self.match_id):
            raise ClientError(ClientErrorType.INVALID_MATCH_ID)

    def validate_player(self):
        if not self.player.is_authenticated:
            raise ClientError(ClientErrorType.NOT_LOGGED_IN)

    def get_match(self, lock=True):
        qs = LiveMatch.objects
        if lock:
            qs = qs.select_for_update()
        return qs.get(id=self.match_id)

    def connect_player(self):
        """
        Tries to add the authenticated player to this match.

        Raises:
            ClientError: If the game is full or this player is already in it
        """

        # Try to join the game
        with transaction.atomic():
            # Get the row and lock it
            live_match, _ = LiveMatch.objects.select_for_update().get_or_create(
                id=self.match_id
            )

            # If the player is already in the game, this will mark them as
            # connected (if they were disconnected). If they were already
            # connected, nothing happens here.
            if not live_match.connect_player(self.player):
                # Get up on outta here with your game hijacking
                raise ClientError(ClientErrorType.GAME_FULL)
            # Player was successfully added - write it to the DB
            live_match.save()
            # Join the channel group for all sockets in this match. Make sure
            # we do this BEFORE releasing the lock, to prevent missing
            # messages
            async_to_sync(self.channel_layer.group_add)(
                self.channel_group_name, self.channel_name
            )

        self.trigger_client_update()

    def disconnect_player(self):
        # Leave the channel group
        async_to_sync(self.channel_layer.group_discard)(
            self.channel_group_name, self.channel_name
        )

        # Tell the DB object we're disconnecting
        with transaction.atomic():
            try:
                live_match = self.get_match()
            except LiveMatch.DoesNotExist:
                return

            if live_match.disconnect_player(self.player):
                if live_match.is_orphaned:
                    live_match.delete()
                else:
                    live_match.save()

    def process_msg(self, msg):
        msg_type = msg["type"]
        if msg_type == ClientMessageType.HEARTBEAT.value:
            with transaction.atomic():
                live_match = self.get_match()
                live_match.heartbeat(self.player)

        elif msg_type == ClientMessageType.READY.value:
            with transaction.atomic():
                live_match = self.get_match()
                live_match.ready_up(self.player)

        elif msg_type == ClientMessageType.MOVE.value:
            with transaction.atomic():
                # If live_match doesn't exist, tenemos problemos
                live_match = self.get_match()
                live_match.apply_move(self.player, msg["move"])
                live_match.save()
        else:
            raise ClientError(
                ClientErrorType.MALFORMED_MESSAGE,
                f"Unknown message type: {msg_type}",
            )

        self.trigger_client_update()

    def connect(self):
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        self.player = self.scope["user"]
        self.accept()
        try:
            self.validate_player()
            self.validate_match_id()
            logger.info(
                f"Player {self.player} connecting to match {self.match_id}"
            )
            self.connect_player()
        except ClientError as e:
            self.handle_error(e)

    def disconnect_json(self, close_code):
        logger.info(
            f"Player {self.player} disconnecting from match {self.match_id}; code={close_code}"
        )
        try:
            self.disconnect_player()
        except ClientError as e:
            self.handle_error(e)

    def receive_json(self, content):
        try:
            msg = validate_content(content)
            self.process_msg(msg)
        except ClientError as e:
            self.handle_error(e)
