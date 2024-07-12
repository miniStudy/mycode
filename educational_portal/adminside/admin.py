from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

class Test_questions_answer_admin(SummernoteModelAdmin):
    summernote_fields = ('tq_question','tq_answer')

class Doubt_section_admin(SummernoteModelAdmin):
    summernote_fields = ('doubt_doubt')

class Doubt_solution_admin(SummernoteModelAdmin):
    summernote_fields = ('solution')

# Register your models here.
admin.site.register(Boards)
admin.site.register(AdminData)
admin.site.register(Students)
admin.site.register(Subject)
admin.site.register(Chepter)
admin.site.register(Chepterwise_material)
admin.site.register(Announcements)
admin.site.register(Std)
admin.site.register(Batches)
admin.site.register(Packs)
admin.site.register(Faculties)
admin.site.register(Timetable)
admin.site.register(Attendance)
admin.site.register(Event)
admin.site.register(Chepterwise_test)
admin.site.register(Test_questions_answer,Test_questions_answer_admin)
admin.site.register(Test_attempted_users)
admin.site.register(Test_submission)
admin.site.register(Event_Image)
admin.site.register(Inquiries)
admin.site.register(Doubt_section, Doubt_section_admin)
admin.site.register(Doubt_solution,Doubt_solution_admin)