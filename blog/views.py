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
from .models import Post

from jalali_date import datetime2jalali, date2jalali


class PostView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    # permission_classes =[IsAuthenticated,]

    def get_object(self):
        posts = get_object_or_404(Post, pk=self.kwargs['id'])
        posts.created_at = datetime2jalali(posts.created_at).strftime('%Y/%m/%d')
        posts.updated_at = datetime2jalali(posts.updated_at).strftime('%Y/%m/%d')

        return posts


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    lookup_field = 'id'

    # permission_classes =[IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'id'

    # permission_classes =[IsAuthenticated,]

    def get_object(self):
        posts = get_object_or_404(Post, pk=self.kwargs['id'])
        posts.created_at = datetime2jalali(posts.created_at).strftime('%Y/%m/%d')
        posts.updated_at = datetime2jalali(posts.updated_at).strftime('%Y/%m/%d')

        return posts
    
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

        query = Post.objects.filter(rooms=search)
        serializers = PostDetailSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)