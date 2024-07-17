import requests
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render
from geopy.geocoders import Nominatim

from .constants import WEATHER_CODE_DESCRIPTIONS
from .forms import CityForm
from .models import CitySearchHistory

GEOAPIFY_API_KEY = 'df8ff8b5c28843ed9e152fd0e7e2e597'


def get_weather(latitude, longitude):
    """Получение погоды по координатам."""
    url = (f'https://api.open-meteo.com/v1/forecast?latitude='
           f'{latitude}&longitude={longitude}&current_weather=true')
    response = requests.get(url)
    data = response.json()
    # Получаем описание погоды по полученному weathercode
    weather_code = data['current_weather']['weathercode']
    weather_description = WEATHER_CODE_DESCRIPTIONS.get(
        weather_code,
        "Unknown"
    )
    # Добавление описания погоды к данным
    data['current_weather']['description'] = weather_description
    return data


def get_city_coordinates(city_name):
    """Получение координат по названию города."""
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    return None, None


def get_city_by_coordinates(latitude, longitude):
    """Получение названия города и страны по координатам."""
    coordinates = str(latitude) + ', ' + str(longitude)
    geolocator = Nominatim(user_agent="weather_app")
    # В параметрах указываем уровень детализации (до города) и язык
    city = geolocator.reverse(coordinates, zoom=10, language="ru")
    return city


def city_autocomplete(request):
    if 'term' in request.GET:
        url = (f'https://api.geoapify.com/v1/geocode/autocomplete?text='
               f'{request.GET.get("term")}&apiKey={GEOAPIFY_API_KEY}')
        response = requests.get(url)
        data = response.json()

        # Ограничиваем подсказки городом и страной, убираем дубликаты
        seen = set()
        unique_cities = []

        for feature in data['features']:
            properties = feature["properties"]
            city = properties.get("city")
            country = properties.get("country")
            if city and country:
                city_country = (city, country)
                if city_country not in seen:
                    seen.add(city_country)
                    unique_cities.append(
                        {
                            'city_name': city,
                            'country': country,
                            'latitude': properties["lat"],
                            'longitude': properties["lon"]
                        }
                    )
        return JsonResponse(unique_cities, safe=False)
    return JsonResponse([], safe=False)


def index(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']
            # Пытаемся извлечь координаты из полей формы,
            # эти поля будут заполнены в случае, если пользователь
            # использовал autocomplete
            latitude = form.cleaned_data.get('latitude', None)
            longitude = form.cleaned_data.get('longitude', None)
            # Если данных в форме нет, то пробуем получить координаты
            # по введенному пользователем названию
            if latitude is None or longitude is None:
                latitude, longitude = get_city_coordinates(city_name)

            # Если координаты получить не удалось,
            # то возвращаем пользователю ошибку
            if latitude is None or longitude is None:
                messages.error(request, 'Такой город не найден')
                return render(
                    request,
                    'weather/index.html',
                    {'form': form}
                )

            weather_data = get_weather(latitude, longitude)
            weather_data['city_name'] = get_city_by_coordinates(
                latitude,
                longitude
            )

            # Сохраняем данные поиска в БД
            if request.user.is_authenticated:
                history, created = CitySearchHistory.objects.get_or_create(
                    user=request.user,
                    city_name=city_name
                )
                if not created:
                    history.search_count += 1
                history.save()

            return render(
                request,
                'weather/index.html',
                {'form': form, 'weather_data': weather_data}
            )

    else:
        form = CityForm()

    return render(request, 'weather/index.html', {'form': form})
