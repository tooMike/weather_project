from weather.models import CitySearchHistory


def get_history(request):
    """Получение истории запросов пользователя."""
    user = request.user
    if user.is_authenticated:
        history = CitySearchHistory.objects.filter(user=user)[:10]
    else:
        history = CitySearchHistory.objects.filter(
            session_key=request.session.session_key
        )[:10]
    return history
