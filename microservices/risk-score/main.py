import joblib
import pandas as pd 
from google.cloud import storage
from sklearn.pipeline import Pipeline
import json

storage_client = storage.Client()
LOCAL_MODEL_PATH = "/tmp/risk-score-gboost-model.joblib"
BUCKET_NAME = "future-campaign-410806.appspot.com"
BUCKET_MODEL_PATH = "risk-score-gboost-model.joblib"

"""
Risk Score Microservice:

Expected Input Format:
data: {
    followers_count
    friends_count
    verified
    geo_enabled
    protected
    listed_count
    favourites_count
    statuses_count
}

Expected Output Format:
{
    risk_score
}
"""
def user_scam_risk(request):
    # parse request data
    request_json = json.loads(request.json)
    if not request_json or 'data' not in request_json:
        return 'No data provided', 400
    twitter_user = request_json['data']

    # initialize Bucket Client
    bucket = storage_client.bucket(BUCKET_NAME)

    # retrieve and load model binary
    blob = bucket.blob(BUCKET_MODEL_PATH)
    blob.download_to_filename(LOCAL_MODEL_PATH)
    lr_model = joblib.load(LOCAL_MODEL_PATH)

    # prepare data for model prediction
    if twitter_user['friends_count'] == 0:
        twitter_user['friends_count'] = 0.001
    twitter_user['follow_ratio'] = twitter_user['followers_count'] / twitter_user['friends_count']
    model_input_columns = ['verified', 'follow_ratio', 'protected', 'listed_count', 'statuses_count']
    model_input = pd.DataFrame.from_dict(twitter_user, orient='index').T[model_input_columns]
    
    # return predictions
    risk_score = lr_model.predict_proba(model_input)[0][1]
    function_response = json.dumps({"risk_score": risk_score})
    return function_response, 200, {'Content-Type': 'application/json'}