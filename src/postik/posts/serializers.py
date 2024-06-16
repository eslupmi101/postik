from rest_framework import serializers

from .models import Card, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 'user', 'title', 'description',
            'price', 'image', 'created_at'
        ]


class CardSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = [
            'id', 'user', 'title', 'description',
            'image', 'posts', 'is_active', 'created_at'
        ]
