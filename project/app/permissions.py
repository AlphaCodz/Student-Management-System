from .models import MyUser
from rest_framework.permissions import BasePermission

class IsBursar(BasePermission):
    def has_permission(self, request, view):
        email = request.user.email
        bursar = MyUser.objects.filter(is_bursar=True)
        return bursar
    
class IsStudent(BasePermission):
    def has_permission(self, request, view):
        email = request.user.email
        student = MyUser.objects.filter(is_student=True)
        return student
