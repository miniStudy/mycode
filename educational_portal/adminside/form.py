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


class chepter_form(forms.ModelForm):  
    class Meta:  
        model = Chepter  
        fields = "__all__"  


class student_form(forms.ModelForm):  
    class Meta:  
        model = Students  
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


class tests_form(forms.ModelForm):
    class Meta:
        model = Chepterwise_test
        fields = "__all__"



class TestQuestionsAnswerForm(forms.ModelForm):
    tq_question = forms.CharField(widget=SummernoteWidget())
    tq_answer = forms.CharField(widget=SummernoteWidget())
    class Meta:
        model = Test_questions_answer
        fields = "__all__"

class pack_form(forms.ModelForm):
    class Meta:
        model = Packs
        fields = "__all__"

class batch_form(forms.ModelForm):
    class Meta:
        model = Batches
        fields = "__all__"


class Cheque_Collection_form(forms.ModelForm):
    class Meta:
        model = Cheque_Collection
        fields = "__all__"

class faculty_access_form(forms.ModelForm):
    class Meta:
        model = Faculty_Access
        fields = "__all__"



class fees_collection_form(forms.ModelForm):
    class Meta:
        model = Fees_Collection
        fields = "__all__"        