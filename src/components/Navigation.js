import React from 'react';
import { Link } from 'react-router-dom';
import './Navigation.css';

const Navigation = () => {
  return (
    <nav className="navbar">
      <ul className="nav-links">
        <li><Link to="/chat">ChatBot</Link></li>
        <li><Link to="/calendar">Calendar</Link></li>
        <li><Link to="/checklist">Event Checklist</Link></li>
        <li><Link to="/googlesignin">Connect Google</Link></li>
      </ul>
    </nav>
  );
};

export default Navigation;