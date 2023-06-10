from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Doctor(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    specialty = models.CharField(max_length=50)
    registered = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        unique_together = ('firstname', 'lastname',)
        ordering = ['-registered']

    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname}"


class Patient(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    # Add 42000 to it in views.py
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    join_time = models.DateTimeField(default=timezone.now)
    appoint_time = models.DateTimeField()
    doctor = models.ForeignKey(Doctor,
                               on_delete=models.CASCADE,
                               related_name='waitlist_patients')

    objects = models.Manager()
    patient_no = models.IntegerField(unique=True)

    class Meta:
        unique_together = ('firstname', 'lastname',)
        ordering = ['join_time']

    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname}"
