
from utils.tools import get_current_time

async def talk_shit_with_malia(user_message, malia, message_buffer):
    
    # Get MALIA output
    malia_response = malia.run(user_message)
    
    malia_sent_time = get_current_time()

    # Update malia chat data to message buffer
    message_buffer.malia_text = malia_response
    message_buffer.malia_time = malia_sent_time
    
    # Update short-term memory buffer
    message_buffer.malia_messages = malia.memory.chat_memory.messages
    message_buffer.malia_moving_summary_buffer = malia.memory.moving_summary_buffer
    
    return malia_response



