import React, { useState } from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import Dashboard from './pages/Dashboard';
import Signals from './pages/Signals';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const mdTheme = createTheme({
  typography: {
    fontFamily: ['Poppins'],
  },
});

const App = () => {
  const [user, setUser] = useState(false);

  const handleLogin = (e) => {
    e.preventDefault();
    setUser(true);
  };

  return (
    <Router>
      <ThemeProvider theme={mdTheme}>
        <Box sx={{ display: 'flex' }}>
          <CssBaseline />
          <Switch>
            <Route exact path="/" component={Dashboard} />
            <Route exact path="/signs" component={Signals} />
            <Route exact path="/signin" component={SignIn} handleLogin={handleLogin}/>
            <Route exact path="/signup" component={SignUp} />
          </Switch>
        </Box>
      </ThemeProvider>
    </Router>
  );
};

export default App;
