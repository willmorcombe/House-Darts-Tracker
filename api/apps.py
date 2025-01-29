from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db import connection
from django.core.management import call_command

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Connect to the post_migrate signal
        post_migrate.connect(self.load_checkouts, sender=self)

    def load_checkouts(self, sender, **kwargs):
        """
        This method will be called after all migrations are done,
        so it is safe to interact with the database here.
        """
        call_command('load_checkouts')