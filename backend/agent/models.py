from langchain.chat_models import ChatOpenAI
from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())


short_term_memory_model = ChatOpenAI(
    temperature=0.5, 
    model='gpt-3.5-turbo'
)

malia_model = ChatOpenAI(
    temperature=0.9, 
    model='gpt-4-1106-preview', 
    max_tokens=512
)


chuck_summary_model = ChatOpenAI(
        temperature=0,
        max_tokens=1000,
        model = 'gpt-4-1106-preview'
    )

# Tweets generator
advanced_summary_model = ChatOpenAI(
    temperature=0.5,
    model='gpt-4-1106-preview',
    request_timeout=120
)

malia_thought_model = ChatOpenAI(
    temperature=0.9, 
    model='gpt-4-1106-preview',
    max_tokens=25
)

