from django.urls import path
from . import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ApplySerializer, ApplicationSerializer
from .models import Application

@api_view(['POST'])
def api_apply_job(request):
    if not request.user.is_job_seeker():
        return Response({'error': 'Only job seekers can apply'}, status=403)

    serializer = ApplySerializer(data=request.data)
    if serializer.is_valid():
        job = serializer.validated_data['job']
        if Application.objects.filter(user=request.user, job=job).exists():
            return Response({'error': 'Already applied'}, status=400)
        application = serializer.save(user=request.user, status='Applied')
        return Response({'message': 'Applied successfully', 'status': 'Applied'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def api_my_applications(request):
    apps = Application.objects.filter(user=request.user)
    serializer = ApplicationSerializer(apps, many=True)
    return Response(serializer.data)

urlpatterns = [
    # HTML Views
    path('apply/<int:pk>/', views.apply_job_view, name='apply_job'),
    path('my-applications/', views.my_applications_view, name='my_applications'),
    path('job/<int:pk>/applications/', views.job_applications_view, name='job_applications'),
    path('update-status/<int:pk>/', views.update_status_view, name='update_status'),

    # API
    path('api/apply/', api_apply_job, name='api_apply'),
    path('api/my-applications/', api_my_applications, name='api_my_applications'),
]