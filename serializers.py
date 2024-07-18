from rest_framework import serializers
from .models import Employee, Timesheet

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['empid', 'name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        employee = Employee.objects.create_user(**validated_data)
        return employee

class TimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timesheet
        fields = ['employee', 'date', 'start_time', 'end_time', 'project_name', 'comments', 'working_hours']
