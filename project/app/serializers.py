from rest_framework import serializers
from .models import Student, Bursar, Department

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=("first_name", "middle_name", "last_name", 
                "address", "contact", "email", "date_of_birth", "passport",
                "nok_name", "relationship", "nok_contact", "department", "password")
        
        def validate(self, attrs):
            email_exists = Student.objects.filter(email=request.data.get("email")).exists()
            if len(attrs["first_name"]) or len(attrs["last_name"]) < 1:
                raise serializers.ValidationError({"error":"Student's name cannot be less than 1 Character"})
            if email_exists:
                raise serializers.ValidationError({"error": "Sorry this email is taken"})
            if attrs["contact"] == attrs["nok_contact"]:
                raise serializers.ValidationError({"error": "Student and Next Of Kin's Contacts must NOT be the same"})
            return attrs
        
        def create(self, validated_data):
            department = validated_data.pop("department")
            last_name = validated_data.get("last_name", "")
            # password = last_name
            
            student = Student.objects.create(
                first_name = validated_data["first_name"],
                middle_name=validated_data["middle_name"],
                last_name=validated_data["last_name"],
                address= validated_data["address"],
                contact=validated_data["contact"],
                date_of_birth=validated_data["date_of_birth"],
                passport=validated_data["passport"],
                department=validated_data["department"],
                email=validated_data["email"],
                nok_name=validated_data["nok_name"],
                relationship=validated_data["relationship"],
                nok_contact=validated_data["nok_contact"],
                **validated_data
            )
            # if not password:
            #     password = last_name
            # student.set_password(raw_password=password)
            student.save()
            return student
        
class BursarSerializer(serializers.ModelSerializer):
    department_id = serializers.PrimaryKeyRelatedField(
        queryset = Department.objects.all(),
        source='department',
        write_only=True
    )
    class Meta:
        model = Bursar
        fields = ("first_name", "last_name", "staff_number", "contact", "email", "passport", "department_id", "address", "date_of_birth")
        
        def create(self, validated_data):
            department_id = validated_data.pop('department_id')
            department = Department.objects.get(id=department_id)
            staff = Bursar.objects.create(
                first_name=validated_data["first_name"],
                last_name = validated_data["last_name"],
                staff_number=validated_data["staff_number"],
                contact=validated_data["contact"],
                email=validated_data["email"],
                passport=validated_data["passport"],
                address=validated_data["address"],
                date_of_birth=validated_data["date_of_birth"],
                department=department,
                **validated_data
            )
            staff.save()
            return staff