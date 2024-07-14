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