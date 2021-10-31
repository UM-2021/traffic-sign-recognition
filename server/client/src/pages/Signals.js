import { Paper } from '@mui/material';
import React from 'react';
import SignalsTable from '../components/SignalsTable';
import Layout from '../components/Layout';

const Signals = () => {
  return (
    <Layout>
      <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
        <SignalsTable />
      </Paper>
    </Layout>
  );
};

export default Signals;
