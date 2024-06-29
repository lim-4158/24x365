import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Register.css';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [registered, setRegistered] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/api/register/', { username, password });
      setMessage('Registration successful');
      setRegistered(true);
    } catch (error) {
      console.error('Registration error:', error);
      setMessage('Registration failed: ' + (error.response?.data?.error || 'Unknown error'));
    }
  };

  const handleLoginClick = () => {
    navigate('/login');
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h1>Create Account</h1>
        <form onSubmit={handleRegister}>
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
          <button type="submit" className="register-button">Register</button>
        </form>
        {message && <p className={`message ${registered ? 'success' : 'error'}`}>{message}</p>}
        {registered && (
          <button onClick={handleLoginClick} className="login-link">
            Proceed to Login
          </button>
        )}
      </div>
    </div>
  );
};

export default Register;