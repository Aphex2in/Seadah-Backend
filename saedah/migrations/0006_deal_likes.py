# Generated by Django 4.2.5 on 2023-10-18 16:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saedah', '0005_comments_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
