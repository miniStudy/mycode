from django.urls import path
from team_ministudy import views as ministudyview

urlpatterns = [
    path('show_institute/', ministudyview.show_institute_function, name='show_institute'),
    path('insert_update_institute/', ministudyview.insert_update_institute_function, name='insert_update_institute'),
]

