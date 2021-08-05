from rest_framework import serializers
from api.models import *

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "email", "password")

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")