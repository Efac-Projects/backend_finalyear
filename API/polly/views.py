from http.client import OK
from django.shortcuts import render
from django.template import Engine
from grpc import Status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import urlSerializer
import boto3
# Create your views here.


@api_view(['GET'])
def checkPolly(request):
    api_urls = {
        'check-status': 'api/getpolly/'
    }
    return Response(api_urls)


@api_view(['GET'])
def getSpeechOutput(request):
    serializer = request.data

    polly = boto3.client('polly',
                         region_name='us-east-1',
                         aws_access_key_id='',
                         aws_secret_access_key='')

    try:
        result = polly.synthesize_speech(Engine="standard", Text='Hellow there polly in AWS',
                                         OutputFormat='mp3',
                                         VoiceId='Joanna')

        # save the file from the response
        audio = result['AudioStream'].read()

        with open("hellowworld.mp3", "wb") as file:
            file.write(audio)

        return Response("Check audio")
    except:
        return Response(HTTP_400_BAD_REQUEST)
