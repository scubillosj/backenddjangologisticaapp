from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

class Command(BaseCommand):
    help = 'Crea un superusuario automáticamente si no existe'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = settings.SUPERUSER_NAME
        email = settings.SUPERUSER_EMAIL
        password = settings.SUPERUSER_PASSWORD

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" creado.'))
        else:
            self.stdout.write(self.style.WARNING('El superusuario ya existe.'))
