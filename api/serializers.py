from rest_framework import serializers
from board.models import Task


class TaskSerializerListCreate(serializers.ModelSerializer):

    updated_at = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    assigner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta():
        model = Task
        fields = ['id', 'name', 'description', 'status', 'creator', 'assigner', 'updated_at']


class TaskAssing(serializers.ModelSerializer):
    
    class Meta():
        model = Task
        fields = ['id']
        read_only_fields = ['name', 'description', 'status', 'creator', 'assigner', 'updated_at']


class TaskByStatusSerializer(serializers.ModelSerializer):

    class Meta():
        model = Task
        fields = ['name', 'creator', 'assigner', 'updated_at']