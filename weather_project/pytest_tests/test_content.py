from http import HTTPStatus

import pytest
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

from users.forms import CustomUserCreationForm
from weather.forms import CityForm


@pytest.mark.parametrize(
    "client_fixture, name",
    [
        ("user_auf_client", "main:index"),
        ("user_auf_client", "login"),
        ("client", "main:index"),
        ("client", "login"),
    ]
)
def test_pages_available(db, request, client_fixture, name):
    """
    Проверяем доступность страниц
    для авторизированного и анонимного пользователя.
    """
    client = request.getfixturevalue(client_fixture)
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "client_fixture, name, form",
    [
        ("user_auf_client", "main:index", CityForm),
        ("client", "main:index", CityForm),
        ("client", "registration", CustomUserCreationForm),
        ("client", "login", AuthenticationForm),
    ]
)
def test_page_contains_form(db, request, client_fixture, name, form):
    """
    Проверяем наличие форм на главной, странице входа и регистрации.
    """
    client = request.getfixturevalue(client_fixture)
    url = reverse(name)
    response = client.get(url)
    assert ("form" in response.context) is True
    if "form" in response.context:
        assert isinstance(response.context["form"], form)
