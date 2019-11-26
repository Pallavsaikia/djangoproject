from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Appointment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    day_of_appointment = models.DateField()

    def __str__(self):
        return str(self.day_of_appointment)


class Query(models.Model):
    asked_by = models.OneToOneField(User, on_delete=models.CASCADE)
    asked_On = models.DateField()
    question = models.TextField()

    def __str__(self):
        return self.question


class Answer(models.Model):
    replied_by = models.OneToOneField(User, on_delete=models.CASCADE)
    replied_to = models.OneToOneField(Query, on_delete=models.CASCADE)
    replied_on = models.DateField()
    reply = models.TextField()
