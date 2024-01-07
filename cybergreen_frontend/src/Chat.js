import React, { useState, useEffect } from "react";
import "./Chat.css"; // Import the CSS file

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [userProblemInput, setUserProblemInput] = useState("");
  const [userSolutionInput, setUserSolutionInput] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(undefined);

  useEffect(() => {
    // on init
    if (isChatLoading === undefined) return;

    // if we're waiting on the backend
    if (isChatLoading === true) {
      setMessages([
        ...messages,
        {
          type: "ai",
          text: "Loading...",
        },
      ]);
    } else if (isChatLoading === false) {
      // Remove the loading
      if (messages[messages.length - 1].text === "Loading...")
        setMessages(messages.slice(0, -1));
    }
  }, [isChatLoading]);

  const handleUserProblemInput = (e) => {
    setUserProblemInput(e.target.value);
  };

  const handleUserSolutionInput = (e) => {
    setUserSolutionInput(e.target.value);
  };

  const handleSendMessage = async () => {
    // Add the user's message to the messages state
    const userMessage =
      "Problem: " + userProblemInput + " Solution: " + userSolutionInput;
    const newUserMessage = { type: "user", text: userMessage };
    setMessages((prevMessages) => [...prevMessages, newUserMessage]);

    const problemSolutionObject = {
      problem: userProblemInput,
      solution: userSolutionInput,
    };

    try {
      setIsChatLoading(true);

      const response = await fetch("http://localhost:5000/user_chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        mode: "cors",
        body: JSON.stringify(problemSolutionObject),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch OpenAI response");
      }

      setIsChatLoading(false);

      const contentType = response.headers.get("content-type");
      if (contentType && contentType.indexOf("application/json") !== -1) {
        // If the response body is JSON, handle it as before
        const responseData = await response.json();
        if (typeof responseData === "object") {
          const newAiMessage = { type: "ai", text: responseData.response };
          setMessages((prevMessages) => [...prevMessages, newAiMessage]);
        } else {
          setMessages([
            ...messages,
            {
              type: "ai",
              text: "I'm sorry, there was an error.",
            },
          ]);
          console.error(
            "Invalid JSON format in OpenAI response:",
            responseData
          );
        }
      } else {
        // If the response body is not JSON, treat it as plain text
        const responseText = await response.text();
        const newAiMessage = { type: "ai", text: responseText };
        setMessages((prevMessages) => [...prevMessages, newAiMessage]);
      }
    } catch (error) {
      setIsChatLoading(false);
      setMessages([
        ...messages,
        {
          type: "ai",
          text: "I'm sorry, there was an error.",
        },
      ]);
      console.error("Error fetching OpenAI response:", error);
    }

    // Clear the user input
    setUserProblemInput("");
    setUserSolutionInput("");
  };

  const handleSubmitMessage = async () => {
    // submitting to mongo
    const mongoSubmission = {
      problem: userProblemInput,
      solution: userSolutionInput,
    };

    try {
      const response = await fetch("http://localhost:5000/submission", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        mode: "cors",
        body: JSON.stringify([mongoSubmission]),
      });

      if (!response.ok) {
        throw new Error("Submission failed");
      }

      alert("Submission succeeded");
    } catch (error) {
      console.error("Submission failed", error);
    }
  };

  return (
    <div className="chat-container">
      <div className="instruction-box">
        <p>Please input your problem and solution, or upload a .csv file.</p>
      </div>
      <div className="message-box">
        {messages.map((message, index) => (
          <div
            key={index}
            className={message.type === "user" ? "user-message" : "ai-message"}
          >
            {message.text}
          </div>
        ))}
      </div>
      <div className="input-container">
        <div className="input-col">
          <input
            type="text"
            placeholder="Type your problem..."
            value={userProblemInput}
            onChange={handleUserProblemInput}
            className="input-field"
          />
          <input
            type="text"
            placeholder="Type your solution..."
            value={userSolutionInput}
            onChange={handleUserSolutionInput}
            className="input-field"
          />
        </div>
        <div className="input-col">
          <button onClick={handleSendMessage} className="send-button">
            Send
          </button>
          <button onClick={handleSubmitMessage} className="send-button">
            Submit
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
