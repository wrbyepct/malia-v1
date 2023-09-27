from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from agent.models import advanced_summary_model
from utils.template import TEST_TWEET_THREAD_TEMPLATE, TWEET_THREAD_TEMPLATE, REWRITE_TWEET_TEMPLATE


def generate_tweets(video):

    video_link = video['url']
    video_title = video['title']
    video_summary = video['summary']
    
    
    print(f"This is the video link: {video_link}")
    print(f"This is the video title: {video_title}")
    
    template = TEST_TWEET_THREAD_TEMPLATE

    prompt = ChatPromptTemplate.from_template(template=template)
    
    chain = prompt | advanced_summary_model | StrOutputParser()

    q = {"video_summary": video_summary, "video_link": video_link, "video_title": video_title}

    twitter_thread = chain.invoke(q)

    return twitter_thread


def rewrite_tweets(tweet):
    template = REWRITE_TWEET_TEMPLATE

    prompt = ChatPromptTemplate.from_template(template=template)
    
    chain = prompt | advanced_summary_model | StrOutputParser()

    q = {"tweet": tweet}

    rewritten_tweet = chain.invoke(q)

    return rewritten_tweet
    

if __name__ == "__main__":

    # start = time.time()
    # with open("../AH-goal-achieving/huberman_summary.txt", "r", encoding="utf-8") as f:
    #     podcast_summary = f.read()

    # podcast_link = "https://www.youtube.com/watch?v=CrtR12PBKb0&t=5s"
    # podcast_title = "Goals Toolkit: How to Set & Achieve Your Goals | Huberman Lab Podcast"

    # podcast = {
    #     "summary": podcast_summary,
    #     "url": podcast_link,
    #     "title": podcast_title
    # }

    # tweets = asyncio.run(generate_tweets(podcast=podcast))
    # end = time.time()

    # print(tweets)
    # print()

    # time_spent = end - start
    # print(f"Time total time spent: {time_spent} seconds")
    pass
    
    