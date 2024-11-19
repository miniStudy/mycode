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

class distributor_form(forms.ModelForm):  
    class Meta:  
        model = Distributor  
        fields = "__all__"

class distributer_institute_form(forms.ModelForm):  
    class Meta:  
        model = Distributer_Institute  
        fields = "__all__"

class distributer_payment_form(forms.ModelForm):  
    class Meta:  
        model = Distributer_Payment 
        fields = "__all__"