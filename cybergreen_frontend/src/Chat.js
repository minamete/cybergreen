// Chat.js
import React, { useState } from 'react';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');

  const handleUserInput = (e) => {
    setUserInput(e.target.value);
  };

  const handleSendMessage = () => {
    // Handle sending user input and receiving AI response
    // For now, let's just echo the user's message as a response
    setMessages([...messages, { type: 'user', text: userInput }]);
    setUserInput('');
  };

  return (
    <div className="chat-container">
      <div className="message-box">
        {messages.map((message, index) => (
          <div key={index} className={message.type === 'user' ? 'user-message' : 'ai-message'}>
            {message.text}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          placeholder="Type your message..."
          value={userInput}
          onChange={handleUserInput}
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
