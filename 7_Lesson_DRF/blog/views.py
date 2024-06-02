from django.shortcuts import render

from .models import Post
from .serializers import PostSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from django.forms.models import model_to_dict



class PostAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostAPIViewV2(APIView):
    def get(self, request):
        posts = Post.objects.all().values()
        
        return Response(
            {'posts': list(posts),}
        )

    def post(self, request):
        post_new = Post.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            cat_id=request.data['cat_id']
        )
        return Response(
            {'post': model_to_dict(post_new)}
        )
