import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Welcome from './components/Welcome';
import AddEvent from './components/AddEvent';

import ChatComponent from './components/ChatComponent';
import ConnectGoogleCalendar from './components/ConnectGoogleCalendar';
import UserCalendar from './components/UserCalendar';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Welcome />} /> 
          <Route path="/addevent" element={<AddEvent />} /> 
          <Route path="/chatbot" element={<ChatComponent />} /> 
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/connectgooglecalendar" element={<ConnectGoogleCalendar />} />
          <Route path="/usercalendar" element={<UserCalendar />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
