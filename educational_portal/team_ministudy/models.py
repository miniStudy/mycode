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
    institute_logo_icon = models.ImageField(upload_to='institution_logos/')
    institute_domain = models.CharField(max_length=155, unique=True)
    institute_admin_app = models.TextField(null=True, blank=True)
    institute_student_app = models.TextField(null=True, blank=True)
    institute_teacher_app = models.TextField(null=True, blank=True)
    institute_parent_app = models.TextField(null=True, blank=True)
    institute_admin_app_version = models.CharField(max_length=20, null=True, blank=True)
    institute_student_app_version = models.CharField(max_length=20, null=True, blank=True)
    institute_teacher_app_version = models.CharField(max_length=20, null=True, blank=True)
    institute_parent_app_version = models.CharField(max_length=20, null=True, blank=True)

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


class suggestions_improvements(models.Model):
    class user_option(models.TextChoices):
        Admin = 'Admin','Admin'
        Teacher = 'Teacher','Teacher'
        Student = 'Student','Student'
        Parent = 'Parent','Parent'

    si_id = models.BigAutoField(primary_key=True)
    si_user_name = models.CharField(max_length=55)
    si_user = models.CharField(choices=user_option.choices, max_length=15)
    si_suggestion = models.TextField()
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.si_user_name}"

    class Meta:
        db_table = 'suggestions_improvements'


class Distributor(models.Model):
    distributer_id = models.BigAutoField(primary_key=True)
    distributer_name = models.CharField(max_length=155)
    distributer_number = models.CharField(max_length=15)
    distributer_email = models.EmailField(unique=True)
    distributer_password = models.CharField(max_length=155, default='12345678')
    distributer_document = models.FileField(upload_to ='uploads/')
    distributer_address = models.TextField()


    def __str__(self):
        return f"{self.distributer_name}"

    class Meta:
        db_table = 'Distributor'

class Distributer_Institute(models.Model):
    distributer_institute_id = models.BigAutoField(primary_key=True)
    distributer_institute_distributer_id = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    distributer_institute_date = models.DateField(auto_now_add=True)
    domain_name = models.CharField(blank=True,null=True,max_length=100)

    def __str__(self):
        return f"{self.distributer_institute_distributer_id.distributer_name} - {self.distributer_institute_date}"

    class Meta:
        db_table = 'Distributer_Institute'

class Distributer_Payment(models.Model):
    distributer_payment_id = models.BigAutoField(primary_key=True)
    distributer_payment_distributer_id = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    distributer_payment = models.IntegerField()
    distributer_payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.distributer_payment_distributer_id.distributer_name} - {self.distributer_payment}"

    class Meta:
        db_table = 'Distributer_Payment'
