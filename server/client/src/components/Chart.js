import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import { LineChart, Line, XAxis, YAxis, Label, ResponsiveContainer } from 'recharts';
import Title from './Title';
import Loader from './Loader';
import instance from '../utils/axiosConfig';

// Generate Sales Data
// function createData(time, amount) {
//   return { time, amount };
// }

// const data = [
//   createData('16 Mar', 0),
//   createData('17 Mar', 23),
//   createData('18 Mar', 12),
//   createData('19 Mar', 2),
//   createData('20 Mar', 45),
//   createData('21 Mar', 39),
//   createData('22 Mar', 37),
//   createData('23 Mar', 71),
//   createData('24 Mar', 68),
// ];

const dateFormatter = (t) => {
  return t.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
};

function sameDay(d1, d2) {
  return d1.getFullYear() === d2.getFullYear() &&
    d1.getMonth() === d2.getMonth() &&
    d1.getDate() === d2.getDate();
}

export default function Chart() {
  const theme = useTheme();
  const [loading, setLoading] = React.useState(false);
  const [data, setData] = React.useState([]);

  React.useEffect(() => {
    const fetchSigns = async () => {
      setLoading(true);

      const res = await instance('/api/signs/records/date', { headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` } });
      let signs = res.data.data.data;
      signs = signs.map((s) => ({ ...s, date: new Date(s.date) }));
      let date = new Date();

      for (let i = 1; i <= 10; i++) {
        if (signs.filter(s => sameDay(s.date, date)).length === 0)
          signs.push({ date: new Date(date), count: 0 });

        date.setDate(date.getDate() - 1);
      }

      signs.sort((a, b) => (a.date > b.date ? 1 : b.date > a.date ? -1 : 0));

      setData(signs);
      setLoading(false);
    };

    fetchSigns();
  }, []);

  return (
    <React.Fragment>
      <Title>Señales reconocidas - 10 días</Title>
      <ResponsiveContainer>
        {loading ? (
          <Loader />
        ) : (
          <LineChart
            data={data}
            margin={{
              top: 16,
              right: 16,
              bottom: 0,
              left: 24,
            }}
          >
            <XAxis
              dataKey="date"
              stroke={theme.palette.text.secondary}
              style={theme.typography.body2}
              tickFormatter={dateFormatter}
            />
            <YAxis stroke={theme.palette.text.secondary} style={theme.typography.body2}>
              <Label
                angle={270}
                position="left"
                style={{
                  textAnchor: 'middle',
                  fill: theme.palette.text.primary,
                  ...theme.typography.body1,
                }}
              >
                Cantidad
              </Label>
            </YAxis>
            <Line
              isAnimationActive={false}
              type="monotone"
              dataKey="count"
              stroke={theme.palette.primary.main}
              dot={false}
            />
          </LineChart>
        )}
      </ResponsiveContainer>
    </React.Fragment>
  );
}
