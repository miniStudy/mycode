from django import forms
from adminside.models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget



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




class doubts_form(forms.ModelForm):
    doubt_doubt = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Doubt_section
        fields = "__all__"    



class solution_form(forms.ModelForm):
    solution = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Doubt_solution
        fields = "__all__"        