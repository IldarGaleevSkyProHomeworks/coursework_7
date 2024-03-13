from django.contrib import admin

from app_habits.forms import HabitForm
from app_habits.models import Habit, HabitNotification


@admin.register(Habit)
class HabitAdminClass(admin.ModelAdmin):
    form = HabitForm


@admin.register(HabitNotification)
class HabitAdminClass(admin.ModelAdmin):
    pass
