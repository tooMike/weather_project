from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm
from users.views_mixins import UserNotAuthenticatedMixin

User = get_user_model()


class UserRegistration(UserNotAuthenticatedMixin, CreateView):
    """Регистрация пользователя."""
    template_name = "registration/registration_form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
