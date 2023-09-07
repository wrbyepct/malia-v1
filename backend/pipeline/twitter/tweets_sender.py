import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_KEY_SECRET = os.getenv('TWITTER_API_KEY_SECRET')
BEARER_TOKEN = rf"{os.getenv('BEARER_TOKEN')}"
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

class TwitterClient:
    def __init__(self) :
        self.client = tweepy.Client(
                        BEARER_TOKEN, 
                        TWITTER_API_KEY, 
                        TWITTER_API_KEY_SECRET,
                        ACCESS_TOKEN,
                        ACCESS_TOKEN_SECRET
                    )
        self.auth = tweepy.OAuth1UserHandler(
                        TWITTER_API_KEY, 
                        TWITTER_API_KEY_SECRET,
                        ACCESS_TOKEN,
                        ACCESS_TOKEN_SECRET
                    )
        
        self.api = tweepy.API(self.auth)


def send_tweet(tweet_id, text):
    client = TwitterClient().client
    try:
        # This is the first tweet
        if tweet_id == -1:
            res = client.create_tweet(text=text)
        else:
            res = client.create_tweet(in_reply_to_tweet_id=tweet_id, text=text)
            
        tweet_id = res.data['id']
        return {"status": "success", "tweet_id": tweet_id}
    except Exception as e:
        print("Something went wrong when creating new tweet")
        print(e)

        return {"status": "failed"}


def send_tweet_thread(tweet_body):
    ## Split the bulk of text into sendable tweets
    tweets = tweet_body.split("\n\n")

    ## Repeatly send the tweets as a thread
    try:
        tweet_id = -1
        for text in tweets:
            res = send_tweet(tweet_id=tweet_id, text=text)
            if res['status'] != "success":
                raise ValueError("Failed sending first tweet")
            
            ## Get main tweet id
            tweet_id = res['tweet_id']

        print("All tweets successfully sent!")
    except ValueError as e:
        print(e)
    except Exception as e:
        print("Failed sending all tweets")


if __name__ == "__main__": 
    pass