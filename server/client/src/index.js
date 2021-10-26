import React from 'react';
import ReactDOM from 'react-dom';
import reportWebVitals from './reportWebVitals';
import Dashboard from './pages/Dashboard';
import Layout from './components/Layout';
import Signals from './pages/Signals';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';

const mdTheme = createTheme({
  typography: {
    fontFamily: ['Poppins'],
  },
});

ReactDOM.render(
  <Router>
    <ThemeProvider theme={mdTheme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <Layout>
          <Switch>
            <Route exact path="/" component={Dashboard} />
            <Route exact path="/signs" component={Signals} />
          </Switch>
        </Layout>
      </Box>
    </ThemeProvider>
  </Router>,

  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
