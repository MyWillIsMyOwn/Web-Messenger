from django.contrib import admin
from .models import User_Model
from .models import Chat, Mess

admin.site.register(User_Model)
# admin.site.register(Message)
admin.site.register(Mess)
admin.site.register(Chat)
