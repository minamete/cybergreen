import React, { useState } from 'react';
import './Chat.css'; // Import the CSS file

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');

  const handleUserInput = (e) => {
    setUserInput(e.target.value);
  };

  const handleSendMessage = async () => {
      // Add the user's message to the messages state
      const newUserMessage = { type: 'user', text: userInput };
      setMessages((prevMessages) => [...prevMessages, newUserMessage]);
    
      try {
        const response = await fetch('http://localhost:5000/user_chat?user_input=' + encodeURIComponent(userInput), {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          mode: 'cors'
        });
    
        if (!response.ok) {
          throw new Error('Failed to fetch OpenAI response');
        }
    
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.indexOf('application/json') !== -1) {
          // If the response body is JSON, handle it as before
          const responseData = await response.json();
          if (typeof responseData === 'object') {
            const newAiMessage = { type: 'ai', text: responseData.response };
            setMessages((prevMessages) => [...prevMessages, newAiMessage]);
          } else {
            console.error('Invalid JSON format in OpenAI response:', responseData);
          }
        } else {
          // If the response body is not JSON, treat it as plain text
          const responseText = await response.text();
          const newAiMessage = { type: 'ai', text: responseText };
          setMessages((prevMessages) => [...prevMessages, newAiMessage]);
        }
    
      } catch (error) {
        console.error('Error fetching OpenAI response:', error);
      }
    
      // Clear the user input
      setUserInput('');
    };
  
  

  return (
    <div className="chat-container">
      <div className="instruction-box">
        <p>Please input your text in the format: "Problem: [your problem text here] Solution: [your solution text here]"</p>
      </div>
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
          className="input-field"
        />
        <button onClick={handleSendMessage} className="send-button">
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;
