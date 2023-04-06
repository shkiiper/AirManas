from django.db import models
from django.contrib.auth.models import AbstractUser
from general.models import Documents, Trainings


# Create your models here.
class Doljnost(models.Model):
    doljnost = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.doljnost


class Employee(AbstractUser):
    date_joined = models.DateField(auto_now_add=True, null=True)
    birthday = models.DateField(null=True)
    phone = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    days_to_trainings = models.IntegerField(default=30)
    available_vacation = models.IntegerField(default=0)
    days_used = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    doljnost = models.ForeignKey(Doljnost, on_delete=models.PROTECT, null=True)
    documents = models.ForeignKey(Documents, on_delete=models.PROTECT, null=True)
    # trainings = models.ForeignKey(Trainings, on_delete=models.PROTECT, null=True)
