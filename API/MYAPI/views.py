import numpy
import json
import requests
from ast import Return
#from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import urlSerializer
import pandas as pd
import numpy as np
import librosa
from sklearn.preprocessing import LabelEncoder
import os
from django.core.files.storage import default_storage


import urllib.request
import json
import os
import ssl
from decouple import config

labelencoder = LabelEncoder()


# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'check-status': 'api/check-status/'
    }
    return Response(api_urls)


# self signed https


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


# method to check machine learning output


# check hosted model
# classification of category
@api_view(['POST'])
def checkHostedMOdel(request):
    serializer = request.data
    print("\n")
    print(serializer)
    print("\n")

    level_list = ['level_2', 'level_3', 'level_4', 'level_5',
                  'level_6', 'level_7', 'level_8', 'level_9']
    labelencoder = LabelEncoder()
    labelencoder.fit(level_list)
    labelencoder.transform(level_list)
    filename = serializer['location']

    audio, sample_rate = librosa.load(filename, res_type='kaiser_fast')
    mfccs_features = librosa.feature.mfcc(
        y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
    mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)
    print(mfccs_scaled_features.tolist())

    # this line is needed if you use self-signed certificate in your scoring service.
    allowSelfSignedHttps(True)

    data = {
        "input_data": mfccs_scaled_features.tolist()
    }

    body = str.encode(json.dumps(data))

    url = 'https://level4.centralindia.inference.ml.azure.com/score'
    # Replace this with the API key for the web service
    api_key = config('api_key')

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type': 'application/json',
               'Authorization': ('Bearer ' + api_key), 'azureml-model-deployment': 'default'}

    req = urllib.request.Request(url, body, headers)

    print(req)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        num_array = np.array(result).reshape(-1, 1)
        predicted_label = np.argmax(num_array, axis=1)
        prediction_class = labelencoder.inverse_transform(predicted_label)
        print(prediction_class)

        return Response(prediction_class)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

        return Response(error.info())


# method for check url
@api_view(['POST'])
def sendUrl(request):
    serializer = urlSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# send file to backend and extract mfcc features
@api_view(['POST'])
def level_prediction(request):
    if request.method != "POST":
        return

    try:
        file = request.FILES['File']
        print(file)
        if not file:
            print("File Issue")
            return Response("Error in file!", status=400)

        try:
            default_storage.save(file.name, file)
            print("File saved", file.name)

            audio, sample_rate = librosa.load(
                f'../media/{file.name}', res_type='kaiser_fast')
            mfccs_features = librosa.feature.mfcc(
                y=audio, sr=sample_rate, n_mfcc=40)
            mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
            mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)

            # Do processing here
            default_storage.delete(file.name)
            print("File deleted", file.name)

            # check the level predictin

            level = checkTheLevel(mfccs_scaled_features)

            return Response(level, status=200)

        except Exception as e:
            print(e)

    except Exception as e:
        print(e)
        return Response(f"Server Error!, {e}", status=500)


# send reinforcement learnig schedule; research findings - comment y
@api_view(['GET'])
def sendOptimizeSchedule(request):
    schedule = {
        'Level6': [1, 1, 1, 1, 1, 1],
        'Level7': [1, 1, 1, 1, 1, 1],
        'Level8': [1, 1, 1, 1, 1, 1],
        'Level9': [1, 1, 1, 1, 1, 1]
    }

    return Response(schedule)


# final function for check level inside mfcc extraction - this is function

def checkTheLevel(mfcc):

    level_list = ['Level_2', 'Level_3', 'Level_4', 'Level_5',
                  'Level_6', 'Level_7', 'Level_8', 'Level_9']
    labelencoder = LabelEncoder()
    labelencoder.fit(level_list)
    labelencoder.transform(level_list)

    allowSelfSignedHttps(True)

    data = {
        "input_data": mfcc.tolist()
    }

    body = str.encode(json.dumps(data))

    url = 'https://level4.centralindia.inference.ml.azure.com/score'
    # Replace this with the API key for the web service
    api_key = config('api_key')

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type': 'application/json',
               'Authorization': ('Bearer ' + api_key), 'azureml-model-deployment': 'default'}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        result1 = json.loads(result)
        num_array = np.array(result1)
        predicted_label = np.argmax(num_array, axis=1)
        prediction_class = labelencoder.inverse_transform(predicted_label)
        print(result1)

        return (prediction_class)

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
