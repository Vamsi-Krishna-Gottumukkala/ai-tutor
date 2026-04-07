from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Create the admin user in the Supabase database (admin@gmail.com / admin@1234)'

    def handle(self, *args, **kwargs):
        email = 'admin@gmail.com'
        password = 'admin@1234'
        username = 'admin'

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Admin user ({email}) already exists in the database.'))
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        user.first_name = 'Admin'
        user.last_name = 'User'
        user.is_staff = True
        user.is_superuser = True
        user.skill_level = 'advanced'
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f'✅ Admin user created successfully!\n'
            f'   Email: {email}\n'
            f'   Password: {password}\n'
            f'   Login at: /accounts/login/'
        ))
