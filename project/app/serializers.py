from rest_framework import serializers
from .models import Student, Bursar

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=("first_name", "middle_name", "last_name", 
                "address", "contact", "email", "date_of_birth", "passport",
                "nok_name", "relationship", "nok_contact", "department", "password")
        
        def validate(self, attrs):
            email_exists = Student.objects.filter(email=request.data.get("email")).exists()
            if len(attrs["first_name"]) or len(attrs["last_name"]) < 1:
                return serializers.ValidationError({"error":"Student's name cannot be less than 1 Character"})
            if email_exists:
                return serializers.ValidationError({"error": "Sorry this email is taken"})
            if attrs["contact"] == attrs["nok_contact"]:
                return serializers.ValidationError({"error": "Student and Next Of Kin's Contacts must NOT be the same"})
            return attrs
            
        
        def create(self, validated_data):
            department = validated_data.pop("department")
            student = Student.objects.create(
                first_name = validated_data["first_name"],
                middle_name=validated_data["middle_name"],
                last_name=validated_data["last_name"],
                address= validated_data["address"],
                contact=validated_data["contact"],
                date_of_birth=validated_data["date_of_birth"],
                passport=validated_data["passport"],
                nok_name=validated_data["nok_name"],
                relationship=validated_data["relationship"],
                nok_contact=validated_data["nok_contact"],
                **validated_data
            )
            student.set_password(raw_password=validated_data["password"])
            student.save()
            return student
        
class BursarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bursar,
        fields = "__all__"
        
        def create(self, validated_data):
            staff = Bursar.objects.create(
                student=validated_data["student"],
                first_name=validated_data["first_name"],
                last_name = validated_data["last_name"],
                staff_number=validated_data["staff_number"],
                contact=validated_data["contact"],
                email=validated_data["email"]
            )
            staff.save()
            return staff