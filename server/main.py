from flask import Flask, request
import json

from url_parser import parse
from scrapers import getTwitterProfile

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_profile():
    print("scanning...")
    dataStr = request.data.decode()
    data = json.loads(dataStr)
    url = data['url']
    profile = parse(url)
    if profile.status >= 400:
        return json.dumps(profile)
    if profile.platform == 'twitter': 
        return json.dumps(getTwitterProfile(profile.username))
    if profile.platform == 'facebook':
        return json.dumps({
            "status": 425,
            "message": "Facebook scanning not yet available"
        })
    if profile.platform == 'instagram':
        return json.dumps({
            "status": 425,
            "message": "Instagram scanning not yet available"
        })
    return json.dumps(parse(url))

if __name__ == '__main__':
    app.run()