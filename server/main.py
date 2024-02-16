from flask import Flask, request
from flask_cors import CORS
import json

from url_parser import parse
# from scrapers import getTwitterProfile

RISK_SCORE_URL = "https://us-central1-future-campaign-410806.cloudfunctions.net/risk-score-api"
NLP_CLF_URL = "https://us-central1-future-campaign-410806.cloudfunctions.net/nlp-classifier-api"

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
        pass
        # return json.dumps(getTwitterProfile(profile['username']))
    if profile['platform'] == 'facebook':
        return json.dumps({
            "status": 425,
            "message": "Facebook scanning not yet available"
        })
    if profile['platform'] == 'instagram':
        return json.dumps({
            "status": 425,
            "message": "Instagram scanning not yet available"
        })
    return json.dumps({
        "status": 200,
        "platform": profile["platform"],
        "username": profile["username"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0')