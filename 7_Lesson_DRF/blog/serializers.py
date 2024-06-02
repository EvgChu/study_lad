from rest_framework import serializers
from .models import *
import io  

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'cat_id')


class PostModel:
    def __init__(self, title, content):
        self.title = title
        self.content = content


class PostSerializerV2(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content  = serializers.CharField()


def encode():
    model = PostModel('title', 'content')
    models_sr = PostSerializerV2(model)
    print(models_sr.data)
    json = JSONRenderer().render(models_sr.data)
    print(json)
    return json


def decode(json=None):
    if not json:
        json = io.BytesIO(b'{"title": "title", "content": "content"}')
    json  = JSONParser().parse(json)
    serializer = PostSerializerV2(data=json)
    serializer.is_valid()
    print(serializer.validated_data)
    return serializer.validated_data

