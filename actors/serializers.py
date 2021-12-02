from rest_framework import serializers
from .models import Actors


class ActorsCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Actors
        fields = '__all__'


class ActorsDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actors
        fields = '__all__'


class ActorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actors
        fields = ('id', 'name', 'image', 'updated_at')