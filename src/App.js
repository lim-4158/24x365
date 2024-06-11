import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Welcome from './components/Welcome';
import Calendar from './components/Calendar';
import Chatbot from './components/Chatbot';
import AddEvent from './components/AddEvent';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Welcome />} /> 
          <Route path="/calendar" element={<Calendar />} /> 
          <Route path="/chatbot" element={<Chatbot />} /> 
          <Route path="/addevent" element={<AddEvent />} /> 
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
