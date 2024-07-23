import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import GoogleSignInButton from './GoogleSignInButton'; // Import GoogleSignInButton
import './Register.css';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [registered, setRegistered] = useState(false);
  const navigate = useNavigate();

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
  const REGISTER_URL = `${BACKEND_URL}api/register/`;

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await axios.post(REGISTER_URL, { username, password });
      setMessage('Registration successful. Please connect with Google to use our services.');
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
        {message && (
          <div className="message-container">
            <p className={`message ${registered ? 'success' : 'error'}`}>
              {message}
            </p>
          </div>
        )}
        {registered && (
          <div className="centered-container">
            <div className="google-signin-button-container">
              <GoogleSignInButton /> {/* Render GoogleSignInButton after registration */}
            </div>
            <button onClick={handleLoginClick} className="login-link">
              Proceed to Login
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Register;
