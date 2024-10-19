from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import requests
import json
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http import Http404, JsonResponse, HttpResponse
from adminside.models import *
import datetime


# changes done
logo_image_url = 'https://metrofoods.co.nz/logoo.png'

def announcement_mail(title,msg,list_of_receivers):
    print(list_of_receivers)
    sub = 'New Announcement from miniStudy'
    mess = ''
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = list_of_receivers
    # send_mail(sub,mess,email_from,recp_list)
    htmly = get_template('Email/announcement.html')
    d = {'title': title,'msg':msg}
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
    htmly = get_template('Email/timetable.html')
    d = {'title':title, 'msg':msg}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def payment_mail(mode, date, amount, student_email):
    sub = 'Payment Satus!'
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = student_email
    htmly = get_template('Email/payment.html')
    d = {'mode':mode, 'amount':amount, 'date':date}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def cheque_mail(bank, amount, date, student_email):
    sub = 'Cheque Satus!'
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = student_email
    htmly = get_template('Email/cheque.html')
    d = {'bank': bank, 'amount':amount, 'date':date}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def parent_cheque_mail(bank, amount, date, parent_email):
    sub = 'Cheque Satus!'
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = parent_email
    htmly = get_template('Email/cheque.html')
    d = {'bank': bank, 'amount':amount, 'date':date}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def institute_send_mail(email_list): 
    sub = 'Team Ministudy Marketing'
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = email_list
    htmly = get_template('Email/institute.html')
    d = {'current_year': datetime.datetime.now().year}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def cheque_update_mail(bank, amount, date, student_email):
    sub = 'Cheque Withdraw!'
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = student_email
    htmly = get_template('Email/cheque_update.html')
    d = {'bank': bank, 'amount':amount, 'date':date}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def faculty_email(fac_name, fac_email, fac_password):
    sub = 'Login Details!'
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = fac_email
    htmly = get_template('Email/faculty.html')
    d = {'fac_name':fac_name, 'fac_email':fac_email[0], 'fac_password':fac_password}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def student_email_send(student_name, student_email, student_password):
    sub = 'Login Details!'
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = student_email
    htmly = get_template('Email/student.html')
    d = {'student_name':student_name, 'student_email':student_email[0], 'student_password':student_password}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# -----------------------------------------Telegram------------------------------------------------------------------------------

# curl -X POST "https://api.telegram.org/bot7606273676:AAH8PlgH262QTaNyeG9ulSLt1rfsYqhfj1U/setWebhook?url=https://aadd-2401-4900-5774-145c-80b4-b65f-5a8e-c0f8.ngrok-free.app/adminside/webhook/"
# curl -X POST "https://api.telegram.org/bot7606273676:AAH8PlgH262QTaNyeG9ulSLt1rfsYqhfj1U/setWebhook?url=https://api.ministudy.in/adminside/webhook/"

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
                if parent_number:
                    parent_number.stud_telegram_parentschat_id = chat_id
                    parent_number.save()
                    set_msg=1

            elif stud_count == 1:
                student_number = get_object_or_404(Students, stud_contact = phone_number)  
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



def announcement_telegram_message_student(student_chatid, announcement_mesage,announcement_title):
    send_telegram_message(student_chatid, announcement_mesage,announcement_title)


def announcement_telegram_message_parent(parent_chat_ids, announcement_mesage,announcement_title):
    send_telegram_message(parent_chat_ids, announcement_mesage,announcement_title)


def payment_telegram_message(stud_name, student_chatid, mode, amount):
    title = "Payment Confirmation"
    message = (
        f"Dear {stud_name},\n\n"
        f"We would like to inform you that your payment of ₹{amount} has been successfully received.\n"
        f"Payment Method: {mode}\n\n"
        f"If you have any questions or need further assistance, feel free to contact us.\n\n"
        f"Thank you for your prompt payment.\n"
        f"Best regards,\n"
        f"MiniStudy"
        f"[Click here for more info](http://api.ministudy.in/)"
    )
    send_telegram_message(student_chatid, message, title)


def timetable_telegram_message_student(chat_ids):
    title = "Timetable Updated"
    for i in chat_ids:
        message = (
            f"Dear Student,\n\n"
            f"Your time has been updated!\n"
            f"If you have any questions or need further assistance, feel free to contact us.\n\n"
            f"Best regards,\n"
            f"MiniStudy"
            f"[Click here for more info](http://api.ministudy.in/)"
        )
        send_telegram_message(i, message, title)


def timetable_telegram_message_parent(chat_ids):
    title = "Timetable Updated"
    for i in chat_ids:
        message = (
            f"Dear Student,\n\n"
            f"Your student time has been updated!\n"
            f"If you have any questions or need further assistance, feel free to contact us.\n\n"
            f"Best regards,\n"
            f"MiniStudy"
            f"[Click here for more info](http://api.ministudy.in/)"
        )
        send_telegram_message(i, message, title)


def event_telegram_message_student(event_name, event_date, student_chat_ids):
    title = "New Event Update"
    for chat_id in student_chat_ids:
        message = (
        f"Dear Student,\n\n"
        f"We are pleased to inform you that our recent event, *{event_name}*, which was held on {event_date}, has successfully concluded.\n"
        f"We trust that you found the event both enjoyable and enriching.\n\n"
        f"To explore event highlights, including photos and key moments, we encourage you to check out out portal for further details.\n"
        f"Warm regards,\n"
        f"MiniStudy\n\n"
        f"[Click here for more info](http://api.ministudy.in/)")
        send_telegram_message(chat_id, message, title)


def event_telegram_message_parent(event_name, event_date, student_email_ids):
    title = "Event Update"
    for email in student_email_ids:
        message = (
            f"Dear Parent,\n\n"
            f"We are happy to inform you that the event, *{event_name}*, which took place on {event_date}, was a great success.\n"
            f"We hope your child enjoyed participating in the event!\n\n"
            f"For more details and event highlights, please check out our portal.\n"
            f"Best regards,\n"
            f"MiniStudy\n\n"
            f"[Click here for more info](http://api.ministudy.in/)"
        )
        send_telegram_message(email, message, title)



def send_notification(playerid,message):
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
    }
    })
    headers = {
    'Cookie': '__cf_bm=536.mIQOyZqwoH2Md12MW9_sMJYL32pWpSRwuOrnhxs-1729177405-1.0.1.1-epZtYVG8IBmhhrDnWrlcskZf5tNZSAT4byzbP4Z0xHErFwDn5c40uRkxJEJCUmXyH2H7L7mxrR3fkJFtaSqguw',
    'Content-Type': 'text/plain',
    'Authorization': 'Basic  ZTA1ZmU1MDktOTNmMy00NDBjLWE3ZWEtNWQ3Njc3ZTA1YWEz',
    'Content-Type': 'application/json'
    }        
    response = requests.request("POST", url, headers=headers, data=payload)