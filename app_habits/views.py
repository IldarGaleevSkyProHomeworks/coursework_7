from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from app_accounts.permissions import IsOwner
from app_habits.models import Habit, HabitNotification
from app_habits.pagination import AppHabitPagination
from app_habits.serializers import HabitFullSerializer, HabitPublicSerializer
from app_habits.serializers.habit_notification_serializer import HabitNotificationSerializer


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


class HabitNotificationViewSet(viewsets.ModelViewSet):
    serializer_class = HabitNotificationSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]

    def get_queryset(self):
        is_swagger = getattr(self, 'swagger_fake_view', False)
        if not is_swagger and self.request.user.is_superuser:
            return HabitNotification.objects.all()
        return HabitNotification.objects.filter(owner=self.request.user)

    filter_backends = (SearchFilter,)
    search_fields = ('description',)
    pagination_class = AppHabitPagination
