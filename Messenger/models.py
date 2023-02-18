from django.db import models
from django.contrib.auth.models import User


class User_Model(models.Model):
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, related_name="profile"
    )
    profile_photo = models.ImageField(
        upload_to="images/", default="default_photo.jpg", null=True, blank=True
    )
    chats = models.ManyToManyField(User, related_name="chats_list", blank=True)
    blocked_list = models.ManyToManyField(User, related_name="blocked_list", blank=True)

    @classmethod
    def add_to_chat_list(cls, current_user, user_to_add):
        user, created = cls.objects.get_or_create(user=current_user)
        user.chats.add(user_to_add)

    @classmethod
    def add_to_blocked(cls, current_user, user_to_block):
        blocked, created = cls.objects.get_or_create(user=current_user)
        blocked.blocked_list.add(user_to_block)

    @classmethod
    def remove_from_blocked(cls, current_user, user_to_remove):
        blocked, created = cls.objects.get_or_create(user=current_user)
        blocked.blocked_list.remove(user_to_remove)

    def __str__(self):
        return f"Nickname: {self.user}, user_id: {self.user.id}"

    def save(self):
        super().save()


# class Message(models.Model):
#     sender = models.IntegerField()
#     receiver = models.IntegerField()
#     body = models.CharField(max_length=2000, null=True, blank=True)
#     photo = models.ImageField(upload_to="send_photos/", null=True, blank=True)
#     send_time = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.sender}, {self.receiver}, {self.body}"


class Mess(models.Model):
    author = models.ForeignKey(
        User_Model, related_name="author_messages", on_delete=models.CASCADE
    )
    body = models.CharField(max_length=2000)
    send_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.user} {self.body}"

    def last_10_messages(self):
        return Mess.objects.order_by("-send_time").all()[:10]


class Chat(models.Model):
    participants = models.ManyToManyField(
        User_Model, related_name="participants", blank=True
    )
    messages = models.ManyToManyField(Mess, blank=True)

    def __str__(self):
        return f"{self.pk} {self.participants.all()}"
