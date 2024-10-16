from django.db import models
from adminside.models import *

# Create your models here.

class NewInstitution(models.Model):
    institute_id = models.BigAutoField(primary_key=True)
    institute_name = models.CharField(max_length=155)
    institute_email = models.EmailField(unique=True)
    institute_contact = models.CharField(max_length=15)
    institute_lock = models.BooleanField(default=False, null=True, blank=True)
    institute_joining_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    institute_logo = models.ImageField(upload_to='institution_logos/')
    institute_domain = models.CharField(max_length=155, unique=True)

    def __str__(self):
        return f"{self.institute_name} - {self.institute_email}"

    class Meta:
        db_table = 'NewInstitution'

class MinistudyPayment(models.Model):
    ministudypay_id = models.BigAutoField(primary_key=True)
    ministudypay_amount = models.IntegerField()
    ministudypay_paid = models.BooleanField(default=False)                                                               
    ministudypay_student_id = models.ForeignKey(Students, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ministudypay_amount} - {self.ministudypay_student_id.stud_name}"

    class Meta:
        db_table = 'MinistudyPayment'