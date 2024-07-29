import django_filters
from .models import *


#Filter CustomerUser
class CustomerUserFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name='is_active', lookup_expr='exact')
    class Meta:
        model = CustomerUser
        fields = ['is_active']


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
                

