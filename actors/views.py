from django.shortcuts import render, get_object_or_404
from rest_framework import generics, views, status
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .models import Actors

from jalali_date import datetime2jalali, date2jalali


class ActorsView(generics.ListAPIView):
    queryset = Actors.objects.all()
    serializer_class = ActorsSerializer
    lookup_field = 'id'
    # permission_classes =[IsAuthenticated,]

    def get_object(self):
        movies = get_object_or_404(Actors, pk=self.kwargs['id'])
        movies.created_at = datetime2jalali(movies.created_at).strftime('%Y/%m/%d')
        movies.updated_at = datetime2jalali(movies.updated_at).strftime('%Y/%m/%d')

        return movies


class ActorsCreateView(generics.CreateAPIView):
    queryset = Actors.objects.all()
    serializer_class = ActorsCreateSerializer
    lookup_field = 'id'

    # permission_classes =[IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save()


class ActorsDetailView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Post.objects.all()
    serializer_class = ActorsDetailSerializer
    lookup_field = 'id'

    # permission_classes =[IsAuthenticated,]

    def get_object(self):
        movies = get_object_or_404(Actors, pk=self.kwargs['id'])
        movies.created_at = datetime2jalali(movies.created_at).strftime('%Y/%m/%d')
        movies.updated_at = datetime2jalali(movies.updated_at).strftime('%Y/%m/%d')

        return movies
    
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.view_count = obj.view_count + 1
        obj.save(update_fields=("view_count", ))
        return super().retrieve(request, *args, **kwargs)


class SearchData(views.APIView):

    def get(self, request):
        search = request.GET.get('rooms', 0)

        if search.isnumeric() is False:
            return Response({"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

        query = Actors.objects.filter(rooms=search)
        serializers = ActorsDetailSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)