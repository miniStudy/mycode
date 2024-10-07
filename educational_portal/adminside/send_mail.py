from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives

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