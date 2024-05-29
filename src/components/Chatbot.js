import React, { useState } from 'react';
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
    <div className="w-[300px] h-[400px] border border-gray-300 flex flex-col">
      <BackButton />
      <div className="flex-1 p-2.5 overflow-y-auto">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`p-2.5 m-1.5 rounded-lg max-w-[75%] ${
              message.user === 'bot' ? 'bg-gray-300 text-black self-start' : 'bg-blue-500 text-white self-end'
            }`}
          >
            {message.text}
          </div>
        ))}
      </div>
      <div className="flex border-t border-gray-300">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          className="flex-1 border-none p-2.5 text-lg outline-none"
        />
        <button
          onClick={handleSend}
          className="p-2.5 bg-blue-500 text-white border-none cursor-pointer disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
