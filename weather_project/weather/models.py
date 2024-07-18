from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CitySearchHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        null=True,
        blank=True
    )
    # Добавляем поле session_key для неавторизованных пользователей
    session_key = models.CharField(
        max_length=32,
        verbose_name="Ключ сессии"
    )
    city_name = models.CharField(max_length=100, verbose_name="Город")
    search_count = models.IntegerField(
        default=0,
        verbose_name="Число запросов"
    )
    last_searched = models.DateTimeField(
        auto_now=True,
        verbose_name="Время последнего запроса"
    )

    class Meta:
        default_related_name = "citysearchhistory"
        ordering = ("-last_searched",)
