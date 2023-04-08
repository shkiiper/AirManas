from django.utils.translation import gettext as _
from rest_framework import serializers
from .models import Employee, Vacations


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'username', 'email', 'date_joined', 'birthday', 'phone', 'image',
                  'days_to_trainings', 'available_vacation', 'days_used', 'status', 'doljnost', 'documents')


class VacationsSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = Vacations
        fields = (
            'id', 'comments', 'requests_date', 'date_of_begin', 'date_of_end', 'count_of_vacations', 'status',
            'employee',)


class CreateVacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacations
        fields = ('comments', 'date_of_begin', 'date_of_end')
