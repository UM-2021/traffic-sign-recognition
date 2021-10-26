import * as React from 'react';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Chart from '../components/Chart';
import CardWithNumber from '../components/CardWithNumber';
import SignTable from '../components/Table';
import axios from 'axios';
import Loader from '../components/Loader';

function DashboardContent() {
  const [totalSigns, setTotalSigns] = React.useState(0);
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    const fetchSigns = async () => {
      setLoading(true);
      const signs = await axios(`http://${process.env.REACT_APP_IP_ADDRESS}:3000/signs/locations`);
      setTotalSigns(signs.data.results);
      setLoading(false);
    };
    fetchSigns();
  }, []);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Chart */}
        <Grid item xs={12} md={8} lg={9}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 240,
            }}
          >
            <Chart />
          </Paper>
        </Grid>
        <Grid item xs={12} md={4} lg={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 240,
            }}
          >
            {loading ? (
              <Loader />
            ) : (
              <CardWithNumber number={totalSigns} title="Señales detectadas" />
            )}
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <SignTable />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default function Dashboard() {
  return <DashboardContent />;
}
