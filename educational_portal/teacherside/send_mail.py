from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
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

# changes done
logo_image_url = 'https://metrofoods.co.nz/logoo.png'

def attendance_student_present_mail(status,date,list_of_receivers):
    sub = "Today's Attendance Update!"
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = list_of_receivers
    # send_mail(sub,mess,email_from,recp_list)
    htmly = get_template('teacherpanel/Email/attendance_student.html')
    d = {'status': status,'date':date,'user':"Student",'to':"Your"}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def attendance_parent_present_mail(status,date,list_of_receivers):
    sub = "Today's Attendance Update!"
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = list_of_receivers
    # send_mail(sub,mess,email_from,recp_list)
    htmly = get_template('teacherpanel/Email/attendance_student.html')
    d = {'status': status,'date':date,'user':"Parents",'to':"Your Child's"}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def attendance_student_absent_mail(status,date,list_of_receivers):
    sub = "Today's Attendance Update!"
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = list_of_receivers
    # send_mail(sub,mess,email_from,recp_list)
    htmly = get_template('teacherpanel/Email/attendance_student.html')
    d = {'status': status,'date':date,'user':"Student",'to':"Your"}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def attendance_parent_absent_mail(status,date,list_of_receivers):
    sub = "Today's Attendance Update!"
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = list_of_receivers
    # send_mail(sub,mess,email_from,recp_list)
    htmly = get_template('teacherpanel/Email/attendance_student.html')
    d = {'status': status,'date':date,'user':"Parents",'to':"Your Child's"}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def timetable_mail(list_of_receivers):
    sub = 'New Update from miniStudy'
    title = 'Time Table Updated'
    msg = 'Your time table has been updated!'
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = list_of_receivers
    htmly = get_template('teacherpanel/Email/timetable.html')
    d = {'title':title, 'msg':msg}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import get_template

def marks_mail(marks, email_ids, test_name, total_marks, test_date):
    sub = f'Test Marks Result for {test_name}'
    email_from = 'miniStudy <mail@ministudy.in>'
    htmly = get_template('teacherpanel/Email/marks_student.html')

    connection = get_connection()

    messages = []

    if isinstance(test_date, str):
        formatted_date = test_date
    else:
        formatted_date = test_date.strftime('%d-%m-%Y')

    for i, email in enumerate(email_ids):
        student_marks = marks[i]
        print(student_marks)
        print(email)
        d = {
            'title': 'Test Marks Notification',
            'test_name': test_name,
            'total_marks': total_marks,
            'test_date': formatted_date,
            'student_marks': student_marks,
        }
        html_content = htmly.render(d)
        
        msg = EmailMultiAlternatives(sub, '', email_from, [email])
        msg.attach_alternative(html_content, "text/html")
      
        messages.append(msg)
    connection.send_messages(messages)


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


from datetime import datetime
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