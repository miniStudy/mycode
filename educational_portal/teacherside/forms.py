from adminside.models import *
from django import forms

class attendence_form(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        
class teacher_materials_form(forms.ModelForm):
    class Meta:
        model = Chepterwise_material
        fields = '__all__'
        