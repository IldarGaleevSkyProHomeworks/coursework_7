from django.contrib.auth.models import User
from rest_framework import serializers


class UserPublicSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=120, write_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        if first_name := validated_data.get('first_name'):
            user.first_name = first_name

        if last_name := validated_data.get('last_name'):
            user.last_name = last_name

        if first_name or last_name:
            user.save()

        return user

    class Meta:
        model = User
        fields = [
            'id',
            'password',
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser',
            'is_active',
        ]

        swagger_schema_fields = {
            "description": "Открытая информация о пользователе"
        }


class UserEditSerializer(UserPublicSerializer):
    password = serializers.CharField(max_length=120, write_only=True, required=False)
    username = serializers.CharField(max_length=120, required=False)
