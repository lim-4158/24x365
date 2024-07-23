import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid'; // Import UUID for unique IDs

const EventChecklist = () => {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [checkedEvents, setCheckedEvents] = useState(new Set()); // State to track checked events

    const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

    useEffect(() => {
        axios.get(`${BACKEND_URL}googlecalendar/list_events`)
            .then(response => {
                console.log('API Response:', response.data);
                if (response.data && Array.isArray(response.data.events)) {
                    // Assign unique IDs to events if they don't have one
                    const eventsWithIds = response.data.events.map(event => ({
                        ...event,
                        uniqueId: uuidv4() // Generate a unique ID for each event
                    }));
                    setEvents(eventsWithIds);
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

    const handleCheckboxChange = (uniqueId) => {
        setCheckedEvents(prev => {
            const newCheckedEvents = new Set(prev);
            if (newCheckedEvents.has(uniqueId)) {
                newCheckedEvents.delete(uniqueId);
            } else {
                newCheckedEvents.add(uniqueId);
            }
            return newCheckedEvents;
        });
    };

    if (loading) {
        return <div style={{ color: 'white' }}>Loading...</div>;
    }

    if (error) {
        return <div style={{ color: 'white' }}>{error}</div>;
    }

    return (
        <div style={{ color: 'white', padding: '20px' }}> {/* White text color and padding */}
            <h1 style={{ color: 'white' }}>Event Checklist</h1>
            <ul>
                {events.length === 0 ? (
                    <li style={{ color: 'white' }}>No events for today!</li>
                ) : (
                    events.map(event => (
                        <li
                            key={event.uniqueId} // Use uniqueId as the key
                            style={{ 
                                textDecoration: checkedEvents.has(event.uniqueId) ? 'line-through' : 'none',
                                color: 'white' // Ensure text is white
                            }}
                        >
                            <input
                                type="checkbox"
                                id={`event-${event.uniqueId}`}
                                checked={checkedEvents.has(event.uniqueId)}
                                onChange={() => handleCheckboxChange(event.uniqueId)}
                            />
                            <label htmlFor={`event-${event.uniqueId}`} style={{ color: 'white' }}>
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
