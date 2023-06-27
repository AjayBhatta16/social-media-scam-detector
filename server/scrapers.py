from tweety.bot import Twitter 
import json
import time

def getTweetDict(tweet):
    return {
        "text": tweet.text
    }

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


def testConnections():
    getTwitterProfile("")

def testData():
    getTwitterProfile("ajaybhatta49")

# Uncomment this line to test API connectivity
#testConnections()

# Uncomment this line to examine return data
#testData()