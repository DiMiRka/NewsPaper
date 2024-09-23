from django_filters import FilterSet, CharFilter, DateFilter, ChoiceFilter
from django import forms
from .models import Category, Author


class PostFilter(FilterSet):
    author = ChoiceFilter(field_name='author__user__username', choices=[], lookup_expr='icontains', label='Автор')
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Название')
    category = ChoiceFilter(field_name='category__name', choices=[], lookup_expr='icontains', label='Категория')
    time_in = DateFilter(field_name='time_in', label='Дата', lookup_expr='gte',
                         widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['category'].extra['choices'] = [
            (category, category)
            for category in Category.objects.values_list('name', flat=True).distinct()
        ]
        self.filters['author'].extra['choices'] = [
            (author, author)
            for author in Author.objects.values_list('user__username', flat=True).distinct()
        ]