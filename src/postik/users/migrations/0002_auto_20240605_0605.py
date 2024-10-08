# Generated by Django 3.2.23 on 2024-06-05 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramprofile',
            name='bio',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Био'),
        ),
        migrations.AddField(
            model_name='telegramprofile',
            name='image',
            field=models.ImageField(default='telegram_profiles/default.png', upload_to='telegram_profiles', verbose_name='Изображение'),
        ),
    ]
