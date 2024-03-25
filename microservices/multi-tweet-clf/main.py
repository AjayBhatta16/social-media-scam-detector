import joblib
import pandas as pd 
from google.cloud import storage
from sklearn.pipeline import Pipeline
import json

storage_client = storage.Client()
LOCAL_MODEL_PATH = "/tmp/multitweet-clf-nb.joblib"
BUCKET_NAME = "gs://future-campaign-410806.appspot.com/"
BUCKET_MODEL_PATH = "multitweet-clf-nb.joblib"

categories = [
  'fake_followers_tweets.csv',
  'social_spambots_1_tweets.csv',
  'social_spambots_2_tweets.csv',
  'social_spambots_3_tweets.csv',
  'traditional_spambots_1_tweets.csv',
  'genuine_accounts_tweets.csv',
]

def pct_in_cat(predictions, cat):
    pred_count = 0
    for prediction in predictions:
        if prediction == cat:
            pred_count += 1
    return pred_count / len(predictions)

"""
Multi-Tweet Voting Classifier Microservice:

Expected Input format:
data: {
    predictions: []
}

Expected Output Format:
{
    category
}
"""
def multitweet_clf(request):
    # parse request data
    request_json = json.loads(request.json)
    if not request_json or 'data' not in request_json:
        return 'No data provided', 400
    req_data = request_json['data']
    predictions = req_data['predictions']

    # initialize Bucket Client
    bucket = storage_client.bucket(BUCKET_NAME)

    # retrieve and load model binary
    blob = bucket.blob(BUCKET_MODEL_PATH)
    blob.download_to_filename(LOCAL_MODEL_PATH)
    lr_model = joblib.load(LOCAL_MODEL_PATH)

    # create input
    model_input_obj = {}
    for cat in categories:
        model_input_obj[f"pct_{cat}"] = pct_in_cat(predictions, cat)

    # transform input
    model_input_columns = [f"pct_{cat}" for cat in categories]
    model_input = pd.DataFrame.from_dict(model_input_obj, orient='index').T[model_input_columns]

    # predict
    category = mt_model.predict(model_input)[0]
    function_response = json.dumps({"category": category})
    return function_response, 200, {'Content-Type': 'application/json'}
