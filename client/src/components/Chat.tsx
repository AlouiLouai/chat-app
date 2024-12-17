"use client";
import { useEffect, useState } from "react";
import io, { Socket } from "socket.io-client";
import Cookie from "js-cookie";
import { ProfileService } from "@/services/profile.services";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { Send, Smile } from "lucide-react";
import EmojiPicker from "emoji-picker-react";

const Chat = () => {
  const [socket, setSocket] = useState<typeof Socket | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [users, setUsers] = useState<any[]>([]);
  const [message, setMessage] = useState("");
  const [username, setUsername] = useState("");
  const [userlogo, setUserlogo] = useState("");
  const [showEmojiPicker, setShowEmojiPicker] = useState(false); // State to toggle emoji picker

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

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const { users } = await ProfileService.getUsers();
        setUsers(users);
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    };

    fetchUsers();
  }, []);

  // Connect to Socket.IO server on component mount
  useEffect(() => {
    const socketConnection = io("http://127.0.0.1:5000", {
      query: { token: token },
    });

    // Listen for server message when connected
    socketConnection.on("server_message", (data: any) => {
      console.log(data.message); // Log server's message to the console
    });

    // Listen for received messages
    socketConnection.on("receive_message", (data: any) => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { username: data.username, message: data.message },
      ]);
    });

    setSocket(socketConnection); // Save the socket connection

    // Cleanup on unmount
    return () => {
      socketConnection.disconnect();
    };
  }, [token]);

  // Handle sending message to the server
  const sendMessage = () => {
    if (message.trim() === "") return; // Don't send empty messages

    const messageData = { username, message };
    socket?.emit("send_message", messageData); // Emit the message to the server
    setMessage(""); // Clear the input field
  };

  // Handle emoji selection
  const handleEmojiClick = (emojiData: any) => {
    setMessage((prevMessage) => prevMessage + emojiData.emoji); // Append emoji to the current message
    setShowEmojiPicker(false); // Close the emoji picker after selection
  };

  return (
    <div className="flex flex-1">
      {/* Sidebar */}
      <div className="w-1/4 bg-white border-r overflow-y-auto">
        <div className="p-4 border-b">
          <h2 className="text-xl font-semibold">Chats</h2>
        </div>
        <div className="p-2">
          {/* Placeholder contacts */}
          {users.map((contact) => (
            <div
              key={contact.id} // Ensure each user has a unique key, typically by using `id`
              className="flex items-center p-2 hover:bg-gray-100 rounded-lg cursor-pointer"
            >
              <Avatar className="h-10 w-10">
                <AvatarImage src={contact.image_url} alt={contact.username} />
                <AvatarFallback>
                  {contact.username
                    .split(" ")
                    .map((n: any) => n[0])
                    .join("")}
                </AvatarFallback>{" "}
                {/* Use the first letter of username */}
              </Avatar>
              {/* Display the username */}
              <span className="ml-2">{contact.username}</span>{" "}
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="w-3/4 flex flex-col">
        {/* Chat Header */}
        <div className="p-4 border-b bg-white">
          <h1 className="text-xl font-semibold">Chat with LouChat</h1>
        </div>

        {/* Display Messages */}
        <div className="flex-1 p-4 overflow-y-auto">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${
                msg.username === username ? "justify-end" : "justify-start"
              } mb-4`}
            >
              <div
                className={`max-w-[70%] p-3 rounded-lg ${
                  msg.username === username
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200"
                }`}
              >
                {/* Display username */}
                <p>{msg.message}</p> {/* Display message content */}
              </div>
            </div>
          ))}
        </div>

        {/* Send Message */}
        <div className="p-4 bg-white border-t">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              sendMessage();
            }}
            className="flex items-center"
          >
            <Input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type a message..."
              className="flex-1 mr-2"
            />
            <Button
              type="button"
              size="icon"
              onClick={() => setShowEmojiPicker((prev) => !prev)}
              className="mr-2"
            >
              <Smile className="h-4 w-4" />
            </Button>
            <Button type="submit" size="icon">
              <Send className="h-4 w-4" />
            </Button>
          </form>
          {showEmojiPicker && (
            <div className="absolute bottom-16 right-4 z-10">
              <EmojiPicker onEmojiClick={handleEmojiClick} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Chat;
