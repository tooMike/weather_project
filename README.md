## Описание

Web приложения для получения прогноза погоды в определенном городе.

Проект реализован на Django. Пользовательская часть реализована на Django шаблонах. 

Сервис погоды: https://open-meteo.com/.

Для получения координат использована библиотека [geopy](https://geopy.readthedocs.io/en/stable/#) и сервис [Nominatim](https://nominatim.org/release-docs/develop/api/Overview/).

В проекте реализованы автодополнения (подсказки) при вводе города с использованием Address Autocomplete API от [Geoapify](https://apidocs.geoapify.com/docs/geocoding/address-autocomplete/).

В проекте написано несколько тестов для проверки доступности страниц и форм для анонимных и авторизированных пользователей.

Реализовано API c использованием DRF для получения количества запросов по каждому городу.

В проекте сохраняется история поиска для каждого пользователя (анонимного и авторизированного), и она доступна всем при посещении сервиса. Пользователь может легко перейти на любой город из истории просмотров.

Проект помещен в Docker контейнер и запускается с использованием Docker Compose.

## Возможные улучшения и изменения

1. Реализовать автодополнения с помощью своей БД, например, на основе cities.json
2. Переписать проект на асинхронном фреймворке, например на FastAPI. В проекте используется много обращений к сторонним сервисом, и в реальном проекте возможность выполнять эти запросы асинхронно будет играть важную роль в скорости работы
3. Покрыть тестами весь проект
4. Сейчас история поиска погоды по городам не присваивается от анонимного пользователя к авторизированному при логине в сервис. Можно сделать перепривязку истории с session_key к user при авторизации

## Автор проекта

[Mikhail](https://github.com/tooMike)

## Установка с использованием Docker

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/tooMike/weather_project
```

```
cd weather_project
```

Запустить сборку проекта:

```
docker compose up
```

Выполнить сбор статики в контейнере backend:

```
docker compose exec backend python manage.py collectstatic
```

Выполнить миграции в контейнере backend:

```
docker compose exec backend python manage.py migrate
```

Запустить тесты в контейнере backend:

```
docker compose exec backend pytest
```

Проект будет доступен по адресу

```
http://127.0.0.1:8000/
```

Для работы сервиса нужно добавить файл .env в корень проекта. Так делать не хорошо, но вот пример файла, чтобы сервис можно было запустить и проверить:

```
SECRET_KEY='django-insecure-op^5wk%t260jx1!*+m=m^zdz9z--obdny%y(vyv3ihi%e=dx3z'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
INTERNAL_IPS=127.0.0.1,
GEOAPIFY_API_KEY='df8ff8b5c28843ed9e152fd0e7e2e597'
DATABASE=PostgreSQL
POSTGRES_USER=django_user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432
```

## Основные технические требования

Python==3.11

## Примеры запросов к API

### Получение публикаций

Описание метода: Получить список всех публикаций. При указании параметров limit и offset выдача работает с пагинацией.

Тип запроса: `GET`

Эндпоинт: `/api/number-of-requests/`

Доступен поиск по названию города: `/api/number-of-requests/?search=Москва`

Доступна пагинация: `/api/number-of-requests/?limit=5&offset=5`

Пример успешного ответа:

```
{
    "count": 5,
    "next": "http://127.0.0.1:8000/api/number-of-requests/?limit=1&offset=1",
    "previous": null,
    "results": [
        {
            "city_name": "Москва, Центральный федеральный округ, Россия",
            "total_searches": 6
        }
    ]
}
```
