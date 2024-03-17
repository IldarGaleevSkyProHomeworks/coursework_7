from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120, write_only=True)
    username = serializers.CharField(max_length=120)
    first_name = serializers.CharField(max_length=120, required=False)
    last_name = serializers.CharField(max_length=120, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name'
        ]
        swagger_schema_fields = {
            "description": "Полная информация о пользователе"
        }
