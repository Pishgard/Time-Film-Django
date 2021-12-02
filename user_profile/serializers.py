from rest_framework import serializers
from .models import UserProfile
from accounts.serializers import UserSerializer

class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('user', 'gender', 'bio', 'image_profile')