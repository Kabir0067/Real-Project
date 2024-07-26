from django.shortcuts import render
from .serializers import *
from rest_framework.generics import *
from .models import *


#CRUD CustomerUser
class CustomerUserListView(ListAPIView):
     queryset=CustomerUser.objects.all()      
     serializer_class=CustomerUserSerializer

class CustomerUserCreateView(CreateAPIView):
     queryset=CustomerUser.objects.all()      
     serializer_class=CustomerUserSerializer

class CustomerUserUpdateView(UpdateAPIView):
     queryset=CustomerUser.objects.all()      
     serializer_class=CustomerUserSerializer

class CustomerUserDeleteView(DestroyAPIView):
     queryset=CustomerUser.objects.all()      
     serializer_class=CustomerUserSerializer


#CRUD ComeAndWent
class ComeAndWentListView(ListAPIView):
     queryset=ComeAndWent.objects.all()      
     serializer_class=ComeAndWentSerializer

class ComeAndWentCreateView(CreateAPIView):
     queryset=ComeAndWent.objects.all()      
     serializer_class=ComeAndWentSerializer

class ComeAndWentUpdateView(UpdateAPIView):
     queryset=ComeAndWent.objects.all()      
     serializer_class=ComeAndWentSerializer

class ComeAndWentDeleteView(DestroyAPIView):
     queryset=ComeAndWent.objects.all()      
     serializer_class=ComeAndWentSerializer


#CRUD Feedback
class FeedbackListView(ListAPIView):
     queryset=Feedback.objects.all()      
     serializer_class=FeedbackSerializer

class FeedbackCreateView(CreateAPIView):
     queryset=Feedback.objects.all()      
     serializer_class=FeedbackSerializer

class FeedbackUpdateView(UpdateAPIView):
     queryset=Feedback.objects.all()      
     serializer_class=FeedbackSerializer

class FeedbackDeleteView(DestroyAPIView):
     queryset=Feedback.objects.all()      
     serializer_class=FeedbackSerializer

#Detail CustomerUserSerializer
class StudentDetailView(RetrieveAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerStudentSerializer


#Giriftani Hammai malumothoi users
class AllUsersListView(ListAPIView):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerStudentSerializer