import React from 'react';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';

const Loader = () => {
  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', height: '100%', alignItems: 'center' }}>
      <CircularProgress />
    </Box>
  );
};

export default Loader;
