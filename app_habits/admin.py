from django.contrib import admin

from app_habits.forms import HabitForm
from app_habits.models import Habit


@admin.register(Habit)
class HabitAdminClass(admin.ModelAdmin):
    form = HabitForm
