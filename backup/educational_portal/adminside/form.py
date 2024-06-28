from django import forms  
from adminside.models import *  

class brd_form(forms.ModelForm):  
    class Meta:  
        model = Boards  
        fields = "__all__"


class std_form(forms.ModelForm):  
    class Meta:  
        model = Std  
        fields = "__all__"


class announcement_form(forms.ModelForm):  
    class Meta:  
        model = Announcements  
        fields = "__all__"        


class subject_form(forms.ModelForm):  
    class Meta:  
        model = Subject  
        fields = "__all__"             