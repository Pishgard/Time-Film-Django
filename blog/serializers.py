from rest_framework import serializers
from .models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = '__all__'


class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'image', 'status', 'updated_at')