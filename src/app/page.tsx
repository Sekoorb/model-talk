// "use client" is a Next.js directive that ensures this code runs only on the client-side (browser) and not during server-side rendering.
"use client";

// Importing components and hooks from React and your project files
import ChatForm from "@/components/ChatForm"; // This is the input area where you type new messages
import ChatItem from "@/components/ChatItem"; // This component represents a single chat message in the list
import { useStore } from "@/store"; // This is a custom hook for state management (like Redux, but likely using Zustand or similar)
import { useEffect } from "react"; // The useEffect hook is used for performing side effects (like fetching data or directly manipulating the DOM) in functional components
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faThumbsUp, faThumbsDown, faTrashAlt, faSquareArrowUpRight, faRecordVinyl, faUser, faRobot, faHandsHoldingCircle, faMountainSun } from '@fortawesome/free-solid-svg-icons';

// ... other imports ...

// Home is a functional component, which is a JavaScript function that returns a React element.
// React.FC is a TypeScript type definition that stands for "Functional Component".
const Home: React.FC = () => {
  // This line declares a variable 'chats' that retrieves the current state of chats from your store, and 'fetchChats' which is a method to fetch chat data
  const chats = useStore((state) => state.chats);
  const fetchChats = useStore((state) => state.fetchChats);

  // This useEffect hook is called when the component mounts (after the first render), because the dependency array is empty.
  // It's calling the 'fetchChats' method which probably fetches chat messages from a database or an API.
  useEffect(() => {
    fetchChats();
  }, [fetchChats]); // The dependency array here makes the effect only re-run if fetchChats changes.

  // This useEffect hook runs every time 'chats' changes (when new chats are added or existing chats are updated).
  useEffect(() => {
    // Define a function that scrolls the window to the bottom of the page
    const handleScrollToBottom = () => {
      // window.scrollTo scrolls the window to a particular set of coordinates in the document.
      // 0 for the x-axis (horizontal) keeps it at the beginning, and the height of the document for y-axis scrolls to the bottom.
      window.scrollTo(0, document.documentElement.scrollHeight);
    };

    // Call the function to scroll to the bottom every time the chats change.
    handleScrollToBottom();
  }, [chats]); // The dependency array with 'chats' ensures this effect runs every time 'chats' is updated.

  // The return statement of the functional component is what gets rendered to the DOM.
  return (
    // Flex container for the entire viewport height, centered horizontally and vertically spaced between
    <div className="flex flex-col h-screen items-center justify-between bg-white">
      {/* Fixed Header at the top of the screen with a z-index of 10 (above other items),
          taking the full width and 16rem in height, items aligned to the start */}
      <div className="w-full fixed top-0 z-10 bg-slate-gray h-16 flex items-center justify-start pl-4">
        {/* Example of a logo or user icon with fixed size and rounded full to make it a circle */}
        <FontAwesomeIcon icon={faMountainSun} className="text-white" />
      </div>

      {/* Main Content with padding top to push content below fixed header and padding bottom to make space for chat input */}
      <main className="w-full flex-1 pt-20 pb-36">
        {/* Vertical padding of 1rem */}
        <div className="py-4">
          {chats.length === 0 ? (
            // Centered text in case there are no chat messages
            <p className="text-center">Start Chatting</p>
          ) : (
            // Map through each chat item and display it
            chats.map((chat) => <ChatItem key={chat.id} chat={chat} />)
          )}
        </div>
      </main>

      {/* ChatForm fixed at the bottom of the screen, taking the full horizontal width with padding */}
      <div className="fixed bottom-0 left-0 right-0 p-4 bg-white shadow-md">
        {/* Centering the ChatForm horizontally within the main container size */}
        <div className="container-class mx-auto">
          <ChatForm />
        </div>
      </div>
    </div>
  );
};

export default Home;