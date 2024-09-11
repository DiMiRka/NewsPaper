from django_filters import FilterSet, CharFilter, DateFilter
from django import forms


class PostFilter(FilterSet):
    author = CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Автор')
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Название')
    time_in = DateFilter(field_name='time_in', label='Дата', lookup_expr='gte',
                         widget=forms.DateInput(attrs={'type': 'date'}))
