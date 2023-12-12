import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faRobot } from '@fortawesome/free-solid-svg-icons';

interface ChatItemProps {
  chat: {
    id: number;
    prompt: string;
    reply: string;
  };
}

const ChatItem: React.FC<ChatItemProps> = ({ chat }) => {
  return (
    <div className="flex flex-col items-center mb-4 flex-1">
      <div className="pt-2 pb-6 w-full">
        <div className="container-class flex items-start">
          <div className="flex-none w-10 flex justify-center"> {/* Center the content horizontally */}
            <FontAwesomeIcon icon={faUser} className="text-purple-500 fa-lg fa-user-icon" />
          </div>
          <p className="text-left ml-2 pl-4"> {/* Adjust margin as needed */}
            {chat.prompt}
          </p>
        </div>
      </div>
      <div className="bg-gray-100 pt-6 pb-6 w-full">
        <div className="container-class flex items-start">
          <div className="flex-none w-10 flex justify-center"> {/* Center the content horizontally */}
            <FontAwesomeIcon icon={faRobot} className="text-blue-500 fa-lg fa-robot-icon" />
          </div>
          <p className="text-left ml-2 pl-4"> {/* Adjust margin as needed */}
            {chat.reply || '...'} {/* Display an ellipsis or a loading indicator if the reply is empty */}
          </p>
        </div>
      </div> 
    </div>
  );
};

export default ChatItem;
