from django.contrib.auth.models import User
from rest_framework import serializers

from app_habits.models import Habit


class HabitFullSerializer(serializers.ModelSerializer):
    linked_habit = serializers.PrimaryKeyRelatedField(
        allow_empty=True,
        required=False,
        queryset=Habit.objects.filter(is_pleasantly=True)
    )

    def create(self, validated_data):
        curr_user: User = self.context['request'].user
        validated_data['owner'] = curr_user
        new_habit: Habit = super().create(validated_data)
        return new_habit

    class Meta:
        model = Habit
        fields = '__all__'


class HabitPublicSerializer(HabitFullSerializer):
    class Meta:
        model = Habit
        exclude = ['owner']

        swagger_schema_fields = {
            'title': 'HabitItem',
            'description': 'Объект "Привычка"',
        }
