// src/components/UserCalendar.js
import React, { useEffect, useState } from 'react';

function UserCalendar() {
  const [calendarId, setCalendarId] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [timezone, setTimezone] = useState('');

  useEffect(() => {
    // Get the user's timezone
    const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    setTimezone(userTimezone);

    // Fetch the calendar ID from the backend
    fetch('http://localhost:8000/googlecalendar/calendar/displayevents', {
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
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  const calendarUrl = `https://calendar.google.com/calendar/embed?src=${calendarId}&ctz=${timezone}`;

  return (
    <div>
      <h2>Your Google Calendar</h2>
      <iframe
        src={calendarUrl}
        style={{ border: 0 }}
        width="800"
        height="600"
        frameBorder="0"
        scrolling="no"
      ></iframe>
    </div>
  );
}

export default UserCalendar;
