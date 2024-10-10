from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http import Http404, JsonResponse, HttpResponse
from adminside.models import *

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


def telegram_announcement_adminside(student_chatid, announcement_mesage,announcement_title):
    send_telegram_message(student_chatid, announcement_mesage,announcement_title)