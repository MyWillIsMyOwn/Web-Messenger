# Generated by Django 4.1.4 on 2023-01-18 12:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Messenger", "0017_message_photo_alter_message_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user_model",
            name="chats",
            field=models.ManyToManyField(
                blank=True, related_name="chats_list", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
