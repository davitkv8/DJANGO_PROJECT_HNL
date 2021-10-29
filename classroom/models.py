import time
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from users.models import TeachersProfile
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator
from django.db.models import Q


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messageSender", null=False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messageReceiver", null=False)
    message = models.TextField(max_length=3000, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)



    def format_time(self):
        return self.timestamp.strftime('%B %d, %H:%M')

    def __str__(self):
        return f"{self.message}"


class ChatRoom(models.Model):
    roomName = models.CharField(max_length=55, unique=True, null=True)
    members = models.ManyToManyField(User, blank=False)

    def get_chat_object(self):
        return Message.objects.filter((Q(sender=self.members.first()) & Q(receiver=self.members.last()))
                                      | (Q(receiver=self.members.first()) & Q(sender=self.members.last())))

    def get_chat(self):
        return self.get_chat_object().all()

    def is_seen(self, user):
        try:
            if user == self.get_chat_object().last().receiver:
                o1 = self.get_chat_object().last()
                o1.seen = True
                o1.save()

        except:
            pass
        finally:
            if self.get_chat_object().last() is not None:
                return self.get_chat_object().last().seen
            else: return None

    def count_messages(self):
        return self.get_chat().count()

    def get_messages(self):
        return self.get_chat().order_by('timestamp')[:70]

    def __str__(self):
        return f"{self.roomName}"


class TimeTable(models.Model):
    available_time = ArrayField(models.TextField(max_length=84), blank=True, null=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="userTable")

    def __str__(self):
        return f"Time table of {self.user}"


class Feedback(models.Model):

    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)], null=False)
    textFeedback = models.TextField(max_length=200, null=False)
    sender = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='feedbackAuthor')
    receiver = models.ForeignKey(to=TeachersProfile, null=False, on_delete=models.CASCADE,
                                 related_name='feedback')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver} score : {self.rating}"
