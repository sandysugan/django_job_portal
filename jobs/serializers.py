from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'company',
            'location', 'salary', 'required_skills',
            'created_by_username', 'created_at', 'is_active'
        ]