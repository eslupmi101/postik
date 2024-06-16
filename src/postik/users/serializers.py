from rest_framework import serializers

from .models import TelegramProfile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'telegram_profile'
        ]


class TelegramProfileGETSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TelegramProfile
        fields = [
            'id', 'user', 'telegram_id', 'username', 'image', 'bio'
        ]
