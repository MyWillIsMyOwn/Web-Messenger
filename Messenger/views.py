from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User_Model, User, Mess, Chat
from django.views.generic.list import ListView, View
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import CreateUserForm, LoginUserForm, UserProfileForm, PasswordChangeForm
from django.db.models import Q
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.http import JsonResponse

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.exceptions import AuthenticationFailed


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class ChatList(APIView):
    def get(self, request, format=None):
        print("hereiam")
        if not request.user.is_authenticated():
            raise AuthenticationFailed("Authentication credentials were not provided.")
        try:
            logged_user_model = User_Model.objects.get(user=request.user.id)
        except User_Model.DoesNotExist:
            raise AuthenticationFailed("User not found.")
        chats = Chat.objects.filter(participants=logged_user_model)
        data_to_send = []
        for chat in chats:
            for participant in chat.participants.all():
                if participant.id != request.user.id:
                    interlocutor = participant.user.username
            last_message = chat.messages.all().last()
            if last_message:
                last_message_body = last_message.body
                last_message_date = last_message.send_time
            else:
                last_message_body = ""
                last_message_date = ""
            data_to_send.append(
                {
                    "chat_id": chat.pk,
                    "interlocutor": interlocutor,
                    "last_message_body": last_message_body,
                    "last_message_date": last_message_date,
                }
            )
        # print(data_to_send)
        return Response(data_to_send)


def get_room(request, choosen_user_id):
    # get logged and chosen user id
    logged_user_model = User_Model.objects.get(user=request.user.id)
    choosen_user_model = User_Model.objects.get(user=choosen_user_id)
    room = (
        Chat.objects.filter(participants=logged_user_model.id)
        .filter(participants=choosen_user_model.id)
        .first()
    )
    # create a room for them if it doesn't exist
    if room not in Chat.objects.all():
        room = Chat.objects.create()
        room.participants.add(logged_user_model.id, choosen_user_model.id)
        room.save()
    return render(request, "Messenger/index.html", {"room_id": room.id})


class Room(View):
    def get(self, request, room_name):

        logged_user_id = self.request.user.id
        logged_user_model = User_Model.objects.get(user=request.user.id)
        # print("tu jestem")
        # chats = Chat.objects.filter(participants=logged_user_model.id)
        # data_to_send = []
        # for chat in chats:
        #     for participant in chat.participants.all():
        #         if participant.id != request.user.id:
        #             interlocutor = participant
        #     last_message = chat.messages.all().last()
        #     data_to_send.append(
        #         {
        #             "chat_id": chat.pk,
        #             "interlocutor": interlocutor,
        #             "last_message": last_message,
        #         }
        #     )

        # print(data_to_send)

        room = Chat.objects.filter(id=room_name).first()
        logged_User_Model_id = User_Model.objects.filter(user=logged_user_id).values(
            "id"
        )[0]

        blocked_users = list(
            User_Model.objects.filter(user=logged_user_id).values("blocked_list")
        )
        list_of_ids_users_from_blocked_list = []
        for element in blocked_users:
            list_of_ids_users_from_blocked_list.append(element["blocked_list"])

        blocked_nicknames_data = User.objects.filter(
            pk__in=list_of_ids_users_from_blocked_list
        ).values()

        chat_users = list(
            User_Model.objects.filter(user=logged_user_id).values("chats")
        )
        list_of_ids_users_from_chat = []
        for element in chat_users:
            if element["chats"] not in list_of_ids_users_from_blocked_list:
                list_of_ids_users_from_chat.append(element["chats"])
        users_chat_nicknames_data = User.objects.filter(
            pk__in=list_of_ids_users_from_chat
        ).values()

        unknown_users = list(User.objects.values("id"))
        list_of_ids_users_from_unknown_users = []
        for element in unknown_users:
            if (
                element["id"] not in list_of_ids_users_from_chat
                and element["id"] not in list_of_ids_users_from_blocked_list
            ):
                list_of_ids_users_from_unknown_users.append(element["id"])
        unknown_users_nicknames_data = User.objects.filter(
            pk__in=list_of_ids_users_from_unknown_users
        ).values()
        # print(users_chat_nicknames_data[0])
        return render(
            request,
            "Messenger/room2.html",
            {
                "room_name": room_name,
                # "messages": room.messages.all(),
                "logged_user": logged_User_Model_id,
                "chats": users_chat_nicknames_data,
                # "room_id": room.id,
            },
        )


