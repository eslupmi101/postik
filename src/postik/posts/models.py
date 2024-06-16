from decimal import Decimal

from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator

from core.models import CreateModel
from users.models import User
from .constants import DEFAULT_CARD_IMAGE_PATH, DEFAULT_POST_IMAGE


class Post(CreateModel):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='posts',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=32,
        validators=[MinLengthValidator(5)]
    )
    description = models.CharField(
        verbose_name='Описание',
        blank=True,
        null=True,
        max_length=255
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    image = models.CharField(
        'эмодзи поста',
        max_length=1,
        default=DEFAULT_POST_IMAGE
    )
    is_active = models.BooleanField(
        verbose_name='Активность',
        default=True
    )

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __str__(self):
        return f'Пост {self.id}: {self.title}'


class Card(CreateModel):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='cards',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=32,
        validators=[MinLengthValidator(5)],
        default='Название'
    )
    description = models.CharField(
        verbose_name='Описание',
        blank=True,
        null=True,
        max_length=255,
        default='Описание'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='cards',
        default=DEFAULT_CARD_IMAGE_PATH
    )
    posts = models.ManyToManyField(
        Post,
        through='CardPost',
        related_name='cards'
    )
    is_active = models.BooleanField(
        verbose_name='Активность',
        default=True
    )

    class Meta:
        verbose_name = 'карточка'
        verbose_name_plural = 'карточки'

    def __str__(self):
        return f'Карта {self.id}: {self.title}'


class CardPost(models.Model):
    card = models.ForeignKey(
        Card,
        verbose_name='карточка',
        related_name='card_posts',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        verbose_name='пост',
        related_name='card_posts',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'карточка-пост'
        verbose_name_plural = 'карточки-посты'
        unique_together = ('card', 'post',)

    def __str__(self):
        return f'{self.card.title} - {self.post.title}'
