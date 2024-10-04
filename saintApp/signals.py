from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from .utils import generate_random_username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:

        random_username = generate_random_username()
        while UserProfile.objects.filter(username=random_username).exists():
            random_username = generate_random_username()

        UserProfile.objects.create(user=instance, username=random_username)
        print('Profile created successfully')

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    
    try:
        if created == False:
            instance.Userprofile.save()
            print('Profile updated successfully')
    except:
        instance.userprofile = None