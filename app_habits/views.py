from celery.schedules import crontab
from django.db.models import Q
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

    def get_data(self, pk: int):
        habit = get_object_or_404(Habit, pk=pk)
        telegram_user = TelegramUser.objects.filter(user=self.request.user).first()
        if not telegram_user:
            raise ValidationError('У пользователя нет связанного Telegram аккаунта')

        return habit, telegram_user

    @swagger_auto_schema(
        request_body=no_body,
        operation_description="Включить оповещения"
    )
    @action(detail=True, methods=['post'])
    def start(self, request, pk: int = None):
        habit, tg_user = self.get_data(pk)

        task = crontab(
            minute=habit.time.minute,
            hour=habit.time.hour,

        )

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=no_body,
        operation_description="Отключить оповещения"
    )
    @action(detail=True, methods=['delete'])
    def stop(self, request, pk: int = None):
        habit, tg_user = self.get_data(pk)
        return Response(status=status.HTTP_200_OK)
