from django.contrib.auth.models import User
from rest_framework import serializers

from app_accounts.serializers import UserPublicSerializer
from app_habits.models import Habit


class HabitFullSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(
        read_only=True
    )

    def create(self, validated_data):
        curr_user: User = self.context['request'].user
        validated_data['owner'] = curr_user
        new_habit: Habit = super().create(validated_data)
        return new_habit

    def validate_linked_habit(self, value: Habit):
        if not value.is_pleasantly:
            raise serializers.ValidationError('Связанная привычка должна быть приятной')

        if not (value.is_public or value.owner == self.context['request'].user):
            raise serializers.ValidationError('Связанная привычка должна быть публичной или вашей')

        return value

    def validate(self, attrs):
        validated = super().validate(attrs)

        is_pleasantly = attrs.get('is_pleasantly')
        is_pleasantly = getattr(self.instance, 'is_pleasantly', None) if is_pleasantly is None else is_pleasantly

        reward = attrs.get('reward')
        reward = getattr(self.instance, 'reward', None) if reward is None else reward

        linked_habit = attrs.get('linked_habit')
        linked_habit = getattr(self.instance, 'linked_habit', None) if linked_habit is None else linked_habit

        duration = attrs.get('duration')
        duration = getattr(self.instance, 'duration', None) if duration is None else duration

        if is_pleasantly and linked_habit:
            raise serializers.ValidationError({
                'linked_habit': 'У приятной привычки не может быть связанной привычки'
            })

        if is_pleasantly and reward:
            raise serializers.ValidationError({
                'reward': 'У приятной привычки не может быть награды'
            })

        if is_pleasantly and duration > 120:
            raise serializers.ValidationError({
                'duration': 'Приятная привычка не должна длиться больше двух минут'
            })

        if not (is_pleasantly or linked_habit or reward):
            raise serializers.ValidationError({
                'linked_habit': 'Укажите награду или связанную привычку',
                'reward': 'Укажите награду или связанную привычку',
            })

        if linked_habit and reward:
            raise serializers.ValidationError({
                'linked_habit': 'Если указана награда, связанную привычку указать нельзя',
                'reward': 'Если указана связанная привычка, награду указывать нельзя'
            })

        return validated

    class Meta:
        model = Habit
        fields = '__all__'


class HabitPublicSerializer(HabitFullSerializer):
    owner = None

    class Meta:
        model = Habit
        exclude = ['owner']

        swagger_schema_fields = {
            'title': 'HabitItem',
            'description': 'Объект "Привычка"',
        }
