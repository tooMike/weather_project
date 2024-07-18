from django.urls import path

from api import views

urlpatterns = [
    path(
        'number-of-requests/',
        views.CitiesRequestNumber.as_view({'get': 'list', })
    )
]
