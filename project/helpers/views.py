from rest_framework.views import APIView
from app.models import Student

def jsonify_student(student:Student):
    return {
        "id":student.id,
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
    }
    