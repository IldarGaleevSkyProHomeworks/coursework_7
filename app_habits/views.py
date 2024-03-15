from django.db.models import Q
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from app_accounts.permissions import IsOwner
from app_habits.models import Habit
from app_habits.pagination import AppHabitPagination
from app_habits.serializers import HabitFullSerializer, HabitPublicSerializer
from app_habits.serializers.start_notification_serializer import StartNotifySerializer
from app_telegrambot import tasks, message_text
from app_telegrambot.models import TelegramUser


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitPublicSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('is_pleasantly', 'periodic')
    ordering_fields = ('duration', 'periodic')
    search_fields = ('action_description', 'reward', 'site')
    pagination_class = AppHabitPagination

    def get_queryset(self):
        is_swagger = getattr(self, 'swagger_fake_view', False)
        if not is_swagger and self.request.user.is_superuser:
            return Habit.objects.all()
        return Habit.objects.filter(Q(owner=self.request.user) | Q(is_public=True))

    def get_serializer_class(self):
        is_swagger = getattr(self, 'swagger_fake_view', False)
        if not is_swagger and self.request.user.is_superuser:
            return HabitFullSerializer
        return HabitPublicSerializer

    def get_data(self, pk: int) -> tuple[Habit, TelegramUser]:
        habit = get_object_or_404(Habit, pk=pk)
        telegram_user = TelegramUser.objects.filter(user=self.request.user).first()
        if not telegram_user:
            raise ValidationError('У пользователя нет связанного Telegram аккаунта')

        return habit, telegram_user

    @staticmethod
    def get_task_name(habit_id, tg_user_id):
        return f'notify_{habit_id}_{tg_user_id}'

    @swagger_auto_schema(
        request_body=StartNotifySerializer,
        operation_description="Включить оповещения"
    )
    @action(detail=True, methods=['post'])
    def start(self, request, pk: int = None):
        habit, tg_user = self.get_data(pk)

        body = StartNotifySerializer(data=self.request.data)
        body.is_valid(raise_exception=True)

        cron_time, _ = CrontabSchedule.objects.get_or_create(
            hour=habit.time.hour,
            minute=habit.time.minute,
            day_of_month=f'*/{habit.periodic}',
            timezone=body.validated_data['timezone']
        )

        task, created = PeriodicTask.objects.get_or_create(
            name=self.get_task_name(habit.id, tg_user.telegram_user_id),
            crontab=cron_time,
            task='app_habits.tasks.send_habit_notification',
            args=f'[{habit.id},{tg_user.telegram_user_id}]'
        )

        if created:
            tasks.send_telegram_message.delay(
                telegram_uid=tg_user.telegram_user_id,
                md_text=message_text.message_notifications_on_off(habit, True)
            )

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=no_body,
        operation_description="Отключить оповещения"
    )
    @action(detail=True, methods=['delete'])
    def stop(self, request, pk: int = None):
        habit, tg_user = self.get_data(pk)

        task = get_object_or_404(PeriodicTask, name=self.get_task_name(habit.id, tg_user.telegram_user_id))
        task.delete()

        tasks.send_telegram_message.delay(
            telegram_uid=tg_user.telegram_user_id,
            md_text=message_text.message_notifications_on_off(habit, False)
        )

        return Response(status=status.HTTP_200_OK)
