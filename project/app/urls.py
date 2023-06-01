from django.urls import path
from .views import GetAllStudents, StudentBiodata, RegStudent, SignUpBursar, StudentLogin, BursarLogin
from . import views

urlpatterns = [
    path("register/student", RegStudent.as_view(), name="register-student"),
    path("all/student", GetAllStudents.as_view(), name="get-students"),
    path("login/student", StudentLogin.as_view(), name="login"),
    
    # # Biodata
    path("biodata/<int:id>", StudentBiodata.as_view(), name="biodata"),
    
    # # Bursars
    path("register/bursar", SignUpBursar.as_view(), name="reg-bursar"),
    path("login/bursar", BursarLogin.as_view(), name="bursar-login"),
    # path("signin/bursar", SignInBursar.as_view(), name="signin-bursar"),
    # path("all/bursar", AllBursars.as_view(), name="get-bursars"),
    # path("my/students", GetAllSIBD.as_view(), name="all-students"),
    # path('bursar/documents/create/<int:staff_id>', SubmitDocuments.as_view(), name="docs"),
    # path('signature', Signature.as_view(), name="signature"),
    # path('all/documents', AllDocuments.as_view(), name="docs"),
    # path('staff/docs', AllBursarDocs.as_view(), name="bursar-doc")
]