from django_filters import rest_framework as filters
from cinema.models import Movie


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MovieFilter(filters.FilterSet):
    title = CharFilterInFilter(field_name='title', lookup_expr='in')
    category = CharFilterInFilter(field_name='category', lookup_expr='in')
    price = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['title', 'category']