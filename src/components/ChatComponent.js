// src/components/ChatComponent.js

import React, { useState } from 'react';
import axios from 'axios';
import './ChatComponent.css';

const ChatComponent = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const sendMessage = async () => {
        if (input.trim() === '') return;

        setMessages([...messages, { type: 'user', text: input }]);
        setInput('');

        try {
            const response = await axios.get('http://127.0.0.1:8000/chat/get_response/', {
                params: { message: input }
            });
            const botMessage = { type: 'bot', text: response.data.message };
            setMessages(prevMessages => [...prevMessages, botMessage]);
        } catch (error) {
            console.error('Error fetching response:', error);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-box">
                <div className="messages">
                    {messages.map((msg, index) => (
                        <div key={index} className={msg.type === 'user' ? 'message user-message' : 'message bot-message'}>
                            {msg.text}
                        </div>
                    ))}
                </div>
                <div className="input-container">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Type your message here..."
                        className="chat-input"
                    />
                    <button onClick={sendMessage} className="send-button">Send</button>
                </div>
            </div>
        </div>
    );
};

export default ChatComponent;
