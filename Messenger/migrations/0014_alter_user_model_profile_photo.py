# Generated by Django 4.1.4 on 2023-01-10 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Messenger", "0013_alter_user_model_profile_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user_model",
            name="profile_photo",
            field=models.ImageField(
                blank=True, default="default_photo.jpg", null=True, upload_to="images/"
            ),
        ),
    ]
