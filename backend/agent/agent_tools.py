

from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import load_tools
from langchain.tools import tool, Tool, BaseTool
from typing import Optional, Type, Union
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from pipeline.podcast_pipeline import podcast_pipeline
from database.memory.long_term_memory import vdb

from pydantic import BaseModel, Field


# def process_thought(thought):
#     return thought

# DynamicTool = Tool(
#     name="Thought Processing",
#     description="""This is useful for when you have a thought that you want to use in a task, 
# but you want to make sure it's formatted correctly. 
# Input is your thought and self-critique and output is the processed thought.""",
#     func=process_thought,
# )



# def output_malia(malia_output):
#     return malia_output

# OutputMaliaTool = Tool(
#     name="Return MALIA's response to the user whenever there is MALIA's response in your 'Observation'",
#     description="""Use this to directly return MALIA's ouput to the user, DON'T modify anything coming back from MALIA.
# DO NOT add any of you thought in it.
# """,
#     func=output_malia
# )


# def mock_twitter_tool(_):
#     instruction = """"MALIA, now please now inform Jay that Andrew Huberman podcast summarize request is now just done \
# and you have also make them tweets and post them on Jay's twitter. Ask Jay to check it out"     
# """
#     malia = conversation_pipeline(instruction)
#     return f"""Here is MALIA's response, use "Return MALIA's response to the user" as next action step.
# MALIA: {malia}"""


class PodcastInput(BaseModel):
    question: Optional[Union[str, list, dict, tuple]] = Field(description="should be a search query string text")


class PodcastTool(BaseTool):
    name = "Summarizing_Andrew_Huberman_newest_Podcast"
    description = """useful for when you are asked to summarize newest podcast episode of \
    Andrew Huberman, The input MUST be a valid tuple.
    """
    args_schema: Type[BaseModel] = PodcastInput

    def _run(
        self, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        raise NotImplementedError("Tweet send does not support async")

    async def _arun(
        self, question: Optional[Union[str, list, dict, tuple]],
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
        
    ) -> str:
        """Use the tool asynchronously."""
        return await pocast_tool(question)
    



class SearchInput(BaseModel):
    question: str = Field(description="should be a search query")


class GoogleSearchTool(BaseTool):
    name = "googl_search_tool"
    description = """Useful when you think it might be the new things you don't know. Just use this tools \
to search for it, and keep the flow of the conversation aligned with you personality.
"""
    args_schema: Type[BaseModel] = SearchInput

    def _run(
        self, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        raise NotImplementedError("Google search does not suppur sync")

    async def _arun(
        self, question, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return await google_search_tool(question)


class RecallInput(BaseModel):
    question: str = Field()


class RecallFactsTool(BaseTool):
    name = "recall_facts_between_you_and_Jay"
    description =  """Useful when you need to recall something what Jay said before \
in order to chat with him and keep the flow of the conversation. Reply with your own personality.
"""
    args_schema: Type[BaseModel] = RecallInput

    def _run(
        self, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        raise NotImplementedError("Google search does not suppur sync")

    async def _arun(
        self, question, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return await recall_facts_tool(question)


class CodingInput(BaseModel):
    question: str = Field()


class CodingTool(BaseTool):
    name = "explain_coding_concepts"
    description =  """Useful when Jay asks you anything about coding. DON't demonstrate any code snippet examples.
Just use plain words to explain the concepts, in a way aligned with your own personality of course.
"""
    args_schema: Type[BaseModel] = CodingInput

    def _run(
        self, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        raise NotImplementedError("Coding tool does not suppur sync")

    async def _arun(
        self, question: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return await coding_tool(question)



# Podcast pipline tool
# @tool("summarize_newest_podcast_of_Andrew_Huberman")
async def pocast_tool(question: Optional[Union[str, list, dict, tuple]]):
    """Use this when Jay want you to summarize the newest podcast of Andrew Huberman. 
"""
    await podcast_pipeline()

    return """Do express your reluctance when you hear such a request in a way that is fully match your personality. Make witty remarks.
However, you still have the request done, now inform Jay that Andrew Huberman podcast summarization is just done \
and you have also make them tweets and post them on Jay's twitter. Ask Jay to check it out,"""



# Recall memory tool
# @tool("recall_facts_between_you_and_Jay")
async def recall_facts_tool(user_input):
    """Useful when you need to recall something what Jay said before \
in order to chat with him and keep the flow of the conversation. Reply with your own personality.
"""
    relavant_info = vdb.v_memory.load_memory_variables({"input": user_input})['history']
    relavant_info = "No such memory, make fun of Jay." if relavant_info == "" else relavant_info
    instruction = f"""You can use the following context to keep the flow of the conversation with Jay.

Revelvant piece of previous conversation:
{relavant_info}

If the information above is not relevant, DO NOT use it.
DON'T make up something you don't remember. Simply make fun of him or something funny.
"""
    return instruction


# @tool("google_search_tool")
async def google_search_tool(query):
    """Useful when you think it might be the new things you don't know. Just use this tools \
to search for it, and keep the flow of the conversation aligned with you personality.
"""
    search = GoogleSerperAPIWrapper()
    result = search.run(query)
    instruction = f"""The following is the search result: 
{result}

Reply Jay's question according to the search result, but in a way that's fully algin with your personality.  
"""
    return instruction
    

# @tool("coding_tool")
async def coding_tool(query):
    """Useful when Jay asks you anything about coding. DON't demonstrate any code examples.
Just use plain words to explain the concepts, in a way aligned wtih your own personality of course.
"""
    instruction = f"""The following is Jay's question about coding: 
{query}

DON't demonstrate any code examples.
Just use plain words to explain the concepts, in a way aligned your own personality of course.  
"""
    return instruction
        
    
llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')
tool_names = ["llm-math"]
tools = load_tools(llm=llm, tool_names=tool_names)

tools += [
    RecallFactsTool(),
    GoogleSearchTool(),
    PodcastTool(),
    CodingTool()
]


# PocastTool = Tool(
#     name="summarize_newest_podcast_of_Andrew_Huberman",
#     description="""Use this when the user want you to summarize the newest podcast of Andrew Huberman. 
# """,
#     func=pocast_tool
# )
# RecallFacts = Tool(
#     name="recall_facts_tool",
#     description="""Useful when you need to recall something what Jay said before \
# in order to chat with him and keep the flow of the conversation. Reply with your own personality.
# """,
#     func=recall_facts_tool
# )
# GoogleSearchTool = Tool(
#     name="google_search_tool",
#     description="""Useful when you think it might be the new things you don't know. Just use this tools \
# to search for it, and keep the flow of the conversation aligned with you personality.
# """,
#     func=google_search_tool
# )




# # OutputMaliaTool = Tool(
# #     name="Return MALIA's response only to the user and don't add any other extra words of yours.",
# #     description="""Use this to directly return MALIA's ouput to the user, DON'T modify anything coming back from MALIA.
# # You don't need say anything else.
# # """,
# #     func=output_malia
# # )


# tools = [
#     MockTwitterTool,
#     FeedToMaliaTool,
#     OutputMaliaTool,
#     DynamicTool
# ]