from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from rest_framework.views import APIView

class EmployeeRegistrationView(APIView):
    serializer_class = EmployeeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            return Response({"message": "Employee registration successful", "employee_id": employee.employee_id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
