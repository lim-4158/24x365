// src/components/ConnectGoogleCalendar.js
import React, { useState, useEffect } from 'react';

function ConnectGoogleCalendar() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Check if the user is authenticated with Google services
    fetch('http://localhost:8000/googlecalendar/calendar/checkauth', {
      method: 'GET',
      credentials: 'include',
    })
      .then(response => response.json())
      .then(data => {
        setIsAuthenticated(data.authenticated);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error checking Google authentication:', error);
        setError('Error checking Google authentication');
        setLoading(false);
      });
  }, []);

  const handleConnectClick = () => {
    if (isAuthenticated) {
      // Redirect to the calendar display page
      window.location.href = 'http://localhost:3000/usercalendar';
    } else {
      // Redirect to the Google authentication endpoint
      window.location.href = 'http://localhost:8000/googlecalendar/calendar/events';
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h2>Connect to Google Calendar</h2>
      <p>Click the button below to connect your Google Calendar.</p>
      <button onClick={handleConnectClick}>
        {isAuthenticated ? 'View Google Calendar' : 'Connect Google Calendar'}
      </button>
    </div>
  );
}

export default ConnectGoogleCalendar;
