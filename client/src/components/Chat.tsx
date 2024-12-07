"use client";
import { useEffect, useState } from "react";
import io, { Socket } from "socket.io-client";

const Chat = () => {
  const [socket, setSocket] = useState<Socket | null>(null); // Holds the socket connection
  const [messages, setMessages] = useState<Message[]>([]); // Stores messages
  const [message, setMessage] = useState(""); // Current input message
  const [username, setUsername] = useState("User1"); // User's name

  // Connect to Socket.IO server on component mount
  useEffect(() => {
    const socketConnection = io("http://127.0.0.1:5000");

    // Listen for server message when connected
    socketConnection.on("server_message", (data) => {
      console.log(data.message); // Log server's message to the console
    });

    // Listen for received messages
    socketConnection.on("receive_message", (data) => {
      setMessages((prevMessages) => [...prevMessages, data]);
    });

    setSocket(socketConnection); // Save the socket connection

    // Cleanup on unmount
    return () => {
      socketConnection.disconnect();
    };
  }, []);

  // Handle sending message to the server
  const sendMessage = () => {
    if (message.trim() === "") return; // Don't send empty messages

    const messageData = { username, message };
    socket?.emit("send_message", messageData); // Emit the message to the server
    setMessage(""); // Clear the input field
  };

  return (
    <div>
      <h1 className="row-start-3 flex gap-6 flex-wrap items-center justify-center pb-6">
        Chat App
      </h1>

      <div
        className="rounded-lg border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex flex-col p-4 hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent"
        id="messages"
        style={{
          maxHeight: "400px", // Adjust this to make the message list bigger
          height: "auto", // Allow the container to grow with content
          overflowY: "auto", // Scroll when content exceeds the container size
          width: "100%", // Make sure the container is full width
          padding: "1rem", // Add padding around the content
          borderRadius: "12px", // Rounded corners for the message container
        }}
      >
        {/* Messages */}
        <div className="w-full">
          {messages.map((msg, index) => (
            <p key={index} className="mb-2">
              <strong>{msg.username}:</strong> {msg.message}
            </p>
          ))}
        </div>
      </div>

      <div className="flex gap-4 items-center flex-col sm:flex-row pt-6">
        <input
          className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type a message..."
        />
        <button
          className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;