class Main(ListView):
    model = User_Model
    template_name = "Messenger/room2.html"

    def get_context_data(self, **kwargs):
        logged_user_id = self.request.user.id

        blocked_users = list(
            User_Model.objects.filter(user=logged_user_id).values("blocked_list")
        )
        list_of_ids_users_from_blocked_list = []
        for element in blocked_users:
            list_of_ids_users_from_blocked_list.append(element["blocked_list"])

        blocked_nicknames_data = User.objects.filter(
            pk__in=list_of_ids_users_from_blocked_list
        ).values()

        chat_users = list(
            User_Model.objects.filter(user=logged_user_id).values("chats")
        )
        list_of_ids_users_from_chat = []
        for element in chat_users:
            if element["chats"] not in list_of_ids_users_from_blocked_list:
                list_of_ids_users_from_chat.append(element["chats"])
        users_chat_nicknames_data = User.objects.filter(
            pk__in=list_of_ids_users_from_chat
        ).values()

        unknown_users = list(User.objects.values("id"))
        list_of_ids_users_from_unknown_users = []
        for element in unknown_users:
            if (
                element["id"] not in list_of_ids_users_from_chat
                and element["id"] not in list_of_ids_users_from_blocked_list
            ):
                list_of_ids_users_from_unknown_users.append(element["id"])
        unknown_users_nicknames_data = User.objects.filter(
            pk__in=list_of_ids_users_from_unknown_users
        ).values()
        logged_user_data = User_Model.objects.filter(user=logged_user_id).values()

        # all_messages = Message.objects.all().filter(
        #     Q(sender=logged_user_id) | Q(receiver=logged_user_id)
        # )
        # print(users_chat_nicknames_data[0])
        # print("nic")
        return {
            # "all_messages": all_messages,
            # "blocked_list": blocked_nicknames_data,
            "chats": users_chat_nicknames_data,
            # "unknown_users": unknown_users_nicknames_data,
            # "logged_user_data": logged_user_data[0],
        }


# class Chat_list_Usernames(ListView):
#     model = User_Model
#     paginate_by = 1
#     template_name = "Messenger/home.html"

#     def get_context_data(self, **kwargs):
#         logged_user_id = self.request.user.id

#         blocked_users = list(
#             User_Model.objects.filter(user=logged_user_id).values("blocked_list")
#         )
#         list_of_ids_users_from_blocked_list = []
#         for element in blocked_users:
#             list_of_ids_users_from_blocked_list.append(element["blocked_list"])

#         blocked_nicknames_data = User.objects.filter(
#             pk__in=list_of_ids_users_from_blocked_list
#         ).values()

#         chat_users = list(
#             User_Model.objects.filter(user=logged_user_id).values("chats")
#         )
#         list_of_ids_users_from_chat = []
#         for element in chat_users:
#             if element["chats"] not in list_of_ids_users_from_blocked_list:
#                 list_of_ids_users_from_chat.append(element["chats"])
#         users_chat_nicknames_data = User.objects.filter(
#             pk__in=list_of_ids_users_from_chat
#         ).values()

#         unknown_users = list(User.objects.values("id"))
#         list_of_ids_users_from_unknown_users = []
#         for element in unknown_users:
#             if (
#                 element["id"] not in list_of_ids_users_from_chat
#                 and element["id"] not in list_of_ids_users_from_blocked_list
#             ):
#                 list_of_ids_users_from_unknown_users.append(element["id"])
#         unknown_users_nicknames_data = User.objects.filter(
#             pk__in=list_of_ids_users_from_unknown_users
#         ).values()
#         logged_user_data = User_Model.objects.filter(user=logged_user_id).values()

