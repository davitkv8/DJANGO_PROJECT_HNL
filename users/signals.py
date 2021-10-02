from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Relationship, UserStatus


@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, **kwargs):
    sender_ = instance.sender
    print(sender)
    receiver_ = instance.receiver

    if instance.status == "Approve":
        receiver_.friends.add(sender_)
        sender_.save()
        receiver_.save()

@receiver(post_save, sender=User)
def watchlist_create(sender, instance=None, created=False, **kwargs):
    if created:
        UserStatus.objects.create(user=instance, status='None')
