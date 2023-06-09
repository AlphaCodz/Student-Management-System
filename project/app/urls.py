from django.urls import path
from .views import (GetAllStudents, StudentBiodata, RegStudent, SignUpBursar, 
                    StudentLogin, BursarLogin, BursarDocumentsView, SubmitDocuments,
                    AllDocuments, AllBursars, StudentPayment, DocumentSignView)
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
    path("my/docs", BursarDocumentsView.as_view(), name="my-docs"),
    path("submit/document/<int:staff_id>", SubmitDocuments.as_view(), name="submit-doc"),
    # path("signin/bursar", SignInBursar.as_view(), name="signin-bursar"),
    path("all/bursar", AllBursars.as_view(), name="get-bursars"),
    path("sign_doc/<int:document_id>",DocumentSignView.as_view(), name="sign" ),
    # path("my/students", GetAllSIBD.as_view(), name="all-students"),
    # path('bursar/documents/create/<int:staff_id>', SubmitDocuments.as_view(), name="docs"),
    # path('signature', Signature.as_view(), name="signature"),
    path('all/documents', AllDocuments.as_view(), name="docs"),
    path('my-signature', views.GetSignature, name="signature"),
    path('validate_payment', StudentPayment.as_view(), name="payment")
    # path('staff/docs', AllBursarDocs.as_view(), name="bursar-doc")
]