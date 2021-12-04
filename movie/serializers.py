from rest_framework import serializers

from actors.serializers import ActorsDetailSerializer
from .models import Movie


class MovieCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = '__all__'


class MovieDetailSerializer(serializers.ModelSerializer):
    actors = ActorsDetailSerializer(many=True)
    class Meta:
        model = Movie
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    actors = ActorsDetailSerializer(many=True)
    class Meta:
        model = Movie
        fields = '__all__'
        # fields = ('id', 'title', 'genre', 'image', 'description', 'rate', 'year_make', 'time')