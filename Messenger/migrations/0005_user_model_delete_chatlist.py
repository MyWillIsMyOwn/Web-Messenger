# Generated by Django 4.1.4 on 2022-12-15 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Messenger", "0004_chatlist_delete_user_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="User_Model",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "blocked_list",
                    models.ManyToManyField(
                        blank=True,
                        related_name="blocked_list",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "chats",
                    models.ManyToManyField(
                        blank=True, related_name="chats", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="ChatList",
        ),
    ]
