from rest_framework import serializers
from .models import *

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('name', 'email', 'password', 'role')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        employee = Employee(**validated_data) 
        if password:
            employee.set_password(password) 
        employee.save()
        return employee
