from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # path("api/chats/", views.ChatList.as_view(), name="chat_list_api"),
    path(
        "testing/<int:choosen_user_id>",
        login_required(views.get_room, login_url="/login"),
        name="index",
    ),
    # path(
    #     "chat/<str:room_name>/",
    #     login_required(views.Room.as_view(), login_url="/login"),
    #     name="room",
    # ),
    path(
        "",
        login_required(views.Main.as_view(), login_url="/login"),
        name="home",
    ),
    # path(
    #     "",
    #     login_required(views.Chat_list_Usernames.as_view(), login_url="/login"),
    #     name="home",
    # ),
    path(
        "change_status/",
        login_required(views.change_status, login_url="/login"),
        name="change_status",
    ),
    path("login/", views.login_page, name="login_page"),
    path(
        "logout/", login_required(views.logout_user, login_url="/login"), name="logout"
    ),
    path("register/", views.register_page, name="register_page"),
    path(
        "update_photo/",
        login_required(views.UpdatePhoto.as_view(), login_url="/login"),
        name="update_photo",
    ),
    path(
        "change_password/",
        login_required(
            views.ChangePassword.as_view(),
            login_url="/login",
        ),
        name="change_password",
    ),
    path(
        "change_password_done/",
        login_required(
            views.ChangePasswordDone.as_view(),
            login_url="/login",
        ),
        name="change_password_done",
    ),
    # path(
    #     "send_message/",
    #     login_required(views.SendMessage.as_view(), login_url="/login"),
    #     name="send_message",
    # ),
]
