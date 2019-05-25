from rest_framework import serializers
from users.models import *
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(required=False,default=timezone.now, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = '__all__'
