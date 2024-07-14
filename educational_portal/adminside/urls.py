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
from adminside import views as adminview
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', adminview.home, name='Admin Home'),
    path('send_mail/', adminview.mail_send, name='send_mail'),
    path('boards/', adminview.show_boards, name='boards'),
    path('insert_update_boards/',adminview.insert_update_boards,name='insert_update_boards'),
    path('delete_boards/', adminview.delete_boards, name='delete_boards'),
    
    # ---------------------------adminside auth-------------------------
    path('Admin_Login/', adminview.admin_login_page, name='Admin Login'),
    path('admin_login_handle/',adminview.admin_login_handle,name='admin_login_handle'),
    path('Admin_Forgot_Password/', adminview.admin_Forgot_Password, name='Admin_Forgot_Password'),
    path('admin_handle_forgot_password/',adminview.admin_handle_forgot_password, name='admin_handle_forgot_password'),
    path('Admin_Set_New_Password/',adminview.admin_Set_New_Password, name='Admin_Set_New_Password'),
    path('admin_handle_set_new_password/',adminview.admin_handle_set_new_password, name='admin_handle_set_new_password'),
    path('admin_logout/',adminview.admin_logout, name = 'admin_logout' ),

    # ==============================adminside Stds=========================

    path('stds/', adminview.show_stds, name='stds'),
    path('insert_update_stds/',adminview.insert_update_stds,name='insert_update_stds'),
    path('delete_stds/', adminview.delete_stds, name='delete_stds'),

     # ==============================adminside Announcements=========================
    
    path('announcements/', adminview.show_announcements, name='admin_announcements'),
    path('insert_update_announcements/',adminview.insert_update_announcements,name='insert_update_announcements'),
    path('delete_announcements/', adminview.delete_announcements, name='delete_announcements'),

    # ============================= adminside subjects=====================================
    path('admin_subjects/', adminview.show_subjects, name='admin_subjects'),
    path('insert_update_subjects/',adminview.insert_update_subjects,name='insert_update_subjects'),
    path('delete_subjects/', adminview.delete_subjects, name='delete_subjects'),


    # ============================= adminside Chepters=====================================
    path('admin_chepters/', adminview.show_chepters, name='admin_chepters'),
    path('insert_update_chepters/',adminview.insert_update_chepters,name='insert_update_chepters'),
    path('delete_chepters/', adminview.delete_chepters, name='delete_chepters'),

    # ============================= adminside Faculties=====================================

    path('admin_faculties/', adminview.show_faculties, name='admin_faculties'),
    path('insert_update_faculties/', adminview.insert_update_faculties, name='insert_update_faculties'),
    path('delete_faculties/', adminview.delete_faculties, name='delete_faculties'),


    # ============================= adminside Timetable=====================================

    path('admin_timetable/', adminview.show_timetable, name='admin_timetable'),
    path('insert_update_timetable/', adminview.insert_update_timetable, name='insert_update_timetable'),
    path('delete_timetable/', adminview.delete_timetable, name='delete_timetable'),

    # ============================= adminside Timetable=====================================

    path('admin_attendance/', adminview.show_attendance, name='admin_attendance'),

    # ==========================add events ====================================================

    path('insert_event/', adminview.insert_events, name="insert_event"),

    # ==========================Tests ====================================================

    path('admin_tests/', adminview.show_tests, name='admin_tests'),
    path('insert_update_tests/', adminview.show_tests, name='insert_update_tests'),
    path('delete_tests/', adminview.delete_tests, name='delete_tests'),

    path('show_test_questions_admin/', adminview.show_test_questions_admin, name='show_test_questions_admin'),
    path('insert_update_test_question_admin/', adminview.insert_update_test_questions, name='insert_update_test_question_admin'),
    path('show_events/', adminview.show_events, name='show_events'),

    # ========================== Students and Faculty Data show =======================================
    path('students_dataAdmin/', adminview.show_students, name='students_dataAdmin'),
    path('inquiry_data/', adminview.show_inquiries, name='inquiry_data'),
<<<<<<< HEAD

    # =========================================packages ================================================
    path('admin_packages', adminview.show_packages, name="admin_packages"),

    

=======
    # =========================================packages ===============================================
    path('admin_packages/', adminview.show_packages, name="admin_packages"),
    path('insert_package/', adminview.insert_admin_package, name="insert_package"),
    path('delete_package/', adminview.delete_admin_package, name="delete_package"),
    # =========================================Batches ===============================================
    path('admin_batches/', adminview.show_batches, name="admin_batches"),
    path('insert_batches/', adminview.insert_admin_batches, name="insert_batches"),
    path('delete_batches/', adminview.delete_admin_batches, name="delete_batches"),
>>>>>>> 8a32422fce6f4de6519dab4c23e849d37d57cffd
]

