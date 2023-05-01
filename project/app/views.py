from django.shortcuts import render
from .models import Student, Bursar
from .serializers import StudentSerializer, BursarSerializer
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse


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
        "passport": str(student.passport)
    }
    return JsonResponse(data)

class SignUpBursar(APIView):
    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
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
            "passport": bursars.passport
        }
        bursar_list.append(resp)
    context_data = {"bursars":bursar_list}
    return JsonResponse(context_data)

class LoginStudent(APIView):
    def post(self, request, format=None):
        data = request.data
        student = Student.objects.filter(matric_number=data["matric_number"])
        if not student:
            res = {
                "code":401,
                "error": "Invalid Matric Number"
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        # INCOMPLETE DUE TO INABILITY TO ACCESS "student.check_password()" function
        

        

