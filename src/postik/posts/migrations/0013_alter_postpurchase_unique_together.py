# Generated by Django 3.2.23 on 2024-07-04 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_alter_post_message_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postpurchase',
            unique_together=set(),
        ),
    ]
