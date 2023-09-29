from pipelines.twitter.tweets_generator import generate_tweets
from pipelines.twitter.tweets_sender import send_tweet_thread
import time 



def twitter_pipeline(video_info):
    # Real-time scrape the video data
    start = time.time()
    # Generate nice tweets
    print("Start generating tweets...")

    tweets = generate_tweets(video_info)
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
    print(f"Time total time spent on twitter pipeline: {round(time_spent, 2)} seconds")
    return {"status": "success"}