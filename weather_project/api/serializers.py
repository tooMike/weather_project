from rest_framework import serializers


class CitySearchHistoryAggregateSerializer(serializers.Serializer):
    """Сериализатор для количества поисков городов."""

    city_name = serializers.CharField(max_length=100)
    total_searches = serializers.IntegerField()
