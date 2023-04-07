from django.db import models
from users.models import Employee


class Vacations(models.Model):
    comments = models.TextField(null=True)
    requests_date = models.DateTimeField(auto_now=True)
    date_of_begin = models.DateField()
    date_of_end = models.DateField()
    count_of_vacations = models.IntegerField(default=0)
    send_to_all = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)

    def __str__(self) -> str:
        return self.employee