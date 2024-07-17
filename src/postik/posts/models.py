from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator)
from django.db import models

from core.models import CreateModel
from users.models import User
from .constants import (DEFAULT_CARD_IMAGE_PATH, DEFAULT_POST_IMAGE,
                        MAX_POST_PRICE)


class Post(CreateModel):
    message_id = models.CharField(
        max_length=255,
        verbose_name='id телеграм сообщения в MongoDB'
    )
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        related_name='posts',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name='название',
        max_length=32,
        validators=[MinLengthValidator(5)],
        default='название',
        blank=True,
        null=True,
    )
    description = models.CharField(
        verbose_name='описание',
        default='описание',
        blank=True,
        null=True,
        max_length=255
    )
    price = models.IntegerField(
        verbose_name='цена',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(MAX_POST_PRICE)
        ],
        default=0
    )
    image = models.CharField(
        'эмодзи поста',
        max_length=1,
        default=DEFAULT_POST_IMAGE
    )
    is_active = models.BooleanField(
        verbose_name='активность',
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
        verbose_name='пользователь',
        related_name='cards',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name='название',
        max_length=32,
        validators=[MinLengthValidator(5)],
        default='название'
    )
    description = models.CharField(
        verbose_name='описание',
        blank=True,
        null=True,
        max_length=255,
        default='описание'
    )
    image = models.ImageField(
        verbose_name='изображение',
        upload_to='cards/',
        default=DEFAULT_CARD_IMAGE_PATH
    )
    posts = models.ManyToManyField(
        Post,
        through='CardPost',
        related_name='cards'
    )
    is_active = models.BooleanField(
        verbose_name='активность',
        default=True
    )

    class Meta:
        verbose_name = 'карточка'
        verbose_name_plural = 'карточки'

    def __str__(self):
        return f'карта {self.id}: {self.title}'


class CardPost(CreateModel):
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
        ordering = ['created_at']

    def __str__(self):
        return f'{self.card.title} - {self.post.title}'


class PostPurchase(CreateModel):
    post = models.ForeignKey(
        Post,
        verbose_name='пост',
        related_name='post_purchases',
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        related_name='post_purchases',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'купленный пост'
        verbose_name_plural = 'купленные посты'

    def __str__(self):
        return f'{self.user.username} купил {self.post.title}'
