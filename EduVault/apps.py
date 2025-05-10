# EduVault/apps.py
from django.apps import AppConfig

class EduVaultConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EduVault'

    def ready(self):
        import EduVault.signals  # importante para registrar los signals
