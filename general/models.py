from django.db import models


# Create your models here.
class Documents(models.Model):
    name = models.CharField(max_length=150)
    data_vidachi = models.DateField(auto_now_add=True)
    document = models.FileField(upload_to="documents")
    description = models.CharField(max_length=500, null=True)

    def __str__(self) -> str:
        return self.name


class Trainings(models.Model):
    name = models.CharField(max_length=100)
    date_of_begin = models.DateField()
    date_of_end = models.DateField(null=True)
    status = models.BooleanField(default=False)
    description = models.CharField(max_length=500, null=True)

    def __str__(self) -> str:
        return self.name
