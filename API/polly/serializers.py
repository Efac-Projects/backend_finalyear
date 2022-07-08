from dataclasses import fields
from rest_framework import serializers
from .models import textTobeAudio


class urlSerializer(serializers.ModelSerializer):
    class Meta:
        model = textTobeAudio
        fields = '__all__'
