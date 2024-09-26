from django.apps import AppConfig


class SaintappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'saintApp'

    def ready(self):
        import saintApp.signals