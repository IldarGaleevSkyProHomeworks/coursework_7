from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app_habits.models import Habit
from app_habits.serializers import HabitFullSerializer, HabitPublicSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitPublicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Habit.objects.all()
        return Habit.objects.filter(Q(owner=self.request.user) | Q(is_public=True))

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return HabitFullSerializer
        return HabitPublicSerializer
