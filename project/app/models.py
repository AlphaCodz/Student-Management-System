from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import string, random as rand
from rest_framework.response import Response

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class Department(models.Model):
    DEPARTMENT = (
        ("Computer Science", "Computer Science"),
        ("Hospitality Management & Technology", "Hospitality Management & Technology"),
        ("Accounting", "Accounting"),
        ("Office Technology Management", "Office Technology Management"),
        ("Mass Communication", "Mass Communication"),
        ("Marketing", "Marketing"),
        ("Civil Engineering", "Civil Engineering"),
        ("Mechanical Engineering", "Mechanical Engineering"),
        ("Electrical Engineering", "Electrical Engineering"),
        ("Mathematics", "Mathematics"),
        ("Statistics", "Statistics"),
        ("Computer Engineering", "Computer Engineering")
    )
    
    department=models.CharField(max_length=70, choices=DEPARTMENT)

class Student(AbstractUser):
    NEXT_OF_KIN = (
        ("Father", "Father"),
        ("Mother", "Mother"),
        ("Friend", "Friend"),
        ("Other", "Other")
    )
    first_name = models.CharField(max_length=250, null=True)
    middle_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250, null=True)
    matric_number = models.CharField(max_length=30)
    address=models.CharField(max_length=250)
    contact=models.BigIntegerField()
    username = models.CharField(max_length=5, null=True)
    email= models.EmailField(unique=True)
    date_of_birth = models.DateField()
    passport = models.ImageField(upload_to="media/student_passport/", null=True)
    
    # Student Docs
    biodata = models.FileField(upload_to="media/documents/", null=True)
    
    # NOK means Next_Of_Kin
    nok_name = models.CharField(max_length=250, null=True)
    relationship = models.CharField(max_length=6, choices=NEXT_OF_KIN, null=True)
    nok_contact=models.BigIntegerField(null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    
    # password
    password= models.CharField(max_length=300, null=True)
    
    
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = ''.join(rand.choices(string.ascii_lowercase + string.digits, k=5))
        if not self.matric_number:
            self.matric_number = 'P/ND/22/3210'+''.join(rand.choices(string.digits, k=3))
        if not self.password:
            self.password = self.last_name
            self.set_password(self.last_name)
        else:
            self.password = self.last_name
            self.set_password(self.last_name)
        super(Student, self).save(*args, **kwargs)

class Bursar(models.Model):
    student = models.ManyToManyField(Student)
    first_name=models.CharField(max_length=250)
    last_name=models.CharField(max_length=250)
    staff_number = models.CharField(max_length=30)
    contact=models.BigIntegerField()
    email= models.EmailField(unique=True)
    passport=models.ImageField(upload_to="media/staff_passport/", null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # FROM WHAT DEPARTMENT
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name
    
class SchoolOfficer(models.Model):
    SCHOOL = (
        ("TECHNOLOGY", "TECHNOLOGY"),
        ("ARTS", "ARTS"),
        ("ENGINEERING", "ENGINEERING"),
    )
    student=models.ManyToManyField(Student, related_name="student")
    first_name=models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    staff_number = models.CharField(max_length=50)
    school = models.CharField(max_length=20, choices=SCHOOL)
    
    def __str__(self):
        return f"Staff: {self.staff_number}"
    

class Semester(models.Model):
    SEMESTER = (
        ("FIRST SEMESTER", "FIRST SEMESTER"),
        ("SECOND SEMESTER", "SECOND_SEMESTER")
    )
    
    ACADEMIC_YEAR = (
        ("2018/2019", "2018/2019"),
        ("2019/2020", "2019/2020"),
        ("2020/2021", "2020/2021"),
        ("2021/2022", "2021/2022"),
        ("2022/2023", "2022/2023")
    )
    semester = models.CharField(max_length=17, choices=SEMESTER)
    academic_year = models.CharField(max_length=9, choices=ACADEMIC_YEAR)
    
    def __str__(self):
        return f"{self.semester} | Year {self.academic_year}"
    
class Course(models.Model):
    department = models.ManyToManyField(Department)
    student= models.ManyToManyField(Student)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True)
    code = models.CharField(max_length=10, null=True)
    
    def __str__(self):
        return self.title
    
    
        
    
    