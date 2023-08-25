from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile

@receiver(post_save, sender=Profile)
def add_user_to_suscriptor_group(sender, instance, created, **kwargs):
    if created:
        try:
            suscriptor = Group.objects.get(name='Suscriptor')
        except Group.DoesNotExist:
            suscriptor = Group.objects.create(name='Suscriptor')
        instance.user.groups.add(suscriptor)

      