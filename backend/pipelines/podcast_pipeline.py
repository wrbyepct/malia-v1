from pipelines.scraper.youtube_scraper_api import get_youtube_transcript
from pipelines.summarizer.summary import start_summarize
from pipelines.twitter.tweets_generator import generate_tweets
from pipelines.twitter.tweets_sender import send_tweet_thread
import time 


async def podcast_pipeline(url, title, video_id):
    
    print(f"This is the video title to scrape:\n{title}")
    print(f"This is the video url to scrape:\n{url}")
    print()
    # Real-time scrape the video data
    start = time.time()
    
    print("Start scraping the video transcript...")
    
    # Get transcripts through youtube api 
    transcript = get_youtube_transcript(video_id=video_id)
    
    if transcript is None:
        return {"status": "failed", "issue_source": "transcript"}

    print("Scraping transcript done!")
    print()
    
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
    result = send_tweet_thread(tweet_body=tweets)
    if result["status"] != "success":
        return {"status": "failed", "issue_source": "twitter"}
    
    print()

    end = time.time()
    time_spent = end - start
    print(f"Time total time spent: {time_spent} seconds")
    return {"status": "success"}
    