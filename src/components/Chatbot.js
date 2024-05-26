import React, { useState } from 'react';
import './Chatbot.css';
import BackButton from './BackButton';

const Chatbot = () => {
  const [messages, setMessages] = useState([{ text: 'Hello! How can I assist you today?', user: 'bot' }]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, user: 'user' }]);
      setInput('');
      setTimeout(() => {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: 'This is a static response.', user: 'bot' }
        ]);
      }, 500);
    }
  };

  return (
    <div className="chatbot-container">
      <BackButton />  
      <div className="messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.user === 'bot' ? 'bot' : 'user'}`}
          >
            {message.text}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
