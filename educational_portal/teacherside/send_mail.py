from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from datetime import datetime
from django.core.mail import EmailMultiAlternatives

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
    htmly = get_template('Email/attendance_student.html')
    d = {'status': status,'date':date,'user':"Student",'to':"Your"}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def attendance_parent_absent_mail(status,date,list_of_receivers, num):
    sub = "Today's Attendance Update!"
    email_from = 'miniStudy <mail@ministudy.in>'
    recp_list = list_of_receivers
    # send_mail(sub,mess,email_from,recp_list)
    htmly = get_template('Email/attendance_student.html')
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
    htmly = get_template('Email/timetable.html')
    d = {'title':title, 'msg':msg}
    text_content = ''
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# def marks_mail(marks, email_ids):
#     sub = 'Test Marks Result'
#     email_from = 'miniStudy <mail@ministudy.in>'
#     htmly = get_template('teacherpanel/Email/marks_student.html')
    
#     for i, email in enumerate(email_ids):
#         student_marks = marks[i]
#         d = {
#             'title': 'Test Marks Notification',
#             'msg': f'Your test marks are: {student_marks}',
#         }
#         text_content = ''
#         html_content = htmly.render(d)
#         msg = EmailMultiAlternatives(sub, text_content, email_from, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()


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
