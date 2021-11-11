from django.contrib import admin
from .models import TimeTable, Feedback, Message, ChatRoom


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = ["sender", "receiver", "message", "timestamp", "seen"]


admin.site.register(Message, ReadOnlyAdmin)
admin.site.register(TimeTable)
admin.site.register(Feedback)
admin.site.register(ChatRoom)

