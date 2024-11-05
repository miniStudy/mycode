from django import forms  
from team_ministudy.models import *  


class Institute_Form(forms.ModelForm):  
    class Meta:  
        model = NewInstitution  
        fields = "__all__"

class Ministudy_Payment_Form(forms.ModelForm):  
    class Meta:  
        model = MinistudyPayment  
        fields = "__all__"

class suggestions_improvements_Form(forms.ModelForm):  
    class Meta:  
        model = suggestions_improvements  
        fields = "__all__"