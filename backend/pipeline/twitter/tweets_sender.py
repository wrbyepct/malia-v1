import tweepy
from dotenv import load_dotenv
import os
from pipeline.twitter.tweets_generator import rewrite_tweets

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

def split_tweet_body(tweet_body):
    tweet_body = tweet_body.replace("    ", "")
    ## Split the bulk of text into sendable tweets
    tweets = tweet_body.split("\n\n")
    
    return tweets

client = TwitterClient().client
def send_tweet(tweet_id, tweet):
    try:
        # This is the first tweet
        if tweet_id == -1:
            res = client.create_tweet(text=tweet)
        else:
            res = client.create_tweet(in_reply_to_tweet_id=tweet_id, text=tweet)
            
        tweet_id = res.data['id']
        return {"status": "success", "tweet_id": tweet_id}
    except Exception as e:
        print("Something went wrong when creating new tweet")
        print(e)

        return {"status": "failed"}


def check_for_valid_tweet(tweet, tweet_count):
    """Check for valid tweet and return valid tweet"""
    tweet_len = len(tweet)
    # Check if this tweet is within 278 characters and not empty
    if tweet_len <= 278 and tweet_len != 0 :
        return tweet
    else:
        if tweet_len == 0:
            # Handle if there is empty tweet content 
            raise ValueError(f"Failed sending the {tweet_count}th tweet: The tweet content is empty!")
        else:
            # re-write tweets and check again
            print(f"{tweet_count}th tweet exceeds 278 characters. Start rewriting it...")
            rewritten_tweet = rewrite_tweets(tweet=tweet)
            print("This is the rewritten version:")
            print(rewritten_tweet)
            print()
            return check_for_valid_tweet(tweet=rewritten_tweet, tweet_count=tweet_count) # It will eventually return a valid tweet or raise empty tweet error
   

def send_tweet_thread(tweet_body):
    """Take in the tweet thread body, and then do the following:
    1. Split tweet body
    2. Send them to Twitter

    Args:
        tweet_body (string): The bulk of tweet thread body

    Raises:
        ValueError: Problem when sending certain tweet
        Exception: Problem when checking valid tweet
    Returns:
        sending_status(dictionary): Reutrn status "failed" if captures errors, otherwise return status "success"
    """    
    # Split the tweet buld body
    tweets = split_tweet_body(tweet_body)
    
    ## Repeatly send the tweets as a thread
    try:
        tweet_id = -1
        tweet_count = 1
        for tweet in tweets:
            tweet = check_for_valid_tweet(tweet=tweet, tweet_count=tweet_count)
            res = send_tweet(tweet_id=tweet_id, tweet=tweet)
            if res["status"] != "success":
                raise ValueError(f"Failed sending the {tweet_count}th tweet.")
            ## Get main tweet id
            tweet_id = res['tweet_id']
            tweet_count += 1

        print("All tweets successfully sent!")
        return {"status": "success"}
    except ValueError as e:
        print(e)
        
        return {"status": "failed"}
    except Exception as e:
        print("Failed sending all tweets")
        return {"status": "failed"}


if __name__ == "__main__": 
    tweet_body = """1/7 🚀 Buckle up, folks! We're diving into the future of #AI with none other than Ray Kurzweil on the @lexfridman podcast. Prepare for a mind-bending journey into singularity, superintelligence, and immortality. 🎧 Watch here: https://www.youtube.com/watch?v=ykY69lSpDdo&pp=ygU9UmF5IEt1cnp3ZWlsOiBTaW5ndWVsYXJpdHksIFN1cGVyaW50ZWxsaWdlbmNlLCBhbmQgSW1tb3J0YWxpdHk%3D #ArtificialIntelligence #FutureTech 🧠🤖

2/7 🧩 Kurzweil predicts a machine passing the Turing test by 2029! But even with their human-like conversation skills, these models have limitations. They can't do accurate math, for example. Yet, they're paving the way to a future where machines might just be conscious. #AI 🤯🔮

3/7 🤔 How do you feel about interacting more with AI? Kurzweil believes most of our meaningful interactions will happen in a virtual world, emulating all aspects of physical interactions. #VirtualReality #AI 🌐💻

4/7 🧬 Have you heard of AlphaFold? It's a neural network that predicts the 3D shape of proteins! And guess what? Kurzweil believes we'll reach the singularity by 2045. That's when AI will surpass human intelligence! #BioTech #Singularity 🧪💡

5/7 💔 Ever wish you could talk to a deceased loved one again? The future might hold that possibility with the creation of replicants - artificial beings that resemble and interact like our loved ones. #AI #EmotionAI 💞👥

6/7 🧠 Imagine nanobots collecting data from your neocortex! This could help recreate individuals using their digital presence. A bittersweet prospect, but one that could revolutionize how we deal with loss. #Nanotech #BigData 📊🔬

7/7 🎂 Mortality - a bug, not a feature? Kurzweil argues for longevity escape velocity, a future where we can extend our lifespan indefinitely. Imagine the opportunities with a larger, longer-living population! #Longevity #Immortality 🚀🌅

This thread is just the tip of the iceberg. Watch the full podcast for a deep dive into these fascinating topics! 🎧🌐🚀🤖🧬🔬💡👥🎂🌅"""

    send_tweet_thread(tweet_body)
    pass