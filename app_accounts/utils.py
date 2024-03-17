from django.contrib.auth.models import User


def generate_password():  # pragma: no cover
    return User.objects.make_random_password()
