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
    path('webhook/', adminview.telegram_webhook, name='webhook'),


    path('test_whatsapp/',adminview.send_whatsapp_message_test_marks, name="test_whatsapp"),
    # path('send_mail/', adminview.mail_send, name='send_mail'),
    path('send_report_card/', adminview.send_report_card, name='send_report_card'),
    path('boards/', adminview.show_boards, name='boards'),
    path('insert_update_boards/',adminview.insert_update_boards,name='insert_update_boards'),
    path('delete_boards/', adminview.delete_boards, name='delete_boards'),
    
    # ---------------------------adminside auth-------------------------
    path('show_admin/', adminview.show_admin_page, name='show_admin'),
    path('insert_update_admin/', adminview.insert_update_admin_page, name='insert_update_admin'),
    path('delete_admin/', adminview.delete_admin_page, name='delete_admin'),
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


    # ============================= adminside Timetable ===========================================

    path('admin_timetable/', adminview.show_timetable, name='admin_timetable'),
    path('insert_update_timetable/', adminview.insert_update_timetable, name='insert_update_timetable'),
    path('delete_timetable/', adminview.delete_timetable, name='delete_timetable'),

    # ============================= adminside Attendence============================================
    path('admin_attendance/', adminview.show_attendance, name='admin_attendance'),

    # ==========================add events =========================================================

    path('insert_event/', adminview.insert_events, name="insert_event"),
    path('delete_event/', adminview.delete_event, name="delete_event"),

    # ==========================Tests ==============================================================

    path('admin_tests/', adminview.show_tests, name='admin_tests'),
    path('insert_update_tests/', adminview.insert_update_tests, name='insert_update_tests'),
    path('delete_tests/', adminview.delete_tests, name='delete_tests'),

    path('show_test_questions_admin/', adminview.show_test_questions_admin, name='show_test_questions_admin'),
    path('insert_update_test_question_admin/', adminview.insert_update_test_questions, name='insert_update_test_question_admin'),
    path('show_events/', adminview.show_events, name='show_events'),
    path('delete_test_question_answer/',adminview.delete_test_question_answer,name="delete_test_question_answer"),

    # ========================== Students ===========================================================
    path('students_dataAdmin/', adminview.show_students, name='students_dataAdmin'),
    path('insert_update_students/',adminview.insert_update_students,name='insert_update_students'),
    path('delete_students/', adminview.delete_students, name='delete_students'),
    path('send_meeting_mail/', adminview.send_meeting_mail, name='send_meeting_mail'),
    path('insert_meeting_date/', adminview.insert_meeting_date, name='insert_meeting_date'),

    path('inquiry_data/', adminview.show_inquiries, name='inquiry_data'),
    path('delete_inquiry/', adminview.delete_inquiries, name='delete_inquiry'),
    
    # =========================================packages ==============================================
    path('admin_packages', adminview.show_packages, name="admin_packages"),

    # =========================================packages ==============================================
    path('admin_packages/', adminview.show_packages, name="admin_packages"),
    path('insert_update_packages/', adminview.insert_update_packages, name="insert_update_packages"),
    path('delete_package/', adminview.delete_admin_package, name="delete_package"),

    # =========================================Batches ===============================================
    path('admin_batches/', adminview.show_batches, name="admin_batches"),
    path('insert_update_batches/', adminview.insert_update_batches, name="insert_update_batches"),
    path('delete_batches/', adminview.delete_admin_batches, name="delete_batches"),


    # =========================================Materials =============================================
    path('admin_show_group/', adminview.admin_show_group_function, name='admin_show_group'),
    path('admin_add_group/', adminview.admin_add_group_function, name='admin_add_group'),
    path('admin_delete_group/', adminview.admin_delete_group_function, name='admin_delete_group'),

    path('admin_show_material/', adminview.admin_show_material_function, name='admin_show_material'),
    path('admin_add_material/', adminview.admin_add_material_function, name='admin_add_material'),
    path('admin_delete_material/', adminview.admin_delete_material_function, name='admin_delete_material'),
    path('admin_show_pdf/',adminview.admin_show_pdf, name="admin_show_pdf"),

    # =========================================Admin Profile =========================================
    path('admin_profile/', adminview.show_admin_profile, name="admin_profile"),

    # =========================================Admin Student Doubts =========================================
    path('Student_doubts_adminside/', adminview.Student_doubts_adminside, name="Student_doubts_adminside"),

    # =========================================Admin Student Report Card =========================================
    path('adminside_report_card/', adminview.adminside_report_card, name="adminside_report_card"),

    # =========================================Admin Payments ====================================================
    path('fees_collection_admin/', adminview.fees_collection_admin, name="fees_collection_admin"),
    path('add_cheques_admin/', adminview.add_cheques_admin, name="add_cheques_admin"),
    path('add_fees_collection_admin/', adminview.add_fees_collection_admin, name="add_fees_collection_admin"),
    # path('update_cheques_admin/', adminview.update_cheques_admin, name="update_cheques_admin"),
    path('admin_fees_collection_delete/',adminview.admin_fees_collection_delete , name="admin_fees_collection_delete"),
    path('payments_history_admin/', adminview.payments_history_admin, name="payments_history_admin"),
    path('delete_cheques_admin/', adminview.delete_cheques_admin, name="delete_cheques_admin"),

    # ========================================Faculty Access======================================================
    path('faculty_access/', adminview.faculty_access_show, name="faculty_access"),
    path('view_faculty_access/', adminview.view_faculty_access, name="view_faculty_access"),
    path('delete-faculty-access/', adminview.delete_faculty_access, name='delete_faculty_access'),
    path('export_data',adminview.export_data, name='export_data'),

    path('bulk_upload_test_questions/', adminview.bulk_upload_questions, name='bulk_upload_test_questions'),
    path('show_question_bank/', adminview.show_question_bank, name="show_question_bank"),
    path('edit_question_bankk/', adminview.edit_question_bankk, name="edit_question_bankk"),
    path('delete_question_bank/', adminview.delete_question_bank, name="delete_question_bank"),

    path('generate_payment_slip/',adminview.generate_payment_slip, name='generate_payment_slip'),

    path('time_slot/', adminview.time_slot_function, name='time_slot'),
    path('institute_main_send/', adminview.institute_main_send_function, name='institute_main_send'),

    path('show_mail_templates/', adminview.show_mail_templates_function, name='show_mail_templates'),
    path('insert_update_mail_templates/', adminview.insert_update_mail_templates, name='insert_update_mail_templates'),
    path('delete_mail_templates/', adminview.delete_mail_templates, name='delete_mail_templates'),

    
    path('admin_insert_suggestions/', adminview.insert_suggestions_function, name='admin_insert_suggestions'),
    path('show_complaints/', adminview.show_complaints_functions, name='show_complaints'),

    path('show_notification/', adminview.show_notification_function, name='show_notification'),

    path('show_expense/', adminview.show_expense_function, name='show_expense'),
    path('add_expense/', adminview.add_expense_function, name='add_expense'),
    path('delete_expense/', adminview.delete_expense_functions, name='delete_expense'),


    path('show_adminlead/', adminview.show_adminlead_function, name='show_adminlead'),
    path('add_adminlead/', adminview.add_adminlead_function, name='add_adminlead'),
    path('delete_adminlead/', adminview.delete_adminlead_function, name='delete_adminlead'),


    path('show_study_videos/', adminview.show_study_videos, name='show_study_videos'),
    path('add_study_videos/', adminview.add_study_videos, name='add_study_videos'),

]