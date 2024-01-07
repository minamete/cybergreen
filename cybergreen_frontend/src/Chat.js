import React, { useState } from 'react';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');

  const handleUserInput = (e) => {
    setUserInput(e.target.value);
  };

  const handleSendMessage = async () => {
    // Add the user's message to the messages state
    setMessages([...messages, { type: 'user', text: userInput }]);

    // Call the Python script to get OpenAI response
    try {
        const response = await fetch('http://localhost:3000/api/get_openai_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput }),
});
          

      if (!response.ok) {
        throw new Error('Failed to fetch OpenAI response');
      }

      const responseData = await response.json();
      console.log('OpenAI Response:', responseData);

    // Add the assistant's reply to the messages state
        setMessages([...messages, { type: 'ai', text: responseData }]);

      // Add the assistant's reply to the messages state
      setMessages([...messages, { type: 'ai', text: responseData }]);
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
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
