from rest_framework import serializers
from prescription.models import Prescription
from user.models import User
from user.serializers import UserBasicSerializer


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = UserBasicSerializer(instance.user).data if instance.user else None
        data["created_by"] = UserBasicSerializer(instance.created_by).data if instance.created_by else None
        return data


class PrescriptionLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ("id", "title")
