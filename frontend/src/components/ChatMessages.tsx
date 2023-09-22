import TypingEffect from "./TypeingEffect";

type MessageProps = {
  message: { sender: string; text: string; time: string };
  lastMessage: boolean;
  isChatStart: boolean;
};

// Make the newest message render tying effect only if the
// Message child's property changes
const ChatMessage: React.FC<MessageProps> = ({
  message,
  lastMessage,
  isChatStart,
}) => {
  return (
    <div
      className={
        "flex flex-col px-5 focus:outline-none " +
        (message.sender == "Jay" ? "items-end" : "items-start")
      }
    >
      {/* Sender */}
      <div className="mt-4">
        <div
          className={
            "bg-cool-dark px-5 py-3 rounded-lg my-3 max-w-[550px] text-gray-300 " +
            (message.sender == "MALIA" && "min-w-400")
          }
        >
          <p
            className={
              "font-bold mb-2 " +
              (message.sender == "Jay"
                ? "text-right text-blue-300"
                : " text-pink-200")
            }
          >
            {message.sender}
          </p>
          {/* Chat Bubble */}
          {/* Use TypingEffect if it's MALIA's message */}
          {message.sender =="MALIA" && lastMessage ? (
            <TypingEffect
              message={message.text}
              isChatStart={isChatStart}
            />
          ) : (
            <p>{message.text}</p>
          )}

          {/* Timestamp */}

          <div className="mt-5 flex"></div>
        </div>

        <p
          className={
            "text-gray-400 " + (message.sender == "Jay" && "text-right mr-2")
          }
        >
          {message.time}
        </p>
      </div>
    </div>
  );
};

export default ChatMessage;
