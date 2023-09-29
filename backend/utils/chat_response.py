from pipelines.conversation_pipeline import talk_shit_with_malia
from utils.tools import reformat_to_hour_min
from utils.audio_handle import convert_text_to_speech


async def get_malia_response(malia, message_buffer):
    
    # Get malia text
    malia_text = await talk_shit_with_malia(
        user_message=message_buffer.jay_text,
        malia=malia,
        message_buffer=message_buffer
    )
    
    # Record malia response time
    malia_time = message_buffer.malia_time
    
    h_m = reformat_to_hour_min(datetime=malia_time)
    
    # Covner malia text response and then play it 
    convert_text_to_speech(malia_text)
    
    # Directly return malia respone
    return {'malia_text': message_buffer.malia_text, 'malia_time': h_m}
    