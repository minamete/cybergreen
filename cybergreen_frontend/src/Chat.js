import React, { useState, useEffect } from "react";
import "./Chat.css"; // Import the CSS file

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [userProblemInput, setUserProblemInput] = useState("");
  const [userSolutionInput, setUserSolutionInput] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(undefined);
  const [lastMessage, setLastMessage] = useState({
    problem: "",
    solution: "",
    category: "",
  });

  useEffect(() => {
    // on init
    if (isChatLoading === undefined) return;

    // if we're waiting on the backend
    if (isChatLoading === true) {
      setMessages([
        ...messages,
        {
          type: "ai",
          text: "Loading... (This may take up to 1 minute)",
        },
      ]);
    } else if (isChatLoading === false) {
      // Remove the loading
      if (messages[messages.length - 1].text.startsWith("Loading..."))
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
    const newUserMessage = {
      type: "user",
      text: userMessage,
      problem: userProblemInput,
      solution: userSolutionInput,
      scores: false,
    };

    lastMessage.problem = userProblemInput;
    lastMessage.solution = userSolutionInput;

    if (isSpam(userSolutionInput)) {
      return alert("Please provide a more comprehensive solution!");
    }

    messages.push(newUserMessage);

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
          messages[messages.length - 1].scores = responseData.response.scores;
          console.log(messages);
          const newAiMessage = {
            type: "ai",
            text: responseData.response.str,
          };
          setMessages((prevMessages) => [...prevMessages, newAiMessage]);
          lastMessage.category = responseData.response.category;
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

  const handleSendPrediction = async (type, name) => {
    console.log(lastMessage);

    const predictSubmission = {
      problem: lastMessage.problem,
      solution: lastMessage.solution,
      category: lastMessage.category,
    };

    if (isSpam(lastMessage.solution)) {
      return alert("Please provide a more comprehensive solution!");
    }

    setIsChatLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/${type}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        mode: "cors",
        body: JSON.stringify(predictSubmission),
      });

      if (!response.ok) {
        throw new Error("Prediction failed");
      }
      setIsChatLoading(false);

      const responseData = await response.json();
      console.log(responseData);
      if (typeof responseData === "object") {
        let newAiMessage = {
          type: "ai",
          text: name + ": " + responseData.response,
        };
        setMessages((prevMessages) => [...prevMessages, newAiMessage]);
      } else {
        setMessages([
          ...messages,
          {
            type: "ai",
            text: "I'm sorry, there was an error.",
          },
        ]);
        console.error("Invalid JSON format in OpenAI response:", responseData);
      }
    } catch (error) {
      setIsChatLoading(false);
      console.error("Prediction failed", error);
    }
  };

  const handleSubmitMessage = async (problem, solution, scores) => {
    // submitting to mongo
    const mongoSubmission = {
      problem: problem,
      solution: solution,
      scores: scores,
    };

    if (isSpam(solution)) {
      return alert("Please provide a more comprehensive solution!");
    }

    setIsChatLoading(true);
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
      setIsChatLoading(false);

      const responseData = await response.json();
      if (typeof responseData === "object") {
        let responseCategories = [
          "Overall impact score",
          "Feasibility score",
          "Novelty score",
          "Overall score",
        ];
        for (let i = 0; i < Object.values(responseData.response).length; i++) {
          let newAiMessage = {
            type: "ai",
            text:
              responseCategories[i] +
              ": " +
              Object.values(responseData.response)[i],
          };
          setMessages((prevMessages) => [...prevMessages, newAiMessage]);
        }
      } else {
        setMessages([
          ...messages,
          {
            type: "ai",
            text: "I'm sorry, there was an error.",
          },
        ]);
        console.error("Invalid JSON format in OpenAI response:", responseData);
      }
    } catch (error) {
      setIsChatLoading(false);
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
            <p>{message.text}</p>
            {message.type === "user" ? (
              <button
                disabled={!message.scores}
                onClick={(e) =>
                  handleSubmitMessage(
                    message.problem,
                    message.solution,
                    message.scores
                  )
                }
                className="submit-button"
              >
                Submit
              </button>
            ) : null}
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
        </div>
      </div>
      <div className="topics">
        <p className="first-text">
          This solution has been sorted into the topic:
        </p>
        <p className="second-text"></p>
      </div>
      <div className="input-row">
        <p>Get more comprehensive explanations on your last proposal:</p>
        <button
          className="predict-button"
          onClick={() => handleSendPrediction("impact", "Comprehensive Impact")}
          disabled={!!!lastMessage.category}
        >
          Comprehensive Impact
        </button>
        <button
          className="predict-button"
          onClick={() =>
            handleSendPrediction("risks", "Business and Financial Risks")
          }
          disabled={!!!lastMessage.category}
        >
          Business and Financial Risks
        </button>
        <button
          className="predict-button"
          onClick={() =>
            handleSendPrediction("market", "Market Insights and Outlooks")
          }
          disabled={!!!lastMessage.category}
        >
          Market Insights and Outlooks
        </button>
        <button
          className="predict-button"
          onClick={() =>
            handleSendPrediction("regulation", "Regulation and Compliance")
          }
          disabled={!!!lastMessage.category}
        >
          Regulation and Compliance
        </button>
        <button
          className="predict-button"
          onClick={() =>
            handleSendPrediction("competition", "Competitive Advantage")
          }
          disabled={!!!lastMessage.category}
        >
          Competitive Advantage
        </button>
        <button
          className="predict-button"
          onClick={() =>
            handleSendPrediction("feasibility", "Idea and Concept Feasibility")
          }
          disabled={!!!lastMessage.category}
        >
          Idea and Concept Feasibility
        </button>
        <button
          className="predict-button"
          onClick={() =>
            handleSendPrediction("funding", "Potential Funding Outlook")
          }
          disabled={!!!lastMessage.category}
        >
          Potential Funding Outlook
        </button>
      </div>
    </div>
  );
};

export default Chat;

const isSpam = (text) => {
  return text.length < 50;
};
