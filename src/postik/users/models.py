from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()


class TelegramProfile(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name='user',
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

    class Meta:
        verbose_name = 'telegram profile'
        verbose_name_plural = 'telegram profiles'
