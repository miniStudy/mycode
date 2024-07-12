from django import forms  
from adminside.models import *  
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


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


class faculty_form(forms.ModelForm):  
    class Meta:  
        model = Faculties  
        fields = "__all__"



class timetable_form(forms.ModelForm):  
    class Meta:  
        model = Timetable  
        fields = "__all__"        


class event_form(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"          


class TestQuestionsAnswerForm(forms.ModelForm):
    tq_question = forms.CharField(widget=SummernoteWidget())
    tq_answer = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Test_questions_answer
        fields = "__all__"
