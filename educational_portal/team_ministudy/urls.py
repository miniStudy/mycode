from django.urls import path
from team_ministudy import views as ministudyview

urlpatterns = [
    path('show_institute/', ministudyview.show_institute_function, name='show_institute'),
    path('insert_update_institute/', ministudyview.insert_update_institute_function, name='insert_update_institute'),

    path('show_ministudy_payment', ministudyview.show_ministudy_payment_function, name='show_ministudy_payment'),
    path('insert_update_ministudy_payment', ministudyview.insert_update_ministudy_payment_function, name='insert_update_ministudy_payment'),

    path('institute_lock', ministudyview.institute_lock_function, name='institute_lock'),



    path('remove_institute', ministudyview.remove_institute_function, name='remove_institute'),
]

