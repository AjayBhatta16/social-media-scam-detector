import joblib
import pandas as pd 
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
import numpy as np 
from transformers import pipeline 
from google.cloud import storage
import json 
import os 

BUCKET_NAME = "future-campaign-410806.appspot.com"
AI_FUNCTION_ITEMS = {
    "KNN_SCALER": "knn-standard-scaler.bin",
    "KNN_MODEL": "knn-model.joblib",
    "DISTILBERT_FOLDER": "distilbert",
    "KNN_PRED_CLASSES": "knn-encoder-classes.npy",
    "NLP_PRED_CLASSES": "nlp-encoder-classes.npy",
    "META_CLF": "dtree-meta-clf.joblib"
}

storage_client = storage.Client()

"""
NLP Meta-Classifier Microservice

Expected Input Format: 
data: {
    text
    use_knn
    retweet_count   ?
    favorite_count  ?
    num_hashtags    ?
    num_urls        ?
}

Expected Output Format:
{
    scam_type
}
"""
verbose=False
def meta_clf_pipeline(tweet):
    # Initialize bucket client
    bucket = storage_client.bucket(BUCKET_NAME)

    # download binaries from cloud storage
    for k, v in AI_FUNCTION_ITEMS.items():
        if k == "DISTILBERT_FOLDER":
            os.makedirs(os.path.dirname(v), exist_ok=True)
            blob_list = bucket.list_blobs(v)
            for blob in blob_list:
                file_name = blob.name.split("/")[0]
                blob.download_to_filename(f"/tmp/{v}/{file_name}")
        else:
            blob = bucket.blob(v)
            blob.download_to_filename(f"/tmp/{v}")

    # load local binaries
    if verbose:
        print("Loading models from storage...")
    knn_scaler = joblib.load(AI_FUNCTION_ITEMS["KNN_SCALER"])
    knn_model = joblib.load(AI_FUNCTION_ITEMS["KNN_MODEL"])
    nlp_model = pipeline(task="text-classification", model=AI_FUNCTION_ITEMS["DISTILBERT_FOLDER"])
    nlp_pred_encoder = LabelEncoder()
    knn_pred_encoder = LabelEncoder()
    nlp_pred_encoder.classes_ = np.load(AI_FUNCTION_ITEMS["NLP_PRED_CLASSES"])
    knn_pred_encoder.classes_ = np.load(AI_FUNCTION_ITEMS["KNN_PRED_CLASSES"])
    meta_model = joblib.load(AI_FUNCTION_ITEMS["META_CLF"])

    # prepare new input
    if verbose:
        print("Reformatting input data...")
    nlp_x = pd.Series(tweet['text'])
    knn_x = pd.DataFrame.from_dict({k: v for k, v in tweet.items() if k != 'text'}, orient='index').T
    if verbose:
        print("Scaling quantitative metrics...")
    knn_x_scaled = knn_scaler.transform(knn_x)

    # base estimator predictions
    if verbose:
        print("Analyzing quantitative metrics with KNN model...")
    knn_predictions = knn_model.predict(knn_x_scaled)
    if verbose:
        print("KNN predictions:", knn_predictions)
        print("Analyzing text data with DistilBERT model...")
    nlp_predictions_raw = nlp_model(nlp_x.tolist())
    nlp_predictions = [p['label'] for p in nlp_predictions_raw]

    # final meta-classifier prediction
    if verbose:
        print("NLP predictions:", nlp_predictions)
        print("Formatting base estimator predictions for meta-classifier...")
    x_combo_test = pd.DataFrame({
        'nlp_pred': nlp_pred_encoder.transform(nlp_predictions),
        'knn_pred': knn_pred_encoder.transform(knn_predictions)
    })
    if verbose:
        print("Computing final predictions with meta-classifier...")
    meta_predictions = meta_model.predict(x_combo_test)

    # return predictions
    function_response = json.dumps({"scam_type": meta_predictions[0]})
    return function_response, 200, {'Content-Type': 'application/json'}

def nlp_only_pipeline(tweet):
     # Initialize bucket client
    bucket = storage_client.bucket(BUCKET_NAME)

    # download binaries from cloud storage
    os.makedirs(os.path.dirname(f'/tmp/distilbert'), exist_ok=True)
    blob_list = bucket.list_blobs(prefix="distilbert")
    for blob in blob_list:
        file_name = blob.name.split("/")[-1]
        blob.download_to_filename(f'/tmp/{file_name}')
    
    # distilbert prediction
    nlp_model = pipeline(task="text-classification", model=f'/tmp')
    nlp_predictions_raw = nlp_model([tweet])
    nlp_predictions = [p['label'] for p in nlp_predictions_raw]
    
    # http response
    function_response = json.dumps({"scam_type": nlp_predictions[0]})
    return function_response, 200, {'Content-Type': 'application/json'}

def nlp_classifier(request):
    # Parse request data
    request_json = json.loads(request.json)
    if not request_json or 'data' not in request_json:
        return 'No data provided', 400
    tweet = request_json['data']

    # check use_knn and route to pipeline
    return meta_clf_pipeline(tweet) if tweet['use_knn'] else nlp_only_pipeline(tweet)