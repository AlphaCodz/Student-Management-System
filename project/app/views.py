from django.shortcuts import render
from .models import MyUser, Department, Document
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from helpers.views import jsonify_student, jsonify_bursar
from app.permissions import IsBursar, IsStudent
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from rest_framework import viewsets
from django.views.decorators.vary import vary_on_cookie
import datetime
from django.db.models import Q


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
        student_data = request.data
        email = student_data["email"]
        student = MyUser.objects.filter(email=email, is_student=True).exists()
        if student:
            res = {
                "code":status.HTTP_401_UNAUTHORIZED,
                "message": "Student Already Exist"
            }
            return Response(res, res["code"])
        dept_id = student_data["department"]
        try:
            dept = Department.objects.get(id=dept_id)
        except Department.DoesNotExist:
            res = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Department Does Not Exist"
            }
            return Response(res, res["code"])
        
        student = MyUser.objects.create(
            first_name=student_data["first_name"],
            middle_name=student_data["middle_name"],
            last_name=student_data["last_name"],
            address=student_data["address"],
            contact=student_data["contact"],
            date_of_birth=student_data["date_of_birth"],
            passport=student_data["passport"],
            nok_name=student_data["nok_name"],
            relationship=student_data["relationship"],
            nok_contact=student_data["nok_contact"],
            department=dept,
            email=email
        )
        student.is_student=True
        student.is_bursar=False
        student.is_school_officer=False
        student.save()
        res = {
            "code": status.HTTP_201_CREATED,
            "message": "Student Created Successfully",
            "student_data": jsonify_student(student)
        }
        return Response(res, res["code"])   
    
class StudentLogin(APIView):
    def post(self, request, format=None):
        student = MyUser.objects.filter(is_student=True, matric_number=request.data.get("matric_number")).first()
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
    
class GetAllStudents(APIView):
    def get(self, request, format=None):
        students = MyUser.objects.filter(is_student=True).order_by("id")
        student_data = [jsonify_student(student) for student in students]
        response_data = {"student_data": student_data}
        return Response(response_data, status=200)


class StudentBiodata(APIView):
    @method_decorator(cache_page(60*60))
    def get(self, request, id):
        try:
            student = MyUser.objects.get(is_student=True, id=id)
        except MyUser.DoesNotExist:
            return Response({"error": "Student does not exist"}, status=status.HTTP_404_NOT_FOUND)
        data = {
            "biodata": jsonify_student(student)
        }
        return JsonResponse(data)
    
class SignUpBursar(APIView):
    def post(self, request, format=None):
        bursar_data = request.data
        email=bursar_data.get("email")
        bursar = MyUser.objects.filter(email=email, is_bursar=True).exists()
        if bursar:
            res = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "Bursar with this email exists"
            }
            return Response(res, res["code"])
        
        # VALIDATE DOB
        date_of_birth_str=bursar_data.get("date_of_birth")
        try:
            date_of_birth = datetime.datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
        except ValueError:
            res = {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid Date Of Birth format. . Required format: YYYY-MM-DD"
            }
            return Response(res, res["code"])
        #GET INSTANCE OF DEPARTMENT
        dept_id = bursar_data["department"]
        try:
            department = Department.objects.get(id=dept_id)
        except Department.DoesNotExist:
            res = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Department Does Not Exist"
            }
            return Response(res, res["code"])
        
        bursar = MyUser.objects.create(
            first_name=bursar_data["first_name"],
            last_name=bursar_data["last_name"],
            staff_number=bursar_data["staff_number"],
            contact=bursar_data["contact"],
            email=email,
            staff_passport=bursar_data["staff_passport"],
            department=department,
            address=bursar_data["address"],
            date_of_birth=date_of_birth,
            staff_signatures=bursar_data["staff_signatures"]
        )
        bursar.is_student=False
        bursar.is_bursar=True
        bursar.is_school_officer=False
        bursar.save()
        res = {
            "code": status.HTTP_201_CREATED,
            "message": "SignUp Successful",
            "bursar_data": jsonify_bursar(bursar)
        }
        return Response(res, res["code"])
    
class BursarLogin(APIView):
    def post(self, request, format=None):
        bursar = MyUser.objects.filter(is_bursar=True, staff_number=request.data.get("staff_number")).first()
        if not bursar:
            resp = {
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "Invalid Staff Number"
            }
            return Response(resp, resp["code"])
        if bursar.check_password(raw_password=request.data["password"]):
            token = RefreshToken.for_user(bursar)
            resp = {
                "code": status.HTTP_200_OK,
                "message": "Login Successful",
                "bursar_data": jsonify_bursar(bursar),
                "token": str(token.access_token)
            }
            return Response(resp, resp["code"])
        resp = {
            "code": status.HTTP_401_UNAUTHORIZED,
            "message": "Incorrect Password"
        }
        return Response(resp, resp["code"])   

