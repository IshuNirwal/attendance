from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.parsers import FileUploadParser
import cv2
import numpy as np
from pyzbar import pyzbar


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


class ScanBarcodeView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request):
        barcode_image = request.FILES.get('file')

        # Read the uploaded barcode image
        image = cv2.imdecode(np.frombuffer(barcode_image.read(), np.uint8), cv2.IMREAD_COLOR)
       
        # Convert image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Perform barcode detection
        decoded_objects = pyzbar.decode(gray_image)

        # Extracting barcode data
        barcode_data = None
        for obj in decoded_objects:
            barcode_data = obj.data.decode('utf-8')
            break  # Assuming there's only one barcode in the image

        # If no barcode is detected
        if barcode_data is None:
            return Response({'error': 'No barcode detected in the uploaded image'}, status=400)

        # Create an instance of Attendance with barcode data
        serializer = AttendanceSerializer(data={'barcode_image': barcode_image, 'barcode_data': barcode_data})

        # Validate and save the serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        













        