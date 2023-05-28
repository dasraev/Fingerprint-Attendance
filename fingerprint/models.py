from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    fingerprint = models.ImageField(upload_to='fingerprints/')
    def __str__(self):
        return self.user.first_name

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='attendances')
    clock_in_time = models.DateTimeField(null=True, blank=True)
    clock_out_time = models.DateTimeField(null=True, blank=True)