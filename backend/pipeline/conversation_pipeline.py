
from database.memory.long_term_memory import save_to_vdb
from database.memory.short_term_memory import save_short_term_memory_to_json
from database.chat_history.chat_history import save_chat_dialogue_to_sql

from utils.tools import get_current_time
import asyncio 

async def talk_shit_with_malia(user_message, malia, message_buffer):
    
    # Get MALIA output
    malia_response = await malia.arun(user_message)
    
    malia_sent_time = get_current_time()

    # Update malia chat data to message buffer
    message_buffer.malia_text = malia_response
    message_buffer.malia_time = malia_sent_time
    
    # Update short-term memory buffer
    message_buffer.malia_messages = malia.memory.chat_memory.messages
    message_buffer.malia_moving_summary_buffer = malia.memory.moving_summary_buffer
    
    return malia_response


def persist_to_memory(message_buffer):
     
    user_message = message_buffer.jay_text 
    jay_time = message_buffer.jay_time 
    malia_response = message_buffer.malia_text
    malia_time = message_buffer.malia_time 
    
    short_term_memory = message_buffer.malia_messages
    moving_summary_buffer = message_buffer.malia_moving_summary_buffer
    
    
    # Save dialogues to vdb
    save_to_vdb(
        dialogues=[user_message, malia_response], 
        message_time=[jay_time, malia_time]
    )

    # Save short-term memory to json
    
    save_short_term_memory_to_json(
        short_term_memory=short_term_memory, 
        moving_summary_buffer=moving_summary_buffer
    )
    
    # Save whole chat history to sqlite
    jay_message = ("Jay", user_message, jay_time)
    malia_message = ("MALIA", malia_response, malia_time)
    save_chat_dialogue_to_sql(message=jay_message)
    save_chat_dialogue_to_sql(message=malia_message)    

