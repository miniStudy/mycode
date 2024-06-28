from django import forms
from adminside.models import Students

class update_form(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['stud_name', 'stud_lastname', 'stud_email', 'stud_username', 'stud_address']