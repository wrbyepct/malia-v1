from pipeline.scraper.youtube_scraper import start_scrape
from pipeline.summarizer.summary import start_summarize
from pipeline.twitter.tweets_generator import generate_tweets
from pipeline.twitter.tweets_sender import send_tweet_thread
import time 
import asyncio


async def podcast_pipeline():
    # Real-time scrape the video data
    start = time.time()
    print("Start scraping the video transcript...")
    data = await start_scrape()
    print("Scraping transcript done!")
    print()

    transcript = data["transcript"]
    url = data['url']
    title = data['title']

    # Summarize the transcript
    print("Start summary process...")
    summary = start_summarize(transcript)
    print("Final summary done!")
    print()

    # Generate nice twits
    print("Start generating tweets...")
    podcast = {"summary": summary, "url": url, "title": title}
    tweets = generate_tweets(podcast)
    print("Generating tweets done!")
    print()
    
    print("The tweets that are going to be sent:")
    print()
    print(tweets)
    print()

    print("Start sending tweets...")
    send_tweet_thread(tweet_body=tweets)
    print("Done sending!")
    
    print()

    end = time.time()
    time_spent = end - start
    print(f"Time total time spent: {time_spent} seconds")
    