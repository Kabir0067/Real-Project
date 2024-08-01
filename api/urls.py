from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'customer_users', CustomerUserViewSet)
router.register(r'comeandwent', ComeAndWentViewSet)
router.register(r'feedback', FeedbackViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Average endpoints
    path('report/<int:pk>/', Report.as_view(), name='report'),
    path('average-attendance/', AverageAttendanceReport.as_view(), name='average_attendance'),
    path('average-group-attendance/<str:group_name>/', AverageGroupAttendanceReport.as_view(), name='average_group_attendance'),
]
