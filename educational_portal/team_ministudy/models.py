from django.db import models

# Create your models here.

class NewInstitution(models.Model):
    institute_id = models.BigAutoField(primary_key=True)
    institute_name = models.CharField(max_length=155)
    institute_email = models.EmailField(unique=True)
    institute_contact = models.CharField(max_length=15)
    institute_logo = models.ImageField(upload_to='institution_logos/')
    institute_domain = models.CharField(max_length=155, unique=True)

    def __str__(self):
        return f"{self.institute_name} - {self.institute_email}"

    class Meta:
        db_table = 'NewInstitution'
