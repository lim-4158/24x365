import React, { useState } from 'react';
import BackButton from './BackButton';
import './Calendar.css'; // Import CSS file for styling

const Calendar = () => {
  const [currentDate, setCurrentDate] = useState(new Date());

  // Function to get the days in a month
  const getDaysInMonth = (month, year) => {
    return new Date(year, month + 1, 0).getDate();
  };

  // Function to get the first day of the month
  const getFirstDayOfMonth = (month, year) => {
    return new Date(year, month, 1).getDay();
  };

  // Function to render the calendar grid
  const renderCalendar = () => {
    const daysInMonth = getDaysInMonth(currentDate.getMonth(), currentDate.getFullYear());
    const firstDay = getFirstDayOfMonth(currentDate.getMonth(), currentDate.getFullYear());
    const weeks = [];
    let days = [];

    // Render empty cells for days of previous month
    for (let i = 0; i < firstDay; i++) {
      days.push(<td key={`empty-${i}`} className="empty-day"></td>);
    }

    // Render days of the current month
    for (let day = 1; day <= daysInMonth; day++) {
      days.push(<td key={day} className="day">{day}</td>);
      if ((day + firstDay) % 7 === 0 || day === daysInMonth) {
        weeks.push(<tr key={day} className="week">{days}</tr>);
        days = [];
      }
    }

    return weeks;
  };

  // Function to handle navigation
  const prevMonth = () => {
    setCurrentDate(prevDate => new Date(prevDate.getFullYear(), prevDate.getMonth() - 1, 1));
  };

  const nextMonth = () => {
    setCurrentDate(prevDate => new Date(prevDate.getFullYear(), prevDate.getMonth() + 1, 1));
  };

  return (
    <div className="calendar">
      <BackButton />  
      <div className="header">
        <button onClick={prevMonth}>Prev</button>
        <h2>{currentDate.toLocaleString('default', { month: 'long', year: 'numeric' })}</h2>
        <button onClick={nextMonth}>Next</button>
      </div>
      <table className="calendar-table">
        <thead>
          <tr>
            <th className="header-cell">Sun</th>
            <th className="header-cell">Mon</th>
            <th className="header-cell">Tue</th>
            <th className="header-cell">Wed</th>
            <th className="header-cell">Thu</th>
            <th className="header-cell">Fri</th>
            <th className="header-cell">Sat</th>
          </tr>
        </thead>
        <tbody>
          {renderCalendar()}
        </tbody>
      </table>
    </div>
  );
};

export default Calendar;
