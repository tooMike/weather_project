import requests
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from geopy.geocoders import Nominatim

from .constants import WEATHER_CODE_DESCRIPTIONS
from .exceptions import CityNotFoundError, WeatherServiceError
from .forms import CityForm
from .models import CitySearchHistory
from .utils import get_history

GEOAPIFY_API_KEY = 'df8ff8b5c28843ed9e152fd0e7e2e597'


def get_weather(latitude, longitude):
    """Получение погоды по координатам."""
    try:
        url = (f'https://api.open-meteo.com/v1/forecast?latitude='
               f'{latitude}&longitude={longitude}&current_weather=true')
        response = requests.get(url)
        response.raise_for_status()
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
    except requests.RequestException:
        raise WeatherServiceError("Ошибка при получении информации о погоде")


def get_city_coordinates(city_name):
    """Получение координат по названию города."""
    try:
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city_name, timeout=10)
        return location.latitude, location.longitude
    except Exception:
        raise CityNotFoundError(f"Не удалось найти город: {city_name}")


def get_city_by_coordinates(latitude, longitude):
    """Получение названия города и страны по координатам."""
    try:
        coordinates = str(latitude) + ', ' + str(longitude)
        geolocator = Nominatim(user_agent="weather_app")
        # В параметрах указываем уровень детализации (до города) и язык
        city = geolocator.reverse(coordinates, zoom=10, language="ru")
        return city
    except Exception:
        raise CityNotFoundError("Не удалось найти город")


def city_autocomplete(request):
    if 'term' in request.GET:
        try:
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
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, safe=False, status=500)
    return JsonResponse([], safe=False)


def index(request):
    context = {}

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']
            # Пытаемся извлечь координаты из полей формы.
            # Эти поля будут заполнены в случае, если пользователь
            # использовал autocomplete
            latitude = form.cleaned_data.get('latitude', None)
            longitude = form.cleaned_data.get('longitude', None)

            try:
                # Если данных в форме нет, то пробуем получить координаты
                # по введенному пользователем названию
                if latitude is None or longitude is None:
                    latitude, longitude = get_city_coordinates(city_name)

                weather_data = get_weather(latitude, longitude)
                weather_data['city_name'] = get_city_by_coordinates(
                    latitude,
                    longitude
                )

                # Сохраняем данные поиска в БД
                if request.user.is_authenticated:
                    history, created = CitySearchHistory.objects.get_or_create(
                        user=request.user,
                        city_name=weather_data['city_name'],
                    )
                    if not created:
                        history.search_count += 1
                    history.save()
                else:
                    # Добавляем сессионный ключ, если его нет
                    if not request.session.session_key:
                        request.session.create()
                    history, created = CitySearchHistory.objects.get_or_create(
                        session_key=request.session.session_key,
                        city_name=weather_data['city_name']
                    )
                    if not created:
                        history.search_count += 1
                    history.save()

                context['weather_data'] = weather_data

            except CityNotFoundError as e:
                messages.error(request, str(e))
            except WeatherServiceError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Неизвестная ошибка: {e}")

    else:
        form = CityForm()

    context['form'] = form
    # Если есть история запросов, до добавляем ее в контекст
    if history := get_history(request):
        context['history'] = history

    return render(request, 'weather/index.html', context=context)
