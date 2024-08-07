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

    const handleSave = () => {
        const checkedEventDetails = events.filter(event => checkedEvents.has(event.uniqueId));
        console.log('Checked Event Details:', checkedEventDetails);

        const eventIdsToDelete = checkedEventDetails.map(event => event.event_id);

        axios.post(`${BACKEND_URL}googlecalendar/delete_events`, { event_ids: eventIdsToDelete })
            .then(response => {
                console.log('Delete response:', response.data);
                // Optionally, update the UI after deletion
                setEvents(prevEvents => prevEvents.filter(event => !eventIdsToDelete.includes(event.event_id)));
            })
            .catch(error => {
                console.error('Delete error:', error);
            });
    };

    const buttonStyle = {
        padding: '0.75rem 1.5rem',
        border: 'none',
        background: 'white', // Set background to white
        color: '#3f51b5', // Set text color to match button gradient
        borderRadius: '8px',
        fontSize: '1rem',
        fontWeight: '600',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        boxShadow: '0 2px 5px rgba(0, 0, 0, 0.2)' // Add subtle shadow for better visibility
    };

    const buttonHoverStyle = {
        transform: 'translateY(-2px)',
        boxShadow: '0 5px 15px rgba(63, 81, 181, 0.4)',
    };

    const [isHovered, setIsHovered] = useState(false);

    return (
        <div style={{ color: 'white', padding: '20px' }}> {/* White text color and padding */}
            <h1 style={{ color: 'white', fontSize: '40px' }}>Event Checklist</h1>
            {loading ? (
                <p style={{ color: 'white', fontSize: '20px' }}>Loading events...</p> // Loading message
            ) : error ? (
                <div className="auth-issue" style={{ color: 'white', fontSize: '20px' }}>
                    Error fetching events. Please <a href={`${BACKEND_URL}googlecalendar/events`} style={{ color: 'lightblue' }}>click here</a> to reauthenticate.
                </div>
            ) : (
                events.length === 0 ? (
                    <p style={{ color: 'white' }}>No events for today!</p>
                ) : (
                    <table style={{ width: '100%', color: 'white', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr>
                                <th style={{ border: '1px solid white', padding: '8px' }}>Select</th>
                                <th style={{ border: '1px solid white', padding: '8px' }}>Event</th>
                                <th style={{ border: '1px solid white', padding: '8px' }}>Date</th>
                                <th style={{ border: '1px solid white', padding: '8px' }}>Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            {events.map(event => {
                                const eventDate = new Date(event.start);
                                return (
                                    <tr key={event.uniqueId} style={{ textDecoration: checkedEvents.has(event.uniqueId) ? 'line-through' : 'none' }}>
                                        <td style={{ border: '1px solid white', padding: '8px' }}>
                                            <input
                                                type="checkbox"
                                                id={`event-${event.uniqueId}`}
                                                checked={checkedEvents.has(event.uniqueId)}
                                                onChange={() => handleCheckboxChange(event.uniqueId)}
                                            />
                                        </td>
                                        <td style={{ border: '1px solid white', padding: '8px' }}>
                                            <label htmlFor={`event-${event.uniqueId}`} style={{ color: 'white' }}>
                                                {event.summary}
                                            </label>
                                        </td>
                                        <td style={{ border: '1px solid white', padding: '8px' }}>
                                            {eventDate.toLocaleDateString()}
                                        </td>
                                        <td style={{ border: '1px solid white', padding: '8px' }}>
                                            {eventDate.toLocaleTimeString()}
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                )
            )}
            {events.length > 0 && (
                <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}> {/* Center the button */}
                    <button
                        onClick={handleSave}
                        style={{
                            ...buttonStyle,
                            ...(isHovered ? buttonHoverStyle : {}),
                        }}
                        onMouseEnter={() => setIsHovered(true)}
                        onMouseLeave={() => setIsHovered(false)}
                    >
                        Save
                    </button>
                </div>
            )}
        </div>
    );
};

export default EventChecklist;
