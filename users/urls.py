from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

# API Views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    from django.contrib.auth import authenticate
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        from django.contrib.auth import login
        login(request, user)
        return Response({'message': f'Logged in as {user.username}', 'role': user.role})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

urlpatterns = [
    # HTML Views
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # API Endpoints
    path('api/register/', api_register, name='api_register'),
    path('api/login/', api_login, name='api_login'),
]