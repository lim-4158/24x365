import React, { useEffect, useState } from 'react';
import axios from 'axios';

const EventChecklist = () => {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

    useEffect(() => {
        axios.get(`${BACKEND_URL}googlecalendar/list_events`)
            .then(response => {
                console.log('API Response:', response.data);
                if (response.data && Array.isArray(response.data.events)) {
                    setEvents(response.data.events);
                } else {
                    console.error('Unexpected response format:', response.data);
                    setError('Unexpected response format');
                }
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching events:', error);
                setError('Error fetching events');
                setLoading(false);
            });
    }, [BACKEND_URL]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h1>Event Checklist</h1>
            <ul>
                {events.length === 0 ? (
                    <li>No events found</li>
                ) : (
                    events.map((event, index) => (
                        <li key={index}>
                            <input type="checkbox" id={`event-${index}`} />
                            <label htmlFor={`event-${index}`}>
                                {event.summary} - {new Date(event.start).toLocaleString()}
                            </label>
                        </li>
                    ))
                )}
            </ul>
        </div>
    );
};

export default EventChecklist;
