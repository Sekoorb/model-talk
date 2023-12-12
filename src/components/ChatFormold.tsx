import { useStore } from "@/store";
import { useState, KeyboardEvent } from "react"; // Import KeyboardEvent for typing

export default function ChatForm() {
  const addChat = useStore((state) => state.addChat);
  const [loading, setLoading] = useState(false);
  const [newChat, setNewChat] = useState("");

  const handleCreateChat = async () => {
    if (!newChat.trim()) return; // Prevent sending empty or only whitespace
    try {
      setLoading(true);
      const chat = { prompt: newChat, reply: newChat };
      await addChat(chat);
      setNewChat("");
    } catch (error) {
      console.error("Error creating chat item:", error);
    } finally {
      setLoading(false);
    }
  };

  // Handle the keyboard event in the textarea
  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault(); // Prevent the default action of inserting a new line
      handleCreateChat();
    }
  };

  return (
    <div className="relative flex items-end space-x-2 mb-4">
      <textarea
        value={newChat}
        onChange={(e) => setNewChat(e.target.value)}
        onKeyDown={handleKeyDown} // Handle the key down event
        className="border rounded pl-2 pr-16 pt-2 pb-24 flex-1 resize-none" // resize-none to prevent resizing of textarea
        placeholder="Send message"
        rows={1} // Start with one row
      />
      <button
        disabled={loading}
        className={`absolute right-2 bottom-2 px-4 py-1 text-white rounded ${
          loading ? "bg-gray-400" : "bg-blue-500"
        }`}
        onClick={handleCreateChat}
      >
        Send
      </button>
    </div>
  );
}