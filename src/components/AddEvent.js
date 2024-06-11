// EventForm.js
import React, { useState } from "react";

const AddEvent = () => {
  const [summary, setSummary] = useState("");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const event = {
      summary,
      start: new Date(start).toISOString(),
      end: new Date(end).toISOString(),
    };

    try {
      const response = await fetch("http://localhost:8000/calendar/events/create/", {
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
