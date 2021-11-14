import * as React from 'react';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Chart from '../components/Chart';
import CardWithNumber from '../components/CardWithNumber';
import SignTable from '../components/Table';
import Loader from '../components/Loader';
import Layout from '../components/Layout';
import instance from '../utils/axiosConfig';

function DashboardContent() {
  const [totalSigns, setTotalSigns] = React.useState(0);
  const [loading, setLoading] = React.useState(false);

  React.useEffect(() => {
    const fetchSigns = async () => {
      setLoading(true);
      // When converting to ISO format, timezone offset is ignored.
      const tzoffset = new Date().getTimezoneOffset() * 60000;
      const today = new Date(Date.now() - tzoffset);
      const todayStr = today.toISOString().split('T')[0];
      const signs = await instance(`/api/signs/records?identifiedAt[gte]=${todayStr}`, { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } });
      setTotalSigns(signs.data.results);
      setLoading(false);
    };
    fetchSigns();
  }, []);

  return (
    <Layout>
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
                <CardWithNumber number={totalSigns} title="Señales reconocidas" />
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
    </Layout>
  );
}

export default function Dashboard() {
  return <DashboardContent />;
}
