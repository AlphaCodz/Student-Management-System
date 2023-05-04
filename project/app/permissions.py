from .models import Student, Bursar
from rest_framework.permissions import BasePermission

class IsBursar(BasePermission):
    def has_permission(self, request, view):
        email = request.user.email
        bursar = Bursar.objects.filter(email=email).exists()
        return bursar
    
class IsStudent(BasePermission):
    def has_permission(self, request, view):
        email = request.user.email
        student = Student.objects.filter(email=email).exists()
        return student
