from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'customer_users', CustomerUserViewSet)
router.register(r'comeandwent', ComeAndWentViewSet)
router.register(r'feedback', FeedbackViewSet)

urlpatterns = router.urls + [
    # Average endpoints
    path('average-time/<str:pk>/', Report.as_view(), name='average-time'),
    path('average-attendance/', AverageAttendanceReport.as_view(), name='average-attendance'),
    path('average-attendance/<str:group_name>/', AverageGroupAttendanceReport.as_view(), name='average-attendance'),

    # Average endpoints for false data
    path('average-time-false/<str:pk>/', ReportFalse.as_view(), name='average-time_False'),
    path('average-attendance-false/', AverageAttendanceReportFalse.as_view(), name='average-attendance_False'),
    path('average-attendance-false/<str:group_name>/', AverageGroupAttendanceReportFalse.as_view(), name='average-attendance_False'),
]
