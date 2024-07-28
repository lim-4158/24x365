import React, { useEffect, useState } from 'react';
import './UserCalendar.css';

function UserCalendar() {
  const [calendarId, setCalendarId] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [timezone, setTimezone] = useState('');

  useEffect(() => {
    // Get the user's timezone
    const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    setTimezone(userTimezone);

    // Get the backend URL from environment variables
    const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
    const API_URL = `${BACKEND_URL}googlecalendar/display_events`;

    // Fetch the calendar ID from the backend
    fetch(API_URL, {
      method: 'GET',
      credentials: 'include',
    })
      .then(response => response.json())
      .then(data => {
        if (data.calendar_id) {
          setCalendarId(data.calendar_id);
        } else {
          setError(data.error || 'No calendar ID found');
        }
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching calendar ID:', error);
        setError('Error fetching calendar ID');
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div style={{ color: 'white', fontSize: '20px' }}>Loading...</div>;
  }

  if (error) {
    return (
      <div style={{ color: 'white', fontSize: '20px' }}>
        Error fetching events. Please <a href={`${process.env.REACT_APP_BACKEND_URL}googlecalendar/events`} style={{ color: 'lightblue' }}>click here</a> to reauthenticate.
      </div>
    );
  }

  const calendarUrl = `https://calendar.google.com/calendar/embed?src=${calendarId}&ctz=${timezone}`;

  return (
    <div className="user-calendar-wrapper">
      <h2 style={{ color: 'white', fontSize: '40px' }}>Your Google Calendar</h2> {/* White text color */}
      <div className="iframe-container">
        <iframe
          src={calendarUrl}
          style={{ border: 0 }}
          width="800"
          height="600"
          frameBorder="0"
          scrolling="no"
        ></iframe>
      </div>
    </div>
  );
}

export default UserCalendar;
