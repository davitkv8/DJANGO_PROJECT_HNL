from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Relationship


@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, **kwargs):
    sender_ = instance.sender

    receiver_ = instance.receiver

    if instance.status == "Approve":
        receiver_.friends.add(sender_)
        sender_.save()
        receiver_.save()
