// EventForm.js
import React, { useState } from "react";

const AddEvent = () => {
  // Set default date to today
  const today = new Date();
  const defaultStart = new Date(today.setHours(21, 0, 0, 0)); // 9:00 PM
  const defaultEnd = new Date(today.setHours(22, 0, 0, 0)); // 10:00 PM

  // Format date for datetime-local input
  const formatDateTimeLocal = (date) => {
    return date.toISOString().slice(0, 16);
  };

  const [summary, setSummary] = useState("badminton");
  const [start, setStart] = useState(formatDateTimeLocal(defaultStart));
  const [end, setEnd] = useState(formatDateTimeLocal(defaultEnd));

  const handleSubmit = async (e) => {
    e.preventDefault();

    const event = {
      summary,
      start: new Date(start).toISOString(),
      end: new Date(end).toISOString(),
    };

    try {
      alert(JSON.stringify(event))
      const response = await fetch("http://localhost:8000/googlecalendar/calendar/createevents", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(event),
      });

      if (response.ok) {
        const data = await response.json();
        alert("Event created successfully!");
        console.log(data);
      } else {
        const errorData = await response.json();
        alert("Error creating event: " + errorData.error);
      }
    } catch (error) {
      alert("Error creating event: " + error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Summary</label>
        <input
          type="text"
          value={summary}
          onChange={(e) => setSummary(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Start Date and Time</label>
        <input
          type="datetime-local"
          value={start}
          onChange={(e) => setStart(e.target.value)}
          required
        />
      </div>
      <div>
        <label>End Date and Time</label>
        <input
          type="datetime-local"
          value={end}
          onChange={(e) => setEnd(e.target.value)}
          required
        />
      </div>
      <button type="submit">Create Event</button>
    </form>
  );
};

export default AddEvent;