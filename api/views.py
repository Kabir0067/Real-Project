from datetime import datetime, timedelta
from collections import defaultdict
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.db.models import Avg, F, ExpressionWrapper, fields
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .serializers import *
from .models import *
from .filters import *



# CRUD CustomerUser
class CustomerUserViewSet(viewsets.ModelViewSet):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CustomerUserFilter
    search_fields = ['group_name']


#CRUD ComeAndWent
class ComeAndWentViewSet(viewsets.ModelViewSet):
    queryset = ComeAndWent.objects.all()
    serializer_class = ComeAndWentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ComeAndWentFilter
    

#CRUD Feedback
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FeedbackFilter
     


#Giriftani avirage soati omadai 1 student
class Report(APIView):
    def get(self, request, pk):
        try:
            student = CustomerUser.objects.get(pk=pk, is_active=True)
        except CustomerUser.DoesNotExist:
            return Response({'error': 'Student not found or inactive'}, status=status.HTTP_404_NOT_FOUND)
        
        student_records = ComeAndWent.objects.filter(user=student)
        attendance_records = []

        for record in student_records:
            if record.time_to_come and record.time_to_go:
                time_spent = record.time_to_go - record.time_to_come
                hours_spent = time_spent.total_seconds() / 3600
                attendance_records.append({
                    'date': record.date,
                    'hours_spent': hours_spent
                })
        
        sorted_attendance_records = sorted(attendance_records, key=lambda x: x['hours_spent'], reverse=True)

        average_hours = (sum(rec['hours_spent'] for rec in sorted_attendance_records) / len(sorted_attendance_records)) if sorted_attendance_records else 0

        return Response({
            'average_hours': average_hours,
            'attendance_records': sorted_attendance_records
        }, status=status.HTTP_200_OK)


#Giriftani avirage hammai  soati studenthoi softclub
class AverageAttendanceReport(APIView):
    def get(self, request):
        active_students = CustomerUser.objects.filter(is_active=True)
        attendance_data = []

        for student in active_students:
            student_records = ComeAndWent.objects.filter(user=student)
            date_time_totals = defaultdict(float)
            
            for record in student_records:
                if record.time_to_come and record.time_to_go:
                    time_spent = record.time_to_go - record.time_to_come
                    hours_spent = time_spent.total_seconds() / 3600
                    date = record.date  
                    date_time_totals[date] += hours_spent
            
            total_hours = sum(date_time_totals.values())
            record_count = len(date_time_totals)
            
            if record_count > 0:
                avg_hours = total_hours / record_count
            else:
                avg_hours = 0

            attendance_data.append({
                'student_id': student.user_id,
                'average_hours': avg_hours
            })

        sorted_attendance_data = sorted(attendance_data, key=lambda x: x['average_hours'], reverse=True)

        overall_average = sum([data['average_hours'] for data in sorted_attendance_data]) / len(sorted_attendance_data) if sorted_attendance_data else 0

        return Response({
            'overall_average_hours': overall_average,
            'attendance_data': sorted_attendance_data
        }, status=status.HTTP_200_OK)


#Giriftani Average group bo studenthoyash
class AverageGroupAttendanceReport(APIView):
    def get(self, request, group_name):
        active_students = CustomerUser.objects.filter(is_active=True, group_name=group_name)
        attendance_data = []

        for student in active_students:
            student_records = ComeAndWent.objects.filter(user=student)
            date_time_totals = defaultdict(float)
            
            for record in student_records:
                if record.time_to_come and record.time_to_go:
                    time_spent = record.time_to_go - record.time_to_come
                    hours_spent = time_spent.total_seconds() / 3600
                    date = record.date  
                    date_time_totals[date] += hours_spent
            
            total_hours = sum(date_time_totals.values())
            record_count = len(date_time_totals)
            
            if record_count > 0:
                avg_hours = total_hours / record_count
            else:
                avg_hours = 0

            attendance_data.append({
                'student_id': student.user_id,
                'average_hours': avg_hours
            })

        sorted_attendance_data = sorted(attendance_data, key=lambda x: x['average_hours'], reverse=True)
        overall_average = sum([data['average_hours'] for data in sorted_attendance_data]) / len(sorted_attendance_data) if sorted_attendance_data else 0
        
        return Response({
            'overall_average_hours': overall_average,
            'attendance_data': sorted_attendance_data
        }, status=status.HTTP_200_OK)
        

