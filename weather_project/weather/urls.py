from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'city-autocomplete/',
        views.city_autocomplete,
        name='city_autocomplete'
    ),
]
