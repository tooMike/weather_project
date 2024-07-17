import requests
from django.http import JsonResponse
from django.shortcuts import render
from geopy.geocoders import Nominatim

from .constants import WEATHER_CODE_DESCRIPTIONS
from .forms import CityForm
from .models import CitySearchHistory

GEOAPIFY_API_KEY = 'df8ff8b5c28843ed9e152fd0e7e2e597'  # Замените на ваш
# ключ API Geoapify


def get_weather(latitude, longitude):
    url = (f'https://api.open-meteo.com/v1/forecast?latitude='
           f'{latitude}&longitude={longitude}&current_weather=true')
    response = requests.get(url)
    data = response.json()

    weather_code = data['current_weather']['weathercode']
    weather_description = WEATHER_CODE_DESCRIPTIONS.get(
        weather_code,
        "Unknown"
    )

    # Добавление описания погоды к данным
    data['current_weather']['description'] = weather_description
    data['current_weather']['latitude'] = latitude
    data['current_weather']['longitude'] = longitude
    return data


def get_city_coordinates(city_name):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city_name)
    return location.latitude, location.longitude


def get_city_by_coordinates(latitude, longitude):
    coordinates = str(latitude) + ', ' + str(longitude)
    geolocator = Nominatim(user_agent="weather_app")
    city = geolocator.reverse(coordinates, zoom=10, language="ru")
    return city


def city_autocomplete(request):
    if 'term' in request.GET:
        url = (f'https://api.geoapify.com/v1/geocode/autocomplete?text='
               f'{request.GET.get("term")}&apiKey={GEOAPIFY_API_KEY}')
        response = requests.get(url)
        data = response.json()
        cities = [feature['properties']['formatted'] for feature in
                  data['features']]
        return JsonResponse(cities, safe=False)
    return JsonResponse([], safe=False)


def index(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']
            latitude, longitude = get_city_coordinates(city_name)
            weather_data = get_weather(latitude, longitude)
            weather_data['city_name'] = get_city_by_coordinates(
                latitude,
                longitude
            )

            # Save search history
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

# def city_autocomplete(request):
#     if 'term' in request.GET:
#         cities = City.objects.filter(name__icontains=request.GET.get('term'))
#         names = list()
#         for city in cities:
#             names.append(city.name)
#         return JsonResponse(names, safe=False)
#     return JsonResponse([], safe=False)
