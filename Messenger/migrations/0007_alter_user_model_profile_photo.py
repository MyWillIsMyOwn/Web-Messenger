# Generated by Django 4.1.4 on 2023-01-06 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Messenger", "0006_user_model_profile_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user_model",
            name="profile_photo",
            field=models.ImageField(blank=True, null=True, upload_to="images"),
        ),
    ]
