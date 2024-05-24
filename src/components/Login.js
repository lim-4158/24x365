import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // Import useNavigate from React Router

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false); // State to track login status
  const navigate = useNavigate(); // Initialize useNavigate

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/login/', { username, password });
      localStorage.setItem('token', response.data.token);
      setMessage('Login successful');
      setIsLoggedIn(true); // Set login status to true
    } catch (error) {
      setMessage('Login failed');
    }
  };

  // Function to handle redirection to calendar component
  const redirectToCalendar = () => {
    navigate('/calendar'); // Use navigate instead of history.push
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
      {/* Conditionally render button if login is successful */}
      {isLoggedIn && (
        <button onClick={redirectToCalendar}>Go to Calendar</button>
      )}
    </div>
  );
};

export default Login;
