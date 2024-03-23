from flask import Flask, request
from flask_cors import CORS
import json

from url_parser import parse
from scrapers import getTwitterProfile, getTweet

from google.auth import app_engine
from google.cloud import functions_v1

gcp_credentials = app_engine.Credentials()
function_cli = functions_v1.services.CloudFunctionsServiceClient(credentials=gcp_credentials)

def call_gcp_serverless(url, data):
    res = function_cli.generate_upload_url(parent=url, body=data)
    return res

RISK_SCORE_URL = "https://us-central1-future-campaign-410806.cloudfunctions.net/risk-score-api"
NLP_CLF_URL = "https://us-central1-future-campaign-410806.cloudfunctions.net/nlp-classifier-api"
MULTI_TWEET_URL = "https://us-central1-future-campaign-410806.cloudfunctions.net/multi-tweet-clf"

def twitter_analyze(username):
    # scrape twitter profile
    tw_profile = getTwitterProfile(username)

    # scrape tweets
    tweets = []
    for tweet_id in tw_profile['tweet_ids']:
        tweets.append(getTweet(tweet_id))

    # call risk score api
    risk_score_data = {
        followers_count: tw_profile['followers_count'],
        friends_count: tw_profile['friends_count'],
        verified: tw_profile['verified'],
        geo_enabled: tw_profile['geo_enabled'],
        protected: tw_profile['protected'],
        listed_count: tw_profile['listed_count'],
        favourites_count: tw_profile['favourites_count'],
        statuses_count: tw_profile['statuses_count']
    }
    risk_score = call_gcp_serverless(RISK_SCORE_URL, risk_score_data)['risk_score']

    # classify with tweets
    multi_tweet_data = {
        'predictions': []
    }
    for tweet in tweets:
        clf_data = {
            'text': tweet['text'],
            'use_knn': False 
        }
        tweet_class = call_gcp_serverless(NLP_CLF_URL, clf_data)['scam_type']
        multi_tweet_data['predictions'].append(tweet_class)
    scam_type = call_gcp_serverless(MULTI_TWEET_URL, multi_tweet_data)['category']

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