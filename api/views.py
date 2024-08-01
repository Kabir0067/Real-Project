from datetime import datetime, timedelta
from collections import defaultdict
from rest_framework.permissions import *
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.db.models import Avg, F, ExpressionWrapper, fields
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from .serializers import *
from .models import *
from .filters import *



# CRUD CustomerUser
class CustomerUserViewSet(viewsets.ModelViewSet):
    queryset = CustomerUser.objects.all()
    serializer_class = CustomerUserSerializer
    permission_classes = [  ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomerUserFilter

# CRUD ComeAndWent
class ComeAndWentViewSet(viewsets.ModelViewSet):
    queryset = ComeAndWent.objects.all()
    serializer_class = ComeAndWentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ComeAndWentFilter

# CRUD Feedback
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FeedbackFilter
     

        
#Funcsiya baroi hisob kardani average studentho     
def calculate_attendance(student_records):
    attendance_records = []
    date_time_totals = defaultdict(float)
    
    for record in student_records:
        if record.time_to_come and record.time_to_go:
            time_spent = record.time_to_go - record.time_to_come
            hours_spent = time_spent.total_seconds() / 3600
            date = record.date
            date_time_totals[date] += hours_spent
    
    for date, hours_spent in date_time_totals.items():
        attendance_records.append({'date': date, 'hours_spent': hours_spent})
    
    sorted_attendance_records = sorted(attendance_records, key=lambda x: x['hours_spent'], reverse=True)
    average_hours = (sum(rec['hours_spent'] for rec in sorted_attendance_records) / len(sorted_attendance_records)) if sorted_attendance_records else 0
    
    return average_hours, sorted_attendance_records


#Giriftani avirage soati omadai 1 student
class Report(APIView):
    def get(self, request, pk):
        active_param = request.query_params.get("active")
        if active_param is None:
            students = CustomerUser.objects.filter(pk=pk)
        else:
            is_active = active_param.lower() == "true"
            students = CustomerUser.objects.filter(pk=pk, is_active=is_active)

        if not students.exists():
            return Response({'error': 'Student not found or inactive'}, status=status.HTTP_404_NOT_FOUND)

        student = students.first()
        student_records = ComeAndWent.objects.filter(user=student)
        average_hours, sorted_attendance_records = calculate_attendance(student_records)
        
        return Response({
            'student_id': student.pk,
            'student username': student.username,
            'average_hours': average_hours,
            'attendance_records': sorted_attendance_records
        }, status=status.HTTP_200_OK)


#Giriftani avirage hammai  soati studenthoi softclub
class AverageAttendanceReport(APIView):
    def get(self, request):
        active_param = request.query_params.get("active")
        if active_param is None:
            students = CustomerUser.objects.all()
        else:
            is_active = active_param.lower() == "true"
            students = CustomerUser.objects.filter(is_active=is_active)
        
        attendance_data = []

        for student in students:
            student_records = ComeAndWent.objects.filter(user=student)
            avg_hours, _ = calculate_attendance(student_records)
            attendance_data.append({
                'student_id': student.user_id,
                'student username': student.username,
                'average_hours': avg_hours
                })

        sorted_attendance_data = sorted(attendance_data, key=lambda x: x['average_hours'], reverse=True)
        overall_average = (sum(data['average_hours'] for data in sorted_attendance_data) / len(sorted_attendance_data)) if sorted_attendance_data else 0

        return Response({
            'overall_average_hours students SoftClub': overall_average,
            'attendance_data': sorted_attendance_data
        }, status=status.HTTP_200_OK)


# #Giriftani Average group bo studenthoyash Ham True ham False
class AverageGroupAttendanceReport(APIView):
    def get(self, request, group_name):
        active_param = request.query_params.get("active")
        date_register_param = request.query_params.get("date-register")

        if active_param is None:
            students = CustomerUser.objects.filter(group_name=group_name)
        else:
            is_active = active_param.lower() == "true"
            students = CustomerUser.objects.filter(is_active=is_active, group_name=group_name)

        if date_register_param:
            try:
                date_register = datetime.strptime(date_register_param, "%Y-%m")
                students = students.filter(registration_date__gte=date_register)
            except ValueError:
                return Response({"error": "Invalid date format. Please use YYYY-MM."}, status=status.HTTP_400_BAD_REQUEST)

        attendance_data = []

        for student in students:
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
                'is active': student.is_active,
                'tudent_id': student.user_id,
                'tudent username': student.username,
                'data registrations': student.registration_date.strftime("%Y:%m:%d"),
                'average_hours': avg_hours
            })

        sorted_attendance_data = sorted(attendance_data, key=lambda x: x['average_hours'], reverse=True)
        overall_average = (sum([data['average_hours'] for data in sorted_attendance_data]) / len(sorted_attendance_data)) if sorted_attendance_data else 0

        return Response({
            'overall_average_hours': overall_average,
            'attendance_data': sorted_attendance_data
        }, status=status.HTTP_200_OK)     
        