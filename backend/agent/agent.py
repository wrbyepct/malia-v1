
from langchain.memory import ConversationSummaryBufferMemory

from langchain.agents import OpenAIFunctionsAgent, AgentExecutor, AgentType, initialize_agent
from langchain.schema import messages_from_dict

from agent.agent_tools import tools
from database.memory.short_term_memory import load_short_term_memory_from_json
from utils.template import MALIA_INSTRUCTION, get_prompt

from agent.models import malia_model, short_term_memory_model
# Prepare short-term memory for the model
def get_summary_memory(data):
    # Create memory
    sum_memory = ConversationSummaryBufferMemory(
        llm=short_term_memory_model,
        ai_prefix="MALIA",
        human_prefix="Jay",
        memory_key='chat_history',
        max_token_limit=200,
        return_messages=True
    )
    # If there's short-term memory in json, load them to model
    if data:
        chat_history = messages_from_dict(data['short_term_chat_history'])
        moving_summary_buffer = data['moving_summary_buffer']

        sum_memory.chat_memory.messages = chat_history
        sum_memory.moving_summary_buffer = moving_summary_buffer 
    
    return sum_memory

# Intialize agent
def get_agent():
    # load memory from json 
    data = load_short_term_memory_from_json()

    # Inititate ConversationSummaryMemory
    sum_memory = get_summary_memory(data)

    # Prepare the agent
    prompt = get_prompt()
    agent = OpenAIFunctionsAgent(
        tools=tools,
        llm=malia_model,
        verbose=True,
        prompt=prompt,
    )
    agent = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=sum_memory,
        verbose=True,
        handle_parsing_errors=True
    )
    return agent

def check_agent_memory(agent):
    chat_history= agent.memory.chat_memory.messages
    moving_summary_buffer = agent.memory.moving_summary_buffer
    print("Current MALIA buffer chat history:")
    print(chat_history)
    
    print("Current MALIA moving buffer summary:")
    print(moving_summary_buffer)


# Simpler way to initialize agent    
def get_agent_with_simpler_way():
    # load memory from json 
    data = load_short_term_memory_from_json()

    # Inititate ConversationSummaryMemory
    sum_memory = get_summary_memory(data)    
    agent = initialize_agent(
        tools=tools,
        llm=malia_model,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory = sum_memory,
        verbose=True,
        max_iteration=5,
        early_stoping_method='generate',
        SystemMessagePromptTemplate=MALIA_INSTRUCTION
    )
    agent.agent.llm_chain.prompt.messages[0].prompt.template = MALIA_INSTRUCTION

    # initialize Malia agent 
    # Don't need to provide prompt template first
    # Cause we best do it in conversation pipeline

    
    