#         all_messages = Message.objects.all().filter(
#             Q(sender=logged_user_id) | Q(receiver=logged_user_id)
#         )
#         return {
#             "all_messages": all_messages,
#             "blocked_list": blocked_nicknames_data,
#             "chats": users_chat_nicknames_data,
#             "unknown_users": unknown_users_nicknames_data,
#             "logged_user_data": logged_user_data[0],
#         }


class UpdatePhoto(TemplateView):
    template_name = "Messenger/update_photo.html"

    def post(self, response):
        user = get_object_or_404(User_Model, pk=self.request.user.id)
        new_image = response.FILES.get("Browser")
        print(new_image)
        user.profile_photo = new_image
        user.save()
        return redirect("/")


class ChangePassword(PasswordChangeView):
    template_name = "Messenger/change_password.html"
    success_url = reverse_lazy("change_password_done")


class ChangePasswordDone(PasswordChangeDoneView):
    template_name = "Messenger/change_password_done.html"


# class SendMessage(TemplateView):
#     template_name = "Messenger/home.html"
#     model = Message

#     def post(self, response):
#         data = response.POST
#         if len(data["msg"]) > 1:
#             Message.objects.create(
#                 sender=self.request.user.id, receiver=data["receiver"], body=data["msg"]
#             )

#         logged_user_chat_list = User_Model.objects.filter(
#             user=self.request.user.id
#         ).values("chats")
#         list_of_users_ids_from_logged_user_chat_list = []
#         for element in logged_user_chat_list:
#             list_of_users_ids_from_logged_user_chat_list.append(element["chats"])
#         if int(data["receiver"]) not in list_of_users_ids_from_logged_user_chat_list:
#             User_Model.add_to_chat_list(self.request.user.id, int(data["receiver"]))

#         receiver_user_chat_list = User_Model.objects.filter(
#             user=data["receiver"]
#         ).values("chats")
#         list_of_users_ids_from_logged_receiver_chat_list = []
#         for element in receiver_user_chat_list:
#             list_of_users_ids_from_logged_receiver_chat_list.append(element["chats"])
#         if self.request.user.id not in list_of_users_ids_from_logged_receiver_chat_list:
#             User_Model.add_to_chat_list(int(data["receiver"]), self.request.user.id)

#         return redirect("/")


def change_status(response):
    if response.method == "POST":
        logged_user_id = response.user.id
        blocked_users = list(
            User_Model.objects.filter(user=logged_user_id).values("blocked_list")
        )
        list_of_ids_users_from_blocked_list = []
        for element in blocked_users:
            list_of_ids_users_from_blocked_list.append(element["blocked_list"])
        highlated_user_id = response.POST
        if int(highlated_user_id["dane"]) not in list_of_ids_users_from_blocked_list:
            User_Model.add_to_blocked(logged_user_id, highlated_user_id["dane"])
        else:
            User_Model.remove_from_blocked(logged_user_id, highlated_user_id["dane"])
    return redirect("/")


def register_page(response):
    form = CreateUserForm()
    if response.method == "POST":
        form = CreateUserForm(response.POST)
        profile_form = UserProfileForm(response.POST)
        if form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)  # create custom form
            profile.user = user  # give a custom form name of user name
            profile.save()  # saving both to db
            user = form.cleaned_data.get("username")
            messages.success(response, "Account was created for: " + user)

            return redirect("/login/")
    context = {"user_creation_form": form}
    return render(response, "Messenger/register.html", context)


def login_page(response):
    form = LoginUserForm()
    if response.method == "POST":
        username = response.POST.get("username")
        password = response.POST.get("password")
        user = authenticate(response, username=username, password=password)
        if user is not None:
            login(response, user)
            return redirect("/")
        else:
            messages.info(response, "Username or password is incorrect")
    context = {"user_login_form": form}
    return render(response, "Messenger/login.html", context)


def logout_user(response):
    logout(response)
    return redirect("/")
