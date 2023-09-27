

from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import load_tools
from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from pipeline.podcast_pipeline import podcast_pipeline
from pipeline.scraper.youtube_scraper_api import get_youtube_video_data
from database.memory.long_term_memory import vdb

from pydantic import BaseModel, Field

# class PodcastInput(BaseModel):
#     question: Optional[Union[str, list, dict, tuple]] = Field(description="should be a search query string text")

class SummarizeVideoTool(BaseTool):
    name = "Summarizing_a_video_or_podcast_from_youtube"
    description = """Only useful for when you are asked to summarize a video or podcast from youtube.
Your input should be like this in quote: "JAY_QUERY", where JAY_QUERY fully captures \
Jay's specified video/podcast information.
"""

    async def summarize_video_tool(self, query):
        # Get video data
        data_res = get_youtube_video_data(query=query)
        # Handle failed
        if data_res["status"] != "success":
            return """Express your annoyance because you found there is no such video.
Tell Jay to check again and make fun of him."""
        
        # Extract data from response
        url = data_res["url"]
        title = data_res["title"]
        video_id = data_res["video_id"]
        
        # Start the podcast_pipeline
        pipeline_res = await podcast_pipeline(url=url, video_id=video_id, title=title)
        
        # Handle failed
        if pipeline_res["status"] != "success":
            
            if pipeline_res["issue_source"] == "transcript":
                return """Express your annoyance because you found that the video Jay specify has no subtitles.
Because by reading you do much faster than simply listening, if it's about listening then why doesn't Jay \
do it himself? Make fun of him."""

            else:
                return """Express your annoyance because you encountered some issue when sending tweets of the video summary. 
Tell Jay to go figure it out. You don't bother because it's not your business"""
        else:

            return """Do express your reluctance when you hear such a request in a way that is fully match your personality. Make witty remarks.
However, you still have the request done, now inform Jay that the video summarization is just done \
and you have also make them tweets and post them on Jay's twitter. Ask Jay to check it out,"""


    def _run(
        self, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        raise NotImplementedError("Tweet send does not support async")

    async def _arun(
        self, query,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
        
    ) -> str:
        """Use the tool asynchronously."""
        return await self.summarize_video_tool(query=query)



class PodcastTool(BaseTool):
    name = "Summarizing_Andrew_Huberman_newest_Podcast"
    description = """useful for when you are asked to summarize newest podcast episode of \
    Andrew Huberman, The input MUST be a valid tuple.
    """
    # args_schema: Type[BaseModel] = PodcastInput

    async def pocast_tool(self, question):
        """Use this when Jay want you to summarize the newest podcast of Andrew Huberman. 
    """
        await podcast_pipeline()

        return """Do express your reluctance when you hear such a request in a way that is fully match your personality. Make witty remarks.
    However, you still have the request done, now inform Jay that Andrew Huberman podcast summarization is just done \
    and you have also make them tweets and post them on Jay's twitter. Ask Jay to check it out,"""

    
    def _run(
        self, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        raise NotImplementedError("Tweet send does not support async")

    async def _arun(
        self, question,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
        
    ) -> str:
        """Use the tool asynchronously."""
        return await self.pocast_tool(question=question)
    

class SearchInput(BaseModel):
    question: str = Field(description="should be a search query")

class GoogleSearchTool(BaseTool):
    name = "googl_search_tool"
    description = """Useful when you think it might be the new things you don't know. Just use this tools \
to search for it, and keep the flow of the conversation aligned with you personality.
"""
    # args_schema: Type[BaseModel] = SearchInput

    
    async def google_search_tool(self, query):
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
    
    def _run(
        self, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        raise NotImplementedError("Google search does not suppur sync")

    async def _arun(
        self, question, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return await self.google_search_tool(query=question)


class RecallInput(BaseModel):
    question: str = Field()

class RecallFactsTool(BaseTool):
    name = "recall_facts_between_you_and_Jay"
    description =  """Useful when you need to recall something what Jay said before \
in order to chat with him and keep the flow of the conversation. Reply with your own personality.
"""
    args_schema: Type[BaseModel] = RecallInput

    
    async def recall_facts_tool(self, user_input):
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
    
    def _run(
        self, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        raise NotImplementedError("Google search does not suppur sync")

    async def _arun(
        self, question, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return await self.recall_facts_tool(user_input=question)
    
    
class CodingInput(BaseModel):
    question: str = Field()


class CodingTool(BaseTool):
    name = "explain_coding_concepts"
    description =  """Useful when Jay asks you anything about coding. DON't demonstrate any code snippet examples.
Just use plain words to explain the concepts, in a way aligned with your own personality of course.
"""
    args_schema: Type[BaseModel] = CodingInput

    
    async def coding_tool(self, query):
        """Useful when Jay asks you anything about coding. DON't demonstrate any code examples.
    Just use plain words to explain the concepts, in a way aligned wtih your own personality of course.
    """
        instruction = f"""The following is Jay's question about coding: 
    {query}

    DON't demonstrate any code examples.
    Just use plain words to explain the concepts, in a way aligned your own personality of course.  
    """
        return instruction
        
    def _run(
        self, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        raise NotImplementedError("Coding tool does not suppur sync")

    async def _arun(
        self, question: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        return await self.coding_tool(query=question)

        
    
llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')
tool_names = ["llm-math"]
tools = load_tools(llm=llm, tool_names=tool_names)

tools += [
    RecallFactsTool(),
    GoogleSearchTool(),
    CodingTool(),
    SummarizeVideoTool()
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