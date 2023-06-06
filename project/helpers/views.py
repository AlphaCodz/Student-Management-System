from rest_framework.views import APIView
from app.models import MyUser

def jsonify_student(student:MyUser):
    return {
        "id":student.id,
        "first_name": student.first_name,
        "middle_name": student.middle_name,
        "last_name": student.last_name,
        "email":student.email,
        "contact": student.contact,
        "date_of_birth": student.date_of_birth,
        "matric_no": student.matric_number,
        "student_address": student.address,
        "department": str(student.department),
        "next_of_kin": student.nok_name,
        "relationship_with_next_of_kin": student.relationship,
        "next_of_kin_contact": student.nok_contact,
        "passport": str(student.passport),
        "is_paid": student.is_paid
    }
    
def jsonify_bursar(bursar:MyUser):
    return {
        "id":bursar.id,
        "first_name": bursar.first_name,
        "last_name": bursar.last_name,
        "contact": bursar.contact,
        "date_of_birth": bursar.date_of_birth,
        "staff_number": bursar.staff_number,
        "staff_address": bursar.address,
        "department": str(bursar.department),
        "staff_passport": str(bursar.staff_passport),
        "staff_signature": bursar.staff_signatures.url
    }