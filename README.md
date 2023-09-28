# M.A.L.I.A. - Your All-in-One Sassy Voice Assistant

Welcome to the repository of **M.A.L.I.A.**, a web-based chatbot powered by OpenAI with a strong and unique personality, designed to be your assistant and friend. MALIA is not just any chatbot; she is cheeky, sarcastic, very smart, and specializes in Psychology, Neuroscience, and Data Science. Enhanced by LangChain's agent library, she is able to perform more useful tasks that can not be achieved by ChatGPT 3.5, solely based on her own decision! Dive in to explore the myriad of features and capabilities MALIA brings to the table!

## Video demo - https://www.youtube.com/watch?v=cyOpJdShq7E

## 🌟 Features

### 🎭 **Strong Personality:**
MALIA is designed to be more than just a tool; she is your friend and assistant with a cheeky and sarcastic personality. She is a young college girl who is very smart and specializes in Psychology, Neuroscience, and Data Science.

### 🧠 **Long-term Memory:**
Thanks to her advanced long-term memory, MALIA can chat with users with flow and coherency, retrieving relevant information from chat history to maintain the context of the conversation.

### 🗣️ **Natural Voice Interaction:**
Interact with MALIA through voice or text, and she will reply with her true natural voice and typed messages, making the conversation more engaging and friend-like.
This is achieved by using ElevenLabs' voice API. The model ID I use is E2Cf5sotGBcJZ0X8nWeQ, with stability set to 0.23 and similarity 0.9

### 🎥 **Automatic Youtube Scraping, Summary, and Tweet-Sending Pipeline:**
MALIA can summarize specified podcasts from Andrew Huberman, scrape subtitles, convert them to digestible tweets, and send them directly to your Twitter!

### 🧮 **Intelligent and Up-to-Date:**
MALIA is not only good at math but also constantly searches the internet to keep herself updated, ensuring she never loses the flow of conversation with the user.

### 💁 **Not a Yes-Girl:**
MALIA has her own character. She will turn down repeated, unnecessary requests with witty remarks, making interactions with her more realistic and lively.

## 🛠️ Framework

### Frontend:
- **TypeScript**
- **React**
- **Tailwind**

### Backend:
- **Python**
- **FastAPI**

### Database:
- **Chromadb** for vectorstore (Storing MALIA's long-term memory)
- **SQLite3** for chat history
- **JSON** for MALIA's short-term memory

## 🌐 APIs Used
- **tweepy**
- **GoogleSerpAPI**
- **OpenAI**

## 🤖 Chatbot Agent Library
- **LangChain**

## 📜 Chatbot Response
- **OpenAI**
- **ElevenLabs (voice)**

## 🌈 Visual Representation of MALIA's Features
```
+----------------------------------------------+
|                                              |
|   🎭 Strong Personality                      |
|   🧠 Long-term Memory                        |
|   🗣️ Natural Voice Interaction               |
|   🎥 Youtube Scraping & Tweet-Sending        |
|   🧮 Intelligent and Up-to-Date              |
|   💁 Not a Yes-Girl                          |
|                                              |
+----------------------------------------------+
```

## 📌 Note
This project is a demonstration of MALIA's capabilities and is not intended for public use or download. The focus here is to showcase the innovative features and the unique personality of MALIA. Feel free to explore and understand the intricacies of developing a chatbot with a strong personality and advanced features.

