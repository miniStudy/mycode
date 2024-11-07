from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import requests
import json
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http import Http404, JsonResponse, HttpResponse
from adminside.models import *
import datetime
from celery import shared_task
from time import sleep
from django.core.mail import send_mail  
from django.conf import settings
import time
import smtplib
from django.utils import timezone
from datetime import timedelta


# changes done
logo_image_url = 'https://metrofoods.co.nz/logoo.png'


@shared_task
def admin_email_send(self,admin_emails, student_name, student_email, selected_subjects):
    subject = 'New Student Inquiry - miniStudy'
    email_from = 'miniStudy <mail@ministudy.in>'
    
    htmly = get_template('Emails/admin_inquiry_mail.html')
    context = {
        'student_name': student_name,
        'student_email': student_email,
        'selected_subjects': ', '.join(selected_subjects),
    }
    html_content = htmly.render(context)

    msg = EmailMultiAlternatives(subject, '', email_from, admin_emails)
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except smtplib.SMTPServerDisconnected as e:
        print(f"SMTP error occurred: {e}")
        # Retry the task after a delay
        raise self.retry(exc=e, countdown=60)  # Retry after 60 seconds
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, you can also retry for other exceptions
        raise self.retry(exc=e, countdown=60)  # Retry after 60 seconds