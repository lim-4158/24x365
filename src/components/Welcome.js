import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Welcome.css';

const Welcome = () => {
  const navigate = useNavigate();

  return (
    <div className="welcome-container">
      <h1 className="welcome-title">Welcome to 24X365!</h1>
      <p className="welcome-subtitle">Your personal time management assistant</p>
      <div className="welcome-card">
        <div className="button-group">
          <button onClick={() => navigate('/login')} className="welcome-button login">
            Login
          </button>
          <button onClick={() => navigate('/register')} className="welcome-button register">
            Register
          </button>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
