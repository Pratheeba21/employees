from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from .models import Employee, Timesheet
from .serializers import EmployeeSerializer, TimesheetSerializer
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta
from collections import defaultdict
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.contrib.auth.models import User
class RegisterView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            if request.data['password'] == request.data['confirm_password']:
                serializer.save()
                return Response({"message": "Employee registered successfully."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        empid = request.data.get('empid')
        password = request.data.get('password')
        try:
            employee = Employee.objects.get(empid=empid)
            if employee.password == password:
                return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials, try again."}, status=status.HTTP_401_UNAUTHORIZED)
        except Employee.DoesNotExist:
            return Response({"error": "Invalid credentials, try again."}, status=status.HTTP_401_UNAUTHORIZED)

class TimesheetView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employee = Employee.objects.get(empid=request.user.username)
        except Employee.DoesNotExist:
            return Response({"error": "Employee matching query does not exist."}, status=status.HTTP_404_NOT_FOUND)

        timesheets = Timesheet.objects.filter(employee=employee)
        serializer = TimesheetSerializer(timesheets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TimesheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def register_page(request):
    return render(request, 'register.html')

def login_page(request):
    return render(request, 'login.html')

def timesheet_page(request):
    # Get the current employee
    employee = request.user

    # Generate a list of dates (e.g., for the current week)
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    dates = [start_of_week + timedelta(days=i) for i in range(7)]

    # Get timesheets for the current employee
    timesheets = Timesheet.objects.filter(employee=employee, date__in=dates)

    # Calculate total working hours for each date
    total_hours = defaultdict(float)
    for timesheet in timesheets:
        total_hours[timesheet.date] += timesheet.working_hours

    # Format total hours for the template
    total_hours = {date: f"{hours:.2f}" for date, hours in total_hours.items()}

    # Render the timesheet page with dates and total hours
    return render(request, 'timesheet.html', {'dates': dates, 'total_hours': total_hours})
