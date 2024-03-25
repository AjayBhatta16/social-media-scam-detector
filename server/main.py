from flask import Flask, request
from flask_cors import CORS
import json
import requests

from url_parser import parse
from scrapers import getTwitterProfile

from google.auth import app_engine
from google.cloud import functions_v1

default_data = {
    'protected': False, 
    'verified': False, 
    'geo_enabled': False, 
    'followers_count': 16, 
    'friends_count': 32, 
    'statuses_count': 183, 
    'listed_count': 0, 
    'favourites_count': 0, 
    'tweets': [
        'Looks like Russell Wilson left his hairline in Denver https://t.co/kFFOGHn1om',
        '7 Conference Championship appearances in 13 years with no rings to show for it. The 49ers are the edging champions of the century. https://t.co/nnkZfRBgmR', 
        'Steve Wilks joining Duo Lingo so he can have fun learning Chinese: https://t.co/M8H1h1qeB8', 
        'Brock Purdy joining Duo Lingo so he can have fun learning Chinese: https://t.co/J8IsJYA6W2', 
        "The Bills could've drafted 3 of the 4 remaining playoff QBs but decided to stick with Caucasian Kaepernick https://t.co/MmpBwBZZQd"
    ]
}

CLOUD_SHELL_TESTING_FLAG = True
if CLOUD_SHELL_TESTING_FLAG:
    function_cli = functions_v1.CloudFunctionsServiceClient()
else: 
    gcp_credentials = app_engine.Credentials()
    function_cli = functions_v1.services.CloudFunctionsServiceClient(credentials=gcp_credentials)

def call_gcp_serverless(url, data):
    data_json = json.dumps({ "data": data })
    res = requests.post(url, json=data_json)
    if res.status_code == 200:
        return res
    else:
        print(url)
        print(res.text)
        return False

RISK_SCORE_URL = "https://us-central1-future-campaign-410806.cloudfunctions.net/risk-score-api"
NLP_CLF_URL = "https://us-central1-future-campaign-410806.cloudfunctions.net/nlp-classifier-api"
MULTI_TWEET_URL = "https://us-central1-future-campaign-410806.cloudfunctions.net/multi-tweet-clf"

def twitter_analyze(username):
    # scrape twitter profile
    if CLOUD_SHELL_TESTING_FLAG:
        tw_profile = default_data
    else: 
        tw_profile = getTwitterProfile(username)

    # scrape tweets
    tweets = []
    for tweet in tw_profile['tweets']:
        tweets.append({
            'text': tweet 
        })

    # call risk score api
    risk_score_data = {
        'followers_count': tw_profile['followers_count'],
        'friends_count': tw_profile['friends_count'],
        'verified': tw_profile['verified'],
        'geo_enabled': tw_profile['geo_enabled'],
        'protected': tw_profile['protected'],
        'listed_count': tw_profile['listed_count'],
        'favourites_count': tw_profile['favourites_count'],
        'statuses_count': tw_profile['statuses_count']
    }
    serverless_res = call_gcp_serverless(RISK_SCORE_URL, risk_score_data)
    if not serverless_res:
        return json.dumps({
            "status": 500,
            "message": "Internal Server Error"
        })
    risk_score = serverless_res.json()['risk_score']

    # classify with tweets
    multi_tweet_data = {
        'predictions': []
    }
    for tweet in tweets:
        clf_data = {
            'text': tweet['text'],
            'use_knn': False 
        }
        serverless_res = call_gcp_serverless(NLP_CLF_URL, clf_data)
        if not serverless_res:
            return json.dumps({
                "status": 500,
                "message": "Internal Server Error"
            })
        tweet_class = serverless_res.json()['scam_type']
        multi_tweet_data['predictions'].append(tweet_class)
    serverless_res = call_gcp_serverless(MULTI_TWEET_URL, multi_tweet_data)
    if not serverless_res:
        return json.dumps({
            "status": 500,
            "message": "Internal Server Error"
        })
    scam_type = serverless_res.json()['category']

    # response
    return json.dumps({
        "status": 200,
        "platform": "Twitter",
        "username": username,
        "riskScore": risk_score,
        "type": scam_type
    })

def facebook_analyze(username):
    return json.dumps({
        "status": 425,
        "message": "Facebook scanning not yet available"
    })

def instagram_analyze(username):
    return json.dumps({
        "status": 425,
        "message": "Instagram scanning not yet available"
    })

def default_analyze(platform, username):
    json.dumps({
        "status": 200,
        "platform": platform,
        "username": username
    })

app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods=['GET'])
def test_server():
    return json.dumps({
        "status": 200,
        "msg": "SocialGuard Flask Middleware Server"
    })

@app.route('/scan', methods=['POST'])
def scan_profile():
    print("scanning...")
    dataStr = request.data.decode()
    data = json.loads(dataStr)
    url = data['url']
    profile = parse(url)
    if profile['status'] >= 400:
        return json.dumps(profile)
    if profile['platform'] == 'twitter': 
        return twitter_analyze(profile['username'])
    if profile['platform'] == 'facebook':
        return facebook_analyze(profile['username'])
    if profile['platform'] == 'instagram':
        return instagram_analyze(profile['username'])
    return default_analyze(profile['platform'], profile['username'])

if __name__ == '__main__':
    app.run(host='0.0.0.0')