from flask import Flask, request
import json

from url_parser import parse

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_profile():
    print("scanning...")
    dataStr = request.data.decode()
    data = json.loads(dataStr)
    url = data['url']
    return json.dumps(parse(url))

if __name__ == '__main__':
    app.run()