class BursarDocumentsView(APIView):
    def get(self, request, format=None):
        bursar = request.user  # Assuming the current user is the bursar
        documents = Document.objects.filter(staff=bursar)
        data = [{"name": doc.name, "file":doc.file.url, "in_review": doc.in_review, "signed":doc.signed, "date_submitted":doc.date_submitted.date()} for doc in documents]
        return Response(data, status=status.HTTP_200_OK)
    
class SubmitDocuments(APIView):
    def post(self, request, staff_id):
        student = request.user
        try:
            user = MyUser.objects.get(id=student.id, is_student=True)
        except Student.DoesNotExist:
            res = {
                "code": 404,
                "message": "Student Doesn't exist"
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        try:
            staff = MyUser.objects.get(id=staff_id, is_bursar=True)
        except MyUser.DoesNotExist:
            res = {
                "code": 404,
                "message": "Bursar Does Not Exist"
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        document = Document(student=student, staff=staff)
        document.name = request.data["name"]
        document.file = request.data["file"]
        document.in_review = True
        document.signed = False
        document.save()

        res = {
            "code": 201,
            "message": "Documents Submitted Successfully",
            "student_name": f"{user.first_name} {user.last_name}",
            "file_name": document.name,
            "file": str(document.file.url),
            "submitted_to": f"{staff.first_name} {staff.last_name}",
            "department": student.department.department,
            "date_submitted":document.date_submitted
        }
        return Response(res, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def GetSignature(request, format=None):
    staff_id = request.user.id
    try:
        staff = MyUser.objects.get(id=staff_id)
    except MyUser.DoesNotExist:
        res = {
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Staff Doesn't Exist"
        }
        return Response(res, res["code"])
    
    resp = {
        "code": status.HTTP_200_OK,
        "signature": staff.staff_signatures.url if staff.staff_signatures.url else None
    }  
    return Response(resp, resp["code"])

class AllDocuments(APIView):
    def get(self, request):
        student = request.user
        docs = Document.objects.filter(student=student)
        data = [
            {
                "name": doc.name,
                "submitted_to": f"{doc.staff.first_name} {doc.staff.last_name}",
                "submitted_by": f"{doc.student.first_name} {doc.student.last_name}",
                "date_submitted": doc.date_submitted.date(),
                "file": doc.file.url,
                "in_review": doc.in_review,
                "signed": doc.signed
            }
            for doc in docs
        ]
        return Response(data, status=200)       

# class Signature(APIView):
#     def get(self, request):
#         bursar = request.user
#         signature = {
#             "signature": bursar.signature.url if bursar.signature.url else None
#         }
#         return Response(signature, status=status.HTTP_200_OK)
 
    
# class AllBursarDocs(APIView):
#     def get(self, request):
#         bursar = request.user
#         bur = Document.objects.filter(staff=bursar)
#         data = [
#             {
#                 "name": doc.name,
#                 "submitted_to": f"{doc.staff.first_name} {doc.staff.last_name}",
#                 "file": doc.file.url,
#                 "in_review": doc.in_review,
#                 "signed": doc.signed
#             }
#             for doc in bur
#         ]
#         return Response(data, status=200)

# class SignUpBursar(APIView):
#     def post(self, request, format=None):
#         serializer = BursarSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SignInBursar(APIView):
#     def post(self, request, format=None):
#         staff_number = request.data["staff_number"]
#         password = request.data["password"]

#         bursar = authenticate(request, staff_number=staff_number, password=password)
#         if bursar is not None:
#             login(request, bursar)
#             token, _ = Token.objects.get_or_create(user=bursar)
#             return Response({"token": token.key})
#         else:
#             return Response({"message": "Invalid credentials"}, status=401)
            
        
class AllBursars(APIView):
    def get(request, format=None):
        bursar = MyUser.objects.filter(is_bursar=True)
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
        

    
# class BursarLogin(APIView):
#     def post(self, request, format=None):
#         data = request.data
#         bursar = Bursar.objects.filter(staff_number=data["staff_number"]).first()
#         if not bursar:
#             resp = {
#                 "code":404,
#                 "message": "Staff Number not Correct"
#             }
#             return Response(resp, status=status.HTTP_404_NOT_FOUND)
    
# class GetAllSIBD(APIView): # SIBD = STUDENTS IN BURSAR'S DEPARTMENT
#     permission_classes=[IsStudent,]

#     # Cache page for the requested url for 1 hr
#     @method_decorator(cache_page(60*60))
#     def get(self, request):
#         dept = request.user.department.id
#         try:
#             bursar_dept = Bursar.objects.get(department=dept)
#             students = Student.objects.filter(department=bursar_dept.id)
#             student_data = [jsonify_student(student) for student in students]
#             data = {
#                 "student_data": student_data
#             }
#             return Response(data, status=status.HTTP_200_OK)
#         except Department.DoesNotExist:
#             return Response({"error": "Department not found."},
#                             status=status.HTTP_404_NOT_FOUND)
#         except Student.DoesNotExist:
#             return Response({"error": "No students found in the department."},
#                             status=status.HTTP_404_NOT_FOUND)
        