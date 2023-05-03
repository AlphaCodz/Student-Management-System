from django.shortcuts import render
from .models import Student, Bursar
from .serializers import StudentSerializer, BursarSerializer
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from helpers.views import jsonify_student

# Create your views here.
class RegStudent(APIView):
    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def GetAllStudents(request, format=None):
    student = Student.objects.all()
    data = []
    for students in student:
        res = {
            "first_name": students.first_name,
            "middle_name":students.middle_name,
            "last_name": students.last_name,
            "address": students.address,
            "contact": students.contact,
            "email": students.email,
            "date_of_birth": students.date_of_birth,
            "passport": str(students.passport),
            "nok_name": students.nok_name,
            "relationship": students.relationship,
            "nok_contact": students.nok_contact,
            "department": students.department.department,
            "matric_number": students.matric_number
        }
        data.append(res)
        context_data = {"yct_students":data}
    return JsonResponse(context_data)

@api_view(["GET"])
def StudentBiodata(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response({"error": "Student does not exist"}, status=status.HTTP_404_NOT_FOUND)

    data = {
        "first_name": student.first_name,
        "middle_name": student.middle_name,
        "last_name": student.last_name,
        "contact": student.contact,
        "matric_no": student.matric_number,
        "student_address": student.address,
        "department": student.department.department,
        "next_of_kin": student.nok_name,
        "relationship_with_next_of_kin": student.relationship,
        "next_of_kin_contact": student.nok_contact,
        "passport": str(student.passport),
        "password": student.password
    }
    return JsonResponse(data)

class SignUpBursar(APIView):
    def post(self, request, format=None):
        serializer = BursarSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def AllBursars(request, format=None):
    bursar = Bursar.objects.all()
    bursar_list = []
    for bursars in bursar:
        resp = {
            "first_name": bursars.first_name,
            "last_name": bursars.last_name,
            "staff_number": bursars.staff_number,
            "contact": bursars.contact,
            "email": bursars.email,
            "department": bursars.department.department,
            "passport": str(bursars.passport),
        }
        bursar_list.append(resp)
    context_data = {"bursars":bursar_list}
    return JsonResponse(context_data)

class StudentLogins(APIView):
    def post(self, request):
        matric_number = request.data.get('email')
        password = request.data.get('password')
        
        student = authenticate(matric_number=matric_number, password=password)
        
        if student:
            request.user = student
            
            # GET ACCESS TOKEN FOR USER
            token = Token.objects.get(user=student)
            return Response({"token": token.key},status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credential'}, status=status.HTTP_401_UNAUTHORIZED)

class StudentLoginss(APIView):
    def post(self, request):
        data = request.data
        matric = data["matric_number"]
        password = data.get("password")

        # Authenticate the student
        student = authenticate(request=request, matric_number=matric, password=password)
        
        if student is not None:
            # Authentication successful
            token, created = Token.objects.get_or_create(user=student)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class StudentLogin(APIView):
    def post(self, request, format=None):
        student = Student.objects.filter(matric_number=request.data.get("matric_number")).first()
        if not student:
            resp = {
                "code": 404,
                "message": "Incorrect Matric Number"
            }
            return Response(resp, status=status.HTTP_404_NOT_FOUND)
        if student.check_password(raw_password=request.data["password"]):
            token = RefreshToken.for_user(student)
            resp = {
                "code": 202,
                "message": "Login Successful",
                "student_data": jsonify_student(student),
                "token": str(token.access_token)
            }
            return Response(resp, status=status.HTTP_200_OK)
        resp = {
            "code": 401,
            "message": "Incorrect Password"
        }
        return Response(resp, status=status.HTTP_401_UNAUTHORIZED)