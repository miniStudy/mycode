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
from parentsside import views as parentview
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', parentview.parent_home, name='parent_home'),

    path('parent_login/', parentview.parent_login_page, name='parent_login'),

    path('parent_login_handle/',parentview.parent_login_handle,name='parent_login_handle'),

    path('parent_forget_password/', parentview.parent_forget_password, name='parent_forget_password'),

    path('parent_handle_forget_password/',parentview.parent_handle_forget_password, name='parent_handle_forget_password'),

    path('parent_set_new_password/',parentview.parent_set_new_password, name='parent_set_new_password'),

    path('parent_handle_set_new_password/',parentview.parent_handle_set_new_password, name='parent_handle_set_new_password'),

    path('parent_logout/',parentview.parent_logout_page, name = 'parent_logout' ),

    path('parent_events/',parentview.show_parent_events, name = 'parent_events' ),
    path('parent_profile/',parentview.show_parent_profile, name = 'parent_profile' ),
    path('parentside_report_card/',parentview.show_parentside_report_card, name = 'parentside_report_card' ),
    path('parentside_payment/',parentview.show_parentside_payment, name = 'parentside_payment' ),
    path('parentside_announcement/',parentview.show_parentside_announcement, name = 'parentside_announcement'),
    path('parentside_timetable/',parentview.show_parentside_timetable, name = 'parentside_timetable'),

    path('parent_insert_suggestions/',parentview.insert_suggestions_function, name = 'parent_insert_suggestions'),
    path('add_complaint/',parentview.add_complaint_function, name = 'add_complaint'),
    path('delete_complaint/',parentview.delete_complaint_function, name = 'delete_complaint'),


    path('parent_chatbox/',parentview.parent_chatbox, name = 'parent_chatbox'),
    path('insert_chatbot_parent/',parentview.insert_chatbot_parent, name = 'insert_chatbot_parent'),

    path('show_notification_parent/',parentview.show_notification_parent_function, name = 'show_notification_parent'),

]