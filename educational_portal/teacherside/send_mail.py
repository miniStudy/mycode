from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
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