from msilib.schema import Class

from attr import fields
from rest_framework import serializers
from .models import approvals


class approveSerializer(serializers.ModelSerializers):
    class Meta:
        model = approvals
        fields = '__all__'
