import pytest

from django.test.client import Client


@pytest.fixture
def user_auf(django_user_model):
    return django_user_model.objects.create(username="User")


@pytest.fixture
def user_auf_client(user_auf):
    client = Client()
    client.force_login(user_auf)
    return client
