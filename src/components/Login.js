import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/login/', { username, password });
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
            <button onClick={() => redirectTo('/addevent')}>Add Event</button>
            <button onClick={() => redirectTo('/connectgooglecalendar')}>Google Calendar</button>
            <button onClick={() => redirectTo('/usercalendar')}>User Calendar</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Login;