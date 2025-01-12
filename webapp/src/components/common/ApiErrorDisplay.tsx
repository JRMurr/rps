import React from 'react';
import { Typography } from '@material-ui/core';
import ErrorSnackbar from 'components/common/ErrorSnackbar';
import useStyles from 'hooks/useStyles';
import clsx from 'clsx';
import { ApiError } from 'state/api';

const ApiErrorDisplay = ({
  error,
  resourceName,
}: {
  error?: ApiError<unknown>;
  resourceName: string;
}): React.ReactElement | null => {
  const classes = useStyles();

  if (error) {
    if (error.status === 404) {
      return (
        <Typography
          className={clsx(classes.normalMessage, classes.errorMessage)}
        >
          That {resourceName} does not exist
        </Typography>
      );
    }
    return <ErrorSnackbar message="An error occurred" />;
  }
  return null;
};

ApiErrorDisplay.defaultProps = {
  resourceName: 'resource',
};

export default ApiErrorDisplay;
