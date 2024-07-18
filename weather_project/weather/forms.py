import re

from django import forms
from django.core.exceptions import ValidationError


class CityForm(forms.Form):
    """Форма для ввода названия города."""

    city_name = forms.CharField(
        label='Город:',
        min_length=3,
        max_length=100,
        widget=forms.TextInput()
    )
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)

    def clean_city_name(self):
        """Валидация названия города."""
        city_name = self.cleaned_data.get('city_name')

        # Проверяем, что все символы – буквы, пробелы или -
        if not re.match(r'^[a-zA-Zа-яА-Я\s\-,ё]+$', city_name):
            raise ValidationError(
                'Название города может состоять только из букв, пробелов, '
                'дефисов и запятых.'
            )

        return city_name
