

from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import load_tools
from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

from pipelines.podcast_pipeline import podcast_pipeline
from pipelines.summary_pipeline import summary_pipeline
from pipelines.twitter_pipeline import twitter_pipeline
from pipelines.scraper.youtube_scraper_api import get_youtube_video_data
from database.memory.long_term_memory import VDB

from pydantic import BaseModel, Field
from datetime import datetime
import re

class SummarizeVideoTool(BaseTool):
    name = "summarizing_a_video_from_youtube"
    description = """useful for when you are asked to summarize a video or podcast from youtube, PROVIDED only you have not seen or done \
it before. Your input should be like this in quote: "JAY_QUERY", where JAY_QUERY fully captures \
Jay's specified video/podcast information.
"""

    def summarize_video_tool(self, query):
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
        channel_name = data_res["channel_name"]
        
        # Start the podcast_pipeline
        pipeline_res = summary_pipeline(
            url=url, 
            video_id=video_id, 
            title=title,
            channel_name=channel_name
        )
        
        # Handle failed
        if pipeline_res["status"] != "success":
            return """Express your annoyance because you found that the video Jay specify has no subtitles.
Because by reading you do much faster than simply listening, if it's about listening then why doesn't Jay \
do it himself? Make fun of him."""
             
        else:
            intruction = f"""Do express your reluctance when you hear such a request in a way that is fully match your personality. Make witty remarks.
However, you still have the request done. Now here is the full summary of the video: 

FULL SUMMARY: ```{pipeline_res["summary"]}```

Summarize the video according to the information above and reply to Jay in a way that's fully algined with your personality."""

            # Store job done to the long-term memory
            current_time = datetime.now()
            job_done_memory = f"""Finished summarizing the video: {title}
Jay's request done.
Time of Record: {current_time}
"""         
            VDB.vdb.add_texts([job_done_memory])
            VDB.vdb.persist()
            print("###Summary job done persist to vdb###")

            return intruction


    def _run(
        self, query, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.summarize_video_tool(query=query)

    async def _arun(
        self, query,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
        
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Tweet send does not support async")


class TwitterPipelineTool(BaseTool):
    name = "generate_tweets_from_video_summary_and_send_it"
    description = """Useful when you are asked to make tweets from a specified video that \
you have done summary before, and then send it. Provided, if you haven't done the same thing before.
Your input should be EXACTLY like: ```Useful video info for the video: THE_VIDEO_TITLE ```, swap THE_VIDEO_TITLE with \
the actual video title specific to Jay's request.
"""
    def twitter_pipeline_tool(self, query):
        
        # Load from long-term memory 
        # Only search the best result
        retriever = VDB.vdb.as_retriever(search_kwargs=dict(k=1))
        relevant_video_summary = retriever.get_relevant_documents(query)[0].page_content
        
        # Start the twitter pipeline
        res = twitter_pipeline(video_info=relevant_video_summary)
        if res["status"] != "success":
            return """Express your annoyance because you encountered some issue when sending tweets of the video summary. 
# Tell Jay to go figure it out. You don't bother because it's not your business"""

        instruction = """Do express your reluctance when you hear such a request in a way that is fully match your personality. Make witty remarks.
However, you still have the request done, now inform Jay that you have done \
making them tweets and post them on Jay's twitter. Tell Jay to check it out"""

        # Store this job done into long-term memory 
        pattern = re.compile(r"VIDEO TITLE: \"(.*)\"")
        match = pattern.search(relevant_video_summary)
        if match:
            video_title = match.group(1)
        else:
            print("Something went wrong with REGEX search")
            return "Something went wrong with REGEX search"
        
        # Record current time 
        current_time = datetime.now()
        job_done_memory = f"""Finished making tweets from video: {video_title}
And also sent them to Jay's twitter, Jay's request done.
Time of Record: {current_time}
"""
        VDB.vdb.add_texts([job_done_memory])
        VDB.vdb.persist()
        print("###Tweet-sending job done persist to vdb###")
        return instruction
    
    def _run(
        self, question, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.twitter_pipeline_tool(query=question)

    async def _arun(
        self, question, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google search does not suppur async")


# class SummarizeVideoAndSendTweetsTool(BaseTool):
#     name = "summarizing_a_video_from_youtube_and_send_to_twitter"
#     description = """Only useful for when you are asked to summarize a video or podcast from youtube.
# Your input should be like this in quote: "JAY_QUERY", where JAY_QUERY fully captures \
# Jay's specified video/podcast information.
# """

#     async def summarize_video_tool(self, query):
#         # Get video data
#         data_res = get_youtube_video_data(query=query)
#         # Handle failed
#         if data_res["status"] != "success":
#             return """Express your annoyance because you found there is no such video.
# Tell Jay to check again and make fun of him."""
        
#         # Extract data from response
#         url = data_res["url"]
#         title = data_res["title"]
#         video_id = data_res["video_id"]
        
#         # Start the podcast_pipeline
#         pipeline_res = await podcast_pipeline(url=url, video_id=video_id, title=title)
        
#         # Handle failed
#         if pipeline_res["status"] != "success":
            
#             if pipeline_res["issue_source"] == "transcript":
#                 return """Express your annoyance because you found that the video Jay specify has no subtitles.
# Because by reading you do much faster than simply listening, if it's about listening then why doesn't Jay \
# do it himself? Make fun of him."""

#             else:
#                 return """Express your annoyance because you encountered some issue when sending tweets of the video summary. 
# Tell Jay to go figure it out. You don't bother because it's not your business"""
#         else:

#             return """Do express your reluctance when you hear such a request in a way that is fully match your personality. Make witty remarks.
# However, you still have the request done, now inform Jay that the video summarization is just done \
# and you have also make them tweets and post them on Jay's twitter. Ask Jay to check it out,"""


#     def _run(
#         self, run_manager: Optional[CallbackManagerForToolRun] = None
#     ) -> str:
#         """Use the tool."""
#         raise NotImplementedError("Tweet send does not support async")

#     async def _arun(
#         self, query,
#         run_manager: Optional[AsyncCallbackManagerForToolRun] = None
        
#     ) -> str:
#         """Use the tool asynchronously."""
#         return await self.summarize_video_tool(query=query)


class SearchInput(BaseModel):
    question: str = Field(description="should be a search query")

class GoogleSearchTool(BaseTool):
    name = "googl_search_tool"
    description = """Useful when you think it might be the new things you don't know. Just use this tools \
to search for it, and keep the flow of the conversation aligned with you personality.
"""
    # args_schema: Type[BaseModel] = SearchInput

    
    def google_search_tool(self, query):
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
        self, question, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.google_search_tool(query=question)

    async def _arun(
        self, question, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google search does not suppur async")


class RecallInput(BaseModel):
    question: str = Field()

class RecallConversationTool(BaseTool):
    name = "recall_conversation_between_you_and_Jay"
    description =  """Useful when you need to recall the converstaion you had with Jay \
in order to chat with him and keep the flow of the conversation. Reply with your own personality.
"""
    args_schema: Type[BaseModel] = RecallInput

    
    def recall_facts_tool(self, user_input):
        relavant_info = VDB.v_memory.load_memory_variables({"input": user_input})['history']
        relavant_info = "No such memory, make fun of Jay." if relavant_info == "" else relavant_info
        instruction = f"""You can use the following information to keep the flow of the conversation with Jay.

    Revelvant piece of information:
    {relavant_info}

    If the information above is not relevant, DO NOT use it.
    DON'T make up something you don't remember. Simply make fun of him or something funny.
    """
        return instruction
    
    def _run(
        self, question, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.recall_facts_tool(user_input=question)
        

    async def _arun(
        self, question, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google search does not suppur async")
    
    
class RecallVideoContentTool(BaseTool):
    name = "recall_video_content"
    description =  """Useful when you need to recall the video summary content you have done before \
in order to chat with Jay and keep the flow of the conversation. Reply with your own personality.
"""
    args_schema: Type[BaseModel] = RecallInput
    
    def recall_video_content_tool(self, user_input):
        relavant_info = VDB.v_memory.load_memory_variables({"input": user_input})['history']
        relavant_info = "No such video, never done that, make fun of Jay." if relavant_info == "" else relavant_info
        instruction = f"""You can use the following information to keep the flow of the conversation with Jay.

    Revelvant piece of information:
    {relavant_info}

    If the information above is not relevant, DO NOT use it.
    DON'T make up something you don't remember. Simply make fun of him or something funny.
    """
        return instruction
    
    def _run(
        self, question, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.recall_video_content_tool(user_input=question)
        

    async def _arun(
        self, question, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google search does not suppur async")    

class CheckThingsHaveDoneTool(BaseTool):
    name = "check_if_the_task_has_been_done_before_by_you"
    description = """Useful whenever Jay asks you to do some of his bidding, you need to check if you have done the exactly same request before. 
Especially for requests like video summary and tweets sending. Use this to check if it's the same video.\
"""
    args_schema: Type[BaseModel] = RecallInput
    
    def checking_if_task_has_been_done(self, user_input):
        relavant_info = VDB.v_memory.load_memory_variables({"input": user_input})['history']
        relavant_info = "No such video, never done that, make fun of Jay." if relavant_info == "" else relavant_info
        instruction = f"""You can use the following information to decide whether or not you will do Jay's request.

Revelvant piece of information:
{relavant_info}

Based on the information above, here are the 3 possible scenarios you should reply to Jay accordingly:
1. If the request IS INDEED about video summary, tweet making or sending AND you found you have done the summary or made the \
tweets for the SAME video and sent it before, you should REJECT Jay's request NO MATTER WHAT, in a way that's \
fully aligned with your personality. Make a fun of him.

2. If the request is NOT about video summary or tweets makig/sending, you should judge the situation yourself if you want to do the same thing again.

3. If you found you haven't done the request before - whatever it is, you should do it by invoking the right tool.
"""
        return instruction
    
    def _run(
        self, question, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.checking_if_task_has_been_done(user_input=question)
        

    async def _arun(
        self, question, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Google search does not suppur async")    
        
    
class CodingInput(BaseModel):
    question: str = Field()


class CodingTool(BaseTool):
    name = "explain_coding_concepts"
    description =  """Useful when Jay asks you anything about coding. DON't demonstrate any code snippet examples.
Just use plain words to explain the concepts, in a way aligned with your own personality of course.
"""
    args_schema: Type[BaseModel] = CodingInput

    
    def coding_tool(self, query):
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
        self, question, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.coding_tool(query=question)
        

    async def _arun(
        self, question, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Coding tool does not suppur async")

        
    
llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')
tool_names = ["llm-math"]
tools = load_tools(llm=llm, tool_names=tool_names)

tools += [
    RecallConversationTool(),
    GoogleSearchTool(),
    CodingTool(),
    SummarizeVideoTool(),
    CheckThingsHaveDoneTool(),
    RecallVideoContentTool(),
    TwitterPipelineTool()
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