import * as React from 'react';
import Typography from '@mui/material/Typography';
import Title from './Title';
import { Box } from '@mui/system';

export default function CardWithNumber(props) {
  let date = new Date(Date.now());

  return (
    <React.Fragment>
      <Title>{props.title}</Title>
      <Box sx={{ flex: 1, marginTop: '10px' }}>
        <Typography component="p" variant="h2">
          {props.number}
        </Typography>
        <Typography color="text.secondary">
          hoy, {' '}
          {date.toLocaleDateString('es-ES', {
            weekday: 'short',
            year: 'numeric',
            month: 'short',
            day: 'numeric',
          })}
        </Typography>
      </Box>
    </React.Fragment>
  );
}
