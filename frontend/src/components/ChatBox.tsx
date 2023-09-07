import { useState } from "react";
import MultilineInput from "./MultilineInput";
import Recorder from "./Recorder";
import SendMessage from "./SendMessage";


type Props = {
  handleStop: any;
  handleUserTextSent: any;
};



const btnStyle =
  "text-gray-500 transition-all duration-200 hover:scale-110 p-5 focus:outline-none";

function ChatBox({ handleStop, handleUserTextSent}: Props) {

  // User text input area variable
  const [text, setText] = useState('');

  // If user type or send text to AI 
  // Then there is no audio file
 

  return (
    <div className="w-9/12 min-w-[600px] max-w-700 rounded-lg fixed bottom-0 flex left-1/2 
    transform -translate-x-1/2 mb-3 bg-cool-dark">
      <div className="w-full h-auto p-2">
        <MultilineInput text={text} setText={setText} handleUserTextSent={handleUserTextSent}/>
      </div>
      <div className="flex flex-col my-2 ">
        <SendMessage btnStyle={btnStyle} text={text} setText={setText} handleUserTextSent={handleUserTextSent}/>
        <Recorder handleStop={handleStop} btnStyle={btnStyle}/>
      </div>
    </div>
  );
}

export default ChatBox;
