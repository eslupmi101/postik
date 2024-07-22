from django.shortcuts import get_object_or_404
from rest_framework import serializers

from posts.models import Post, Lead
from posts.serializers import PostSerializer
from users.models import User


class TelegramProfileSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    username = serializers.CharField(max_length=255)


class PostCreateSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'message_id', 'telegram_id'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        user = get_object_or_404(
            User,
            telegram_profile__telegram_id=validated_data.pop('telegram_id')
        )
        return Post.objects.create(user=user, **validated_data)


class PostPurchaseSerializer(serializers.ModelSerializer):
    telegram_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'message_id', 'telegram_id', 'title', 'description', 'price'
        ]
        read_only_fields = fields

    def get_telegram_id(self, obj):
        return obj.user.telegram_profile.telegram_id


class LeadSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    post_details = serializers.SerializerMethodField()
    author_telegram_id = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = [
            'id', 'post', 'post_details', 'author_telegram_id', 'author',
            'subscriber_username', 'subscriber_telegram_id', 'author_username',
        ]
        read_only_fields = ['id', 'author', 'post_details', 'author_telegram_id', 'author_username']

    def get_post_details(self, instance):
        serializer = PostSerializer(instance.post)
        return serializer.data

    def get_author_telegram_id(self, instance):
        return instance.post.user.telegram_profile.telegram_id

    def get_author_username(self, instance):
        return instance.post.user.telegram_profile.username
