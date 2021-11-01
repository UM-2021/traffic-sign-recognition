import React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import Dashboard from './pages/Dashboard';
import Signals from './pages/Signals';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './hooks/useAuth';

const mdTheme = createTheme({
  typography: {
    fontFamily: ['Poppins'],
  },
});

const App = () => {
  return (
    <ThemeProvider theme={mdTheme}>
      <Box sx={{ display: 'flex' }}>
        <Router>
          <AuthProvider>
            <CssBaseline />
            <Switch>
              <ProtectedRoute exact path="/" component={Dashboard} />
              <ProtectedRoute exact path="/signs" component={Signals} />
              <Route exact path="/signin" component={SignIn} />
              <Route exact path="/signup" component={SignUp} />
            </Switch>
          </AuthProvider>
        </Router>
      </Box>
    </ThemeProvider>
  );
};

export default App;
