from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import requests
import json
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http import Http404, JsonResponse, HttpResponse
from adminside.models import *
import datetime




def admin_email_send(admin_emails, student_name, student_email, selected_subjects):
    subject = 'New Student Inquiry - miniStudy'
    email_from = 'miniStudy <mail@ministudy.in>'
    
    htmly = get_template('Emails/admin.html')
    context = {
        'student_name': student_name,
        'student_email': student_email,
        'selected_subjects': ', '.join(selected_subjects),
    }
    html_content = htmly.render(context)

    msg = EmailMultiAlternatives(subject, '', email_from, admin_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()