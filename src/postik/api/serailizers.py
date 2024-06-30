from rest_framework import serializers

from django.shortcuts import get_object_or_404
from posts.models import Post
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
