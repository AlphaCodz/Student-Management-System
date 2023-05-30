from django.urls import path
from .views import RegStudent, SignUpBursar, StudentLogin, GetAllSIBD, StudentBiodata, GetAllStudents, AllBursars, SubmitDocuments
from . import views

urlpatterns = [
    path("register/student", RegStudent.as_view(), name="register-student"),
    path("all/student", GetAllStudents.as_view(), name="get-students"),
    path("login/student", StudentLogin.as_view(), name="login"),
    
    # Biodata
    path("biodata/<int:id>", StudentBiodata.as_view(), name="biodata"),
    
    # Bursars
    path("register/bursar", SignUpBursar.as_view(), name="reg-bursar"),
    path("all/bursar", AllBursars.as_view(), name="get-bursars"),
    path("my/students", GetAllSIBD.as_view(), name="all-students"),
    path('bursar/documents/create/<int:staff_id>', SubmitDocuments.as_view(), name="docs")
]