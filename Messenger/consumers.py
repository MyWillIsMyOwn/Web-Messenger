import json
import asyncio
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import Mess, Chat
from Messenger.models import User_Model, User
from channels.consumer import AsyncConsumer


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        # getting info about room
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # accept connection
        await self.send({"type": "websocket.accept"})

    ######################### preload messages #########################
    async def fetch_messages(self, data):
        messages_back_to_frontend = {
            "messages": await (self.get_messages_from_db()),
            "logged_user": await self.get_user_model(),
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_preloaded_messages",
                "messages": json.dumps(messages_back_to_frontend),
            },
        )

    @sync_to_async
    def get_messages_from_db(self):
        messages = Mess.last_10_messages(self)
        content = {"messages": self.messages_to_json(messages)}
        return content

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            "author": message.author.id,
            "body": message.body,
            "send_time": str(message.send_time),
        }

    async def send_preloaded_messages(self, event):
        await self.send({"type": "websocket.send", "text": event["messages"]})

    ######################### send new message #########################
    async def new_message(self, data):
        await self.save_message_to_db(data)

        # prepare message to send to frontend
        message = data["message"]
        print(message)
        message_back_to_frontend = {
            "message": {
                "body": message,
                "author": await self.get_user_model(),
            }
        }
        # brodcast message event to group to be sent
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "send_chat_message", "mess": json.dumps(message_back_to_frontend)},
        )

    @sync_to_async
    def get_user_model(self):
        return User_Model.objects.get(pk=self.scope["user"].id).id

    @sync_to_async
    def save_message_to_db(self, data):
        logged_user_model = User_Model.objects.get(pk=self.scope["user"].id)
        # save message to database messages
        new_message = Mess(author=logged_user_model, body=data["message"])
        new_message.save()

        # save message to current chat messages
        chat = Chat.objects.get(id=self.room_name)
        chat.messages.add(new_message)
        # return new_message

    async def send_chat_message(self, event):
        # send message to group
        await self.send({"type": "websocket.send", "text": event["mess"]})

    ######################### preload chat #########################
    async def preload_users(self, data):
        # await self.select_user_models_from_db(await self.get_user_model())
        message_to_frontend = {
            "all_users": await self.select_user_models_from_db(
                await self.get_user_model()
            ),
            "logged_user": await self.get_user_model(),
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "load_users",
                "users": json.dumps(message_to_frontend),
            },
        )

    @sync_to_async
    def select_user_models_from_db(self, user_model_id):
        blocked_users = User_Model.objects.filter(user=user_model_id).values(
            "blocked_list"
        )
        all_chat_users = list(
            User_Model.objects.filter(user=user_model_id).values("chats")
        )
        blocked_users_ids = []
        for user in blocked_users:
            blocked_users_ids.append(user["blocked_list"])
        chat_users_ids = []
        for user in all_chat_users:
            if user["chats"] not in blocked_users_ids:
                chat_users_ids.append(user["chats"])
        chat_users_data = User.objects.filter(pk__in=chat_users_ids).values()
        blocked_users_data = User.objects.filter(pk__in=blocked_users_ids).values()
        content = {
            "users": {
                "chats": self.users_to_json(chat_users_data),
                "blocked": self.users_to_json(blocked_users_data),
            }
        }
        return content

    def users_to_json(self, users):
        result = []
        for user in users:
            result.append(self.user_to_json(user))
        return result

    def user_to_json(self, user):
        return {
            "user_id": user["id"],
            "user_username": user["username"],
        }

    async def load_users(self, event):
        await self.send({"type": "websocket.send", "text": event["users"]})

    ######################### change chat #########################
    async def choose_chat(self, data):
        data_to_send = []
        for element in await self.get_current_chat(data, await self.get_user_model()):
            data_to_send.append(element)
        message_to_frontend = {
            "chat_id": data_to_send[0],
            "choosen_user": data_to_send[1],
        }
        print(message_to_frontend)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_room_data",
                "room_data": json.dumps(message_to_frontend),
            },
        )

    @sync_to_async
    def get_current_chat(self, data, logged_user):
        choosen_user = User_Model.objects.get(user=data["user"]).id
        current_chat = (
            Chat.objects.filter(participants=logged_user)
            .filter(participants=choosen_user)
            .first()
        )
        return current_chat.id, choosen_user

    async def send_room_data(self, event):
        await self.send({"type": "websocket.send", "text": event["room_data"]})

    ######################### receive message from websocket #########################
    # getting messages from frontend
    async def websocket_receive(self, data):
        # check which command to preform
        get_command = json.loads(data["text"])
        # send json data to particular function
        await self.commands[get_command["command"]](self, get_command)

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message,
        "preload_users": preload_users,
        "choose_chat": choose_chat,
    }
