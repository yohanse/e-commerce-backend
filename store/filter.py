import django_filters
from . import models

class ProductFilter(django_filters.FilterSet):
    day = django_filters.NumberFilter(field_name='last_update', lookup_expr='day')
    month = django_filters.NumberFilter(field_name='last_update', lookup_expr='month')
    class Meta:
        model = models.Product
        fields = ['day', 'month']