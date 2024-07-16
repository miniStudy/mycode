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
    path('teacher_events', teacherview.teacher_events, name='teacher_events'),
    path('teacher_test', teacherview.teacher_test, name='teacher_test'),
    path('teacher_materials', teacherview.teacher_materials, name='teacher_materials'),
    path('teacher_timetable', teacherview.teacher_timetable, name='teacher_timetable'),
    path('teacher_attendance', teacherview.teacher_attendance, name='teacher_attendance'),
    path('teacher_syllabus', teacherview.teacher_syllabus, name='teacher_syllabus'),
    path('teacher_announcement', teacherview.teacher_announcement, name='teacher_announcement'),
    path('teacher_doubts', teacherview.teacher_doubts, name='teacher_doubts'),
    path('teacher_logout', teacherview.teacher_announcement, name='teacher_logout'),

]