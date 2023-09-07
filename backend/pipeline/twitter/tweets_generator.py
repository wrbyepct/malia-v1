from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser


def generate_tweets(podcast):

    podcast_link = podcast['url']
    podcast_tile = podcast['title']
    podcast_summary = podcast['summary']

    tweet_model = ChatOpenAI(temperature=0, model='gpt-4')

    template = """
    PODCAST LINK: {podcast_link}
    PODCAST TITLE: {podcast_title}
    PODCAST SUMMARY: 
    ```
    {podcast_summary}
    ```
    You are a world class journalist and viral twitter influencer, not only that you are also a \
    neuroscientist and a big fan of well-known podcaster Andrew Huberman.
    The information above is a professional summary of a podcast content by Andrew Huberman.
    Please write a viral twitter thread using the context above, and follow all of the rules below:

    1. The content needs to be viral, and get at least 1000 likes.
    2. Makre sure the reader know the content of the tweets are from the mentioned podcast episode by Andrew Huberman.
    3. Make sure at the beginning of the tweet contains the link and title of the podcast
    4. Make sure the content is engaging, informative with good data.
    5. Make sure the thread contains about 7 tweets, with numbering, starting from 1.
    6. Add in some appropriate stickers in each tweet would be nice.
    7. Make sure every tweet should STRICTLY within 270 "characters", not tokens, and NO MORE.
    8. The content should address the salient points of the podcast very well and helpful for readers to apply the information to improve their daily life.
    9. The content needs to give audience actionable advices & insights too.

    TWITTER THREAD: 

    """

    prompt = ChatPromptTemplate.from_template(template=template)
    
    chain = prompt | tweet_model | StrOutputParser()

    q = {"podcast_summary": podcast_summary, "podcast_link": podcast_link, "podcast_title": podcast_tile}

    twitter_thread = chain.invoke(q)

    return twitter_thread


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
    
    