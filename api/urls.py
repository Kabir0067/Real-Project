from django.urls import path
from .views import *

urlpatterns = [
     # CustomerUser endpoints
    path('customer_users/', CustomerUserListView.as_view(), name='customer_user_list'),
    path('customer_users/create/', CustomerUserCreateView.as_view(), name='customer_user_create'),
    path('customer_users/<str:pk>/update/', CustomerUserUpdateView.as_view(), name='customer_user_update'),
    path('customer_users/<str:pk>/delete/', CustomerUserDeleteView.as_view(), name='customer_user_delete'),
    path('student/<str:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('students/', AllUsersListView.as_view(), name='all-users'),

    # ComeAndWent endpoints
    path('come_and_went/', ComeAndWentListView.as_view(), name='come_and_went_list'),
    path('come_and_went/create/', ComeAndWentCreateView.as_view(), name='come_and_went_create'),
    path('come_and_went/<int:pk>/update/', ComeAndWentUpdateView.as_view(), name='come_and_went_update'),
    path('come_and_went/<int:pk>/delete/', ComeAndWentDeleteView.as_view(), name='come_and_went_delete'),

    # Feedback endpoints
    path('feedback/', FeedbackListView.as_view(), name='feedback_list'),
    path('feedback/create/', FeedbackCreateView.as_view(), name='feedback_create'),
    path('feedback/<int:pk>/update/', FeedbackUpdateView.as_view(), name='feedback_update'),
    path('feedback/<int:pk>/delete/', FeedbackDeleteView.as_view(), name='feedback_delete'),
]
