"use client";
import { useEffect, useState } from "react";
import io, { Socket } from "socket.io-client";
import Cookie from "js-cookie";
import { ProfileService } from "@/services/profile.services";

const Chat = () => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [message, setMessage] = useState("");
  const [username, setUsername] = useState("");
  const [userlogo, setUserlogo] = useState("");

  const token = Cookie.get("access_token");

  // Fetch profile data on component mount
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const { profile } = await ProfileService.getProfile();
        setUsername(profile.username);
        setUserlogo(profile.image_url);
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    };

    fetchProfile();
  }, []);

  // Connect to Socket.IO server on component mount
  useEffect(() => {
    const socketConnection = io("http://127.0.0.1:5000", {
      query: { token },
    });

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
    <div className="flex">

      {/* Main Chat Area */}
      <div className="flex-1 p-6">
        <h1 className="text-2xl font-semibold mb-4">Chat App</h1>

        {/* Display messages */}
        <div
          id="messages"
          style={{
            maxHeight: "400px",
            height: "auto",
            overflowY: "auto",
            width: "100%",
            padding: "1rem",
            borderRadius: "12px",
            backgroundColor: "#f7f7f7",
          }}
        >
          {messages.map((msg, index) => (
            <p key={index} className="mb-2">
              <strong>{username}:</strong> {msg.message}
            </p>
          ))}
        </div>

        {/* Send Message */}
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
    </div>
  );
};

export default Chat;
