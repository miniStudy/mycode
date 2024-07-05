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
from studentside import views as studentview
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ---------------------------studentside auth-------------------------
    
    path('', studentview.student_home, name='Student_home'),
    path('Student_Login/', studentview.student_login_page, name='Student_Login'),
    path('Student_login_handle/',studentview.student_login_handle,name='Student_login_handle'),
    path('Student_Forgot_Password/', studentview.student_Forgot_Password, name='Student_Forgot_Password'),
    path('Student_handle_forgot_password/',studentview.student_handle_forgot_password, name='Student_handle_forgot_password'),
    path('Student_Set_New_Password/',studentview.student_Set_New_Password, name='Student_Set_New_Password'),
    path('Student_handle_set_new_password/',studentview.student_handle_set_new_password, name='Student_handle_set_new_password'),
    path('Student_logout/',studentview.student_logout, name = 'Student_logout' ),
    path('Student_InfoUpdate/',studentview.student_info_update, name = 'Student_InfoUpdate' ),

    path('Student_Announcement/',studentview.student_announcement, name = 'Student_Announcement' ),
    path('Student_Subjects/', studentview.show_subjects, name='Student_Subjects'),
    path('Student_Chepters/', studentview.show_chepters, name = 'Student_Chepters'),
    path('Student_Materials/', studentview.show_materials, name = 'Student_Materials'),
    path('Student_Timetable/', studentview.show_timetables, name = 'Student_Timetable'),
    path('Student_Attendence/', studentview.show_attendence, name = 'Student_Attendence'),
    path('Student_Event/', studentview.show_event, name = 'Student_Event'),
    path('Student_Test/', studentview.show_test, name = 'Student_Test'),
    path('Student_Test_Q/<int:id>/', studentview.show_test_questions, name='Student_Test_Q'),
    path('Student_Syllabus/', studentview.show_syllabus, name='Student_Syllabus'),
    path('Student_Inquiries/', studentview.student_inquiries_data, name='Student_Inquiries'),
]