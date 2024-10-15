from django import forms  
from team_ministudy.models import *  


class Institute_Form(forms.ModelForm):  
    class Meta:  
        model = NewInstitution  
        fields = "__all__"