from rest_framework import serializers


class TelegramProfileSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    username = serializers.CharField(max_length=255)
