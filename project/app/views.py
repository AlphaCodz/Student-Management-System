from django.shortcuts import render
from .models import Student, Bursar, Department
from .serializers import StudentSerializer, BursarSerializer
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from helpers.views import jsonify_student
from app.permissions import IsBursar, IsStudent

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
            "department": str(students.department),
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
        "department": str(student.department),
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
            "department": str(bursars.department),
            "passport": str(bursars.passport),
        }
        bursar_list.append(resp)
    context_data = {"bursars":bursar_list}
    return JsonResponse(context_data)
        
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
                "code": 200,
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
    
class GetAllSIBD(APIView): # SIBD = STUDENTS IN BURSAR'S DEPARTMENT
    permission_classes=[IsStudent,]
    def get(self, request):
        dept = request.user.department.id
        try:
            bursar_dept = Bursar.objects.get(department=dept)
            students = Student.objects.filter(department=bursar_dept.id)
            student_data = [jsonify_student(student) for student in students]
            data = {
                "student_data": student_data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Department.DoesNotExist:
            return Response({"error": "Department not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({"error": "No students found in the department."},
                            status=status.HTTP_404_NOT_FOUND)
        