from django.urls import path
from . import views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import JobSerializer
from .models import Job

@api_view(['GET'])
@permission_classes([AllowAny])
def api_job_list(request):
    jobs = Job.objects.filter(is_active=True)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

urlpatterns = [
    # HTML Views
    path('', views.job_list_view, name='job_list'),
    path('<int:pk>/', views.job_detail_view, name='job_detail'),
    path('add/', views.job_create_view, name='job_add'),
    path('<int:pk>/edit/', views.job_edit_view, name='job_edit'),
    path('<int:pk>/delete/', views.job_delete_view, name='job_delete'),
    path('my-jobs/', views.recruiter_jobs_view, name='recruiter_jobs'),
    path('<int:pk>/match/', views.match_score_view, name='match_score'),

    # API
    path('api/jobs/', api_job_list, name='api_job_list'),
]