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

    # <==============Teacher Authencation==================>
    path('teacher_login/', teacherview.teacher_login_page, name='teacher_login'),
    path('teacher_login_handle/',teacherview.teacher_login_handle,name='teacher_login_handle'),
    path('teacher_forget_password/', teacherview.teacher_forget_password, name='teacher_forget_password'),
    path('teacher_handle_forget_password/',teacherview.teacher_handle_forget_password, name='teacher_handle_forget_password'),
    path('teacher_set_new_password/',teacherview.teacher_set_new_password, name='teacher_set_new_password'),
    path('teacher_handle_set_new_password/',teacherview.teacher_handle_set_new_password, name='teacher_handle_set_new_password'),
    path('teacher_logout/',teacherview.teacher_logout_page, name = 'teacher_logout' ),
    # path('Student_InfoUpdate/',studentview.student_info_update, name = 'Student_InfoUpdate' ),path
]