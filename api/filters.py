import django_filters
from .models import *
from django.db.models import Q
from django.utils.dateparse import parse_date

#Filter CustomerUser
class CustomerUserFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name='is_active', lookup_expr='exact', required=False)
    registration_date = django_filters.DateFilter(
        field_name='registration_date',
        lookup_expr='exact',
        required=False
    )
    date_registration_month = django_filters.CharFilter(
        method='filter_by_registration_month',
        label='Registration Month (YYYY-MM)',
        required=False
    )
    group_name = django_filters.CharFilter(
        method='filter_by_group_name',
        label='Group Name',
        required=False
    )

    class Meta:
        model = CustomerUser
        fields = ['is_active', 'registration_date', 'group_name']

    def filter_by_registration_month(self, queryset, name, value):
        if value:
            try:
                year, month = value.split('-')
                start_date = f'{year}-{month}-01'
                end_date = f'{year}-{month}-31'
                return queryset.filter(
                    registration_date__range=[start_date, end_date]
                )
            except ValueError:
                return queryset
        return queryset

    def filter_by_group_name(self, queryset, name, value):
        if value:
            print(f"Filtering by group_name: {value}")
            return queryset.filter(group_name__icontains=value)
        print("No group_name filter applied")
        return queryset


#Filter ComeAndWent
class ComeAndWentFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name='user__is_active')
    class Meta:
        model = ComeAndWent
        fields = ['is_active']
        

#Filter Feedback
class FeedbackFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name='user__is_active')
    class Meta:
        model = Feedback
        fields = ['is_active']
                

