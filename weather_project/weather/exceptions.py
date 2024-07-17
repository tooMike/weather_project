class CityNotFoundError(Exception):
    """Исключение для случая, когда город не найден."""
    pass


class WeatherServiceError(Exception):
    """Исключение для ошибок при запросе к сервису погоды."""
    pass
