# Generated by Django 3.2.23 on 2024-06-17 13:11

from decimal import Decimal

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='message_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='id телеграм сообщения'),
        ),
        migrations.AlterField(
            model_name='card',
            name='description',
            field=models.CharField(blank=True, default='Описание', max_length=255, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='card',
            name='image',
            field=models.ImageField(default='cards/default/card-logo.svg', upload_to='cards', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='card',
            name='title',
            field=models.CharField(default='Название', max_length=32, validators=[django.core.validators.MinLengthValidator(5)], verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Цена'),
        ),
    ]
