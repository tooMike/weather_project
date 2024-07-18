from rest_framework import mixins, viewsets


class ListViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Миксин для детального и спискового представления."""
