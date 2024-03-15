from django.contrib.auth.models import User
from rest_framework import serializers


class UserPublicSerializer(serializers.ModelSerializer):
    owner = None

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser',
            'is_active',
        ]
