from django.core.mail import send_mail
from celery import shared_task
import smtplib
from django.template.loader import get_template
from django.template import Context, Template
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import requests
import json
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http import Http404, JsonResponse, HttpResponse
from adminside.models import *
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import get_template

# changes done
logo_image_url = 'https://metrofoods.co.nz/logoo.png'


@shared_task(bind=True, max_retries=5)  # Use None for infinite retries
def attendance_student_present_mail(self, email_list, html_content):
    sub = "Today's Attendance Update!"
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = email_list
    text_content = ''
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
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


@shared_task(bind=True, max_retries=5)  # Use None for infinite retries
def attendance_student_absent_mail(self, email_list, html_content):
    sub = "Today's Attendance Update!"
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = email_list
    text_content = ''
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
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

@shared_task(bind=True, max_retries=5)  # Retry up to 5 times
def marks_mail(self, student_names, student_marks, test_date, test_name, total_marks, student_email_ids, htmly):
    subject = f'Test Marks Result for {test_name}'
    email_from = 'miniStudy <mail@ministudy.in>'
    htmly = get_template('teacherpanel/Email/marks_student.html')
    connection = get_connection()
    messages = []
    html_content = htmly.render(Context(context_data))
    htmly = Template(htmly)
    # Format the test date
    if isinstance(test_date, str):
        formatted_date = test_date
    else:
        formatted_date = test_date.strftime('%d-%m-%Y')

    for i, email in enumerate(student_email_ids):
        student_marks = student_marks[i]
        context_data = {
            'title': 'Test Marks Notification',
            'test_name': test_name,
            'student_name': student_names,
            'total_marks': total_marks,
            'test_date': formatted_date,
            'student_marks': student_marks,
        }
        html_content = htmly.render(context_data)

        # Create the email message
        msg = EmailMultiAlternatives(subject, '', email_from, [email])
        msg.attach_alternative(html_content, "text/html")
        messages.append(msg)
    try:
        connection.send_messages(messages)
    except smtplib.SMTPServerDisconnected as e:
        print(f"SMTP error occurred: {e}")
        # Retry the task after a delay if there's an SMTP server issue
        raise self.retry(exc=e, countdown=60)  # Retry after 60 seconds
    except Exception as e:
        print(f"An error occurred: {e}")
        # Retry on other exceptions as well
        raise self.retry(exc=e, countdown=60)  # Retry after 60 seconds


# -----------------------------------------Telegram------------------------------------------------------------------------------
# curl -X POST "https://api.telegram.org/bot7606273676:AAH8PlgH262QTaNyeG9ulSLt1rfsYqhfj1U/setWebhook?url=https://aadd-2401-4900-5774-145c-80b4-b65f-5a8e-c0f8.ngrok-free.app/adminside/webhook/"
BOT_TOKEN = '7606273676:AAH8PlgH262QTaNyeG9ulSLt1rfsYqhfj1U' 


