import './index.css';
import Home from './Home';
import Chat from './Chat';
import Login from './Login';
import Register from './Register';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { useEffect, useState } from 'react';
import PrivareRoute from './utils/PrivateRoute';

import {AuthProvider} from './context/AuthContext';

function App() {
  return (
    <Router>
      <div className="App">
      <div className="content">
        <Switch>
          <AuthProvider>
            <Route exact path="/login">
              <Login />
            </Route>
            <Route exact path="/register">
              <Register />
            </Route>
            <PrivareRoute exact path="/">
              <Home />
            </PrivareRoute>
            <Route exact path="/chat/:id">
              <Chat />
            </Route>
            {/* <Route exact path="/chat/:id">
              <Chat />
            </Route> */}
          </AuthProvider>
        </Switch>
      </div>
      </div>
    </Router>

  );
}

export default App;
