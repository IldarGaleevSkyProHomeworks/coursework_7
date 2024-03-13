from django.contrib.auth.models import User
from django.db import models
from timezone_field import TimeZoneField

from app_habits.models import Habit


class HabitNotification(models.Model):
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно',
        help_text='Если активно, уведомления будут приходить',
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='habit_notifications',
        verbose_name='Владелец',
    )

    habits = models.ManyToManyField(
        Habit,
        related_name='notification',
        verbose_name='Привычки',
        help_text='Выберите привычки, которые хотите выполнять',
    )

    description = models.CharField(
        max_length=150,
        verbose_name='Описание цели',
        help_text='Опишите какую конечную цель вы преследуете, выполняя эти привычки'
    )

    timezone = TimeZoneField(
        default='Europe/Moscow',
        use_pytz=False,
        verbose_name='Часовой пояс',
        help_text='Укажите часовой пояс по которому будут формироваться уведомления',
    )

    def __str__(self):
        return f'Цель: {self.description} | Привычек: {self.habits.count()}'
