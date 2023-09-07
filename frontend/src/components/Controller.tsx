import { useEffect, useState, useRef } from "react";
import Title from "./Title";
import ChatBox from "./ChatBox";
import ChatWindow from "./ChatWindow";
import axios from "axios";

function Controller() {
  // Send message loading state
  const [isLoading, setIsLoading] = useState(false);

  // Chat history
  const [messages, setMessages] = useState<any[]>([]);
  const [isChatStart, setChatStart] = useState(false);
  const [maliaDoneResponding, setMaliaDoneResponding] = useState(false);

  const [maliaComplaint, setMaliaComplaint] = useState("*Processing...*");

  // // Request malia complaint only if isLoading is true
  // useEffect(() => {
  //   if (isLoading) {
  //     // Request malia complaint
  const requestMaliaComplaint = async (nonsense: string) => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/post-malia-complaint/",
        { nonsense: nonsense }
      );
      const complaint = res.data.complaint;
      setMaliaComplaint(complaint);

      return complaint;
    } catch (err) {
      console.error(err);
      const error = "Opps, requesting OpenAI got errors from frontend";
      setMaliaComplaint(error);
      return error;
    }
  };
  //     requestMaliaComplaint(nonsense);
  //   }
  // }, [isLoading]);

  // Create a ref for out scroll window
  const scrollableDivRef = useRef<HTMLDivElement>(null);

  // Turn backend-sent audio data to url
  const createBlobUrl = (data: any) => {
    const blob = new Blob([data], { type: "audio/mpeg" });
    const url = window.URL.createObjectURL(blob);
    return url;
  };

  // Loading chat history from backend
  const fetchWholeChatHistory = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/get-whole-chat-history"
      );
      const chatHistory = res.data;

      setMessages(chatHistory);
    } catch (err) {
      console.error(err);
    }
  };

  // Loading chat history from backend
  const requestBackendPersistMemroy = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/request-persist-to-memory"
      );
      const status = res.data.status;
      console.log(status);
    } catch (err) {
      console.error(err);
    }
  };

  // First send Jay audio to backend and get back text message
  const sendAudioAndGetJayText = async (myAudioUrl: string) => {
    try {
      // Fetch the audio and convert to blob
      const response = await fetch(myAudioUrl);
      const userBlob = await response.blob();

      // Construct our audio file format
      const formData = new FormData();
      formData.append("file", userBlob, "myFile.wav");

      // Send audio to backend
      const axiosResponse = await axios.post(
        "http://127.0.0.1:8000/post-audio-and-get-jay-text/",
        formData,
        {
          headers: { "Content-Type": "audio/mpeg" },
        }
      );

      return axiosResponse.data; // Return jay text
    } catch (err) {
      console.error(err);
    }
  };

  // Get back malia audio response
  const getMaliaAudioUrl = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/get-malia-audio-response",
        { responseType: "arraybuffer" }
      );
      const maliaAudioBlob = response.data;
      const maliaAudioUrl = createBlobUrl(maliaAudioBlob);

      return maliaAudioUrl;
    } catch (err) {
      console.error("Something went wrong when getting malia audio", err);
    }
  };

  const getMaliaMessage = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/get-malia-message"
      );
      const messages = response.data;

      return messages;
    } catch (err) {
      console.error(
        "Something went wrong when getting malia message from backend",
        err
      );
    }
  };

  // When user stops recording, it triggers sending recording requests
  const handleStop = async (myAudioUrl: string) => {
    // Start processing recorded audio

    // Send the jay audio as a file to our backend and get back jay text
    const jay = await sendAudioAndGetJayText(myAudioUrl);

    const userMessage = {
      sender: "Jay",
      text: jay.jay_text,
      time: jay.time,
    };

    // Prepare the messages array
    const messageArr = [...messages, userMessage];
    // Update user messages
    setMessages(messageArr);

    // User sent the message, set the loading to true
    setIsLoading(true);
    requestMaliaComplaint(jay.jay_text);
    // Get malia audio response
    const maliaAudioUrl = await getMaliaAudioUrl();

    // Play the audio
    const maliaAudio = new Audio();
    maliaAudio.src = maliaAudioUrl as string;
    maliaAudio.play();

    // Request malia text message and time
    const data = await getMaliaMessage();
    console.log(data);
    // Update frontend chathistory
    if (data) {
      const maliaMessage = {
        sender: "MALIA",
        text: data.malia_text,
        time: data.malia_time,
      };

      messageArr.push(maliaMessage);
      setMessages(messageArr);
    } else {
      console.log("Something went wrong with the message result");
    }

    setIsLoading(false);

    setChatStart(true);
    setMaliaDoneResponding(true);
    setMaliaComplaint("*Processing...*");
    setIsLoading(false);
  };

  // Send user text and get back malia voice
  const sendTextAndGetUrl = async (text: string) => {
    const endpoint =
      "http://127.0.0.1:8000/post-user-text-and-get-malia-voice/";

    const userText = { user_text: text };
    try {
      const response = await axios.post(endpoint, userText, {
        responseType: "arraybuffer",
      });
      // Convert backend audio data to frontend usable audio url
      const maliaAudioBlob = response.data;
      const maliaAudioUrl = createBlobUrl(maliaAudioBlob);
      return maliaAudioUrl; // Return the created URL
    } catch (err) {
      console.error(err);
    }
  };

  const handleUserTextSent = async (text: string) => {
    // Get timestampe: Hour:Min
    const currentTime = new Date();
    const hours = currentTime.getHours().toString().padStart(2, "0");
    const minutes = currentTime.getMinutes().toString().padStart(2, "0");
    // Format the Jay's message
    const userMessage = {
      sender: "Jay",
      text: text,
      time: `${hours}:${minutes}`,
    };

    // Append Jay' message to chat history
    const messageArr = [...messages, userMessage];

    // Update whole chat history
    setMessages(messageArr);

    // Start requesting malia voice
    setIsLoading(true);
    requestMaliaComplaint(text);
    // Get malia voice and play the audio
    const maliaAudioUrl = await sendTextAndGetUrl(text);
    const maliaAudio = new Audio();
    maliaAudio.src = maliaAudioUrl as string;
    maliaAudio.play();

    const data = await getMaliaMessage();
    console.log(data);
    // Update frontend chathistory
    // This time we only want malia message data
    if (data) {
      const maliaMessage = {
        sender: "MALIA",
        text: data.malia_text,
        time: data.malia_time,
      };

      messageArr.push(maliaMessage);
      setMessages(messageArr);
    } else {
      console.log("Something went wrong with the message result");
    }
    setChatStart(true);
    setMaliaDoneResponding(true);
    setMaliaComplaint("*Processing...*");
    setIsLoading(false);
  };

  useEffect(() => {
    if (scrollableDivRef.current) {
      // If there is a proper documents
      // Scroll it
      const div = scrollableDivRef.current;
      div.scrollTop = div.scrollHeight;
    }
  });

  useEffect(() => {
    // Request backend to reset chat history
    if (maliaDoneResponding) {
      // Every time MALIA done responding, we persist the message to memeory
      requestBackendPersistMemroy();
      setMaliaDoneResponding(false);
    }
  }, [maliaDoneResponding]);

  useEffect(() => {
    // First time the page rendered, grab the whole chat history from backend
    fetchWholeChatHistory();
  }, []);

  return (
    <div className="relative h-screen bg-black">
      <div
        className="fixed bg-transparent-purple mx-5 blurred-edges
      inset-0 z-20"
      >
        {/* Three blobs */}
        <div
          className="fixed top-1/4 right-1/2  
          w-72 h-72 bg-purple-300 rounded-full filter
          opacity-70 blur-xl animate-blob animation-delay-5s"
        ></div>
        <div
          className="fixed top-1/4 left-1/2   
          w-72 h-72 bg-yellow-300 rounded-full filter
          opacity-70 blur-xl animate-blob animation-delay-8s "
        ></div>
        <div
          className="fixed top-1/3 left-1/3 
          w-72 h-72 bg-pink-300 rounded-full filter
          opacity-70 blur-xl animate-pink-blob animation-delay-11s"
        ></div>
      </div>

      {/* Chat window */}
      <div className="relative h-screen overflow-y-hidden font-mono text-base z-30">
        <Title
          setMessages={setMessages}
          isLoading={isLoading}
          maliaComplaint={maliaComplaint}
        />
        <div
          ref={scrollableDivRef}
          className="flex flex-col h-full overflow-y-scroll pb-96 hide-scrollbar "
        >
          <ChatWindow
            messages={messages}
            isLoading={isLoading}
            isMaliaResponding={isChatStart}
            setMessages={setMessages}
          />
          <ChatBox
            handleStop={handleStop}
            handleUserTextSent={handleUserTextSent}
          />
        </div>
        ;
      </div>
    </div>
  );
}

export default Controller;
