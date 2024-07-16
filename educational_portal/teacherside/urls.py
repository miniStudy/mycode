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
<<<<<<< HEAD
    path('teacher_events', teacherview.teacher_events, name='teacher_events'),
    path('teacher_test', teacherview.teacher_test, name='teacher_test'),
    path('teacher_materials', teacherview.teacher_materials, name='teacher_materials'),
    path('teacher_timetable', teacherview.teacher_timetable, name='teacher_timetable'),
    path('teacher_attendance', teacherview.teacher_attendance, name='teacher_attendance'),
    path('teacher_syllabus', teacherview.teacher_syllabus, name='teacher_syllabus'),
    path('teacher_announcement', teacherview.teacher_announcement, name='teacher_announcement'),
    path('teacher_doubts', teacherview.teacher_doubts, name='teacher_doubts'),
    path('teacher_logout', teacherview.teacher_announcement, name='teacher_logout'),

=======

    # <==============Teacher Authencation==================>
    path('teacher_login/', teacherview.teacher_login_page, name='teacher_login'),
    path('teacher_login_handle/',teacherview.teacher_login_handle,name='teacher_login_handle'),
    path('teacher_forget_password/', teacherview.teacher_forget_password, name='teacher_forget_password'),
    path('teacher_handle_forget_password/',teacherview.teacher_handle_forget_password, name='teacher_handle_forget_password'),
    path('teacher_set_new_password/',teacherview.teacher_set_new_password, name='teacher_set_new_password'),
    path('teacher_handle_set_new_password/',teacherview.teacher_handle_set_new_password, name='teacher_handle_set_new_password'),
    path('teacher_logout/',teacherview.teacher_logout_page, name = 'teacher_logout' ),
    # path('Student_InfoUpdate/',studentview.student_info_update, name = 'Student_InfoUpdate' ),path
>>>>>>> 16f77c56a53f53566ac4d75f5d7e84ccb3cfa7bb
]