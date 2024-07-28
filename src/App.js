import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Welcome from './components/Welcome';
import ChatComponent from './components/ChatComponent';
import ConnectGoogleCalendar from './components/ConnectGoogleCalendar';
import UserCalendar from './components/UserCalendar';
import EventChecklist from './components/EventChecklist';
import Navigation from './components/Navigation';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Welcome />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/*" element={
            <>
              <Navigation />
              <Routes>
                <Route path="/chat" element={<ChatComponent />} />
                <Route path="/calendar" element={<UserCalendar />} />
                <Route path="/checklist" element={<EventChecklist />} />
                <Route path="/connect" element={<ConnectGoogleCalendar />} />
              </Routes>
            </>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;