from rest_framework import serializers
from django.contrib.gis.geos import Point
# from rest_framework_gis.fields import GeometryField

from task_manager.models import Task, Checkpoint
from task_manager import services

"""
class TaskSerializer_1(serializers.ModelSerializer):
    # point = GeometryField()
    lat = serializers.CharField()
    lon = serializers.CharField()
    datetime_created = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    # datetime_deadline = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Task
        fields = ['id', 'lat', 'lon', 'description', 'datetime_created', 'datetime_deadline',]
"""

class TaskSerializer(serializers.ModelSerializer):
    # point = GeometryField()
    lat = serializers.CharField()
    lon = serializers.CharField()
    datetime_created = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    # datetime_deadline = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    datetime_planned = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    def __init__(self, *args, **kwargs):
        super(TaskSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        data = dict()
        data['point'] = services.getPointByCoords(validated_data['lat'], validated_data['lon'])
        if data['point'] is None:
            return None
        else:
            return super(TaskSerializer, self).create(data)

    class Meta:
        model = Task
        # fields = ['id', 'status', 'lat', 'lon', 'description', 'datetime_created', 'datetime_deadline', 'datetime_planned',]
        fields = ['id', 'status', 'lat', 'lon', 'description', 'datetime_created', 'datetime_planned',]


class CheckpointSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    lat = serializers.CharField()
    lon = serializers.CharField()
    datetime_created = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False)

    def __init__(self, *args, **kwargs):
        super(CheckpointSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        data = dict()
        data['user_id'] = services.getUserIdByName(validated_data['username'])
        data['point'] = services.getPointByCoords(validated_data['lat'], validated_data['lon'])
        if (data['point'] is None) or (data['user_id'] is None):
            return None
        else:
            services.checkTasks2Execute(data['user_id'], data['point'])
            return super(CheckpointSerializer, self).create(data)

    class Meta:
        model = Checkpoint
        fields = ('username', 'lat', 'lon', 'datetime_created',)

