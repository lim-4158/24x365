import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Welcome from './components/Welcome';
import Calendar from './components/Calendar';
import AddEvent from './components/AddEvent';

import ChatComponent from './components/ChatComponent';


function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Welcome />} /> 
          <Route path="/calendar" element={<Calendar />} /> 
          <Route path="/addevent" element={<AddEvent />} /> 
          <Route path="/chatbot" element={<ChatComponent />} /> 
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
