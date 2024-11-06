"""educational_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from teacherside import views as teacherview
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', teacherview.teacher_home, name='teacher_home'),
    path('teacher_events/', teacherview.teacher_events, name='teacher_events'),
    path('teacher_timetable/', teacherview.teacher_timetable, name='teacher_timetable'),
    path('teacher_attendance/', teacherview.teacher_attendance, name='teacher_attendance'),
    path('teacher_edit_attendance/', teacherview.teacher_edit_attendance, name='teacher_edit_attendance'),
    path('edit_handle_attendance/', teacherview.edit_handle_attendance, name='edit_handle_attendance'),

    # <==============Teacher syllabus==================>
    path('teacher_syllabus/', teacherview.teacher_syllabus, name='teacher_syllabus'),
    path('insert_update_syllabus/', teacherview.insert_update_syllabus, name='insert_update_syllabus'),


    # <==============teacher doubts==================>
    path('teacher_doubts/', teacherview.teacher_doubts, name='teacher_doubts'),
    path('teacher_solution_verify/', teacherview.show_teacher_solution_verified, name='teacher_solution_verify'),
    path('teacher_add_solution/', teacherview.teacher_add_solution_function, name='teacher_add_solution'),
    path('teacher_edit_solution/', teacherview.teacher_edit_solution_function, name='teacher_edit_solution'),

    # <==============Insert Update==================>
    path('insert_update_attendance/', teacherview.insert_update_attendance, name='insert_update_attendance'),
    path('handle_attendance/', teacherview.handle_attendance, name='handle_attendance'),

    # <==============Teacher Authencation==================>
    path('teacher_login/', teacherview.teacher_login_page, name='teacher_login'),
    path('teacher_login_handle/',teacherview.teacher_login_handle,name='teacher_login_handle'),
    path('teacher_forget_password/', teacherview.teacher_forget_password, name='teacher_forget_password'),
    path('teacher_handle_forget_password/',teacherview.teacher_handle_forget_password, name='teacher_handle_forget_password'),
    path('teacher_set_new_password/',teacherview.teacher_set_new_password, name='teacher_set_new_password'),
    path('teacher_handle_set_new_password/',teacherview.teacher_handle_set_new_password, name='teacher_handle_set_new_password'),
    path('teacher_logout/',teacherview.teacher_logout_page, name = 'teacher_logout' ),
    
    # <==============Teacher Profile==================>
    path('teacher_profile/', teacherview.teacher_view_profile, name='teacher_profile'),
    path('teacher_profile_update/', teacherview.teacher_profile_update, name='teacher_profile_update'),

    # ==========================Test===================================================
    path('teacher_tests/', teacherview.teacher_test, name='teacher_tests'),
    path('teacher_insert_update_tests/', teacherview.insert_update_tests, name='teacher_insert_update_tests'),
    path('teacher_delete_tests/', teacherview.delete_tests, name='teacher_delete_tests'),
    path('show_question_paper/', teacherview.show_question_paper, name='show_question_paper'),

    path('show_test_questions_teacher/', teacherview.show_test_questions_teacher, name='show_test_questions_teacher'),
    path('insert_update_test_question_teacher/', teacherview.insert_update_test_questions_teacher, name='insert_update_test_question_teacher'),
    path('view_attemp_students/', teacherview.view_attemp_students, name='view_attemp_students'),
    path('delete_test_question_answer_teacher/',teacherview.delete_test_question_answer_teacher,name="delete_test_question_answer_teacher"),

    path('insert_offline_marks/', teacherview.teacher_insert_offline_marks, name='insert_offline_marks'),
    path('save_offline_marks/', teacherview.teacher_save_offline_marks, name='save_offline_marks'),
    
    # ===============================announcements============================================
    path('teacher_announcement/', teacherview.teacher_announcement, name='teacher_announcement'),
    path('announcements_insert_update_teacher/', teacherview.announcements_insert_update_teacher, name='announcements_insert_update_teacher'),
    path('announcements_delete_teacher/', teacherview.announcements_delete_teacher, name='announcements_delete_teacher'),


    # =================================materials==================================================

    path('teacher_materials/', teacherview.teacher_materials, name='teacher_materials'),
    path('teacher_insert_update_materials/', teacherview.teacher_insert_update_materials, name='teacher_insert_update_materials'),
    path('materials_delete_teacher/', teacherview.materials_delete_teacher, name='materials_delete_teacher'),

    # =================================Report-Card==================================================
    path('report_card/', teacherview.report_card_show, name='report_card'),


    # =================================Today's Learning==================================================
    path('today_learning/', teacherview.today_learning_show, name='today_learning'),
    path('today_learning_delete/', teacherview.today_learning_delete, name='today_learning_delete'),
    path('today_learning_insert_update/', teacherview.today_learning_insert_update, name='today_learning_insert_update'),


    path('teacher_export_data/',teacherview.teacher_export_data, name='teacher_export_data'),

    path('teacher_insert_suggestions/',teacherview.insert_suggestions_function, name='teacher_insert_suggestions'),
]