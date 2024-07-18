from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include, path, reverse_lazy

from users.forms import CustomUserCreationForm
from users.views import UserRegistration

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration',
        UserRegistration.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('login'),
        ),
        name='registration'
    ),
    path('api/', include('api.urls')),
    path('', include('weather.urls')),
]
