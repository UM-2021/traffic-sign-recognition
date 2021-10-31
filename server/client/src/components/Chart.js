import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import { LineChart, Line, XAxis, YAxis, Label, ResponsiveContainer } from 'recharts';
import Title from './Title';
import Loader from './Loader';
import axios from 'axios';

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

export default function Chart() {
  const theme = useTheme();
  const [loading, setLoading] = React.useState(false);
  const [data, setData] = React.useState([]);

  React.useEffect(() => {
    const fetchSigns = async () => {
      setLoading(true);

      const res = await axios(`http://${process.env.REACT_APP_IP_ADDRESS}:3000/signs/records/date`);
      let signs = res.data.data.data;
      signs = signs.map((s) => ({ ...s, date: new Date(s.date) }));

      const minDate = new Date(Math.min(...signs.map((s) => s.date)));
      let date = new Date(minDate);

      const signsLength = signs.length;
      if (signsLength < 10) {
        for (let i = 1; i <= 10 - signsLength; i++) {
          const newDate = date.setDate(date.getDate() - 1);
          console.log(newDate);
          signs.push({ date: new Date(newDate), count: 0 });
        }
      }

      signs.sort((a,b) => (a.date > b.date) ? 1 : ((b.date > a.date) ? -1 : 0))

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
