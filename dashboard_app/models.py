from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_of_appointment = models.DateTimeField()

    def __str__(self):
        return str(self.day_of_appointment)


class Query(models.Model):
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    asked_On = models.DateTimeField(auto_now_add=True, blank=True)
    question = models.TextField()
    replied = models.BooleanField(default=False)

    def __str__(self):
        return self.question


class Answer(models.Model):
    replied_by = models.ForeignKey(User, on_delete=models.CASCADE)
    replied_to = models.ForeignKey(Query, on_delete=models.CASCADE)
    replied_on = models.DateTimeField(auto_now_add=True, blank=True)
    reply = models.TextField()
