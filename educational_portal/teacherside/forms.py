from adminside.models import Attendance
from django import forms

class attendence_form(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
        
