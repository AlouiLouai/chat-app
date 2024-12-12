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
  const [currentChannel, setCurrentChannel] = useState<string>(""); 

  const token = Cookie.get('access_token'); 

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
      transports: ['websocket'],
    });

    // Listen for server message when connected
    socketConnection.on("server_message", (data) => {
      console.log(data.message); // Log server's message to the console
    });

    // Listen for received messages
    socketConnection.on("receive_message", (data) => {
      setMessages((prevMessages) => [...prevMessages, data]);
    });

    // Listen for channel updates (e.g., user joins/leaves channels)
    socketConnection.on("channel_update", (data) => {
      // Handle channel updates here, e.g., updating the list of active channels
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

    const messageData = { username, message, channel: currentChannel };
    socket?.emit("send_message", messageData); // Emit the message to the server
    setMessage(""); // Clear the input field
  };

  // Handle joining a channel
  const joinChannel = (channel: string) => {
    socket?.emit("join_channel", { channel });
    setCurrentChannel(channel); // Set the current channel
  };

  // Handle leaving the current channel
  const leaveChannel = () => {
    if (currentChannel) {
      socket?.emit("leave_channel", { channel: currentChannel });
      setCurrentChannel(""); // Clear the current channel
    }
  };

  return (
    <div>
      <h1 className="row-start-3 flex gap-6 flex-wrap items-center justify-center pb-6">Chat App</h1>

      <div className="channel-list">
        <h2>Channels</h2>
        <button onClick={() => joinChannel("General")}>General</button>
        <button onClick={() => joinChannel("Random")}>Random</button>
        <button onClick={leaveChannel}>Leave Channel</button>
      </div>

      <div
        className="rounded-lg border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex flex-col p-4 hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent"
        id="messages"
        style={{
          maxHeight: "400px",
          height: "auto",
          overflowY: "auto",
          width: "100%",
          padding: "1rem",
          borderRadius: "12px",
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
