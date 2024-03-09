# Generated by Django 4.2.7 on 2024-03-10 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Habit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("time", models.TimeField(verbose_name="Время")),
                ("site", models.CharField(max_length=250, verbose_name="Место")),
                (
                    "action_description",
                    models.CharField(max_length=250, verbose_name="Действие"),
                ),
                (
                    "is_pleasantly",
                    models.BooleanField(verbose_name="Приятное действие"),
                ),
                (
                    "periodic",
                    models.SmallIntegerField(
                        choices=[
                            (0, "Почасовая"),
                            (1, "Ежедневно"),
                            (2, "Еженедельно"),
                            (3, "Ежемесячно"),
                        ],
                        default=1,
                        verbose_name="Частота повторения",
                    ),
                ),
                (
                    "reward",
                    models.CharField(
                        blank=True, max_length=250, null=True, verbose_name="Награда"
                    ),
                ),
                (
                    "duration",
                    models.IntegerField(
                        default=2, verbose_name="Длительность выполнения (минут)"
                    ),
                ),
                (
                    "is_public",
                    models.BooleanField(
                        default=False, verbose_name="Сделать публичным"
                    ),
                ),
                (
                    "linked_habit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="app_habits.habit",
                        verbose_name="Связанная привычка",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Владелец",
                    ),
                ),
            ],
        ),
    ]