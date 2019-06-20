from rest_framework import serializers
from api.models import *
from users.serializers import UserSerializer
from django.utils import timezone


class ProjectSerializer(serializers.ModelSerializer):
    # env = serializers.ChoiceField(choices=Project.ENV, source='get_env_display')
    # type = serializers.ChoiceField(choices=Project.TYPE, source='get_type_display')
    ctime = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(required=False, default=timezone.now, format='%Y-%m-%d %H:%M:%S')
    username = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Project
        fields = '__all__'


class ScriptSerializer(serializers.ModelSerializer):
    # request_type = serializers.ChoiceField(choices=Script.REQUEST_TYPE, source='get_request_type_display')
    # protocol = serializers.ChoiceField(choices=Script.REQUEST_TYPE, source='get_protocol_display')
    create_time = serializers.DateTimeField(required=False,format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(required=False, default=timezone.now, format='%Y-%m-%d %H:%M:%S')
    username = serializers.ReadOnlyField(source='user.name')
    projectname = serializers.ReadOnlyField(source='project.name')
    class Meta:
        model = Script
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(required=False, format='%Y-%m-%d %H:%M:%S')
    md5 = serializers.CharField(read_only=True)
    script_name = serializers.ReadOnlyField(source='script.name')
    username = serializers.ReadOnlyField(source='user.name')
    project_name = serializers.ReadOnlyField(source='script.project.name')

    class Meta:
        model = History
        fields = '__all__'