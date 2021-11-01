import React from 'react';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';

const Loader = ({ size }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        height: '100%',
        alignItems: 'center',
        padding: '5px',
      }}
    >
      <CircularProgress size={size || 40} />
    </Box>
  );
};

export default Loader;
