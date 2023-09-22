import { useState } from "react";
import axios from "axios";

// Refresh button to reset all chat history
type Props = {
  setMessages: any;
  isLoading: boolean;
  maliaComplaint: string;
};


function Title({ setMessages, isLoading, maliaComplaint }: Props) {
  // Signal MALIA's memeory is being resetting
  const [isResetting, setIsResetting] = useState(false);
  const [alert, setAlert] = useState("Hey, you are not gonna acutally do it, are you...?")

  const resetChatHistory = async () => {
    // Alert user the memory is about to be reset
    const userConfirmed = window.confirm(alert);
    if (userConfirmed) {
      setIsResetting(true);
      
      // Request backend to reset memory and chat history
      await axios
      .get("http://127.0.0.1:8000/reset")
      .then((res) => {
        if (res.status == 200) {
          setMessages([]);
        } else {
          console.error(
            "Error occur when calling reset chat history on local Fast API."
          );
        }
      })
      .catch((err) => {
        console.error(err.message);
      });
    setIsResetting(false);
      console.log("Memory washed!");
    } else {
      console.log("User canceled the action.");
    }
  };
  return (
  
    <div className="rounded-3xl mx-auto max-w-700 max-h-title bg-cool-dark-light font-bold">
      {/* If resetting memory, display 'Oh no' */}
      { isResetting ? 
      (<p className="text-white text-center text-4xl px-20 py-10 animate-pulse">What? wait! Oh no...</p>) 
      // If isLoading, display thought complaint with pulsing effect
      : isLoading ?  (
          // Display malia's complaint when it's loading
          <div className="text-white text-center text-lg px-10 py-10">
            <p className="font-bold  text-gray-200">MALIA's thought bubble:</p>
            <p className="font-light italic mt-2 animate-pulse text-gray-200">{maliaComplaint}</p> 
          </div>
        )  :(
        <div >
          <div className="text-white text-center text-4xl px-10 py-7">
            <div className="mb-5">You speak</div>
            <div>MALIA listens and remembers...</div>
          </div>
         <div className="flex">
          <button
            onClick={resetChatHistory}
            className="transition-all duration-200 hover:scale-125
            text-gray-400 hover:text-white mx-auto pb-3"
            >
              wash memory
          </button>
         </div> 
        </div>
        )}
      
    </div>


  );
}

export default Title;
