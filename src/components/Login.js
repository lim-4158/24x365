import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css';
import GoogleSignInButton from './GoogleSignInButton';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
  const GOOGLE_AUTH_URL = `${BACKEND_URL}googlecalendar/events`;

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${BACKEND_URL}api/login/`, { username, password });
      localStorage.setItem('token', response.data.token);
      setMessage('Login successful');
      setIsLoggedIn(true);
    } catch (error) {
      setMessage('Login failed');
    }
  };

  const redirectTo = (path) => {
    navigate(path);
  };

  const handleGoogleSignInClick = () => {
    // Redirect to the Google authentication endpoint
    window.location.href = GOOGLE_AUTH_URL;
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Login</h1>
        <form onSubmit={handleLogin}>
          <div className="input-group">
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              required
            />
          </div>
          <div className="input-group">
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              required
            />
          </div>
          <button type="submit" className="login-button">Sign In</button>
        </form>
        {message && <p className={`message ${isLoggedIn ? 'success' : 'error'}`}>{message}</p>}
        {isLoggedIn && (
          <div className="navigation-buttons">
            <button onClick={() => redirectTo('/chatbot')}>Chatbot</button>
            <button onClick={() => redirectTo('/usercalendar')}>Calendar</button>
            <button onClick={() => redirectTo('/eventchecklist')}>Event Checklist</button>
            <GoogleSignInButton onClick={handleGoogleSignInClick} />
          </div>
        )}
      </div>
    </div>
  );
};

export default Login;
