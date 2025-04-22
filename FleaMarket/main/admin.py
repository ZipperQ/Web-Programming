from django.contrib import admin
from . models import Thing
from . models import Chat
from . models import Message

admin.site.register(Thing)
admin.site.register(Chat)
admin.site.register(Message)
