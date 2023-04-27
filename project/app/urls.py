from django.urls import path
from .views import RegStudent
from . import views

urlpatterns = [
    path("register/student", RegStudent.as_view(), name="register-student"),
    path("all/student", views.GetAllStudents, name="get-students"),
    
    # Biodata
    path("biodata/<int:id>", views.StudentBiodata, name="biodata")
]
