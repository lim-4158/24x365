import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
  const GOOGLE_AUTH_URL = `${BACKEND_URL}googlecalendar/events`;

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${BACKEND_URL}api/login/`, { username, password });
      localStorage.setItem('token', response.data.token);
      setMessage('Login successful');
      navigate('/chat'); // Redirect to the main page after successful login
    } catch (error) {
      setMessage('Login failed');
    }
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
        {message && <p className={`message ${message === 'Login successful' ? 'success' : 'error'}`}>{message}</p>}
      </div>
    </div>
  );
};

export default Login;