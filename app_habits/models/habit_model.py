from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Habit(models.Model):
    time = models.TimeField(
        verbose_name='Время',
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец'
    )

    site = models.CharField(
        max_length=250,
        verbose_name='Место'
    )

    action_description = models.CharField(
        max_length=250,
        verbose_name='Действие'
    )

    is_pleasantly = models.BooleanField(
        verbose_name='Приятное действие'
    )

    linked_habit = models.ForeignKey(
        'Habit',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Связанная привычка'
    )

    periodic = models.SmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(7)
        ],
        verbose_name='Периодичность в днях'
    )

    reward = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name='Награда'
    )

    duration = models.IntegerField(
        default=2,
        verbose_name='Длительность выполнения (минут)'
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Сделать публичным'
    )

    def __str__(self):
        return f'{"Приятная" if self.is_pleasantly else "Неприятная"} привычка {self.action_description}'


