from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from app_habits.models import Habit
from app_habits.pagination import AppHabitPagination
from app_habits.serializers import HabitFullSerializer, HabitPublicSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitPublicSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('is_pleasantly', 'periodic')
    ordering_fields = ('duration', 'periodic')
    search_fields = ('action_description', 'reward', 'site')
    pagination_class = AppHabitPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Habit.objects.all()
        return Habit.objects.filter(Q(owner=self.request.user) | Q(is_public=True))

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return HabitFullSerializer
        return HabitPublicSerializer
