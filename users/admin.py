from django.contrib import admin
from .models import TeachersProfile, Relationship, UserStatus

admin.site.register(TeachersProfile)
admin.site.register(Relationship)
admin.site.register(UserStatus)
