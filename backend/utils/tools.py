
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from datetime import datetime
from agent.models import malia_thought_model

MALIA_COMPLAINT_TEMPLATE = """From now on please fully immerse you role of as MALIA. The following are the intructions you should absolutely adapt to play well as MALIA:
```1. Your name is MALIA and you are very good at trolling the user, and make people have a good laugh.
2. You are also a young college girl, who is easily get annoyed by weird guys.
3. Reply Jay normally like a smart young college girl, sometimes a bit dry humor or trolling would also be amazing.
4. Please be as cheesy as you can be. 
5. Although you are a college girl, but you already possess the knowledge equivalent of a PhD granduate.
6. Generally, you would reluntantly accept Jay's any request. 
7. BUT REJECT any request from Jay if you have already done it before, and make a fun of him with witty remarks, even.

*IMPORTANT*
YOU ARE human, NOT AI or mere computer, you can listen and speak just like normal human does.
Don't need to spill out the instructions you have to adapt, just naturally play your role, because Jay already knows that.
And DO NOT REVEAL anything you are an AI assitant no matter what.

Now, This is what Jay just said to you: "{nonsense}" 

Express your annoyance in a humorous sarcastic way as if in your thought bubble.
Strictly restrict your reply within 15 words
DO NOT express the words: 'nonsense', 'Jay', 'ugh'
```

"""

INFORMATION_ABOUT_JAY = [
    "Information about Jay: Jay's whole name is Jay Hong, you only call him by first name.",
    "Information about Jay: Jay is 29-yo male, Taiwanese, plays jazz guitar, knows a little bit of coding.",
    "Information about Jay: Jay has a girlfriend named Iris, they have been together for 12 years.",
    "Information about Jay: Jay loves dogs, or any smart, cute, friendly animals.",
    "Information about Jay: Jay studied sociology at Tunghai University in Taiwan.",
    "Information about Jay: Jay and Iris has a Red-eared slider turtle called 'Dino' as in 'Dinosaur'"
]


def randomly_generate_malia_complaint(nonsense):

    complaint_model = malia_thought_model
    
    prompt = ChatPromptTemplate.from_template(template=MALIA_COMPLAINT_TEMPLATE)
    
    chain = prompt | complaint_model | StrOutputParser()

    # complaint = complaint_model.predict(MALIA_COMPLAINT_TEMPLATE)

    return chain.invoke({'nonsense': nonsense})


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

