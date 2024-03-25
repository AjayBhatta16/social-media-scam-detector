# from tweety.bot import Twitter 
import tweepy
import json
import time

with open("./twitter_keys.json") as infile:
    json_obj = json.load(infile)
    bearer_token = json_obj["bearer_token"]
client = tweepy.Client(bearer_token)

def getTweetDict(tweet):
    return {
        "text": tweet.text
    }

# new getTwitterProfile using official Twitter API
def getTwitterProfile(username):
    user_api_response = client.get_user(
        username=username,
        user_fields=[
            "id",
            "public_metrics",
            "protected",
            "verified",
            "location"
        ]
    )
    user_data = {
        "protected": user_api_response.data.protected,
        "verified": user_api_response.data.verified,
        "geo_enabled": user_api_response.data.location != None and user_api_response.data.location != "",
        "followers_count": user_api_response.data.public_metrics["followers_count"],
        "friends_count": user_api_response.data.public_metrics["following_count"],
        "statuses_count": user_api_response.data.public_metrics["tweet_count"],
        "listed_count": user_api_response.data.public_metrics["listed_count"],
        "favourites_count": 0,
        "tweets": []
    }
    tweets_api_response = client.get_users_tweets(
        user_api_response.data.id,
        exclude=["retweets", "replies"],
        max_results=5,
        tweet_fields=["text"]
    )
    if tweets_api_response.data is not None:
        for tweet in tweets_api_response.data:
            user_data["tweets"].append(tweet.text)
    print(user_data)
    return user_data

"""
# old getTwitterProfile using workaround scraper
# keeping for future reference 
def getTwitterProfile(username):
    try:
        user = Twitter().get_user_info(username)
        tweets = Twitter().get_tweets(username)
        return {
            "status": 200,
            "platform": "Twitter",
            "username": username,
            "data": {
                "bio": user.bio,
                "description": user.description,
                "created_at": int(time.mktime(user.created_at.timetuple()))*1000,
                "fast_followers_count": user.fast_followers_count,
                "followers_count": user.followers_count,
                "normal_followers_count": user.normal_followers_count,
                "location": user.location,
                "media_count": user.media_count,
                "statuses_count": user.statuses_count,
                "verified": user.verified,
                "screen_name": user.screen_name,
                "name": user.name,
                "tweets": [getTweetDict(tweet) for tweet in tweets]
            }
        }
    except Exception as e:
        print('twitter scraping failed: '+str(e))
        return {
            "status": 400,
            "message": "Twitter scanning currently unavailable"
        }
"""

def testConnections():
    getTwitterProfile("")

def testData():
    getTwitterProfile("ajaybhatta49")

# Uncomment this line to test API connectivity
# should return "404 not found" when connected properly
# testConnections()

# Uncomment this line to examine return data
# testData()