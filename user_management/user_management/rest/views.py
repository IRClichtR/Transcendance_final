from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .serializers import UserSerializer, AppUserSerializer
from rest_framework import permissions, viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
import requests
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

def user_data(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)

def getProfile_from_db(id):
    try:
        user = User.objects.get(id=id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data, safe=False)

def get_profile_from_school(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get('https://api.intra.42.fr/v2/me', headers=headers)
    if response.status_code == 200:
        return response.json()
    return {}

def me_data(request):
    auth_method = request.session.get('authMethod')
    if auth_method == 'school':
        token = request.session.get('access_token')
        profile_data = get_profile_from_school(token)
        return JsonResponse(profile_data, safe=False)
    else:
        user = request.user
        user_data = {
            'id': user.id,
            'last_login': user.last_login,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'date_joined': user.date_joined,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
        }
        return JsonResponse(user_data, safe=False)

class UpdateUserProfileView(generics.UpdateAPIView):
    serializer_class = AppUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# from django.http import JsonResponse
# from .serializers import UserSerializer, AppUserSerializer
# from rest_framework import permissions, viewsets, status, generics
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import JSONParser
# from rest_framework.decorators import api_view, permission_classes
# import requests

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = get_user_model().objects.all().order_by('id')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

# def user_data(request):
#     users = get_user_model().objects.all()
#     serializer = UserSerializer(users, many=True)
#     return JsonResponse(serializer.data, safe=False)

# def getProfile_from_db(id):
#     user = get_user_model().objects.get(id=id)  # Corrected to use keyword argument
#     serializer = UserSerializer(user)
#     return JsonResponse(serializer.data, safe=False)

# def get_profile_from_school(token):
#     headers = {'Authorization': f'Bearer {token}'}
#     response = requests.get('https://api.intra.42.fr/v2/me', headers=headers)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {}

# def me_data(request):
#     auth_method = request.session.get('authMethod')
#     profile = {}
#     if auth_method == 'school':
#         token = request.session.get('access_token')
#         profile_data = get_profile_from_school(token)
#         profile = JsonResponse(profile_data, safe=False)
#     else:
#         user = request.user
#         user_data = {
# 			'id': user.id,
# 			'last_login': user.last_login,
# 			'username': user.username,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'email': user.email,
# 			'is_active': user.is_active,
# 			'is_staff': user.is_staff,
# 			'date_joined': user.date_joined,
# 			'profile_picture': user.profile_picture,
#         }
#         profile = JsonResponse(user_data, safe=False)
#     return profile

# class UpdateUserProfileView(generics.UpdateAPIView):
#     serializer_class = AppUserSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return self.request.user
