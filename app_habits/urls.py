from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_habits.apps import AppHabitsConfig
from app_habits.views import HabitViewSet, HabitNotificationViewSet

router = DefaultRouter()
router.register('habits', HabitViewSet, basename='habits')
router.register('targets', HabitNotificationViewSet, basename='targets')

app_name = AppHabitsConfig.name

urlpatterns = [
    path('', include(router.urls)),
]
