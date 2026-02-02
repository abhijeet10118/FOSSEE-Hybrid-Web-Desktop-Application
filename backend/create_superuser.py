import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin'
password = 'admin123'

if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists.")
else:
    User.objects.create_superuser(username=username, password=password, email='admin@example.com')
    print(f"Superuser '{username}' created successfully!")
    print(f"Username: {username}")
    print(f"Password: {password}")
