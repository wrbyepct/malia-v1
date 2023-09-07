import ChatMessages from "./ChatMessages";

type Props = {
  messages: any;
  isLoading: boolean;
  isMaliaResponding: boolean;
  setMessages:any;
};

function ChatWindow({ messages, isLoading, setMessages, isMaliaResponding }: Props) {
  const clearChatWindow = () => {
    setMessages([]);
  }
  return (
    <div className="flex justify-center ">
      <div className="w-chat-window bg-transparent">
        {messages.map((message: any, index: number) => {
          return <ChatMessages
              key={index + message.sender}
              message={message}
              lastMessage={index === messages.length - 1}
              isMaliaResponding={isMaliaResponding}
          />
        })}

        {/* Display when chat history is empty */}
        {messages.length == 0 && !isLoading && (
          <div className="text-center font-bold text-gray-200 italic mt-10 text-lg">
            Just talk already!
          </div>
        )}
        {messages.length != 0 && (
          <div className="flex mt-10">
          <button onClick={clearChatWindow}
            className="transition-all duration-200 hover:scale-125
            text-gray-400 hover:text-white mx-auto pb-3"
            >
              clear chat window
          </button>
        </div>
        )}
        
      </div>

    </div>
    
  );
}

export default ChatWindow;
