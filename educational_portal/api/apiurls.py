



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
from api import views as apiviews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('get_boards/', apiviews.get_boards, name='get_boards'),
    path('api_update_boards/', apiviews.api_update_boards, name='api_update_boards'),
    path('delete_boards/', apiviews.delete_boards, name='delete_boards'),

    path('get_stds/', apiviews.get_stds, name='get_stds'),
    path('api_update_stds/', apiviews.api_update_stds, name='api_update_stds'),
    path('api_delete_stds/', apiviews.api_delete_stds, name='api_delete_stds'),
    
    path('api_subjects/', apiviews.api_subjects, name='api_subjects'),
    path('api_update_subjects/', apiviews.api_update_subjects, name='api_update_subjects'),
    path('api_delete_subjects/', apiviews.api_delete_subjects, name='api_delete_subjects'),

    path('api_chepters/', apiviews.api_chepters, name='api_chepters'),
    # path('insert_update_chepters/', apiviews.insert_update_chepters, name='insert_update_chepters'),
    path('api_delete_chepters/', apiviews.api_delete_chepters, name='api_delete_chepters'),

    path('api_faculties/', apiviews.api_faculties, name='api_faculties'),
    path('api_update_faculties/', apiviews.api_update_faculties, name='api_update_faculties'),
    path('api_delete_faculties/', apiviews.api_delete_faculties, name='api_delete_faculties'),

    path('api_batches/', apiviews.api_batches, name='api_batches'),
    path('api_update_batches/', apiviews.api_update_batches, name='api_update_batches'),
    path('api_delete_batches/', apiviews.api_delete_batches, name='api_delete_batches'),

    path('api_announcements/', apiviews.api_announcements, name='api_announcements'),
    path('api_update_announcements/', apiviews.api_update_announcements, name='api_update_announcements'),
    path('api_delete_announcements/', apiviews.api_delete_announcements, name='api_delete_announcements'),

    path('api_timetable/', apiviews.api_timetable, name='api_timetable'),
    path('api_update_timetable/', apiviews.api_update_timetable, name='api_update_timetable'),
    path('api_delete_timetable/', apiviews.api_delete_timetable, name='api_delete_timetable'),

    path('api_packages/', apiviews.api_packages, name='api_packages'),
    path('api_update_packages/', apiviews.api_update_packages, name='api_update_packages'),
    path('api_delete_package/', apiviews.api_delete_package, name='api_delete_package'),

    path('api_students/', apiviews.api_students, name='api_students'),
    path('api_update_students/', apiviews.api_update_students, name='api_update_students'),
    path('api_delete_students/', apiviews.api_delete_students, name='api_delete_students'),

    path('api_admin_profile/', apiviews.api_admin_profile, name='api_admin_profile'),

    path('api_attendance/', apiviews.api_attendance, name='api_attendance'),

    path('api_admin_report_card/', apiviews.api_admin_report_card, name='api_admin_report_card'),



]