# Function to request user's phone number
def request_phone_number(chat_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    # Create a keyboard button that requests contact
    keyboard = {
        "keyboard": [
            [{"text": "Share your contact", "request_contact": True}]
        ],
        "one_time_keyboard": True,
        "resize_keyboard": True
    }

    # Message data including the custom keyboard
    data = {
        "chat_id": chat_id,
        "text": "For Getting Updates, Please share your phone number by clicking the button below:",
        "reply_markup": json.dumps(keyboard)
    }

    # Send the message
    requests.post(url, json=data)

# Function to send messages
def send_telegram_message(chat_id, text, title=''):
    
    message = (
        f"{title}\n\n{text}")
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    data = {
        'chat_id': chat_id,
        'photo': logo_image_url,
        'caption': message, 
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, json=data)


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        update = json.loads(request.body)  # Parse incoming JSON
        message = update.get('message', {})
        chat_id = message['chat']['id']  # Get the user's chat ID
        text = message.get('text', '')  # Get the text sent by the user

        # Handle the '/start' command
        if text.lower() == '/start':
            request_phone_number(chat_id)
        elif 'contact' in message:
            phone_number = message['contact']['phone_number']
            user_id = message['contact']['user_id']
            # Save the phone number or take any necessary actions
            print(f"Phone number received: {phone_number} from user ID: {user_id}")
            
            set_msg = 0
            count = Students.objects.filter(stud_guardian_number=phone_number).count()
            stud_count = Students.objects.filter(stud_contact=phone_number).count()
            
            if count == 1:
                parent_number = Students.objects.get(stud_guardian_number = phone_number)
                print(parent_number)
                if parent_number:
                    parent_number.stud_telegram_parentschat_id = chat_id
                    parent_number.save()
                    set_msg=1

            elif stud_count == 1:
                student_number = get_object_or_404(Students, stud_contact = phone_number)
                print(student_number)    
                if student_number:
                    student_number.stud_telegram_studentchat_id = chat_id
                    student_number.save()
                    set_msg = 1
            
            if set_msg == 1:
                welcome_message = (
                    "🌟 *Welcome to miniStudy on Telegram!* 🌟\n\n"
                    "Hi there! We're thrilled to have you join our miniStudy community. 🎉\n\n"
                    "To make the experience even better, please share your phone number so we can send you personalized updates.\n"
                    "Click the button below to share your contact details.\n\n"
                    "If you have any questions, feel free to reach out at *mail@ministudy.in* or visit us at [api.ministudy.in](https://api.ministudy.in). We're always happy to assist you.\n\n"
                    "Thank you for choosing miniStudy – let’s make learning an incredible experience together! 🎓"
                )
                send_telegram_message(chat_id, welcome_message)
            else:
                send_telegram_message(chat_id, 'Verification Failed, Please check that the phone number on your miniStudy account matches your Telegram number. Both should be the same. Try again!')    
        else:
            pass    
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


def attendance_telegram_message_student(status, date, student_chatids):
    title = "Attendance Status"
    formatted_date = date.strftime("%Y-%m-%d %H:%M")

    for student_chatid in student_chatids:
        message = (
            f"Dear Student,\n\n"
            f"We are writing to inform you of your attendance status.\n\n"
            f"Attendance Status: **{status}**\n"
            f"Date and Time: {formatted_date}\n\n"
            f"If you have any questions regarding your attendance, feel free to contact us.\n\n"
            f"Thank you.\n"
            f"Best regards,\n"
            f"MiniStudy"
            f"[Click here for more info](http://api.ministudy.in/)"
        )
        send_telegram_message(student_chatid, message, title)

def attendance_telegram_message_parent(status, date, parent_chatids):
    title = "Student Attendance Status"
    formatted_date = date.strftime("%Y-%m-%d %H:%M")

    for parent_chatid in parent_chatids:
        # Professional message addressed to parents
        message = (
            f"Dear Parent,\n\n"
            f"We would like to inform you about the attendance status of your child.\n\n"
            f"Attendance Status: **{status}**\n"
            f"Date and Time: {formatted_date}\n\n"
            f"If you have any concerns or questions about this status, please do not hesitate to contact the school administration.\n\n"
            f"Thank you for your attention.\n"
            f"Best regards,\n"
            f"MiniStudy"
            f"[Click here for more info](http://api.ministudy.in/)"
        )    
        send_telegram_message(parent_chatid, message, title)



def send_notification(playerid,title,message, request):
    url = "https://onesignal.com/api/v1/notifications"

    payload = json.dumps({
    "app_id": "9d720639-6e9a-466a-9c95-be085af75a7f",
    "include_player_ids": [
        playerid
    ],
    "data": {
        "key": "value"
    },
    "contents": {
        "en": message
    },
    "headings": {
        "en": title
    },
    })
    headers = {
    'Cookie': '__cf_bm=536.mIQOyZqwoH2Md12MW9_sMJYL32pWpSRwuOrnhxs-1729177405-1.0.1.1-epZtYVG8IBmhhrDnWrlcskZf5tNZSAT4byzbP4Z0xHErFwDn5c40uRkxJEJCUmXyH2H7L7mxrR3fkJFtaSqguw',
    'Content-Type': 'text/plain',
    'Authorization': 'Basic  ZTA1ZmU1MDktOTNmMy00NDBjLWE3ZWEtNWQ3Njc3ZTA1YWEz',
    'Content-Type': 'application/json'
    }        
    response = requests.request("POST", url, headers=headers, data=payload)