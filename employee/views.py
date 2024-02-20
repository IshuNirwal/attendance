from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from datetime import datetime

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class EmployeeRegistrationView(APIView):
    serializer_class = EmployeeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            employee = serializer.save()
            return Response({"message": "Employee registration successful", "employee_id": employee.employee_id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeLoginView(APIView):

    def post(self, request):
        serializer = EmployeeLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({"message":"Login Successful",'token': token}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ScanQRCodeView(APIView):
    def post(self, request):
        qrcode_data = request.data.get('qrCode')
        if not qrcode_data:
            return Response({'error': 'QR code data not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            employee = Employee.objects.get(employee_id=qrcode_data) 
            attendance, created = Attendance.objects.get_or_create(employee=employee)
            if created:  
                attendance.arrival_time = datetime.now()
                attendance.is_present=True
                attendance.save()
            return Response({'message': 'QR code verified successfully', 'employeeName': employee.name, 'employeeId': employee.employee_id}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({'error': 'QR code does not match any records'}, status=status.HTTP_404_NOT_FOUND)
        

