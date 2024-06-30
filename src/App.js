import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Welcome from './components/Welcome';
import ChatComponent from './components/ChatComponent';
import ConnectGoogleCalendar from './components/ConnectGoogleCalendar';
import UserCalendar from './components/UserCalendar';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Welcome />} /> 
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
