from django.shortcuts import render
from .models import Student, Bursar, Department, Document
from .serializers import StudentSerializer, BursarSerializer, DocumentSerializer
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from helpers.views import jsonify_student
from app.permissions import IsBursar, IsStudent
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from rest_framework import viewsets
from django.views.decorators.vary import vary_on_cookie


class UserViewSet(viewsets.ViewSet):
    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def list(self, request, format=None):
        content = {
            'user_feed': request.user.get_user_feed()
        }
        return Response(content)

# Create your views here.
class RegStudent(APIView):
    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAllStudents(APIView):
    @method_decorator(cache_page(60*2))
    def get(self, request, format=None):
        student = Student.objects.all().order_by('id')

        # PAGINATE LIST
        paginator = Paginator(student, 10)

        page_number = request.GET.get('page') #GET REQUESTED PAGE NUMBER FROM THE REQUEST PARAMETER
        page_obj = paginator.get_page(page_number) #RETRIEVE THE PAGE OBJECT FOR THE REQUESTED PAGE

        data = []
        for students in page_obj:
            res = {
                "student_data": jsonify_student(students)
            }
            data.append(res)
            
            context_data = {
                "yct_students":data,
                "current_page": page_obj.number,
                "total_pages": paginator.num_pages,
                "has_previous": page_obj.has_previous(),
                "has_next": page_obj.has_next()
                }
        return JsonResponse(context_data)

class StudentBiodata(APIView):
    @method_decorator(cache_page(60*60))
    def get(self, request, id):
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response({"error": "Student does not exist"}, status=status.HTTP_404_NOT_FOUND)
        data = {
            "biodata": jsonify_student(student)
        }
        return JsonResponse(data)

class BursarDocumentsView(APIView):
    def get(self, request, format=None):
        bursar = request.user  # Assuming the current user is the bursar
        documents = Document.objects.filter(staff=bursar)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)
    
class SubmitDocuments(APIView):
    def post(self, request, staff_id):
        student=request.user
        try:
            staff = Bursar.objects.get(id=staff_id)
        except Bursar.DoesNotExist:
            res = {
                "code": 404,
                "message": "Staff Does Not Exist"
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)
        
        bursar = Document.objects.create(
            staff=staff,
            name=request.data["name"],
            file=request.data["file"]
        )
        bursar.save()
        res = {
            "code":201,
            "message": "Documents Submitted Successfully",
            "file_name": bursar.name,
            "file": str(bursar.file.url),
            "student": f"{student.first_name} {student.last_name}",
            "department": student.department.department
        }
        return Response(res, status=status.HTTP_201_CREATED)
        
class SignUpBursar(APIView):
    def post(self, request, format=None):
        serializer = BursarSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllBursars(APIView):
    def get(request, format=None):
        bursar = Bursar.objects.all()
        bursar_list = []
        for bursars in bursar:
            resp = {
                "id":bursars.id,
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
    
class BursarLogin(APIView):
    def post(self, request, format=None):
        data = request.data
        bursar = Bursar.objects.filter(staff_number=data["staff_number"]).first()
        if not bursar:
            resp = {
                "code":404,
                "message": "Staff Number not Correct"
            }
            return Response(resp, status=status.HTTP_404_NOT_FOUND)
    
class GetAllSIBD(APIView): # SIBD = STUDENTS IN BURSAR'S DEPARTMENT
    permission_classes=[IsStudent,]

    # Cache page for the requested url for 1 hr
    @method_decorator(cache_page(60*60))
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
        