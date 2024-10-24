from adminside.models import *
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class attendence_form(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        
class teacher_materials_form(forms.ModelForm):
    class Meta:
        model = Chepterwise_material
        fields = '__all__'
        
class teacher_update_form(forms.ModelForm):
    class Meta:
        model = Faculties
        fields = ['fac_name', 'fac_email', 'fac_number', 'fac_address', 'fac_profile']

class teacher_solution_form(forms.ModelForm):
    solution = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Doubt_solution
        fields = "__all__"   

class teacher_todaylearn_form(forms.ModelForm):
    class Meta:
        model = Today_Teaching
        fields = "__all__" 
                