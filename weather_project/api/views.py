from django.db.models import Sum
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from api.mixins import ListViewSet
from api.serializers import CitySearchHistoryAggregateSerializer
from weather.models import CitySearchHistory


class CitiesRequestNumber(ListViewSet):
    """Получение количества запросов по городам."""

    serializer_class = CitySearchHistoryAggregateSerializer
    filter_backends = (
        filters.SearchFilter,
    )
    search_fields = ("city_name",)
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = CitySearchHistory.objects.values('city_name').annotate(
            total_searches=Sum('search_count')
        ).order_by('-total_searches')
        return queryset
