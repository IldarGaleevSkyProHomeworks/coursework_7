from django.contrib.auth.models import User
from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from app_habits.models import HabitNotification
from app_habits.serializers import HabitPublicSerializer


class HabitNotificationSerializer(serializers.ModelSerializer):
    timezone = TimeZoneSerializerField(
        default='Europe/Moscow',
        use_pytz=False,
    )

    habits = HabitPublicSerializer(
        many=True,
        required=True,
    )

    def create(self, validated_data):
        curr_user: User = self.context['request'].user
        validated_data['owner'] = curr_user
        return super().create(validated_data)

    class Meta:
        model = HabitNotification
        exclude = ['owner']

        swagger_schema_fields = {
            'title': 'GoalItem',
            'description': 'Объект "Конечная цель"'
        }
