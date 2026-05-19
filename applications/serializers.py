from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.ReadOnlyField(source='job.title')
    applicant = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Application
        fields = ['id', 'job', 'job_title', 'applicant', 'status', 'applied_at']

class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['job', 'cover_letter']