#Giriftani avirage soati omadai 1 student False
class ReportFalse(APIView):
    def get(self, request, pk):
        try:
            student = CustomerUser.objects.get(pk=pk, is_active=False)
        except CustomerUser.DoesNotExist:
            return Response({'error': 'Student not found or inactive'}, status=status.HTTP_404_NOT_FOUND)
        
        student_records = ComeAndWent.objects.filter(user=student)
        attendance_records = []

        for record in student_records:
            if record.time_to_come and record.time_to_go:
                time_spent = record.time_to_go - record.time_to_come
                hours_spent = time_spent.total_seconds() / 3600
                attendance_records.append({
                    'date': record.date,
                    'hours_spent': hours_spent
                })
        
        sorted_attendance_records = sorted(attendance_records, key=lambda x: x['hours_spent'], reverse=True)

        average_hours = (sum(rec['hours_spent'] for rec in sorted_attendance_records) / len(sorted_attendance_records)) if sorted_attendance_records else 0

        return Response({
            'average_hours': average_hours,
            'attendance_records': sorted_attendance_records
        }, status=status.HTTP_200_OK)


#Giriftani avirage hammai  soati studenthoi softclub False
class AverageAttendanceReportFalse(APIView):
    def get(self, request):
        active_students = CustomerUser.objects.filter(is_active=False)
        attendance_data = []

        for student in active_students:
            student_records = ComeAndWent.objects.filter(user=student)
            date_time_totals = defaultdict(float)
            
            for record in student_records:
                if record.time_to_come and record.time_to_go:
                    time_spent = record.time_to_go - record.time_to_come
                    hours_spent = time_spent.total_seconds() / 3600
                    date = record.date 
                    date_time_totals[date] += hours_spent
            
            total_hours = sum(date_time_totals.values())
            record_count = len(date_time_totals)
            
            if record_count > 0:
                avg_hours = total_hours / record_count
            else:
                avg_hours = 0

            attendance_data.append({
                'student_id': student.user_id,
                'average_hours': avg_hours
            })

        sorted_attendance_data = sorted(attendance_data, key=lambda x: x['average_hours'], reverse=True)

        overall_average = sum([data['average_hours'] for data in sorted_attendance_data]) / len(sorted_attendance_data) if sorted_attendance_data else 0

        return Response({
            'overall_average_hours': overall_average,
            'attendance_data': sorted_attendance_data
        }, status=status.HTTP_200_OK)


#Giriftani Average group bo studentho False
class AverageGroupAttendanceReportFalse(APIView):
    def get(self, request, group_name):
        active_students = CustomerUser.objects.filter(is_active=False, group_name=group_name)
        attendance_data = []

        for student in active_students:
            student_records = ComeAndWent.objects.filter(user=student)
            date_time_totals = defaultdict(float)
            
            for record in student_records:
                if record.time_to_come and record.time_to_go:
                    time_spent = record.time_to_go - record.time_to_come
                    hours_spent = time_spent.total_seconds() / 3600
                    date = record.date  
                    date_time_totals[date] += hours_spent
            
            total_hours = sum(date_time_totals.values())
            record_count = len(date_time_totals)
            
            if record_count > 0:
                avg_hours = total_hours / record_count
            else:
                avg_hours = 0

            attendance_data.append({
                'student_id': student.user_id,
                'average_hours': avg_hours
            })

        sorted_attendance_data = sorted(attendance_data, key=lambda x: x['average_hours'], reverse=True)
        overall_average = sum([data['average_hours'] for data in sorted_attendance_data]) / len(sorted_attendance_data) if sorted_attendance_data else 0
        
        return Response({
            'overall_average_hours': overall_average,
            'attendance_data': sorted_attendance_data
        }, status=status.HTTP_200_OK)
        
        
       
