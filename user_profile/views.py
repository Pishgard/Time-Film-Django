from django.http import request
from django.http.response import Http404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from user_profile.serializers import ProfileSerializer
from .models import UserProfile
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import AuthenticationFailed, NotFound
from django.shortcuts import get_object_or_404
from accounts.models import User
from rest_framework.views import APIView


class EditProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)
    # lookup_field = 'id'

    def get(self, request, format=None):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': "You haven't access to this profile"}, status=status.HTTP_403_FORBIDDEN)
 

    def put(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            gender = serializer.validated_data.get('gender', '')
            country = serializer.validated_data.get('country', '')
            UserProfile.objects.filter(user=request.user).update(gender=gender, country=country)
            return Response({'success': 'Profile Successfully updated'}, status=status.HTTP_200_OK)
        except AuthenticationFailed:
            return Response({'error': 'Please login first'}, status=status.HTTP_401_UNAUTHORIZED)
        except NotFound:
            return Response({'error': 'No such profile'}, status=status.HTTP_404_NOT_FOUND)


    def patch(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            gender = serializer.validated_data.get('gender', '')
            country = serializer.validated_data.get('country', '')
            UserProfile.objects.filter(user=request.user).update(gender=gender, country=country)
            return Response({'success': 'Profile Successfully updated'}, status=status.HTTP_200_OK)
        except AuthenticationFailed:
            return Response({'error': 'Please login first'}, status=status.HTTP_401_UNAUTHORIZED)
        except NotFound:
            return Response({'error': 'No such profile'}, status=status.HTTP_404_NOT_FOUND)



class ProfileListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)
    # lookup_field = 'id'

    def get(self, request, format=None):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': "You haven't access to this profile"}, status=status.HTTP_403_FORBIDDEN)
 

    def put(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            gender = serializer.validated_data.get('gender', '')
            country = serializer.validated_data.get('country', '')
            UserProfile.objects.filter(user=request.user).update(gender=gender, country=country)
            return Response({'success': 'Profile Successfully updated'}, status=status.HTTP_200_OK)
        except AuthenticationFailed:
            return Response({'error': 'Please login first'}, status=status.HTTP_401_UNAUTHORIZED)
        except NotFound:
            return Response({'error': 'No such profile'}, status=status.HTTP_404_NOT_FOUND)


    def patch(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            gender = serializer.validated_data.get('gender', '')
            country = serializer.validated_data.get('country', '')
            UserProfile.objects.filter(user=request.user).update(gender=gender, country=country)
            return Response({'success': 'Profile Successfully updated'}, status=status.HTTP_200_OK)
        except AuthenticationFailed:
            return Response({'error': 'Please login first'}, status=status.HTTP_401_UNAUTHORIZED)
        except NotFound:
            return Response({'error': 'No such profile'}, status=status.HTTP_404_NOT_FOUND)



class ProfileAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        profile_serializer = ProfileSerializer(user.profile)
        return Response(profile_serializer.data)