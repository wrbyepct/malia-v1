# uvicorn main:app
# uvicorn main:app --reload

# FastAPI
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agent.agent import get_agent, check_agent_memory
from database.memory.long_term_memory import persist_to_memory

# Memory database
from database.memory.long_term_memory import delete_vdb
from database.memory.short_term_memory import delete_short_term_history
from database.chat_history.chat_history import delete_whole_chat_history_from_sql, get_frontend_chat_history_from_sql

# Utils audio functions, tool and config
from utils.audio_handle import (
    get_voices, 
    convert_audio_to_text,
    process_audio_file,
)
from utils.tools import (
    randomly_generate_malia_complaint,
    get_current_time,
    reformat_to_hour_min
)
from utils.chat_response import get_malia_response

from dataclasses import dataclass


# Initiate App
app = FastAPI()

# CORS - Origins
# The domain you allow for connecting to backend
origins = {
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:5174",
    "http://localhost:3000"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Recent dialogue buffer
@dataclass
class MessageBuffer:
    jay_text: str=""
    jay_time: str=""
    malia_text: str=""
    malia_time: str=""
    malia_moving_summary_buffer: str=""
    def __post_init__(self):
        self.malia_messages: list=[]

# Initialize message buffer
message_buffer = MessageBuffer()

# Inistialize MALIA
malia = get_agent()

@app.get("/health")
async def check_health():
    return "healthy"

# Get available voices from my ElevenLabs
@app.get("/get-voices")
async def get_the_voices():
    get_voices()
    return "done"


@app.get("/reset")
async def reset_conversation():
    # Reset VDB
    delete_vdb()
    
    # Reset short term history
    delete_short_term_history()
    
    # Reset whole chat history
    delete_whole_chat_history_from_sql()
    
    # Re-initialize malia again
    # Because if we don't leave the app
    # the agent will continue using the summary memory to replay
    global malia
    malia_new = get_agent()
    malia = malia_new
    check_agent_memory(malia)
    print("###Successfully re-initialized MALIA###")
    return {"message": "All chat history reset"}


# Provide frontend with all chat history
@app.get("/get-whole-chat-history")
async def get_frontend_chat(): 
    chat_history = get_frontend_chat_history_from_sql()     
    if chat_history is None:
        return HTTPException(status_code=400, detail="Something went wrong when retrieving whole chat history")    
    return chat_history


# Process frontend recorded voice and sent jay message data to frontend
@app.post("/post-audio-and-get-jay-text/")
async def get_user_text(file: UploadFile = File(...)):
    # Get jay text send timestamp
    jay_sent_time = get_current_time()
    
    # Save timestamp into buffer
    message_buffer.jay_time = jay_sent_time
    
    # Convert jay audio to text
    audio_input = process_audio_file(file)
    
    user_message = convert_audio_to_text(audio_input)
    if not user_message:
        return HTTPException(status_code=400, detail="Failed to convert voice to text")

    # Save jay text to buffer
    message_buffer.jay_text = user_message
    
    # Convert timestamp to frontend time format H:M
    h_m = reformat_to_hour_min(datetime=jay_sent_time)
    
    
    return {"jay_text": user_message, "time": h_m}



# Provdie malia audio response
@app.get("/get-malia-audio-response")
async def provide_malia_audio():
    
    return await get_malia_response(malia=malia, message_buffer=message_buffer)
    

# Accept user text and send back AI voice response
@app.post("/post-user-text-and-get-malia-voice/")
async def get_audio_using_text(user_data: dict):
    jay_text = user_data.get("user_text")
    jay_sent_time = get_current_time()
    
    # Save jay chat to message buffer
    message_buffer.jay_text = jay_text
    message_buffer.jay_time = jay_sent_time
    
    return await get_malia_response(malia=malia, message_buffer=message_buffer)


# Persist dialogues to memory 
@app.get("/request-persist-to-memory")
async def request_persist_to_memory():
    
    try:
        persist_to_memory(message_buffer=message_buffer)
        return {"status": "Successfully persist chat to memory"}
    except Exception as e:
        print("Failed to persist chat to memory")
        return HTTPException(status_code=400, detail="Failed to persist chat to memory")

# Provide malia complaint
@app.post("/post-malia-complaint/")
async def provide_malia_complaint(data: dict):
    
    try:
        nonsense = data.get('nonsense')
        print('This is nonsense from jay')
        print(nonsense)
        complaint = randomly_generate_malia_complaint(nonsense=nonsense)
        print("Request malia complaint successfully")
        return {"complaint": complaint}
    except Exception as e:
        print(e)
        print("Failed to request malia complaint from opneai")
        return {"complaint": "Opps, requesting OpenAI got errors from backend"}
        
    



    