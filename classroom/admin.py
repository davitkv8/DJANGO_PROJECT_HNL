from django.contrib import admin
from .models import TimeTable, Feedback, Message, ChatRoom

admin.site.register(Message)
admin.site.register(TimeTable)
admin.site.register(Feedback)
admin.site.register(ChatRoom)

