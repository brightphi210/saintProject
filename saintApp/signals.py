from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('Profile created successfully')

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    
    try:
        if created == False:
            instance.Userprofile.save()
            print('Profile updated successfully')
    except:
        instance.userprofile = None