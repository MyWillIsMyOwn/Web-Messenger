from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from Messenger.models import User_Model, User, Mess, Chat
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Max


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "/api/token",
        "/api/token/refresh",
    ]

    return Response(routes)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getChats(request):
    try:
        logged_user_model = User_Model.objects.get(user=request.user.id)
    except User_Model.DoesNotExist:
        raise AuthenticationFailed("User not found.")
    chats = Chat.objects.filter(participants=logged_user_model).annotate(
        last_message_date=Max("messages__send_time")
    )
    data_to_send = []
    for chat in chats:
        last_message = chat.messages.all().last()
        if last_message:
            last_message_body = last_message.body
            last_message_date = last_message.send_time
            last_message_owner = last_message.author.id
        else:
            last_message_body = ""
            last_message_date = ""
        for participant in chat.participants.all():
            if participant.id != request.user.id:
                interlocutor = participant.user.username
        data_to_send.append(
            {
                "chat_id": chat.pk,
                "interlocutor": interlocutor,
                "last_message_owner": last_message_owner,
                "last_message_body": last_message_body,
                "last_message_date": last_message_date,
            }
        )
    sorted_data_to_send = sorted(
        data_to_send, key=lambda x: x["last_message_date"], reverse=False
    )
    return Response(sorted_data_to_send)
