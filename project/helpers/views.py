from rest_framework.views import APIView
from app.models import Student

def jsonify_student(student:Student):
    return {
        "first_name": student.first_name,
        "middle_name": student.middle_name,
        "last_name": student.last_name,
        "department": student.department.department,
        "passport": str(student.passport),
        "contact": student.contact
    }
    