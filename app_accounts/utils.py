from django.contrib.auth.models import User


def generate_password():
    return User.objects.make_random_password()
