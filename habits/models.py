from datetime import timedelta, datetime

from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):
    """
    Модель привычки.
    """

    PERIODS = {
        ("1 time in 1 days", "1 раз в день"),
        ("1 time in 7 days", "1 раз в неделю"),
    }

    action = models.CharField(max_length=150, verbose_name="Действие")
    place = models.CharField(max_length=100, verbose_name="Место выполнения привычки", **NULLABLE)
    time = models.TimeField(verbose_name="Время выполнения привычки")
    is_pleasant_habit = models.BooleanField(verbose_name="Признак приятной привычки", default=False, **NULLABLE)
    periodicity = models.CharField(max_length=100, choices=PERIODS, default="1 time in 1 days",
                                   verbose_name="Периодичность")
    reward = models.CharField(max_length=100, verbose_name="Вознаграждение", **NULLABLE)
    time_to_complete = models.PositiveIntegerField(verbose_name="Время на выполнение привычки")
    is_publicity = models.BooleanField(verbose_name="Признак публичности", default=False, **NULLABLE)
    next_reminder = models.DateField(verbose_name="Следующее напоминание", **NULLABLE)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Cоздатель привычки",
        **NULLABLE
    )
    associated_habit = models.ForeignKey(
        "Habit",
        verbose_name="Связанная привычка",
        related_name="habits",
        on_delete=models.SET_NULL,
        **NULLABLE
    )

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def save(self, *args, **kwargs):
        """
        Сверяет время привычки с текущим.
        Определяет день напоминания в зависимости от сверки времени.
        """

        now_time = datetime.now().time()
        now_date = datetime.now().date()
        if now_time > self.time:
            self.next_reminder = now_date + timedelta(minutes=1)
        else:
            self.next_reminder = now_date

        super(Habit, self).save(*args, **kwargs)
