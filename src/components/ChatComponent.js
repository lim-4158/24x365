// ChatComponent.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './ChatComponent.css';

const ChatComponent = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    // Access the environment variable
    const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

    const sendMessage = async () => {
        if (input.trim() === '') return;

        const newMessages = [...messages, { type: 'user', text: input }];
        setMessages(newMessages);
        setInput('');

        try {
            const response = await axios.post(`${BACKEND_URL}chat/get_response/`, {
                messages: newMessages
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

    const navigate = useNavigate();

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
