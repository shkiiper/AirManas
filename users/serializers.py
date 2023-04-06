from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class AddNewEmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password', 'birthday']

    def validate_email(self, email):
        if Employee.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email address is already in use.')
        return email

    def create(self, validated_data):
        validated_data.pop('username')
        validated_data.pop('email')
        validated_data.pop('password')
        employee = Employee.objects.create(**validated_data)
        return employee
