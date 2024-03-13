from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_habits.apps import AppHabitsConfig
from app_habits.views import HabitViewSet

router = DefaultRouter()
router.register('', HabitViewSet, basename='habits')

app_name = AppHabitsConfig.name

urlpatterns = [
    path('', include(router.urls)),
]
