from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import UserProfile, ROLES

ROLE_TO_GROUP = {code: code for code, _ in ROLES}

@receiver(post_save, sender=UserProfile)
def sync_profile_group(sender, instance: UserProfile, **kwargs):
    user = instance.user
    # Remove all role groups
    for code in ROLE_TO_GROUP.values():
        try:
            g = Group.objects.get(name=code)
            user.groups.remove(g)
        except Group.DoesNotExist:
            continue
    if instance.role:
        g, _ = Group.objects.get_or_create(name=ROLE_TO_GROUP[instance.role])
        user.groups.add(g)
    user.is_staff = True
    user.save(update_fields=["is_staff"])
