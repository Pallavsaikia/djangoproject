from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    day_of_appointment = models.DateTimeField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    requested_on = models.DateTimeField(auto_now_add=True)
    appointed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.requested_on)


class Query(models.Model):
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    asked_On = models.DateTimeField(auto_now_add=True)
    question = models.TextField()
    replied = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.question

    @property
    def answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    replied_by = models.ForeignKey(User, on_delete=models.CASCADE)
    replied_to = models.ForeignKey(Query, on_delete=models.CASCADE)
    replied_on = models.DateTimeField(auto_now_add=True)
    reply = models.TextField()

