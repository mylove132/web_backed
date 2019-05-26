from rest_framework import serializers
from users.models import *
from django.utils import timezone
from api import models

class UserSerializer(serializers.ModelSerializer):
    # projects = serializers.PrimaryKeyRelatedField(many=True,queryset=models.Project.objects.all())
    create_time = serializers.DateTimeField(required=False,default=timezone.now, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = '__all__'
