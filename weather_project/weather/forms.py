from django import forms


class CityForm(forms.Form):
    city_name = forms.CharField(
        label='Город:',
        min_length=3,
        max_length=100,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
