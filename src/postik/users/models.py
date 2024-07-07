from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

from .constants import DEFAULT_IMAGE_PATH

User = get_user_model()


class TelegramProfile(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name='пользователь',
        related_name='telegram_profile',
        db_index=True,
        on_delete=models.CASCADE
    )
    telegram_id = models.IntegerField(
        verbose_name='telegram id',
        unique=True,
        validators=[MinValueValidator(1)]
    )
    username = models.CharField(
        verbose_name='telegram username',
        max_length=255
    )
    image = models.ImageField(
        verbose_name='изображение',
        upload_to='telegram_profiles',
        default=DEFAULT_IMAGE_PATH
    )
    bio = models.CharField(
        verbose_name='био',
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'telegram профиль'
        verbose_name_plural = 'telegram профили'

    def __str__(self):
        return f'{self.telegram_id}'


class BotAccessToken(models.Model):
    token = models.CharField(
        verbose_name='токен',
        max_length=255,
    )
    bot_name = models.CharField(
        verbose_name='Имя телеграм бота',
        max_length=255,
        unique=True
    )

    class Meta:
        verbose_name = 'Токен доступа телеграм бота'
        verbose_name_plural = 'Токены доступа телеграм бота'

    def __str__(self):
        return f'Токен доступа: {self.bot_name}'
