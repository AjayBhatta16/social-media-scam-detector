import tweepy
from config import twitter

twitterAPIKey = twitter["APIKey"]
twitterAPISecret = twitter["APISecret"]
twitterAccessToken = twitter["AccessToken"]
twitterAccessSecret = twitter["AccessSecret"]

def getTwitterProfile(username):
    auth = tweepy.OAuthHandler(twitterAPIKey, twitterAPISecret)
    auth.set_access_token(twitterAccessToken, twitterAccessSecret)
    api = tweepy.API(auth)
    try:
        if username == "":
            api.verify_credentials()
            print('Successful authentication')
        else:
            api.verify_credentials()
            user = api.get_user(screen_name=username)
    except Exception as e:
        print('failed authentication: '+str(e))
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
testData()