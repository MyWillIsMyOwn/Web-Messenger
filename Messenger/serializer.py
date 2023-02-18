from .models import User, User_Model, Chat, Mess
from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"
        print("tutaj")
