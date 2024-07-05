from django import forms
from adminside.models import *

class update_form(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['stud_name', 'stud_lastname', 'stud_email', 'stud_username', 'stud_address']

class update_test_answer(forms.ModelForm):
    class Meta:
        model = Test_submission
        fields = "__all__"

class student_inquiries(forms.ModelForm):
    class Meta:
        model = Inquiries
        fields = "__all__"