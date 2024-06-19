import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

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

  const redirectToCalendar = () => {
    navigate('/calendar');
  };

  const redirectToChatbot = () => {
    navigate('/chatbot');
  };

  const redirectToAddEvent = () => {
    navigate('/addevent');
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        <button type="submit">Login</button>
      </form>
      {message && <p>{message}</p>}
      {isLoggedIn && (
        <div>
          <button onClick={redirectToCalendar}>Go to Calendar</button>
          <button onClick={redirectToChatbot}>Go to Chatbot</button>
          <button onClick={redirectToAddEvent}>Go to Add Event</button>
        </div>
      )}
    </div>
  );
};

export default Login;
