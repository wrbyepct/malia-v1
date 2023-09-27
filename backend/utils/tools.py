
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from datetime import datetime
from agent.models import malia_thought_model
from utils.template import MALIA_COMPLAINT_TEMPLATE
from database.memory.short_term_memory import load_short_term_memory_from_json

INFORMATION_ABOUT_JAY = [
    "Information about Jay: Jay's whole name is Jay Hong, you only call him by first name.",
    "Information about Jay: Jay is 29-yo male, Taiwanese, plays jazz guitar, knows a little bit of coding.",
    "Information about Jay: Jay has a girlfriend named Iris, they have been together for 12 years.",
    "Information about Jay: Jay loves dogs, or any smart, cute, friendly animals.",
    "Information about Jay: Jay studied sociology at Tunghai University in Taiwan.",
    "Information about Jay: Jay and Iris has a Red-eared slider turtle called 'Dino' as in 'Dinosaur'"
]


def format_short_term_memory(chat_history):
    moving_summary_buffer = chat_history["moving_summary_buffer"]
    dialogues = ""
    for d in chat_history["short_term_chat_history"]:
        if d["type"] == "human":
            dialogues += "Jay: " + d["data"]["content"] + "\n"
        else:
            dialogues += "MALIA: " + d["data"]["content"] + "\n\n"
    return moving_summary_buffer + "\n\n" + dialogues


def randomly_generate_malia_complaint(nonsense):
    # Load short-term memory from JSON
    chat_history = load_short_term_memory_from_json()
    
    # Reformat the memory into string
    memory = format_short_term_memory(chat_history)

    complaint_model = malia_thought_model
    
    prompt = ChatPromptTemplate.from_template(template=MALIA_COMPLAINT_TEMPLATE)
    
    chain = prompt | complaint_model | StrOutputParser()

    return chain.invoke({"chat_history": memory, 'nonsense': nonsense})


def get_current_time():
    current_time = datetime.now()
    return current_time.strftime("%Y-%m-%d %H:%M:%S")


def reformat_to_hour_min(datetime):
    h_m_s = datetime.split()[-1]
    h_m = ":".join(h_m_s.split(":")[:-1])
    return h_m




if __name__ == '__main__':
    # complaint = asyncio.run(randomly_generate_malia_complaint())
    # print(complaint)
    pass

