

from rest_framework import serializers
from .models import audios


class urlSerializer(serializers.ModelSerializer):
    class Meta:
        model = audios
        fields = '__all__'
