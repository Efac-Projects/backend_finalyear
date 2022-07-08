import numpy
import json
import requests
from ast import Return
#from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import urlSerializer
import joblib
import pandas as pd
import numpy as np
import librosa
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from keras.models import load_model
import os


labelencoder = LabelEncoder()


# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'check-status': 'api/check-status/'
    }
    return Response(api_urls)


# method to check machine learning output


@api_view(['POST'])
def checkStatues(request):
    serializer = request.data
    print("\n")
    print(serializer)
    print("\n")

    category_list = ['Category1', 'Category2', 'Category3', 'Category4']
    labelencoder = LabelEncoder()
    labelencoder.fit(category_list)
    labelencoder.transform(category_list)
    try:
        model = load_model(
            "D:\Engineering\Sem_8\FYP\Project_App\Backend\API\models\classifier.h5")

        filename = serializer['location']

        print("\n")
        print(filename)
        print("\n")

        audio, sample_rate = librosa.load(filename, res_type='kaiser_fast')
        mfccs_features = librosa.feature.mfcc(
            y=audio, sr=sample_rate, n_mfcc=40)
        mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
        mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)
        predicted_label1 = model.predict(mfccs_scaled_features)
        predicted_label = np.argmax(predicted_label1, axis=1)
        #prediction_class = labelencoder.inverse_transform(predicted_label)

        return Response(predicted_label)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


# check hosted model
@api_view(['POST'])
def checkHostedMOdel(request):
    serializer = request.data
    print("\n")
    print(serializer)
    print("\n")

    category_list = ['Category1', 'Category2', 'Category3', 'Category4']
    labelencoder = LabelEncoder()
    labelencoder.fit(category_list)
    labelencoder.transform(category_list)

    try:

        filename = serializer['location']

        print("\n")
        print(filename)
        print("\n")

        audio, sample_rate = librosa.load(filename, res_type='kaiser_fast')
        mfccs_features = librosa.feature.mfcc(
            y=audio, sr=sample_rate, n_mfcc=40)
        mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
        mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)
        numpyData = {'instances':  mfccs_scaled_features}
        encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncorder)

        url = 'http://c3d6fc8f-2805-4880-8275-4dce4ac202b6.eastus.azurecontainer.io/v1/models/audio-classifier-model:predict'
        headers = {"Content-Type": "application/json"}
        res = requests.post(url, data=encodedNumpyData, headers=headers).json()
        np_array = np.array(res["predictions"])
        predicted_label = np.argmax(np_array, axis=1)
        prediction_class = labelencoder.inverse_transform(predicted_label)

        return Response(prediction_class)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


# method for check url
@api_view(['POST'])
def sendUrl(request):
    serializer = urlSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


class NumpyArrayEncorder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
