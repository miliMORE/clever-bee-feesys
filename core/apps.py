from django.apps import AppConfig
from django.db.models.signals import post_migrate

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .signals import sync_profile_group  # noqa
        from .auth_bootstrap import ensure_groups_and_perms  # noqa
        post_migrate.connect(ensure_groups_and_perms, sender=self)
