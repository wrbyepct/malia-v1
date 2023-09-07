// TypingEffect.tsx
import React, { useState, useEffect} from "react";

type Props = {
  message: string;
  typingSpeed?: number;
  isMaliaResponding: boolean;
};

const TypingEffect: React.FC<Props> = ({
  message,
  isMaliaResponding,
  typingSpeed = 50
}) => {
  const [displayedMessage, setDisplayedMessage] = useState("");

  useEffect(() => {
    if (isMaliaResponding) {
      // Only when the user sends the message the loading starts
      // and we display the typing effect
      if (displayedMessage.length < message.length) {
        setTimeout(
          () => {
            setDisplayedMessage(message.slice(0, displayedMessage.length+1))
          },typingSpeed)
      }
    } else {
          setDisplayedMessage(message);
        }
    
  }, [message, isMaliaResponding, displayedMessage])
  
    
  return <p>{displayedMessage}</p>;
};

export default TypingEffect;
