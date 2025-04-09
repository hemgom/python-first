import django_filters
from .models import ViewerHistory

class ViewerHistoryFilter(django_filters.FilterSet):
    file_name = django_filters.CharFilter(field_name='file_name', lookup_expr='icontains')
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = ViewerHistory
        fields = ['file_name', 'created_at']