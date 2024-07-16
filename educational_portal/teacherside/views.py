from django.shortcuts import render,get_object_or_404,redirect
from adminside.models import *
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import math
from django.db.models import Sum,Count
from django.db.models import Count, Case, When, IntegerField
import random
from django.http import Http404,JsonResponse
from studentside.forms import *
from adminside.form import *
from django.db.models import OuterRef, Subquery, BooleanField,Q
# Create your views here.
# mail integration 
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from studentside.decorators import student_login_required

# Create your views here.
def teacher_home(request):
     return render(request, 'teacherpanel/index.html')


def teacher_test(request):
     return render(request, 'teacherpanel/index.html')


def teacher_materials(request):
     return render(request, 'teacherpanel/index.html')


def teacher_timetable(request):
     return render(request, 'teacherpanel/index.html')


def teacher_attendance(request):
     return render(request, 'teacherpanel/index.html')


def teacher_syllabus(request):
     return render(request, 'teacherpanel/index.html')   


def teacher_announcement(request):
     return render(request, 'teacherpanel/index.html')     


def teacher_doubts(request):
     return render(request, 'teacherpanel/index.html')     


def teacher_events(request):
    event_data = Event.objects.all()
    event_imgs = Event_Image.objects.all()
    selected_events = Event.objects.all()[:1]
    context={
        'event_data':event_data,
        'event_imgs':event_imgs,
        'selected_events':selected_events
    }

    if request.GET.get('event_id'):
        event_id = request.GET['event_id']
        selected_events = Event.objects.filter(event_id = event_id)
        event_imgs = Event_Image.objects.filter(event__event_id = event_id)
        
        context.update({'selected_events':selected_events, 'events_img':event_imgs})

    return render(request, 'teacherpanel/events.html', context) 