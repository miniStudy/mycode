from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from adminside.form import *
from adminside.models import *
from django.contrib import messages
from django.urls import reverse
import pandas as pd
from datetime import datetime
from django.conf import settings
import math
import statistics
from django.db.models.functions import TruncMonth
import calendar
from django.utils.timezone import make_aware
import random
from django.http import Http404, JsonResponse, HttpResponse
from datetime import datetime
from django.db.models import Count,Sum, F, Case, When, Value, IntegerField
from django.core.files.storage import FileSystemStorage
# mail integration 
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from adminside.decorators import admin_login_required
from django.db.models import Count, Q
from django.http import Http404
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
import requests
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from team_ministudy.models import *
from django.contrib.auth.hashers import check_password



import fitz  # PyMuPDF
from PIL import Image
import io
from django.core.files.base import ContentFile


from team_ministudy.forms import suggestions_improvements_Form
from team_ministudy.models import suggestions_improvements

logo_image_url = 'https://metrofoods.co.nz/logoo.png'
from adminside.send_mail import *
from django.core.exceptions import ObjectDoesNotExist
from django.template import Template, Context
from django.contrib.auth.hashers import make_password

# =================celery=========================
from educational_portal.celery import add
from adminside.tasks import *
# ================================================


import logging

logger = logging.getLogger(__name__)

global_domain = None



# =================================================

@csrf_exempt  # Skip CSRF verification for API testing (enable CSRF protection for production)
def send_whatsapp_message_test_marks(request):
    # User details
    api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3MDBlYTNjODQ4NGQ2MGI4NDhhZDczMiIsIm5hbWUiOiJtaW5pU3R1ZHlfd2hhdHNhcHAiLCJhcHBOYW1lIjoiQWlTZW5zeSIsImNsaWVudElkIjoiNjY5ZTMwOGZmYmE3OTE3ZjE1MGRmNTMyIiwiYWN0aXZlUGxhbiI6Ik5PTkUiLCJpYXQiOjE3MjgxMTMyMTJ9.aZSCryj6KAkD5ETSkYsmiGwOzs87-wwz70fs6D9kBcg'  # Replace with your actual API key
    campaign_name = 'miniStudy_test'  # Replace with your campaign name
    destination = '+917285818382'  # User's phone number
    user_name = 'Ajay Patel'  # Name of the user
    source = 'MiniStudy'  # e.g., 'MiniStudy' or any other identifier
    template_params = ['Ajay Patel', 'MiniStudy', '05-10-2024', 'Polynomials', '20', '25']  # Dynamic template parameters
    media = {
        "url": "https://metrofoods.co.nz/logoo.png",  # Optional: URL for media (if needed)
        "filename": "1nobg.png"  # Optional: Filename for the media
    }

    # Prepare the payload for the request
    data = {
        "apiKey": api_key,
        "campaignName": campaign_name,
        "destination": destination,
        "userName": user_name,
        "source": source,
        "media": media,
        "templateParams": template_params,
    }
    
    # AiSensy API endpoint
    url = 'https://backend.aisensy.com/campaign/t1/api/v2'
    # Make the POST request to the AiSensy API
    response = requests.post(url, json=data)

    # Check the response and handle accordingly
    if response.status_code == 200:
        return HttpResponse("WhatsApp message sent successfully!")
    else:
        error_message = f"Failed to send WhatsApp message: {response.text}"
        return HttpResponse(error_message, status=response.status_code)

def paginatoorrr(queryset,request):
        paginator = Paginator(queryset, 20)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return page_obj


def send_report_card(request):
    # Define your context
    context = {
        'logo_url': 'https://metrofoods.co.nz/1nobg.png',
        'student': {
            'name': 'Trushal Patel',
            'roll_no': '20'
        },
        'attendance': {
            'overall': '50%',
            'maths': '70%',
            'english': '50%',
            'science': '60%',
            'total_classes': '50',
            'absent_classes': '10'
        },
        'test_results': {
            'overall': '70%',
            'maths': '30%',
            'science': '60%',
            'english': '80%',
            'total_tests': '10',
            'absent_tests': '2',
            'average': '70%'
        },
        'doubts': {
            'solved': '20',
            'asked': '10',
            'verified': '8'
        }
    }
    

    # Generate the PDF
    # pdf = render_to_pdf('reportcardtable.html', context)
    # # Email configuration
    # subject = 'Student Report Card'
    # body = 'Please find attached the report card.'
    # from_email = 'miniStudy <mail@ministudy.in>'
    # to_email = 'tmp1221pmt@gmail.com'

    # # Create EmailMessage instance
    # email = EmailMessage(
    #     subject,
    #     body,
    #     from_email,
    #     [to_email],
    # )

    # # Attach PDF
    # email.attach('report_card.pdf', pdf, 'application/pdf')
    # # Send the email
    # email.send()
    # return HttpResponse("Email sent successfully!")
    return render(request, 'reportcardtable.html',context)

# -----------------------------auth Start---------------------------



def mail_send(request):
    # ------------mail sending ---------------
        sub = 'Offer Letter from miniStudy'
        mess = 'Offer Letter'
        email_from = 'miniStudy <mail@ministudy.in>'
        recp_list = ['mail.trushalpatel@gmail.com','sakahisharma88172@gmail.com']
        # send_mail(sub,mess,email_from,recp_list)
        htmly = get_template('Email/sakshi_offer_letter.html')
        # d = {'pname': pname,'qty':qty,'size': ring_size,'clr':ring_color,'uname':fname,'uemail':email,'ucontact':cnumber}
        text_content = ''
        html_content = htmly.render()
        msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect('Admin Home')



def show_admin_page(request):
    domain = request.get_host()
    admin_data = AdminData.objects.filter(domain_name = domain)
    context = {'admin_data': admin_data, 'title': 'Admin'}
    return render(request, 'show_admin.html', context)

def insert_update_admin_page(request):
    domain = request.get_host()
    context = {'title': 'Admin'}
    if request.method == 'POST':
        form = admin_form(request.POST)
        if form.is_valid():
            hashed_password = make_password('123456')
            form.instance.admin_pass = hashed_password
            form.instance.domain_name = domain
            admin_password = form.instance.admin_pass
            admin_name = form.cleaned_data['admin_name']
            admin_email = form.cleaned_data['admin_email']
            form.save()
            messages.success(request, "You have been registed successfully!")

            htmly = mail_templates.objects.get(mail_temp_type = 'Admin_mail', mail_temp_selected=1).mail_temp_html
            context_data={}
            if domain != '127.0.0.1:8000':
                Institute_data = NewInstitution.objects.get(institute_domain = domain)
                
                logo = '{}/media/{}'.format(domain,Institute_data.institute_logo)
                context_data.update({
                    'logo':logo,
                    'institute_name': Institute_data.institute_name,
                    'institute_email': Institute_data.institute_email,
                    'institute_number': Institute_data.institute_contact,
                })
            else:
                logo = 'api.ministudy.in/static/imgs/My_dream_logo/logo_text_sidebyside_dark.png'
                context_data.update({
                    'logo':logo,
                    'institute':'miniStudy',
                    'email':'mail.trushalpatel@gmail.com',
                    'phone_num':'8511962611',
                })
            context_data.update({
            'title': "Admin Register",
            'name': admin_name,
            'password': admin_password
            })
            htmly = Template(htmly)
            html_content = htmly.render(Context(context_data))
            admin_register_email.delay([admin_email], html_content)
            return redirect('show_admin')
        else:
            form = admin_form()
    return render(request, "insert_update/add_admin.html", context)

def delete_admin_page(request):
    domain  = request.get_host()
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                AdminData.objects.filter(admin_id__in=selected_ids, domain_name = domain).delete()
                messages.success(request, 'Admin deleted successfully!')
                return redirect('show_admin')
            except Exception as e:
                messages.error(request, f'<i class="fa-solid fa-triangle-exclamation me-2"></i> An error occurred: {str(e)}')


def admin_login_page(request):  
    login=1
    if request.COOKIES.get("admin_email"):
            cookie_email = request.COOKIES['admin_email'].lower()
            cookie_pass = request.COOKIES['admin_password']
            return render(request, 'master_auth.html',{'login_set':login,'c_email':cookie_email,'c_pass':cookie_pass, 'title':'login'})
    else:
            return render(request, 'master_auth.html',{'login_set':login, 'title':'login'})


def admin_login_handle(request):
    domain = request.get_host()
    if request.method == "POST":
        email = request.POST['email'].lower()
        password = request.POST['password']
        val = AdminData.objects.filter(admin_email=email, domain_name = domain).count()
        if val==1:
            Data = AdminData.objects.filter(admin_email=email, domain_name = domain)
            admin_id = AdminData.objects.get(admin_id = Data[0] .admin_id)
            # if check_password(password, admin_id.admin_pass):
            if 1:
                for item in Data:
                    request.session['admin_id'] = item.admin_id
                    request.session['admin_name'] = item.admin_name
                    request.session['admin_logged_in'] = 'yes'

                if request.POST.get("remember"):
                    response = redirect("Admin Home")
                    response.set_cookie('admin_email', email) 
                    response.set_cookie('admin_password', password)   
                    return response
                
                messages.success(request, 'Logged In Successfully')
                url = '/adminside/'
                return redirect(url)
            else:
                messages.error(request, "password Wrong")
                return redirect('Admin Login')
        else:
            messages.error(request, "Invalid Username & Password.")
            return redirect('Admin Login')
    else:
        return redirect('Admin Login')



def admin_Forgot_Password(request):  
    login=2
    if request.COOKIES.get("admin_email"):
            cookie_email = request.COOKIES['admin_email']
            return render(request, 'master_auth.html',{'login_set':login,'c_email':cookie_email, 'title': 'Forget Password'})
    else:
            return render(request, 'master_auth.html',{'login_set':login, 'title': 'Forget Passoword'})
    
def admin_handle_forgot_password(request):
     domain = request.get_host()
     if request.method == "POST":
        email2 = request.POST['email']
        val = AdminData.objects.filter(admin_email=email2, domain_name = domain).count()
        if val!=1:
            messages.error(request, "Email is Wrong")
            url = f"{reverse('Admin_Forgot_Password')}?email={email2}"
            return redirect(url)
     # ------------mail sending ---------------
        sub = 'OTP from EDUPORTAL'
        otp = random.randint(000000,999999)
        mess = 'YOUR OTP IS {}'.format(otp)
        email_from = settings.EMAIL_HOST_USER
        recp_list = [email2,]
        send_mail(sub,mess,email_from,recp_list)
        daata = AdminData.objects.get(admin_email = email2)
        daata.admin_otp = otp
        daata.save()
        messages.success(request, "Otp Sent Successfully")
        url = f"{reverse('Admin_Set_New_Password')}?email={email2}"
        return redirect(url)
     else:
        return redirect('Admin_Forgot_Password')
    
def admin_Set_New_Password(request):  
    login=3      
    if request.GET['email']:
         foremail = request.GET['email']
    return render(request, 'master_auth.html',{'login_set':login,'email':foremail, 'title': 'New Password'})

def admin_handle_set_new_password(request):
     domain = request.get_host()
     if request.method == "POST":
        otp = int(request.POST['otp'])
        password = request.POST['password']
        conf_password = request.POST['confirm_password']
        if password == conf_password:
             obj = AdminData.objects.filter(admin_otp = otp, domain_name = domain).count()
             if obj == 1:
                  data = AdminData.objects.get(admin_otp = otp)
                  data.admin_pass = password
                  data.admin_otp = None
                  data.save()
                  response = redirect("Admin Login")
                  response.set_cookie('admin_password', '')
                  messages.success(request, "Password has been changed Successfully")
                  return response
             else:
                  messages.error(request, "OTP is Wrong")
                  return redirect('Admin Set New Password')
        else:
             messages.error(request, "Password and Confirm Password are not same.")
             return redirect('Admin Set New Password')  
     else:
        messages.error(request, "Method is not Post")
        return redirect('Admin Set New Password')
 
     
def admin_logout(request):
    try:
        del request.session['admin_id']
        del request.session['admin_name']
        del request.session['admin_logged_in']
        messages.success(request, "Logged out Successfully")
        return redirect("Admin Login")
    except:
        pass
    return redirect("Admin Login")     




# -----------------------------------auth End -------------------------
@admin_login_required
def home(request):
    domain = request.get_host()

    # ================celery_testing========================
    # logger.error("result")
    # # add.delay(10,20)
    # logger.error("=============================================================================================")
    # logger.error("=============================================================================================")
    # result = add.delay(10,20)
    # logger.error(result)
    # logger.error("=============================================================================================")
    # result2 = sub.delay(10,20)
    # logger.error(result2)
    # logger.error("=============================================================================================")
    # logger.error("=============================================================================================")
    # =================================================================
    # sending push Notification
    onesignal_player_id = request.session.get('deviceId', 'Error')
    if onesignal_player_id != 'Error':      
        admindata = AdminData.objects.get(admin_id=1)
        admindata.admin_onesignal_player_id = onesignal_player_id
        # logger.error("============================databaseplayerid:{}".format(admindata.admin_onesignal_player_id))
        admindata.save()
    mess = 'Welcome To miniStudy Admin Dashboard'
    title = 'MiniStudy'

    # send_notification(onesignal_player_id,title,mess,request)

    
    # ----------------------------------------------------------------
    all_students = Students.objects.filter(domain_name = domain).count()

    all_male=Students.objects.filter(stud_gender='Male', domain_name = domain).count()
    all_female=Students.objects.filter(stud_gender='Female', domain_name = domain).count()
    all_other=Students.objects.filter(stud_gender='Other', domain_name = domain).count()
    piechart_category = ['Male','Female','Other']
    piechart_data = [all_male,all_female,all_other]
    stds = Std.objects.filter(domain_name = domain).order_by('-std_board')

    #-----------------------Inquires-----------------------------------------
    total_inquiries = Inquiries.objects.filter(domain_name = domain).values('inq_email').count()
    inquiries = Inquiries.objects.filter(domain_name = domain).values('inq_email')

    count = 0
    for email in inquiries:
        count_st = Students.objects.filter(stud_email = email['inq_email'], domain_name = domain)
        if count_st:
            count += 1
    
    if total_inquiries == 0:
        conversion = 0.0
        lead = 0.0
    else:
        conversion = round((count / total_inquiries) * 100, 2)
        lead = round(100 - conversion, 2)

    std_list = []
    students_for_that_std = []
    for x in stds:
        n = (x.std_name+' '+x.std_board.brd_name)
        std_list.append(n)
        noss = Students.objects.filter(stud_std__std_id=x.std_id, domain_name = domain).count()
        students_for_that_std.append(noss)

    # Performance of all standards
    std_data = Std.objects.filter(domain_name = domain)
    subject_data = Subject.objects.filter(domain_name = domain)
    context = {'std_data': std_data, 'subject_data': subject_data}    



    get_std = request.GET.get('get_std')
    if get_std:
        subject_data = Subject.objects.filter(sub_std__std_id = int(get_std))
        get_std = Std.objects.get(std_id = get_std)
        context.update({'subject_data': subject_data, 'get_std':get_std})
    else:
        get_std = Std.objects.first()
        subject_data = Subject.objects.filter(sub_std__std_id = get_std.std_id)
        context.update({'subject_data': subject_data, 'get_std':get_std})

    get_subject = request.GET.get('get_subject')
    if get_subject:
        get_subject = Subject.objects.get(sub_id = get_subject)
        context.update({'get_subject':get_subject})
    else:
        get_subject = Subject.objects.filter(sub_std__std_id = get_std.std_id).first()
        context.update({'get_subject':get_subject})  

    students_li = Students.objects.filter(stud_std = get_std, domain_name = domain).values('stud_id','stud_name','stud_lastname')
    overall_attendance_li = []
    for x in students_li:
        total_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x['stud_id'], domain_name = domain, atten_timetable__tt_subject1__sub_id = get_subject.sub_id).count()
        present_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x['stud_id'], atten_present=True, domain_name = domain, atten_timetable__tt_subject1__sub_id = get_subject.sub_id).count()
        if total_attendence_studentwise > 0:
            overall_attendence_studentwise = round((present_attendence_studentwise/total_attendence_studentwise)*100,2)
        else:
            overall_attendence_studentwise = 0
        

        total_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x['stud_id'], domain_name = domain, tau_test_id__test_sub__sub_id = get_subject.sub_id).aggregate(total_sum_marks=Sum('tau_total_marks'))['total_sum_marks'] or 0
        
        
        obtained_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x['stud_id'], domain_name = domain, tau_test_id__test_sub__sub_id = get_subject.sub_id).aggregate(total_obtained_marks=Sum('tau_obtained_marks'))['total_obtained_marks'] or 0
        

        if total_marks == 0:
            overall_result = 0
        else:
            overall_result = round((obtained_marks/total_marks)*100,2)

        overall_attendance_li.append({'stud_name':x['stud_name'], 'stud_lastname':x['stud_lastname'], 'overall_attendance_studentwise':overall_attendence_studentwise, 'overall_result':overall_result})

    overall_attendance_li = sorted(overall_attendance_li, key=lambda x: x['overall_result'], reverse=True)
    overall_attendance_li = overall_attendance_li[:5]   
    context.update({'overall_attendance_li':overall_attendance_li})     
    

    context.update({
        'title' : 'Home',
        'all_students':all_students,
        'piechart_category':piechart_category,
        'piechart_data':piechart_data,
        'get_std': get_std,
        'std_list':std_list,
        'students_for_that_std':students_for_that_std,
        'conversion': conversion,
        'lead': lead,
        'domain':domain,
        'total_inquiries':total_inquiries,
        'total_conversion': count,
    })
    return render(request, 'index.html',context)

@admin_login_required
def show_boards(request):
    domain = request.get_host()
    data = Boards.objects.filter(domain_name = domain)
    context ={
        'data' : data,
        'title' : 'Boards',

    }
    return render(request, 'show_boards.html',context)

@admin_login_required
def insert_update_boards(request):
    domain = request.get_host()
    context = {
        'title' : 'Boards',
    }
    if request.GET.get('pk'):
        pk = request.GET['pk']
        instance = get_object_or_404(Boards, pk=pk)
        if request.method == "POST":
            form = brd_form(request.POST, instance=instance)
            if form.is_valid():
                form.instance.domain_name = domain
                check = Boards.objects.filter(domain_name = domain, brd_name = form.instance.brd_name).count()
                if check < 1:
                    form.save()
                    messages.success(request, 'Board Updated Successfully')
                    return redirect('boards')
                else:
                    messages.error(request, 'Board Name Already Exists')
                    filled_data = form.data
                    return render(request, 'insert_update/boards.html', {'filled_data':filled_data})
            else:
                filled_data = form.data
                return render(request, 'insert_update/boards.html', {'errors': form.errors,'filled_data':filled_data})
    
    if request.GET.get('update_id'):
        update_id = request.GET['update_id']
        update_data = Boards.objects.get(brd_id = update_id, domain_name = domain)
        context2 = {
            'update_data' : update_data

        }
        context.update(context2)
        return render(request, 'insert_update/boards.html',context)

    if request.method == "POST":
        form = brd_form(request.POST)
        if form.is_valid():
            form.instance.domain_name = domain
            check = Boards.objects.filter(domain_name = domain, brd_name = form.instance.brd_name).count()
            if check < 1:
                form.save()
                messages.success(request, 'Board Added Successfully')
                return redirect('boards')
            else:
                messages.error(request, 'Board Name Already Exists')
        else:
            filled_data = form.data
            return render(request, 'insert_update/boards.html', {'errors': form.errors,'filled_data':filled_data})
    return render(request, 'insert_update/boards.html',context)

@admin_login_required
def delete_boards(request):
    domain  = request.get_host()
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Boards.objects.filter(brd_id__in=selected_ids, domain_name = domain).delete()
                messages.success(request, 'Board Deleted Successfully')
            except Exception as e:
                messages.error(request, f'<i class="fa-solid fa-triangle-exclamation me-2"></i> An error occurred: {str(e)}')

    return redirect('boards')

# -------------------------Logic for Std-======================

@admin_login_required
def show_stds(request):
    domain = request.get_host()
    data = Std.objects.filter(domain_name = domain)
    context ={
        'data' : data,
        'title' : 'Stds',
    }
    return render(request, 'show_stds.html',context)

def insert_update_stds(request):
    domain = request.get_host()
    brddata = Boards.objects.filter(domain_name = domain)
    context = {
        'title' : 'Stds',
        'brddata':brddata,
    }
    if request.GET.get('pk'):
        pk = request.GET['pk']
        instance = get_object_or_404(Std, pk=pk)
        if request.method == "POST":
            form = std_form(request.POST, instance=instance)
            if form.is_valid():
                form.instance.domain_name = domain
                check = Std.objects.filter(domain_name = domain, std_name = form.instance.std_name, std_board__brd_name = form.instance.std_board).count()
                if check < 1:
                    form.save()
                    messages.success(request, 'Standard Updated Successfully')
                    return redirect('stds')
                else:
                    messages.error(request, 'Standard Already Exists')
                    update_data = Std.objects.get(std_id = pk, domain_name = domain)
                    context.update({'update_data':update_data})
                    return render(request, 'insert_update/stds.html', context)
            else:
                filled_data = form.data
                return render(request, 'insert_update/stds.html', {'errors': form.errors,'filled_data':filled_data})
    
    if request.GET.get('update_id'):
        update_id = request.GET['update_id']
        update_data = Std.objects.get(std_id = update_id, domain_name = domain)
        context.update({'update_data':update_data})
        return render(request, 'insert_update/stds.html',context)

    if request.method == "POST":
        form = std_form(request.POST)
        if form.is_valid():
            form.instance.domain_name = domain
            check = Std.objects.filter(domain_name = domain, std_name = form.instance.std_name, std_board__brd_name = form.instance.std_board).count()
            if check < 1:
                form.save()
                messages.success(request, 'Standard Added Successfully')
                return redirect('stds')
            else:
                messages.error(request, 'Standard Already Exists')
                filled_data = form.data
                context.update({'filled_data':filled_data})
                return render(request, 'insert_update/stds.html', context)
        else:
            filled_data = form.data
            return render(request, 'insert_update/stds.html', {'errors': form.errors,'filled_data':filled_data})
    return render(request, 'insert_update/stds.html',context)


def delete_stds(request):
    domain = request.get_host()
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Std.objects.filter(std_id__in=selected_ids, domain_name = domain).delete()
                messages.success(request, 'Standard Deleted Successfully')
            except Exception as e:
                messages.error(request, f'<div class="bg-danger text-white p-2 rounded-2 returnmessage mb-2" id="returnmessage"><i class="fa-solid fa-triangle-exclamation me-2"></i> An error occurred: {str(e)} </div>')

    return redirect('stds')



@admin_login_required
def show_announcements(request):
    domain = request.get_host()
    data = Announcements.objects.filter(domain_name = domain).order_by('-pk')
    std_data = Std.objects.filter(domain_name = domain)
    batch_data = Batches.objects.filter(domain_name = domain)
   
    context ={
        'data' : data,
        'title' : 'Announcements',
        'std_data' : std_data,
        'batch_data': batch_data,
    }
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(announce_std__std_id = get_std).order_by('-pk')
            batch_data = batch_data.filter(batch_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'batch_data':batch_data,'get_std':get_std})
            

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = data.filter(announce_batch__batch_id = get_batch).order_by('-pk')
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'data':data,'get_batch':get_batch})        
            
    return render(request, 'show_announcements.html',context)



def insert_update_announcements(request):
    domain = request.get_host()
    std_data = Std.objects.filter(domain_name = domain)
    batch_data = Batches.objects.filter(domain_name = domain)
    # ------------getting students for mail------------------
    students_for_mail = Students.objects.filter(domain_name = domain)

    context = {
        'title' : 'Announcements',
        'std_data':std_data,
        'batch_data':batch_data,
    }
    
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        batch_data = batch_data.filter(batch_std__std_id = get_std)
        students_for_mail = students_for_mail.filter(stud_std=get_std)
        context.update({'get_std ':get_std,'std_data':std_data,'batch_data':batch_data}) 
        
    
    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        batch_data = batch_data.filter(batch_id = get_batch)
        students_for_mail = students_for_mail.filter(stud_batch=get_batch)
        context.update({'get_batch ':get_batch,'batch_data':batch_data})

    if request.method == 'POST':
        std_name = request.POST.get('announce_std')
        batch_name = request.POST.get('announce_batch')
        url = '/adminside/announcements/?get_std={}&get_batch={}'.format(std_name,batch_name)
        # ================update Logic============================
        if request.GET.get('pk'):
            instance = get_object_or_404(Announcements, pk=request.GET['pk'])
            form = announcement_form(request.POST, instance=instance)       
            if form.is_valid():
                form.instance.domain_name = domain
                form.save()
                messages.success(request, 'Announcement Updated Successfully')
                return redirect(url)
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})

        # ===================insert_logic===========================
        form = announcement_form(request.POST)
        if form.is_valid():
            form.instance.domain_name = domain 
            form.save()
            messages.success(request, 'Announcement Added Successfully')           
            students_email_list = []
            parents_email_list = []
            onesignal_player_id_list = []
            for x in students_for_mail:
                students_email_list.append(x.stud_email)
                parents_email_list.append(x.stud_guardian_email)
                if x.stud_onesignal_player_id:  
                    onesignal_player_id_list.append(x.stud_onesignal_player_id)
                if x.stud_telegram_studentchat_id:    
                    # announcement_telegram_message_student(x.stud_telegram_studentchat_id, form.cleaned_data['announce_msg'],form.cleaned_data['announce_title'])
                    # announcement_telegram_message_parent(x.stud_telegram_parentschat_id, form.cleaned_data['announce_msg'],form.cleaned_data['announce_title'])
                    pass

            # htmly = get_template('Email/announcement.html')
            htmly = mail_templates.objects.get(mail_temp_type = 'Announcement_mail', mail_temp_selected=1).mail_temp_html
            context_data={}
            if domain != '127.0.0.1:8000':
                Institute_data = NewInstitution.objects.get(institute_domain = domain)
                
                logo = '{}/media/{}'.format(domain,Institute_data.institute_logo)
                context_data.update({
                    'logo':logo,
                    'institute_name':Institute_data.institute_name,
                    'institute_email':Institute_data.institute_email,
                    'institute_number':Institute_data.institute_contact
                })
            else:
                logo = 'api.ministudy.in/static/imgs/My_dream_logo/logo_text_sidebyside_dark.png'
                context_data.update({
                    'logo':logo,
                    'institute':'miniStudy',
                    'email':'mail.trushalpatel@gmail.com',
                    'phone_num':'8511962611',
                })
                

            context_data.update({
            'title': form.cleaned_data['announce_title'],
            'msg': form.cleaned_data['announce_msg'],
            
            })
            htmly = Template(htmly)
            html_content = htmly.render(Context(context_data))     
            announcement_mail.delay(students_email_list, html_content)
            announcement_mail.delay(parents_email_list, html_content)
            # -------------One Single Player Id------------------------------------------------------------------------

            title = 'New Announcement'
            mess = f"{form.cleaned_data['announce_title']}: {form.cleaned_data['announce_msg']}"

            for player_id in onesignal_player_id_list:
                send_notification(player_id,title,mess,request)
                
            notification = Notification(
            notify_title=title,
            notify_notification=mess,
            notify_user = 'student',
            domain_name=domain)
            notification.save()

            

            # -------------One Single Player Id------------------------------------------------------------------------       
            return redirect(url)         
        else:
            filled_data = form.data
            context.update({'filled_data ':filled_data,'errors':form.errors})
            return render(request, 'insert_update/announcements.html', context)

    if request.GET.get('pk'):
        update_data = Announcements.objects.get(announce_id = request.GET['pk'])
        context.update({'update_data':update_data})
    return render(request, 'insert_update/announcements.html',context)

def delete_announcements(request):
    domain = request.get_host()
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Announcements.objects.filter(announce_id__in=selected_ids, domain_name = domain).delete()
                messages.success(request, 'Announcements Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_announcements')



@admin_login_required
def show_subjects(request):
    domain = request.get_host()
    data = Subject.objects.filter(domain_name = domain).values('sub_id','sub_name','sub_std__std_name','sub_std__std_board__brd_name')
    std_data = Std.objects.filter(domain_name = domain)
   
    context ={
        'data' : data,
        'title' : 'Subjects',
        'std_data' : std_data,
    }
    get_std = request.GET.get('get_std')

    if get_std is not None:
        try:
            get_std = int(get_std)
            if get_std == 0:
                pass
            else:
                data = data.filter(sub_std__std_id=get_std)
                get_std_instance = Std.objects.get(std_id=get_std)
                context.update({'data': data, 'get_std': get_std_instance}) 
        except ValueError:
            context.update({'error': 'Invalid standard ID provided.'})

    return render(request, 'show_subjects.html', context)


def insert_update_subjects(request):
    domain = request.get_host()
    std_data = Std.objects.filter(domain_name = domain)
    
    context = {
        'title' : 'Insert Subjects',
        'std_data':std_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        context.update({'get_std ':get_std,'std_data':std_data}) 


 # ================update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            sub_std = request.POST.get('sub_std')
            url = '/adminside/admin_subjects/?get_std={}'.format(sub_std)
            instance = get_object_or_404(Subject, pk=request.GET['pk'])
            form = subject_form(request.POST, instance=instance)
            check = Subject.objects.filter(sub_name = form.data['sub_name'], sub_std__std_id = form.data['sub_std']).count()
            if check >= 1:
                messages.error(request,'{} is already Exists'.format(form.data['sub_name']))
            else:
                if form.is_valid():
                    form.instance.domain_name = domain
                    form.save()
                    messages.success(request, 'Subject Updated Successfully')
                    form.instance.domain_name = domain
                    return redirect(url)
                else:
                    filled_data = form.data
                    context.update({'filled_data ':filled_data,'errors':form.errors})
        
        update_data = Subject.objects.get(sub_id = request.GET['pk'])
        context.update({'update_data':update_data})  
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            sub_std = request.POST.get('sub_std')
            url = '/adminside/admin_subjects/?get_std={}'.format(sub_std)
            form = subject_form(request.POST)
            if form.is_valid():
                check = Subject.objects.filter(sub_name = form.data['sub_name'], sub_std__std_id = form.data['sub_std']).count()
                if check >= 1:
                    messages.error(request,'{} is already Exists'.format(form.data['sub_name']))
                else:  
                    form.instance.domain_name = domain  
                    form.save()
                    messages.success(request, 'Subject Added Successfully')
                    return redirect(url)
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
                return render(request, 'insert_update/subjects.html', context) 
        
    return render(request, 'insert_update/subjects.html',context)                     

def delete_subjects(request):
    domain = request.get_host()
    if request.method == 'POST': 
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Subject.objects.filter(sub_id__in=selected_ids, domain_name = domain).delete()
                messages.success(request, 'Subjects Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    return redirect('admin_subjects')


@admin_login_required
def show_chepters(request):
    domain = request.get_host()
    data = Chepter.objects.filter(domain_name = domain).values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name','chep_sub__sub_std__std_id')
    std_data = Std.objects.filter(domain_name = domain)
    subject_data = Subject.objects.filter(domain_name = domain)

    data = paginatoorrr(data, request)
    context ={
        'data' : data,
        'title' : 'Chepters',
        'std_data' : std_data,
        'subject_data':subject_data,
    }
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = Chepter.objects.filter(chep_sub__sub_std__std_id = get_std, domain_name = domain).values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name','chep_sub__sub_std__std_id')
            data = paginatoorrr(data, request)
            subject_data = subject_data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'get_std':get_std,'std_data':std_data,'subject_data':subject_data}) 


    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        if get_subject == 0:
            pass
        else:    
            data =  Chepter.objects.filter(chep_sub__sub_id = get_subject, domain_name = domain).values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name','chep_sub__sub_std__std_id')
            data = paginatoorrr(data, request)
            get_subject = Subject.objects.get(sub_id = get_subject)
            context.update({'data':data,'subject_data':subject_data,'get_subject':get_subject}) 


    if request.GET.get('searchhh'):
        searchhh = request.GET['searchhh']
        if searchhh:
            data = Chepter.objects.filter(
            Q(chep_name__icontains=searchhh) |
            Q(chep_sub__sub_name__icontains=searchhh) |
            Q(chep_sub__sub_std__std_name__icontains=searchhh), domain_name = domain).values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name','chep_sub__sub_std__std_id')
            data = paginatoorrr(data, request)
            context.update({'data':data,'searchhh':searchhh})      

    return render(request, 'show_chepters.html',context)



def insert_update_chepters(request):
    domain = request.get_host()
    std_data = Std.objects.filter(domain_name = domain)
    subject_data = Subject.objects.filter(domain_name = domain)
    context = {
        'title' : 'Chepters',
        'std_data':std_data,
        'subject_data':subject_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        context.update({'get_std ':get_std,'std_data':std_data})

    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        subject_data = subject_data.filter(sub_id = get_subject)
        context.update({'get_subject':get_subject,'subject_data':subject_data})     


   

 # ================update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            chep_std = request.POST.get('chep_std')
            chep_sub = request.POST.get('chep_sub')

            url = '/adminside/admin_chepters/?get_std={}&get_subject={}'.format(chep_std, chep_sub)

            instance = get_object_or_404(Chepter, pk=request.GET['pk'])
            form = chepter_form(request.POST,request.FILES, instance=instance)
            check = Chepter.objects.filter(chep_name = form.data['chep_name'], chep_std__std_id = form.data['chep_std'], domain_name = domain).count()
            if check >= 1:
                messages.error(request,'{} is already Exists'.format(form.data['chep_name']))
            else:
                if form.is_valid():
                    form.instance.domain_name = domain
                    form.save()
                    messages.success(request, 'Chapter Updated Successfully')
                    return redirect(url)
                else:
                    filled_data = form.data
                    context.update({'filled_data ':filled_data,'errors':form.errors})
        update_data = Chepter.objects.get(chep_id = request.GET['pk'])
        context.update({'update_data':update_data}) 
        
        update_data = Chepter.objects.get(chep_id = request.GET['pk'])
        context.update({'update_data':update_data})  
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            chep_std = request.POST.get('chep_std')
            chep_sub = request.POST.get('chep_sub')

            url = '/adminside/admin_chepters/?get_std={}&get_subject={}'.format(chep_std, chep_sub)
            form = chepter_form(request.POST, request.FILES)
            if form.is_valid():
                check = Chepter.objects.filter(chep_name = form.data['chep_name'], chep_std__std_id = form.data['chep_std'], domain_name = domain).count()
                if check >= 1:
                    messages.error(request,'{} is already Exists'.format(form.data['chep_name']))
                else:    
                    form.instance.domain_name = domain
                    form.save()
                    messages.success(request, 'Chapter Added Successfully')
                    return redirect(url)
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
                return render(request, 'insert_update/add_chepters.html', context) 
        
    return render(request, 'insert_update/add_chepters.html',context)                

        
        

def delete_chepters(request):
    domain = request.get_host()
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Chepter.objects.filter(chep_id__in=selected_ids, domain_name = domain).delete()
                messages.success(request, 'Chapters Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_chepters')




@admin_login_required
def show_faculties(request):
    domain = request.get_host()
    faculties = Faculties.objects.filter(domain_name = domain)
    faculties = paginatoorrr(faculties,request)
    faculty_data = Faculties.objects.filter(domain_name = domain)
    faculty_access_data = Faculty_Access.objects.filter(domain_name = domain)
    context = {
        'faculty_data':faculty_data,
        'faculty_access_data':faculty_access_data,
        'title': 'Faculties'
    }

    if request.GET.get('searchhh'):
        searchhh = request.GET['searchhh']
        if searchhh:
            faculty_data = Faculties.objects.filter(
            Q(fac_name__icontains=searchhh) |
            Q(fac_number__icontains=searchhh) |
            Q(fac_email__icontains=searchhh) |
            Q(fac_address__icontains=searchhh) |
            Q(Subjects__icontains=searchhh), domain_name = domain)
            faculty_data = paginatoorrr(faculty_data, request)
            context.update({'faculty_data':faculty_data,'searchhh':searchhh})  

    return render(request, 'show_faculties.html', context)

@admin_login_required
def view_faculty_access(request):
    domain = request.get_host()
    if request.GET.get('fac_id'):
        fac_id = request.GET.get('fac_id')
        faculty_data = Faculties.objects.get(fac_id = fac_id)
        faculty_access_data = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)
        context = {
            'faculty_data':faculty_data,
            'faculty_access_data':faculty_access_data,
            'title': 'Access'
        }
        return render(request, 'view_faculty_access.html', context)

@admin_login_required
def delete_faculty_access(request):
    if request.GET.get('fac_access_id'):
        fac_access_id = request.GET.get('fac_access_id')

        faculty_access_del = get_object_or_404(Faculty_Access, fa_id=fac_access_id)
        faculty_access_del.delete()
        messages.success(request, "Access deleted successfully")
        url = '/adminside/view_faculty_access/?fac_id={}'.format(request.GET['fac_id']) 
        return redirect(url)


@admin_login_required
def insert_update_faculties(request):
    domain = request.get_host()
    group_data = Groups.objects.filter(domain_name = domain)
    context = {
        'title': 'Faculties',
        'group_data':group_data,
    }
    # Update Logic
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Faculties, pk=request.GET['pk'])
            form = faculty_form(request.POST, instance=instance)
            check = Faculties.objects.filter(fac_email=form.data['fac_email']).exclude(pk=request.GET['pk'], domain_name = domain).count()
            if check >= 1:
                messages.error(request, '{} is already Exists'.format(form.data['fac_email']))
            else:
                if form.is_valid():
                    form.instance.domain_name = domain
                    form.save()
                    messages.success(request, 'Faculty Updated Successfully')
                    return redirect('admin_faculties')
                else:
                    filled_data = form.data
                    context.update({'filled_data': filled_data, 'errors': form.errors})

        update_data = Faculties.objects.get(fac_id=request.GET['pk'])
        context.update({'update_data': update_data})
    else:
        # Insert Logic
        if request.method == 'POST':
            form = faculty_form(request.POST)
            if form.is_valid():
                check = Faculties.objects.filter(fac_email=form.data['fac_email']).count()
                if check >= 1:
                    messages.error(request, '{} is already Exists'.format(form.data['fac_email']))
                else:
                    hashed_password = make_password('123456')
                    form.instance.admin_pass = hashed_password
                    form.instance.domain_name = domain
                    form.instance.fac_email = request.POST.get('fac_email')
                    instance = form.save()
                    # ------------------give access to Faculties====================
                    selected_groups = request.POST.getlist('material_group[]')
                    for x in selected_groups:
                        group_obj = Groups.objects.get(group_id = int(x))
                        Materials_access.objects.update_or_create(
                            materialaccess_email=request.POST.get('fac_email').lower(),
                            materialaccess_group=group_obj,
                            defaults={'domain_name': domain}
                        )
                    # ======================================================
                    fac_password = instance.fac_password
                    fac_name = form.cleaned_data['fac_name']
                    fac_email = [form.cleaned_data['fac_email']]

                    htmly = mail_templates.objects.get(mail_temp_type = 'Faculty_mail', mail_temp_selected=1).mail_temp_html
                    context_data={}
                    if domain != '127.0.0.1:8000':
                        Institute_data = NewInstitution.objects.get(institute_domain = domain)
                        
                        logo = '{}/media/{}'.format(domain,Institute_data.institute_logo)
                        context_data.update({
                            'logo':logo,
                            'institute_name': Institute_data.institute_name,
                            'institute_email': Institute_data.institute_email,
                            'institute_number': Institute_data.institute_contact,
                        })
                    else:
                        logo = 'api.ministudy.in/static/imgs/My_dream_logo/logo_text_sidebyside_dark.png'
                        context_data.update({
                            'logo':logo,
                            'institute':'miniStudy',
                            'email':'mail.trushalpatel@gmail.com',
                            'phone_num':'8511962611',
                        })

                    context_data.update({
                    'title': "Student Register",
                    'name': fac_name,
                    'password': fac_password
                    })
                    htmly = Template(htmly)
                    html_content = htmly.render(Context(context_data))
                    faculty_email.delay(fac_email, html_content)

                    messages.success(request, 'Faculty Added Successfully')
                    return redirect('admin_faculties')
            else:
                filled_data = form.data
                context.update({'filled_data': filled_data, 'errors': form.errors})
    return render(request, 'insert_update/faculties.html', context)



@admin_login_required
def delete_faculties(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Faculties.objects.filter(fac_id__in=selected_ids).delete()
                messages.success(request, 'Faculties Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_faculties')

@admin_login_required
def show_timetable(request):
    domain = request.get_host()
    data = Timetable.objects.filter(domain_name = domain)
    std_data = Std.objects.filter(domain_name = domain)
    batch_data = Batches.objects.filter(domain_name = domain)

    context = {
        'data': data,
        'title': 'Timetable',
        'std_data': std_data,
        'batch_data': batch_data,
    }
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std != 0:  
            data = data.filter(tt_batch__batch_std__std_id=get_std)
            batch_data = batch_data.filter(batch_std__std_id=get_std)
            get_std = Std.objects.get(std_id=get_std)
            context.update({'data': data, 'batch_data': batch_data, 'get_std': get_std})

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch != 0:
            data = data.filter(tt_batch__batch_id=get_batch)
            get_batch = Batches.objects.get(batch_id=get_batch)
            context.update({'data': data, 'get_batch': get_batch})        
            
    return render(request, 'show_timetable.html', context)

def insert_update_timetable(request):
    domain = request.get_host()
    std_data = Std.objects.filter(domain_name = domain)

    batch_data = Batches.objects.filter(domain_name = domain)
    faculty_data = Faculties.objects.filter(domain_name = domain)
    subject_data = Subject.objects.filter(domain_name = domain)
    tt_students_for_mail = Students.objects.filter(domain_name = domain)

    context = {
        'title': 'Timetable',
        'std_data': std_data,
        'batch_data': batch_data,
        'subject_data':subject_data,
        'faculty_data':faculty_data,
        'DaysChoice': Timetable.DaysChoice,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id=get_std, domain_name = domain)
        subject_data = Subject.objects.filter(sub_std__std_id = get_std, domain_name = domain)
        batch_data = batch_data.filter(batch_std__std_id=get_std, domain_name = domain)
        tt_students_for_mail = tt_students_for_mail.filter(stud_std=get_std, domain_name = domain)
        context.update({'get_std': get_std, 'std_data': std_data, 'batch_data': batch_data, 'subject_data':subject_data, 'tt_students_for_mail':tt_students_for_mail})
        

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        batch_data = batch_data.filter(batch_id=get_batch, domain_name = domain)
        tt_students_for_mail = tt_students_for_mail.filter(stud_batch=get_batch, domain_name = domain)
        context.update({'get_batch': get_batch, 'batch_data': batch_data, 'tt_students_for_mail':tt_students_for_mail})


    
    # Update logic
    if request.GET.get('pk'):
        instance = get_object_or_404(Timetable, pk=request.GET['pk'])
        if request.method == 'POST':
            tt_batch = request.POST.get('tt_batch')
            url = '/adminside/admin_timetable/?get_batch={}'.format(tt_batch)
            form = timetable_form(request.POST, instance=instance)
            if form.is_valid():
                form.instance.domain_name = domain
                messages.success(request, "Timetable updated successfully")
                form.save()             
                # ---------------------sendmail Logic===================================
                tt_students_email_list = []
                student_chat_ids = []
                parent_chat_ids = []
                onesignal_player_id_list = []
                for x in tt_students_for_mail:
                    tt_students_email_list.append(x.stud_email)
                    student_chat_ids.append(x.stud_telegram_studentchat_id)
                    parent_chat_ids.append(x.stud_telegram_parentschat_id)
                    if x.stud_onesignal_player_id:
                        onesignal_player_id_list.append(x.stud_onesignal_player_id)

                
                htmly = mail_templates.objects.get(mail_temp_type = 'Timetable_mail', mail_temp_selected=1).mail_temp_html
                context_data={}
                if domain != '127.0.0.1:8000':
                    Institute_data = NewInstitution.objects.get(institute_domain = domain)
                    
                    logo = '{}/media/{}'.format(domain,Institute_data.institute_logo)
                    context_data.update({
                        'logo':logo,
                        'institute_name': Institute_data.institute_name,
                        'institute_email': Institute_data.institute_email,
                        'institute_number': Institute_data.institute_contact,
                    })
                else:
                    logo = 'api.ministudy.in/static/imgs/My_dream_logo/logo_text_sidebyside_dark.png'
                    context_data.update({
                        'logo':logo,
                        'institute':'miniStudy',
                        'email':'mail.trushalpatel@gmail.com',
                        'phone_num':'8511962611',
                    })
                context_data.update({
                'title': 'Time Table Updated',
                'msg': 'Your time table has been updated!',
                })
                htmly = Template(htmly)
                html_content = htmly.render(Context(context_data))     
                timetable_mail(tt_students_email_list, html_content)

                # ------------------------ Telegram Message -------------------------------
                timetable_telegram_message_student(student_chat_ids)
                timetable_telegram_message_parent(parent_chat_ids)

                # ------------------------ Notification Updated --------------------------
                mess = 'Your timetable has been updated.'
                title = 'Timetable Updated!'
                notification = Notification(
                notify_title=title,
                notify_notification=mess,
                notify_user = 'student',
                domain_name=domain)
                notification.save()

                for palayer_id in onesignal_player_id_list:
                    send_notification(palayer_id,title,mess, request)
                return redirect(url)
            else:
                filled_data = form.data
                context.update({'filled_data': filled_data, 'errors': form.errors})


    if request.GET.get('pk'):
        update_data = Timetable.objects.get(tt_id=request.GET['pk'])
        context.update({'update_data': update_data})
        return render(request, 'insert_update/timetable.html', context)

    # Insert logic
    if request.method == 'POST':
        form = timetable_form(request.POST)
        if form.is_valid():
            tt_batch = request.POST.get('tt_batch')
            url = '/adminside/admin_timetable/?get_batch={}'.format(tt_batch)
            form.instance.domain_name = domain
            form.save()
            return redirect(url)
        else:
            filled_data = form.data
            context.update({'filled_data': filled_data, 'errors': form.errors})
            return render(request, 'insert_update/timetable.html', context)
    return render(request, 'insert_update/timetable.html', context)

    

def delete_timetable(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Timetable.objects.filter(tt_id__in=selected_ids).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_timetable')

@admin_login_required
def show_attendance(request):
    domain = request.get_host()
    data = Attendance.objects.filter(domain_name = domain)
    std_data = Std.objects.filter(domain_name = domain)
    batch_data = Batches.objects.filter(domain_name = domain)
    stud_data = Students.objects.filter(domain_name = domain)
    subj_data = Subject.objects.filter(domain_name = domain)
    
    context ={
        'data' : data,
        'title' : 'Attendance',
        'std_data' : std_data,
        'batch_data':batch_data,
        'stud_data':stud_data,
        'sub_data':subj_data,
    }

    
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(atten_timetable__tt_batch__batch_std__std_id = get_std)
            batch_data = batch_data.filter(batch_std__std_id = get_std)
            stud_data = stud_data.filter(stud_std__std_id = get_std)
            subj_data = subj_data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'batch_data':batch_data,'get_std':get_std,'stud_data':stud_data,'sub_data':subj_data})
           

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = data.filter(atten_timetable__tt_batch__batch_id = get_batch, domain_name = domain)
            stud_data = stud_data.filter(stud_batch__batch_id = get_batch)
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'data':data,'get_batch':get_batch,'stud_data':stud_data}) 

    if request.GET.get('get_student'):
        get_student = int(request.GET['get_student'])
        if get_student == 0:
            pass
        else:
            data = data.filter(atten_student__stud_id = get_student, domain_name = domain)
            get_student = Students.objects.get(stud_id = get_student)
            context.update({'data':data,'get_student':get_student})      

    if request.GET.get('atten_date'):
        atten_date = request.GET.get('atten_date')
        context.update({'atten_date':atten_date})
        if atten_date:
            atten_date = datetime.datetime.strptime(atten_date, '%Y-%m-%d').date()
            data = data.filter(atten_date__date=atten_date, domain_name=domain)
            try:
                atten_obj = Attendance.objects.get(atten_date=atten_date)
                get_date = atten_obj.atten_date
            except ObjectDoesNotExist:
                get_date = None
            context.update({'data': data, 'get_date': get_date})               

    if request.GET.get('searchhh'):
        searchhh = request.GET['searchhh']
        if searchhh:
            data = data.filter(
            Q(atten_timetable__tt_day__icontains=searchhh) |
            Q(atten_timetable__tt_time1__icontains=searchhh) |
            Q(atten_timetable__tt_subject1__sub_name__icontains=searchhh) |
            Q(atten_timetable__tt_tutor1__fac_name__icontains=searchhh) |
            Q(atten_present__icontains=searchhh) |
            Q(atten_student__stud_name__icontains=searchhh) |
            Q(atten_student__stud_lastname__icontains=searchhh) |
            Q(atten_date__icontains=searchhh), domain_name = domain)
            
            context.update({'data':data,'searchhh':searchhh}) 
    data = context['data'].values('atten_id', 'atten_timetable__tt_day', 'atten_timetable__tt_time1', 'atten_date', 'atten_timetable__tt_subject1__sub_name','atten_timetable__tt_tutor1__fac_name', 'atten_present', 'atten_student__stud_name', 'atten_student__stud_lastname', 'atten_student__stud_roll_no').order_by('-atten_date', '-atten_timetable__tt_time1')
    data = paginatoorrr(data, request)
    context.update({'data': data}) 

    attendance_present = Attendance.objects.filter(atten_present = True, domain_name = domain).count()
    attendance_all = Attendance.objects.filter(domain_name = domain).count()
    if attendance_all>0:
        overall_attendance = round((attendance_present/attendance_all) * 100,2)
        context.update({'overall_attendance':overall_attendance})

    sub_list = subj_data.filter(domain_name = domain).values('sub_name').distinct()
    subject_wise_attendance = []
    subjects = []
    for x in sub_list:
        sub_name = x['sub_name']
        sub_one = Attendance.objects.filter(atten_present = True,atten_timetable__tt_subject1__sub_name=sub_name, domain_name = domain).count()
        sub_all = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = sub_name, domain_name = domain).count()
        if sub_all>0:
            sub_attendance = round((sub_one/sub_all) * 100, 2)
            subject_wise_attendance.append(sub_attendance)
            subjects.append(sub_name)
            
    combined_data = zip(subject_wise_attendance, subjects)

    context.update({'combined_data': combined_data})
    
    attendance_list = []

    for id in Students.objects.filter(domain_name = domain):
        if request.GET.get("month"):
            selected_month = request.GET.get("month")
            selected_month_name = request.GET.get("month_name")
            get_student_records = Attendance.objects.filter(atten_student__stud_id=id.stud_id, atten_date__month=selected_month, domain_name = domain)
            context.update({'selected_month': selected_month_name})
        else:
            get_student_records = Attendance.objects.filter(atten_student__stud_id=id.stud_id, atten_date__month=1, domain_name = domain)
        
        # Initialize a dictionary for each student to store their name and attendance
        attendance_disc = {
            'Name': id.stud_name,
            'Roll': id.stud_roll_no,
            'Attendance': {},
            'Present_counter': 0,
            'Absent_counter': 0,
        }

        # Loop through each day of the month (1 to 31)
        for day in range(1, 32):
            # Default to "Absent" for each day, will update to "Present" if record is found
            attendance_disc['Attendance'][day] = ''
            a_list = []
            for stud in get_student_records:
                if stud.atten_date.day == day:
                    # Update attendance status for this day if a record is found
                    tt = 'Present' if stud.atten_present else 'Absent'
                    if stud.atten_present == 1:
                        attendance_disc['Present_counter'] += 1
                    elif stud.atten_present == 0:
                        attendance_disc['Absent_counter'] += 1
                    a_list.append({"attendance_status": tt, "subject_name": stud.atten_timetable.tt_subject1.sub_name, "time": stud.atten_timetable.tt_time1})
                    # Stop searching once the attendance is found for the day
            attendance_disc['Attendance'][day] = a_list
        # Add the completed dictionary for the student to the attendance list
        attendance_list.append(attendance_disc)

    # Output attendance list
    days_list = list(range(1, 32))
    context.update({'attendance_list': attendance_list, 'days': days_list})

    return render(request, 'show_attendance.html',context)


@admin_login_required
def show_events(request):
    domain = request.get_host()
    events = Event.objects.filter(domain_name = domain).values('event_id', 'event_name')
    events_imgs = Event_Image.objects.filter(domain_name = domain)
    selected_events = Event.objects.first()
 
    context = {
        'events':events,
        'events_imgs':events_imgs,
        'selected_events':selected_events,
        'title' : 'Events',
    }
    if request.GET.get('event_id'):
        event_id = request.GET['event_id']
        selected_events = Event.objects.get(event_id = event_id)
        events_imgs = Event_Image.objects.filter(event__event_id = event_id)
        context.update({'selected_events':selected_events,'events_imgs':events_imgs})
    return render(request, 'show_events.html',context)

@admin_login_required
def insert_events(request):
    domain = request.get_host()
    title = 'Insert Events'
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        event_desc = request.POST.get('event_desc')
        event_images = request.FILES.getlist('event_img')
        event = Event(event_name=event_name, event_date=event_date, event_desc=event_desc, domain_name = domain)
        event.save()
        messages.success(request, 'Event Added Successfully')


        from django.utils.dateformat import format
        from django.utils.dateparse import parse_date

        event_date_parsed = parse_date(event_date)
        formatted_event_date = format(event_date_parsed, 'F j, Y')

        #------------------Telegram and Mail Message----------------------------------------------
        student_chat_ids = Students.objects.filter(domain_name = domain).values_list('stud_telegram_studentchat_id', flat=True)
        student_player_id = Students.objects.filter(domain_name = domain)
        student_email_ids = Students.objects.filter(domain_name = domain).values_list('stud_email', flat=True)
        
        event_telegram_message_student(event_name,formatted_event_date, student_chat_ids)
        event_telegram_message_parent(event_name,formatted_event_date, student_email_ids)

        title = "New Event : {}".format(event_name)
        msg = f"We have added Latest Event Information, Please Check it out."
        notification = Notification(
        notify_title=title,
        notify_notification=msg,
        notify_user = 'student',
        domain_name=domain)
        notification.save()
        for x in student_player_id:
            if x.stud_onesignal_player_id:
                send_notification(x.stud_onesignal_player_id, title, msg, request)
            if x.guardian_onesignal_player_id:    
                send_notification(x.guardian_onesignal_player_id, title, msg, request)
        #-------------------------End-------------------------------------------------------------
        fs = FileSystemStorage(location='media/uploads/events/')
        for image in event_images:
            filename = fs.save(image.name, image)
            Event_Image.objects.create(event=event, event_img=filename, domain_name = domain)
        return redirect('show_events')
    return render(request, 'insert_update/events_insert_admin.html', {'title':title})

def delete_event(request):
    if request.GET.get('event_id'):
        event_id = request.GET.get('event_id')
        event_data_del = get_object_or_404(Event, event_id=event_id)
        event_data_del.delete()
        messages.success(request, "Event deleted successfully")
        return redirect('show_events')

@admin_login_required
def show_tests(request):
    domain = request.get_host()
    data = Chepterwise_test.objects.filter(domain_name = domain).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage')).values('test_sub__sub_name','num_questions','total_marks','test_std__std_name','test_std__std_board__brd_name','test_name','test_id')
    std_data = Std.objects.filter(domain_name = domain)
    subject_data = Subject.objects.filter(domain_name = domain)
    data = paginatoorrr(data, request)
    context ={
        'data' : data,
        'title' : 'Tests',
        'std_data' : std_data,
        'subject_data':subject_data,
    }
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = Chepterwise_test.objects.filter(test_sub__sub_std__std_id = get_std, domain_name = domain).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage')).values('test_sub__sub_name','num_questions','total_marks','test_std__std_name','test_std__std_board__brd_name','test_name','test_id')
            data = paginatoorrr(data, request)
            subject_data = subject_data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'get_std':get_std,'std_data':std_data,'subject_data':subject_data}) 


    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        if get_subject == 0:
            pass
        else:    
            data = Chepterwise_test.objects.filter(test_sub__sub_id = get_subject, domain_name = domain).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage')).values('test_sub__sub_name','num_questions','total_marks','test_std__std_name','test_std__std_board__brd_name','test_name','test_id')
            data = paginatoorrr(data, request)
            get_subject = Subject.objects.get(sub_id = get_subject)
            context.update({'data':data,'subject_data':subject_data,'get_subject':get_subject}) 

    if request.GET.get('searchhh'):
        searchhh = request.GET['searchhh']
        if searchhh:
            data = Chepterwise_test.objects.filter(
            Q(test_name__icontains=searchhh) |
            Q(test_sub__sub_name__icontains=searchhh) |
            Q(test_std__std_name__icontains=searchhh), domain_name = domain).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage')).values('test_sub__sub_name','num_questions','total_marks','test_std__std_name','test_std__std_board__brd_name','test_name','test_id')
            data = paginatoorrr(data, request)
            context.update({'data':data,'searchhh':searchhh}) 

    return render(request, 'show_tests.html',context)


def insert_update_tests(request):
    domain = request.get_host()
    std_data = Std.objects.filter(domain_name = domain)
    subject_data = Subject.objects.filter(domain_name = domain)
    chap_data = Chepter.objects.filter(domain_name = domain).values('chep_name','chep_id','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name')
    context = {
        'title': 'Tests',
        'std_data': std_data,
        'subject_data': subject_data,
        'chap_data': chap_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id=get_std)
        subject_data = subject_data.filter(sub_std__std_id=get_std)
        chap_data = Chepter.objects.filter(chep_std__std_id = get_std, domain_name = domain).values('chep_name','chep_id','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name')
        context.update({'get_std': get_std, 'std_data': std_data,'subject_data':subject_data,'chap_data':chap_data})

    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        subject_data = subject_data.filter(sub_id=get_subject)
        chap_data = Chepter.objects.filter(chep_sub__sub_id = get_subject, domain_name = domain).values('chep_name','chep_id','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name')

        context.update({'get_subject': get_subject, 'subject_data': subject_data,'chap_data':chap_data})

    # Update Logic
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Chepterwise_test, pk=request.GET['pk'])
            form = tests_form(request.POST, instance=instance)
            check = Chepterwise_test.objects.filter(test_name=form.data['test_name'], test_std__std_id=form.data['test_std'], domain_name = domain).count()
            if check >= 1:
                messages.error(request, '{} already exists'.format(form.data['test_name']))
            else:
                if form.is_valid():
                    form.instance.domain_name = domain
                    form.save()
                    return redirect('admin_tests')
                else:
                    filled_data = form.data
                    context.update({'filled_data': filled_data, 'errors': form.errors})
        
        update_data = Chepterwise_test.objects.get(test_id=request.GET['pk'])
        context.update({'update_data': update_data})

    else:
        # Insert Logic
        if request.method == 'POST':
            form = tests_form(request.POST, request.FILES)
            if form.is_valid():
                check = Chepterwise_test.objects.filter(
                    test_name=form.data['test_name'], test_std__std_id=form.data['test_std']
                ).count()
                if check >= 1:
                    messages.error(request, '{} already exists'.format(form.data['test_name']))
                else:
                    form.instance.domain_name = domain
                    test_instance = form.save()

                    # Check for auto-generate test
                    if request.POST.get('auto_generate_test'):
                        one_mark_count = int(request.POST.get('one_mark_questions', 0))
                        two_mark_count = int(request.POST.get('two_mark_questions', 0))
                        three_mark_count = int(request.POST.get('three_mark_questions', 0))
                        four_mark_count = int(request.POST.get('four_mark_questions', 0))
                        chap_object = Chepter.objects.get(chep_id = request.POST.get('test_chap'))

                        # Function to get questions by weightage
                        def get_questions_by_weightage(weightage, count):
                            return question_bank.objects.filter(
                                qb_chepter = chap_object.chep_name,
                                qb_std = chap_object.chep_std.std_name,
                                qb_subject = chap_object.chep_sub.sub_name,
                                qb_weightage=weightage,
                            ).order_by('?')[:count]

                        # Retrieve questions based on weightage
                        one_mark_questions = get_questions_by_weightage(1, one_mark_count)
                        two_mark_questions = get_questions_by_weightage(2, two_mark_count)
                        three_mark_questions = get_questions_by_weightage(3, three_mark_count)
                        four_mark_questions = get_questions_by_weightage(4, four_mark_count)

                        # Insert the generated questions into Test_questions_answer
                        for question in one_mark_questions:
                            chep_id = Chepter.objects.get(chep_name = question.qb_chepter, domain_name = domain)
                            Test_questions_answer.objects.create(     
                                tq_name=test_instance,
                                tq_chepter=chep_id,
                                tq_q_type=Test_questions_answer.que_type.Question_Answer,
                                tq_question=question.qb_question,
                                tq_answer=question.qb_answer,
                                tq_weightage=1,
                                tq_hint=question.qb_hint,
                                tq_optiona=question.qb_optiona,
                                tq_optionb=question.qb_optionb,
                                tq_optionc=question.qb_optionc,
                                tq_optiond=question.qb_optiond,
                                domain_name = domain,
                            )

                        for question in two_mark_questions:
                            chep_id = Chepter.objects.get(chep_name = question.qb_chepter, domain_name = domain)
                            Test_questions_answer.objects.create(
                                tq_name=test_instance,
                                tq_chepter=chep_id,
                                tq_q_type=Test_questions_answer.que_type.Question_Answer,
                                tq_question=question.qb_question,
                                tq_answer=question.qb_answer,
                                tq_weightage=2,
                                tq_hint=question.qb_hint,
                                tq_optiona=question.qb_optiona,
                                tq_optionb=question.qb_optionb,
                                tq_optionc=question.qb_optionc,
                                tq_optiond=question.qb_optiond,
                                domain_name = domain
                            )

                        for question in three_mark_questions:
                            chep_id = Chepter.objects.get(chep_name = question.qb_chepter, domain_name = domain)
                            Test_questions_answer.objects.create(
                                tq_name=test_instance,
                                tq_chepter=chep_id,
                                tq_q_type=Test_questions_answer.que_type.Question_Answer,
                                tq_question=question.qb_question,
                                tq_answer=question.qb_answer,
                                tq_weightage=3,
                                tq_hint=question.qb_hint,
                                tq_optiona=question.qb_optiona,
                                tq_optionb=question.qb_optionb,
                                tq_optionc=question.qb_optionc,
                                tq_optiond=question.qb_optiond,
                                domain_name = domain
                            )

                        for question in four_mark_questions:
                            chep_id = Chepter.objects.get(chep_name = question.qb_chepter, domain_name = domain)
                            Test_questions_answer.objects.create(
                                tq_name=test_instance,
                                tq_chepter=chep_id,
                                tq_q_type=Test_questions_answer.que_type.Question_Answer,
                                tq_question=question.qb_question,
                                tq_answer=question.qb_answer,
                                tq_weightage=4,
                                tq_hint=question.qb_hint,
                                tq_optiona=question.qb_optiona,
                                tq_optionb=question.qb_optionb,
                                tq_optionc=question.qb_optionc,
                                tq_optiond=question.qb_optiond,
                                domain_name = domain
                            )

                    return redirect('admin_tests')
            else:
                filled_data = form.data
                context.update({'filled_data': filled_data, 'errors': form.errors})
                return render(request, 'insert_update/add_tests.html', context)
    return render(request, 'insert_update/add_tests.html', context)



@admin_login_required
def delete_tests(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Chepterwise_test.objects.filter(test_id__in=selected_ids).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_tests')


@admin_login_required
def show_test_questions_admin(request):
    domain = request.get_host()
    if request.GET.get('test_id'):
        Test_Questions_data = Test_questions_answer.objects.filter(tq_name = request.GET['test_id'], domain_name = domain)
        No_of_q = Test_Questions_data.count()
        total_marks = 0
        for x in Test_Questions_data:
            total_marks += x.tq_weightage
        test_info = Chepterwise_test.objects.get(test_id = request.GET['test_id'])

        if request.GET.get('que_id'):
            que_id = request.GET.get('que_id')
            test_question = Test_questions_answer.objects.filter(tq_id = que_id, domain_name = domain) 
        else:
            test_question = Test_questions_answer.objects.filter(tq_name__test_id = request.GET['test_id'], domain_name = domain)[:1]


        context = {
            'Test_Questions_data':Test_Questions_data,
            'test_info':test_info,
            'test_question':test_question,
            'total_marks':total_marks,
            'no_of_q':No_of_q,
            'title' : 'Tests',
        }
        return render(request, 'show_test_questions_admin.html',context)
    
    else:
        return redirect('admin_tests') 

@admin_login_required
def insert_update_test_questions(request):
    domain = request.get_host()
    chep_data = Chepter.objects.filter(domain_name = domain)
    context = {
        'chep_data': chep_data,
        'que_type': Test_questions_answer.que_type,
        'title' : 'Tests',
    }

    if request.GET.get('test_id'):
        test_id = request.GET['test_id']
        test_data = Chepterwise_test.objects.get(test_id = request.GET['test_id'])
        chep_data = chep_data.filter(chep_sub__sub_id = test_data.test_sub.sub_id)
        context.update({'test_id': test_id,'chep_data': chep_data})

    if request.method == 'POST':
        form = TestQuestionsAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            testt_id = form.cleaned_data['tq_name']
            chep_id = form.cleaned_data['tq_chepter']
            testt_id = testt_id.test_id
            chep_id = chep_id.chep_id
            form.instance.domain_name = domain
            form.save()
            url = '/adminside/insert_update_test_question_admin/?test_id={}&chep_id={}'.format(testt_id,chep_id)
            return redirect(url) 
        else:
            context.update({'form': form,'errors':form.errors})
            return render(request, 'insert_update/add_test_questions.html', context)
    else:
        form = TestQuestionsAnswerForm()
        context.update({'form': form})
        return render(request, 'insert_update/add_test_questions.html', context)


# ============================================packages logic====================================
@admin_login_required
def show_packages(request):
    domain = request.get_host()
    data = Packs.objects.prefetch_related('pack_subjects').filter(domain_name = domain)
    std_data = Std.objects.filter(domain_name = domain)
    data = paginatoorrr(data, request)

    context ={
        'data' : data,
        'title' : 'Packages',
        'std_data' : std_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = Packs.objects.prefetch_related('pack_subjects').filter(pack_std__std_id = get_std, domain_name = domain)
            data = paginatoorrr(data, request)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'get_std':get_std})  

    if request.GET.get('searchhh'):
        searchhh = request.GET['searchhh']
        if searchhh:
            data = Packs.objects.filter(
            Q(pack_name__icontains=searchhh) |
            Q(pack_subjects__sub_name__icontains=searchhh) |
            Q(pack_fees__icontains=searchhh) |
            Q(pack_std__std_name__icontains=searchhh), domain_name = domain).prefetch_related('pack_subjects')
            data = paginatoorrr(data, request)
            context.update({'data':data,'searchhh':searchhh})  
    return render(request, 'show_packages.html',context)



def insert_update_packages(request):
    domain = request.get_host()
    std_data = Std.objects.filter(domain_name = domain)
    subjects_data = Subject.objects.filter(domain_name = domain)

    context = {
        'title' : 'Packages',
        'std_data':std_data,
        'subjects_data':subjects_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        subjects_data = subjects_data.filter(sub_std__std_id = get_std)
        context.update({'get_std ':get_std,'std_data':std_data, 'subjects_data':subjects_data}) 



 # ================update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            pack_std = request.POST.get('pack_std')
            url = '/adminside/admin_packages/?get_std={}'.format(pack_std)
            instance = get_object_or_404(Packs, pk=request.GET['pk'])
            form = pack_form(request.POST, instance=instance)
            if form.is_valid():
                form.instance.domain_name = domain
                form.save()
                messages.success(request, 'Package Updated Successfully')
                return redirect(url)
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
        
        update_data = Packs.objects.get(pack_id = request.GET['pk'])
        context.update({'update_data':update_data})  
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            pack_std = request.POST.get('pack_std')
            url = '/adminside/admin_packages/?get_std={}'.format(pack_std)
            form = pack_form(request.POST)
            if form.is_valid():
                check = Packs.objects.filter(pack_name = form.data['pack_name'], pack_std__std_id = form.data['pack_std'], domain_name = domain).count()
                if check >= 1:
                    messages.error(request,'{} is already Exists'.format(form.data['pack_name']))
                else:
                    form.instance.domain_name = domain   
                    form.save()
                    messages.success(request, 'Package Added Successfully') 
                    return redirect(url)
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
                return render(request, 'insert_update/packages.html', context) 
        
    return render(request, 'insert_update/package.html',context)



@admin_login_required
def delete_admin_package(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Packs.objects.filter(pack_id__in=selected_ids).delete()
                messages.success(request, 'Packages Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_packages')

@admin_login_required
@require_GET  # Ensure that only GET requests are allowed
def show_students(request):
    domain = request.get_host()
    context = {'title': 'Students'}
    std_data = Std.objects.filter(domain_name = domain)
    get_std_id = request.GET.get('get_std')
    get_batch_id = request.GET.get('get_batch')

    if get_std_id and get_batch_id:
        data = Students.objects.filter(stud_batch__batch_id=get_batch_id, domain_name = domain).values(
            'stud_id', 'stud_name', 'stud_lastname', 'stud_username', 'stud_contact', 
            'stud_email', 'stud_dob', 'stud_std__std_name', 'stud_std__std_board__brd_name', 
            'stud_batch__batch_name', 'stud_std__std_id', 'stud_batch__batch_id', 
            'stud_pack__pack_name', 'stud_guardian_email', 'stud_guardian_name', 
            'stud_guardian_number', 'stud_address', 'stud_guardian_profession', 'stud_gender','stud_roll_no'
        )

        batch_data = Batches.objects.filter(batch_std__std_id=get_std_id, domain_name = domain)
        get_batch = Batches.objects.get(batch_id=get_batch_id)
        get_std = Std.objects.get(std_id=get_std_id)

        data = paginatoorrr(data,request)
        context.update({
            'data': data,
            'std_data': std_data,
            'batch_data': batch_data,
            'get_batch': get_batch,
            'get_std': get_std,
        })

    elif get_std_id:
        data = Students.objects.filter(stud_std__std_id=get_std_id, domain_name = domain).values(
            'stud_id', 'stud_name', 'stud_lastname', 'stud_username', 'stud_contact', 
            'stud_email', 'stud_dob', 'stud_std__std_name', 'stud_std__std_board__brd_name', 
            'stud_batch__batch_name', 'stud_std__std_id', 'stud_batch__batch_id', 
            'stud_pack__pack_name', 'stud_guardian_email', 'stud_guardian_name', 
            'stud_guardian_number', 'stud_address', 'stud_guardian_profession', 'stud_gender','stud_roll_no'
        )

        batch_data = Batches.objects.filter(batch_std__std_id=get_std_id, domain_name = domain)
        get_std = Std.objects.get(std_id=get_std_id)

        data = paginatoorrr(data,request)
        context.update({
            'data': data,
            'std_data': std_data,
            'batch_data': batch_data,
            'get_std': get_std,
        })

    else:
        data = Students.objects.filter(domain_name = domain).values(
            'stud_id', 'stud_name', 'stud_lastname', 'stud_username', 'stud_contact', 
            'stud_email', 'stud_dob', 'stud_std__std_name', 'stud_std__std_board__brd_name', 
            'stud_batch__batch_name', 'stud_std__std_id', 'stud_batch__batch_id', 
            'stud_pack__pack_name', 'stud_guardian_email', 'stud_guardian_name', 
            'stud_guardian_number', 'stud_address', 'stud_guardian_profession', 'stud_gender','stud_roll_no'
        )
        
        batch_data = Batches.objects.filter(domain_name = domain)
        data = paginatoorrr(data,request)
        
        context.update({
            'data': data,
            'std_data': std_data,
            'batch_data': batch_data,
        })

    if request.GET.get('searchhh'):
        searchhh = request.GET['searchhh']
        if searchhh:
            data = Students.objects.filter(
            Q(stud_name__icontains=searchhh) |
            Q(stud_lastname__icontains=searchhh) |
            Q(stud_username__icontains=searchhh) |
            Q(stud_contact__icontains=searchhh) |
            Q(stud_email__icontains=searchhh) |
            Q(stud_dob__icontains=searchhh) |
            Q(stud_std__std_name__icontains=searchhh) |
            Q(stud_std__std_board__brd_name__icontains=searchhh) |
            Q(stud_batch__batch_name__icontains=searchhh) |
            Q(stud_pack__pack_name__icontains=searchhh) |
            Q(stud_guardian_email__icontains=searchhh) |
            Q(stud_guardian_name__icontains=searchhh) |
            Q(stud_guardian_number__icontains=searchhh) |
            Q(stud_address__icontains=searchhh) |
            Q(stud_guardian_profession__icontains=searchhh) |
            Q(stud_gender__icontains=searchhh), domain_name = domain).values(
            'stud_id', 'stud_name', 'stud_lastname', 'stud_username', 'stud_contact', 
            'stud_email', 'stud_dob', 'stud_std__std_name', 'stud_std__std_board__brd_name', 
            'stud_batch__batch_name', 'stud_std__std_id', 'stud_batch__batch_id', 
            'stud_pack__pack_name', 'stud_guardian_email', 'stud_guardian_name', 
            'stud_guardian_number', 'stud_address', 'stud_guardian_profession', 'stud_gender','stud_roll_no'
            )
            data = paginatoorrr(data, request)
            context.update({'data':data,'searchhh':searchhh})  

    return render(request, 'show_students.html', context)


def insert_meeting_date(request):
    pk = request.GET['pk']
    return render(request, 'meeting_date.html', {'pk': pk})


@admin_login_required
def send_meeting_mail(request):
    if request.method == 'POST':
            domain = request.get_host()
            pk = request.POST['pk']
            student_parent = Students.objects.get(stud_id = pk)
            parent_email = student_parent.stud_guardian_email
            parent_name = student_parent.stud_guardian_name
            meeting_date = request.POST['meeting_date']
            meeting_time = request.POST['meeting_time']

            htmly = mail_templates.objects.get(mail_temp_type = 'Parent_meeting_mail', mail_temp_selected=1).mail_temp_html
            context_data={}
            if domain != '127.0.0.1:8000':
                Institute_data = NewInstitution.objects.get(institute_domain = domain)
                
                logo = '{}/media/{}'.format(domain,Institute_data.institute_logo)
                context_data.update({
                    'logo':logo,
                    'institute_name': Institute_data.institute_name,
                    'institute_email': Institute_data.institute_email,
                    'institute_number': Institute_data.institute_contact,
                })
            else:
                logo = 'api.ministudy.in/static/imgs/My_dream_logo/logo_text_sidebyside_dark.png'
                context_data.update({
                    'logo':logo,
                    'institute':'miniStudy',
                    'email':'mail.trushalpatel@gmail.com',
                    'phone_num':'8511962611',
                })

            context_data.update({
            'title': "Parent Meeting",
            'name': parent_name,
            'date': meeting_date,
            'time': meeting_time
            })
            htmly = Template(htmly)
            html_content = htmly.render(Context(context_data)) 
            send_email_for_meeting.delay(parent_email, html_content)

            title = "Parent Meeting"
            msg = f"Dear Parent, we would like to inform you that a parent meeting is scheduled for {meeting_date} on {meeting_time}. Your presence is highly encouraged as we will be discussing important updates concerning your child's academic progress."
            notification = Notification(
            notify_title=title,
            notify_notification=msg,
            notify_user = 'student',
            domain_name=domain)
            notification.save()

            send_notification.delay(student_parent.guardian_onesignal_player_id, title, msg, request)
    return render(request, 'meeting_date.html')

@admin_login_required
def insert_update_students(request):
    domain = request.get_host()
    std_data = Std.objects.filter(domain_name = domain)
    batch_data = Batches.objects.filter(domain_name = domain)
    pack_data = Packs.objects.filter(domain_name = domain)
    group_data = Groups.objects.filter(domain_name = domain)
    context = {
        'title' : 'Students',
        'std_data':std_data,
        'batch_data':batch_data,
        'pack_data':pack_data,
        'group_data':group_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        batch_data = batch_data.filter(batch_std__std_id = get_std)
        pack_data = pack_data.filter(pack_std__std_id = get_std)
        context.update({'get_std ':get_std,'std_data':std_data,'batch_data':batch_data,'pack_data':pack_data}) 


    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        batch_data = batch_data.filter(batch_id = get_batch)
        context.update({'get_batch ':get_batch,'batch_data':batch_data})

    if request.method == 'POST':

        # ================update Logic============================
        if request.GET.get('pk'):
            instance = get_object_or_404(Students, pk=request.GET['pk'])
            form = student_form(request.POST, instance=instance)
            if form.is_valid():
                form.instance.domain_name = domain
                form.save()
                student_std = request.POST.get('stud_std')
                student_batch = request.POST.get('stud_batch')

                url = '/adminside/students_dataAdmin/?get_std={}&get_batch={}'.format(student_std, student_batch)
                messages.success(request, 'Student updated successfully')
                return redirect(url)
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})

        # ===================insert_logic===========================
        form = student_form(request.POST)
        if form.is_valid():
            hashed_password = make_password('12345678')
            hashed_password_parent = make_password('123456')
            form.instance.stud_pass = hashed_password
            form.instance.stud_guardian_password = hashed_password_parent
            form.instance.stud_email = request.POST.get('stud_email').lower()
            form.instance.stud_guardian_email = request.POST.get('stud_guardian_email').lower()
            form.instance.domain_name = domain
            instance = form.save()

            # ------------------give access to student====================
            selected_groups = request.POST.getlist('material_group[]')
            for x in selected_groups:
                group_obj = Groups.objects.get(group_id = int(x))
                Materials_access.objects.update_or_create(
                    materialaccess_email=request.POST.get('stud_email').lower(),
                    materialaccess_group=group_obj,
                    defaults={'domain_name': domain}
                )
            # ----------Mail Send-------------------------------------------
            student_name = instance.stud_name
            student_email = [instance.stud_email]
            student_password = instance.stud_pass


            htmly = mail_templates.objects.get(mail_temp_type = 'Student_mail', mail_temp_selected=1).mail_temp_html
            context_data={}
            if domain != '127.0.0.1:8000':
                Institute_data = NewInstitution.objects.get(institute_domain = domain)
                
                logo = '{}/media/{}'.format(domain,Institute_data.institute_logo)
                context_data.update({
                    'logo':logo,
                    'institute_name': Institute_data.institute_name,
                    'institute_email': Institute_data.institute_email,
                    'institute_number': Institute_data.institute_contact,
                })
            else:
                logo = 'api.ministudy.in/static/imgs/My_dream_logo/logo_text_sidebyside_dark.png'
                context_data.update({
                    'logo':logo,
                    'institute':'miniStudy',
                    'email':'mail.trushalpatel@gmail.com',
                    'phone_num':'8511962611',
                })
            context_data.update({
            'title': "Student Register",
            'name': student_name,
            'password': student_password
            })
            htmly = Template(htmly)
            html_content = htmly.render(Context(context_data))
            student_email_send.delay(student_email, html_content)
            
            student_std = request.POST.get('stud_std')
            student_batch = request.POST.get('stud_batch')

            url = '/adminside/students_dataAdmin/?get_std={}&get_batch={}'.format(student_std, student_batch)
            return redirect(url)
        else:
            filled_data = form.data
            context.update({'filled_data ':filled_data,'errors':form.errors})
            return render(request, 'insert_update/add_student.html', context)

    if request.GET.get('pk'):
        update_data = Students.objects.get(stud_id = request.GET['pk'])
        context.update({'update_data':update_data})
    
    if request.GET.get('inq_id'):
        inq_id = request.GET.get('inq_id')
        inquires_admission_data = Inquiries.objects.get(inq_id=inq_id)
        context.update({'inquires_admission_data':inquires_admission_data})
    return render(request, 'insert_update/add_student.html',context)


def delete_students(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Students.objects.filter(stud_id__in=selected_ids).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    return redirect('students_dataAdmin')




@admin_login_required
def show_inquiries(request):
    domain = request.get_host()
    title = "Leads"
    email_ids = list(Students.objects.values_list('stud_email', flat=True))
    inquiries_data = Inquiries.objects.filter(domain_name = domain).order_by('-inq_date')
    total_inquiries = inquiries_data.count()
    students_email = Students.objects.filter(domain_name = domain).values('stud_email')
    matching_inquiries = Inquiries.objects.filter(domain_name = domain, inq_email__in=students_email)

    total_conversion = matching_inquiries.count()
    if total_inquiries != 0:
        percentage = round((total_conversion/total_inquiries)*100,2)
    else:
        percentage = 0

    monthly_data = (
        inquiries_data
        .annotate(month=TruncMonth('inq_date'))  # Extract month from 'inq_date'
        .values('month')
        .annotate(lead_count=Count('inq_id'))  # Count inquiries per month
        .order_by('month')
    )

    formatted_monthly_leads = [
    f"{calendar.month_name[item['month'].month]} - {item['lead_count']} Leads"
    for item in monthly_data
]

    context = {
        "title":title,
        "inquiries_data":inquiries_data,
        "total_inquiries":total_inquiries,
        "total_conversion":total_conversion,
        "matching_inquiries":matching_inquiries,
        "percentage":percentage,
        'email_ids': email_ids,
        'formatted_monthly_leads': formatted_monthly_leads,
        'domain':domain
    }
    return render(request, 'show_inquiries.html', context)

@admin_login_required
def delete_inquiries(request):
    if request.method == 'POST':
        domain  = request.get_host()
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Inquiries.objects.filter(inq_id__in=selected_ids, domain_name = domain).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    return redirect('inquiry_data')


# ------------------------------------------batches data-----------------------------------------

@admin_login_required
def show_batches(request):
    domain = request.get_host()
    data = Batches.objects.filter(domain_name = domain)
    std_data = Std.objects.filter(domain_name = domain)
    data = paginatoorrr(data, request)
    context ={
        'data' : data,
        'title' : 'Batches',
        'std_data' : std_data,
    }
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = Batches.objects.filter(batch_std__std_id = get_std, domain_name = domain)
            data = paginatoorrr(data, request)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'get_std':get_std})     
    return render(request, 'show_batches.html',context)


@admin_login_required
def insert_update_batches(request):
    domain = request.get_host()
    std_data = Std.objects.filter(domain_name = domain)
    
    context = {
        'title' : 'Batches',
        'std_data':std_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        context.update({'get_std ':get_std,'std_data':std_data}) 


 # ================update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Batches, pk=request.GET['pk'])
            form = batch_form(request.POST, instance=instance)
            check = Batches.objects.filter(batch_name = form.data['batch_name'], batch_std__std_id = form.data['batch_std'], domain_name = domain).count()
            if check >= 1:
                messages.error(request,'{} is already Exists'.format(form.data['batch_name']))
            else:
                if form.is_valid():
                    form.instance.domain_name = domain
                    form.save()
                    messages.success(request, 'Batch Updated Successfully')
                    std_name = request.POST.get('batch_std')
                    url = '/adminside/admin_batches/?get_std={}'.format(std_name)
                    return redirect(url)
                else:
                    filled_data = form.data
                    context.update({'filled_data ':filled_data,'errors':form.errors})
        
        update_data = Batches.objects.get(batch_id = request.GET['pk'])
        context.update({'update_data':update_data})  
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            form = batch_form(request.POST)
            if form.is_valid():
                check = Batches.objects.filter(batch_name = form.data['batch_name'], batch_std__std_id = form.data['batch_std'], domain_name = domain).count()
                if check >= 1:
                    messages.error(request,'{} is already Exists'.format(form.data['batch_name']))
                else:
                    form.instance.domain_name = domain
                    form.save()
                    messages.success(request, 'Batch Added Successfully')    
                    std_name = request.POST.get('batch_std')
                    url = '/adminside/admin_batches/?get_std={}'.format(std_name)
                    return redirect(url)
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
                return render(request, 'insert_update/batches.html', context) 
        
    return render(request, 'insert_update/batches.html',context)                     



@admin_login_required
def delete_admin_batches(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Batches.objects.filter(batch_id__in=selected_ids).delete()
                messages.success(request, 'Batches Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_batches')

@admin_login_required
def show_admin_profile(request):
    domain = request.get_host()
    admin_id = request.session['admin_id']
    admin_data = AdminData.objects.filter(admin_id = admin_id, domain_name = domain)
    context = {
        'admin_data':admin_data,
        'title' : 'Profile',
    }
    return render(request, 'show_profile.html', context)


@admin_login_required
def Student_doubts_adminside(request):
    domain = request.get_host()
    Total_doubts = Doubt_section.objects.filter(domain_name = domain).count()
    Total_solutions = Doubt_solution.objects.filter(domain_name = domain).count()

    unverified_doubts_count = Doubt_section.objects.filter(domain_name = domain).annotate(
    verified_solution_count=Count('doubt_solution', filter=Q(doubt_solution__solution_verified=True))
    ).filter(verified_solution_count = 0).count()

    verified_doubts_count = Doubt_solution.objects.filter(solution_verified=1, domain_name = domain).count()

    doubts_zero_solution = Doubt_section.objects.filter(domain_name = domain).annotate(
        zero_solution_count = Count('doubt_solution')
    ).filter(zero_solution_count=0).count()

    context = {
        'title' : 'Doubts',
        'Total_doubts':Total_doubts,
        'Total_solutions':Total_solutions,
        'unverified_doubts_count':unverified_doubts_count,
        'verified_doubts_count':verified_doubts_count,
        'doubts_zero_solution':doubts_zero_solution,
    }
    return render(request, 'show_doubts_admin.html', context)


@admin_login_required
def adminside_report_card(request):
    domain = request.get_host()
    data = Attendance.objects.filter(domain_name = domain)
    std_data = Std.objects.filter(domain_name = domain)
    batch_data = Batches.objects.filter(domain_name = domain)
    stud_data = Students.objects.filter(domain_name = domain)
    subj_data = Subject.objects.filter(domain_name = domain)

    context ={
        'data' : data,
        'title' : 'Report-Card',
        'std_data' : std_data,
        'batch_data':batch_data,
        'stud_data':stud_data,
        'sub_data':subj_data,
    }
    
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(atten_timetable__tt_batch__batch_std__std_id = get_std)
            batch_data = batch_data.filter(batch_std__std_id = get_std)
            stud_data = stud_data.filter(stud_std__std_id = get_std)
            subj_data = subj_data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'batch_data':batch_data,'get_std':get_std,'stud_data':stud_data,'sub_data':subj_data})
            student_std = get_std.std_name
        student_std = get_std.std_id
    
    
    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = data.filter(atten_timetable__tt_batch__batch_id = get_batch)
            stud_data = stud_data.filter(stud_batch__batch_id = get_batch)
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'data':data,'get_batch':get_batch,'stud_data':stud_data}) 
        student_batch = get_batch.batch_name      
    
    
    if request.GET.get('get_student'):
        get_student = int(request.GET['get_student'])
        if get_student == 0:
            pass
        else:
            data = data.filter(atten_student__stud_id = get_student)
            get_student = Students.objects.get(stud_id = get_student)
            my_package = Packs.objects.filter(domain_name = domain).prefetch_related('pack_subjects').get(pack_id = get_student.stud_pack.pack_id)
            pack_subject_list = []
            for subject in my_package.pack_subjects.all():
                pack_subject_list.append(subject.sub_id)
            context.update({'data':data,'get_student':get_student})

        student_id = get_student.stud_id

    if ((request.GET.get('get_std')) and (request.GET.get('get_batch')) and (request.GET.get('get_student'))):    
        # ===============Overall Attendance==================

        # student_data = Students.objects.filter(stud_std__std_id = student_std)
        # print(student_data)
        total_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, domain_name = domain).count()
        
        present_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=True, domain_name = domain).count()

        absent_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=False, domain_name = domain).count()
        
        if total_attendence > 0:
            overall_attendence = round((present_attendence/total_attendence)*100,2)
        else:
            overall_attendence = 0



        # ==================Test Report and Attendance Report============
        students_li = Students.objects.filter(stud_std__std_id = student_std, domain_name = domain)
        overall_attendance_li = []
        for x in students_li:
            total_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x.stud_id, domain_name = domain).count()
            present_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x.stud_id, atten_present=True, domain_name = domain).count()
            # print("==============================================",total_attendence_studentwise)
            if total_attendence_studentwise > 0:
                overall_attendence_studentwise = round((present_attendence_studentwise/total_attendence_studentwise)*100,2)
            else:
                overall_attendence_studentwise = 0
            

            total_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x.stud_id, domain_name = domain).aggregate(total_sum_marks=Sum('tau_total_marks'))['total_sum_marks'] or 0
            
            
            obtained_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x.stud_id, domain_name = domain).aggregate(total_obtained_marks=Sum('tau_obtained_marks'))['total_obtained_marks'] or 0
            

            if total_marks == 0:
                overall_result = 0
            else:
                overall_result = round((obtained_marks/total_marks)*100,2)
            if student_id == x.stud_id: 
                current_student_overall_test_result = overall_result
                context.update({'current_student_overall_test_result':current_student_overall_test_result})

            overall_attendance_li.append({'stud_name':x.stud_name, 'overall_attendance_studentwise':overall_attendence_studentwise, 'overall_result':overall_result})
        overall_attendance_li = sorted(overall_attendance_li, key=lambda x: x['overall_result'], reverse=True)
        overall_attendance_li = overall_attendance_li[:5]
        
        # ===================SubjectsWise Attendance============================
        subjects_li = Subject.objects.filter(sub_std__std_id = student_std, sub_id__in = pack_subject_list, domain_name = domain).values('sub_name').distinct()
        overall_attendance_subwise = []
        for x in subjects_li:
            x = x['sub_name']
            total_attendence_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = x, atten_student__stud_id=student_id, domain_name = domain).count()

            present_attendence_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = x, atten_present=True,atten_student__stud_id=student_id, domain_name = domain).count()

            if total_attendence_subwise > 0:
                attendance_subwise = round((present_attendence_subwise/total_attendence_subwise)*100,2)
            else:
                attendance_subwise = 0
            overall_attendance_subwise.append({'sub_name': x, 'attendance_subwise':attendance_subwise})

        # ======================SubjectWise TestResult==============================
        subjects_data = Subject.objects.filter(sub_std=student_std, sub_id__in = pack_subject_list, domain_name = domain)
        final_average_marks_subwise = []
        for x in subjects_data:
            total_marks_subwise = Test_attempted_users.objects.filter(tau_test_id__test_sub__sub_name = x.sub_name, tau_stud_id__stud_id=student_id, domain_name = domain).aggregate(total_sum_marks_subwise=Sum('tau_total_marks'))['total_sum_marks_subwise'] or 0
        

            obtained_marks_subwise = Test_attempted_users.objects.filter(tau_test_id__test_sub__sub_name = x.sub_name, tau_stud_id__stud_id=student_id, domain_name = domain).aggregate(obtained_sum_marks_subwise=Sum('tau_obtained_marks'))['obtained_sum_marks_subwise'] or 0
            
            
            if total_marks_subwise == 0:
                average_marks_subwise = 0
            else:
                average_marks_subwise = round((obtained_marks_subwise/total_marks_subwise)*100,2)
            
            final_average_marks_subwise.append({'subject_name':x.sub_name, 'average_marks_subwise':average_marks_subwise})

        # ====================Average Test Result=================================
        overall_results = [i['overall_result'] for i in overall_attendance_li]
        if overall_results:
            class_average_result = round(statistics.mean(overall_results),2)
        else:
            class_average_result = 0

        total_test_conducted = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id, domain_name = domain).count()

        absent_in_test = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id,tau_obtained_marks = 0, domain_name = domain).count()


        # =============Doubts and Solution Counts================================

        doubt_asked = Doubt_section.objects.filter(doubt_stud_id__stud_id = student_id, domain_name = domain).count()

        solutions_gives = Doubt_section.objects.filter(doubt_stud_id__stud_id = student_id, domain_name = domain).annotate(verified_solution=Count(
            Case(
                When(doubt_solution__solution_verified=True, then=1),
                output_field=IntegerField(),
            )))
        
        my_solve_doubts = 0
        for x in solutions_gives:
            if x.verified_solution > 0:
                my_solve_doubts += 1
            else:
                print("no verified")

        doubt_solved_byme = Doubt_solution.objects.filter(solution_stud_id__stud_id = student_id, solution_verified = True, domain_name = domain).count()
        # print(student_data)
        context.update({
            'title': 'Report-Card',
            'logo_url': 'http://ministudy.in/staticfiles/logos/logo_text_sidebyside_dark.png',
            # 'student_data':student_data,
            'overall_attendence':overall_attendence,
            'overall_attendance_li':overall_attendance_li,
            'overall_attendance_subwise':overall_attendance_subwise,
            'total_attendence':total_attendence,
            'absent_attendence':absent_attendence,
            'class_average_result':class_average_result,
            'final_average_marks_subwise':final_average_marks_subwise,
            'doubt_asked':doubt_asked,
            'solutions_gives':solutions_gives,
            'doubt_solved_byme':doubt_solved_byme,
            'my_solve_doubts':my_solve_doubts,
            'total_test_conducted':total_test_conducted,
            'absent_in_test':absent_in_test,
        })
    else:
        noreport_card = 1       
        nobody = 0
        context.update({'nobody':nobody, 'noreport_card':noreport_card})
    return render(request, 'show_report_card_admin.html', context)



@admin_login_required
def fees_collection_admin(request):
    domain = request.get_host()
    cheque_collections_data = Cheque_Collection.objects.filter(cheque_paid=False, domain_name = domain)
    std_data = Std.objects.filter(domain_name = domain)
    Context = {'std_data':std_data}
             
    students_data = Students.objects.filter(domain_name = domain).annotate(
    amount_paid=Coalesce(Sum('fees_collection__fees_paid'), Value(0)),
    discountt=Case(
        When(discount__discount_amount=None, then=Value(0)),
        default=F('discount__discount_amount'),output_field=IntegerField()
    )).values('stud_id','amount_paid','discountt','stud_std__std_name','stud_std__std_board__brd_name','stud_name','stud_lastname','stud_pack__pack_fees')

    students_data = paginatoorrr(students_data, request)
    # -------------filter--------------------------------------------
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            students_data = Students.objects.filter(stud_std__std_id = get_std, domain_name = domain).annotate(
            amount_paid=Coalesce(Sum('fees_collection__fees_paid'), Value(0)),
            discountt=Case(
                When(discount__discount_amount=None, then=Value(0)),
                default=F('discount__discount_amount'),output_field=IntegerField()
            )).values('stud_id','amount_paid','discountt','stud_std__std_name','stud_std__std_board__brd_name','stud_name','stud_lastname','stud_pack__pack_fees')
            students_data = paginatoorrr(students_data, request)
            get_std = Std.objects.get(std_id = get_std)
            Context.update({'get_std':get_std,'students_data':students_data}) 
    # ------------------end filter-------------------------------------

    #=================Total Amount Fees Paid============================================
    total_amount_fees_paid = Fees_Collection.objects.filter(domain_name = domain).aggregate(total_amu_paid = Sum('fees_paid'))
    total_cheque_amount = Cheque_Collection.objects.filter(domain_name = domain, cheque_paid=False).aggregate(total_che_paid = Sum('cheque_amount'))
    if total_cheque_amount['total_che_paid'] == 0 or total_cheque_amount['total_che_paid'] == None:
        total_cheque_amount_paid = 0
    else:
        total_cheque_amount_paid = total_cheque_amount['total_che_paid']
    
    if total_amount_fees_paid['total_amu_paid'] != None:
        total_amount_fees_paid = total_amount_fees_paid['total_amu_paid']
    else:
        total_amount_fees_paid = 0

    #==================Total Fees Amount After Discount=================================
    total_discount_amount = Discount.objects.filter(domain_name = domain).aggregate(discount_amount=Sum('discount_amount'))
    if total_discount_amount['discount_amount'] != None:
        total_discount_amount = total_discount_amount['discount_amount']
    else:
        total_discount_amount = 0

    total_fees_amount = Students.objects.filter(domain_name = domain).aggregate(fees_amount=Sum('stud_pack__pack_fees'))
    if total_fees_amount['fees_amount'] != None:
        total_fees_amount = total_fees_amount['fees_amount']
    else:
        total_fees_amount = 0

    total_fees_amount_after_discount = (total_fees_amount-total_discount_amount)
    
    #===================Total Pending Fees==============================================
    total_pending_fees = total_fees_amount_after_discount - total_amount_fees_paid
    
    if (total_pending_fees >= total_cheque_amount_paid):
        final_pending_fees_after_cheque_amount = total_pending_fees - total_cheque_amount_paid
    else:
        final_pending_fees_after_cheque_amount = 0

    Context.update({
        'title':'Payments',
        'std_data':std_data,
        'cheque_collections_data':cheque_collections_data,
        'total_amount_fees_paid':total_amount_fees_paid,
        'total_fees_amount_after_discount':total_fees_amount_after_discount,
        'total_pending_fees':total_pending_fees,
        'students_data':students_data,
        'total_cheque_amount_paid': total_cheque_amount_paid,
        'final_pending_fees_after_cheque_amount': final_pending_fees_after_cheque_amount,

    })
    
    model_name = request.GET.get('model_name')
    get_standard = request.GET.get('get_standard')
    if model_name == 'fees_collection':
        payment_data = []
        if get_standard:
            data = Fees_Collection.objects.filter(stud_std__std_id=get_standard, domain_name = domain)
        else:
            data = Fees_Collection.objects.filter(domain_name = domain)
        field_names = ['Roll No.','Student Name','Student Standard','Total Payable Amount','Discount Fees','Amount Paid','Remaining Amount']
        for x in data:
            temp_data = {}
            temp_data.update({'roll_no':x.fees_stud_id.stud_roll_no,
                              'student_name':x.fees_stud_id.stud_name,
                              'student_lastname':x.fees_stud_id.stud_name,
                              'student_standard':x.fees_stud_id.stud_std,
                              'total_payable_amount':total_amount_fees_paid,
                              'discount_fees':total_discount_amount,
                              'amount_paid':total_fees_amount,
                              'remaining_amount':total_pending_fees,})
            payment_data.append(temp_data)
        Context.update({'payment_data':payment_data,'field_names':field_names})
        return render(request, 'export_data.html', Context)


    if request.GET.get('searchhh'):
        searchhh = request.GET['searchhh']
        if searchhh:
            students_data = Students.objects.filter(
            Q(stud_std__std_name__icontains=searchhh) |
            Q(stud_name__icontains=searchhh) |
            Q(stud_lastname__icontains=searchhh) |
            Q(stud_pack__pack_fees__icontains=searchhh), domain_name = domain).annotate(
                amount_paid=Coalesce(Sum('fees_collection__fees_paid'), Value(0)),
                discountt=Case(
                    When(discount__discount_amount=None, then=Value(0)),
                    default=F('discount__discount_amount'),output_field=IntegerField()
                )).values('stud_id','amount_paid','discountt','stud_std__std_name','stud_std__std_board__brd_name','stud_name','stud_lastname','stud_pack__pack_fees')
            students_data = paginatoorrr(students_data, request)
            Context.update({'students_data':students_data,'searchhh':searchhh}) 

    return render(request, 'fees_collection_admin.html', Context)


@admin_login_required
def add_cheques_admin(request):
    domain = request.get_host()
    students = Students.objects.filter(domain_name = domain)
    banks = Banks.objects.filter(domain_name = domain)

    context={
        'title' : 'Add Cheques',
        'students':students,
        'banks':banks,    
    }   

    if request.GET.get('get_std'):
        get_std = request.GET.get('get_std')
        students = Students.objects.filter(stud_std__std_id = get_std)
        context.update({'students':students})

 # ================update Logic==================================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Cheque_Collection, pk=request.GET['pk'])
            form = Cheque_Collection_form(request.POST, instance=instance)
            if form.is_valid():
                
                if form.cleaned_data['cheque_paid']==True:
                    studid = form.cleaned_data['cheque_stud_id']
                    cheque_amt = form.cleaned_data['cheque_amount']
                    cheque_amt = form.cleaned_data['cheque_amount']
                    cheque_number = form.cleaned_data['cheque_number']
                    fees_mode = 'CHECK'
                    cheque_date = form.cleaned_data['cheque_date']
                    fees_collection_create = Fees_Collection.objects.create(fees_stud_id = studid,fees_paid=cheque_amt,fees_mode=fees_mode,fees_date=cheque_date, domain_name = domain)
                form.instance.domain_name = domain
                form.save()
                if form.cleaned_data['cheque_paid']==True:
                    student_name = form.cleaned_data['cheque_stud_id']
                    student_email = [student_name.stud_email]
                    parent_email = [student_name.stud_guardian_email]
                    date = datetime.datetime.today()

                    htmly = mail_templates.objects.get(mail_temp_type = 'Cheque_update_mail', mail_temp_selected=1).mail_temp_html
                    context_data = {}
                    if domain != '127.0.0.1:8000':
                        Institute_data = NewInstitution.objects.get(institute_domain = domain)
                        logo = '{}/media/{}'.format(domain,Institute_data.institute_logo)
                        context_data.update({
                        'logo':logo,
                        'institute_name': Institute_data.institute_name,
                        'institute_email': Institute_data.institute_email,
                        'institute_number': Institute_data.institute_contact,
                        })

                    else:
                        logo = 'api.ministudy.in/static/imgs/My_dream_logo/logo_text_sidebyside_dark.png'
                        context_data.update({
                            'logo':logo,
                            'institute':'miniStudy',
                            'email':'mail.trushalpatel@gmail.com',
                            'phone_num':'8511962611',
                        })
                    context_data.update({
                    'title': "Cheque Payment Update",
                    'name': student_name.stud_name,
                    'amount': form.cleaned_data['cheque_amount'],
                    'bank': form.cleaned_data['cheque_bank'],
                    'Cheque_number': cheque_number,
                    'date': date
                    })

                    htmly = Template(htmly)
                    html_content = htmly.render(Context(context_data))     
                    cheque_update_mail.delay(student_email, html_content)
                    cheque_update_mail.delay(parent_email, html_content)

                    title = "Cheque Payment Update"
                    mess = f"Dear {student_name.stud_name}, your cheque of ₹{form.cleaned_data['cheque_amount']} "f"from {form.cleaned_data['cheque_bank']} has been successfully withdraw on {date}."

                    notification = Notification(
                    notify_title=title,
                    notify_notification=mess,
                    notify_user = 'student',
                    domain_name=domain)
                    notification.save()
                    send_notification(student_name.stud_onesignal_player_id,title,mess, request)
                messages.success(request, "Cheque Updated Successfully")

                return redirect('fees_collection_admin')
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
        
        update_data = Cheque_Collection.objects.get(cheque_id = request.GET['pk'])
        context.update({'update_data':update_data})  
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            form = Cheque_Collection_form(request.POST)
            if form.is_valid():
                check = Cheque_Collection.objects.filter(cheque_number = form.data['cheque_number'], domain_name = domain).count()
                if check >= 1:
                    messages.error(request,'{} is already Exists'.format(form.data['cheque_number']))
                else:
                    form.instance.domain_name = domain    
                    form.save()
                    student_name = form.cleaned_data['cheque_stud_id']
                    student_email = [student_name.stud_email]
                    parent_email = [student_name.stud_guardian_email]
                    cheque_number = form.cleaned_data['cheque_number']
                    date = datetime.datetime.today()

                    htmly = mail_templates.objects.get(mail_temp_type = 'Cheque_mail', mail_temp_selected=1).mail_temp_html
                    context_data = {}
                    if domain != '127.0.0.1:8000':
                        Institute_data = NewInstitution.objects.get(institute_domain = domain)
                        logo = '{}/media/{}'.format(domain,Institute_data.institute_logo)
                        context_data.update({
                        'logo':logo,
                        'institute_name': Institute_data.institute_name,
                        'institute_email': Institute_data.institute_email,
                        'institute_number': Institute_data.institute_contact,
                        })

                    else:
                        logo = 'api.ministudy.in/static/imgs/My_dream_logo/logo_text_sidebyside_dark.png'
                        context_data.update({
                            'logo':logo,
                            'institute':'miniStudy',
                            'email':'mail.trushalpatel@gmail.com',
                            'phone_num':'8511962611',
                        })
                    context_data.update({
                    'title': "Cheque Payment",
                    'name': student_name.stud_name,
                    'amount': form.cleaned_data['cheque_amount'],
                    'bank': form.cleaned_data['cheque_bank'],
                    'date': date,
                    'Cheque_number': cheque_number
                    })
                    htmly = Template(htmly)
                    html_content = htmly.render(Context(context_data))     
                    cheque_mail.delay(student_email, html_content)
                    cheque_mail.delay(parent_email, html_content)

                    title = "Cheque Payment Update"
                    mess = f"Dear {student_name.stud_name}, your cheque of ₹{form.cleaned_data['cheque_amount']} "f"from {form.cleaned_data['cheque_bank']} has been processed on {date}."
                    notification = Notification(
                    notify_title=title,
                    notify_notification=mess,
                    notify_user = 'student',
                    domain_name=domain)
                    notification.save()
                    send_notification(student_name.stud_onesignal_player_id,title,mess, request)
                    messages.success(request, "Cheque Added Successfully!")

                    return redirect('fees_collection_admin')
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
                return render(request, 'insert_update/add_cheques_admin.html', context)          
            
    return render(request, 'insert_update/add_cheques_admin.html', context)


@admin_login_required
def delete_cheques_admin(request):
    if request.GET.get('delete_cheque'):
        del_id = request.GET['delete_cheque']
        try:
            check_data = Cheque_Collection.objects.get(cheque_id=del_id)
            check_data.delete()
        except Cheque_Collection.DoesNotExist:
            raise Http404("Cheque not found")
    return redirect('fees_collection_admin') 


@admin_login_required
def add_fees_collection_admin(request):
    domain = request.get_host()
    students = Students.objects.filter(domain_name = domain)
    context={
        'title' : 'Add Fees',
        'students':students,    
    }

    if request.GET.get('get_std'):
        get_std = request.GET.get('get_std')
        students = Students.objects.filter(stud_std__std_id = get_std, domain_name = domain)
        context.update({'get_std':get_std,'students':students})
        
    
    # ================update Logic==================================
    if request.GET.get('pk'):
        if request.method == 'POST':
            get_std = request.POST.get('get_std')
            url = '/adminside/fees_collection_admin/?get_std={}'.format(get_std)
            instance = get_object_or_404(Fees_Collection, pk=request.GET['pk'])
            form = fees_collection_form(request.POST, instance=instance)
            if form.is_valid():
                form.instance.domain_name = domain
                form.save()
                return redirect(url)
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
        
        update_data = Fees_Collection.objects.get(fees_id = request.GET['pk'])
        context.update({'update_data':update_data})  
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            print(request.POST.get('get_std'))
            get_std = request.POST.get('get_std')
            url = '/adminside/fees_collection_admin/?get_std={}'.format(get_std)
            form = fees_collection_form(request.POST)
            if form.is_valid(): 
                form.instance.domain_name = domain  
                messages.success(request, "Payment added successfully")
                form.save()
                # -------------Mail Send----------------------------------------------------------------------
                student_name = form.cleaned_data['fees_stud_id']
                student_email = [student_name.stud_email]
                parent_email = [student_name.stud_guardian_email]
                date = datetime.datetime.today()


                htmly = mail_templates.objects.get(mail_temp_type = 'Payment_mail', mail_temp_selected=1).mail_temp_html
                context_data = {}
                if domain != '127.0.0.1:8000':
                    Institute_data = NewInstitution.objects.get(institute_domain = domain)
                    logo = '{}/media/{}'.format(domain,Institute_data.institute_logo)
                    context_data.update({
                    'logo':logo,
                    'institute_name': Institute_data.institute_name,
                    'institute_email': Institute_data.institute_email,
                    'institute_number': Institute_data.institute_contact,
                    })

                else:
                    logo = 'api.ministudy.in/static/imgs/My_dream_logo/logo_text_sidebyside_dark.png'
                    context_data.update({
                        'logo':logo,
                        'institute':'miniStudy',
                        'email':'mail.trushalpatel@gmail.com',
                        'phone_num':'8511962611',
                    })
                context_data.update({
                'title': "Payment Update",
                'name': student_name.stud_name,
                'amount': form.cleaned_data['fees_paid'],
                'mode': form.cleaned_data['fees_mode'],
                'date': date
                })

                htmly = Template(htmly)
                html_content = htmly.render(Context(context_data))     
                payment_mail.delay(student_email, html_content)
                payment_mail.delay(parent_email, html_content)               
                # -------------Telegram Send-------------------------------------------------------------------
               
                payment_telegram_message(student_name.stud_name, student_name.stud_telegram_studentchat_id, form.cleaned_data['fees_mode'],form.cleaned_data['fees_paid'])

                title = "Payment Update"
                mess = f"Dear {student_name.stud_name}, your payment of ₹{form.cleaned_data['fees_paid']} "f"via {form.cleaned_data['fees_mode']} has been successfully processed on {date}."
                notification = Notification(
                notify_title=title,
                notify_notification=mess,
                notify_user = 'student',
                domain_name=domain)
                notification.save()
                send_notification(student_name.stud_onesignal_player_id,title,mess, request)
                return redirect(url)
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
                return render(request, 'insert_update/add_fees_collection_admin.html', context)
    return render(request, 'insert_update/add_fees_collection_admin.html', context)


@admin_login_required
def admin_fees_collection_delete(request):
    if request.GET.get('delete_payment'):
        del_id = request.GET['delete_payment']
        try:
            fees_data = Fees_Collection.objects.get(fees_id=del_id)
            fees_data.delete()
        except Fees_Collection.DoesNotExist:
            messages.error(request, 'Error in Deleting Data') 
            raise Http404("Cheque not found")
              
    return redirect('fees_collection_admin') 


@admin_login_required
def payments_history_admin(request):
    domain = request.get_host()
    fees_collections_data = Fees_Collection.objects.filter(domain_name = domain)
    std_data = Std.objects.filter(domain_name = domain)
    stud_data = Students.objects.filter(domain_name = domain)
    context = {
        'fees_collections_data':fees_collections_data,
        'std_data':std_data,
        'stud_data':stud_data,
    }

    if request.GET.get('get_std'):
        get_std = request.GET.get('get_std')
        if get_std == 0:
            pass
        else:
            fees_collections_data = fees_collections_data.filter(fees_stud_id__stud_std__std_id = get_std, domain_name = domain)
            stud_data = stud_data.filter(stud_std__std_id = get_std, domain_name = domain)
            get_std = Std.objects.filter(std_id = get_std, domain_name = domain).first()
            context.update({"fees_collections_data":fees_collections_data, "get_std":get_std, "stud_data":stud_data})
    
    if request.GET.get('get_student'):
        get_student = int(request.GET['get_student'])
        if get_student == 0:
            pass
        else:
            fees_collections_data = fees_collections_data.filter(fees_stud_id__stud_id = get_student, domain_name = domain)
            get_student = Students.objects.filter(stud_id = get_student, domain_name = domain).first()
            context.update({'fees_collections_data':fees_collections_data,'get_student':get_student})

    return render(request, 'payments_history_admin.html', context)


@admin_login_required
def faculty_access_show(request):
    domain = request.get_host()
    standard_data = Std.objects.filter(domain_name = domain)
    batch_data = Batches.objects.filter(domain_name = domain)
    subject_data = Subject.objects.filter(domain_name = domain)
    teachers_names = Faculties.objects.filter(domain_name = domain)
    context = {
        'standard_data':standard_data,
        'batch_data':batch_data,
        'subject_data':subject_data,
        'teachers_names':teachers_names,
        'title': 'Faculties',
    }
    if request.GET.get('get_std'):
        get_std = request.GET.get('get_std')
        batch_data = Batches.objects.filter(batch_std__std_id = get_std, domain_name = domain)
        subject_data = Subject.objects.filter(sub_std__std_id = get_std, domain_name = domain)
        selected_standard = Std.objects.get(std_id = get_std)
        context.update({'batch_data':batch_data, 'subject_data':subject_data, 'selected_standard':selected_standard})

    if request.GET.get('fac_id'):
        fac_id = int(request.GET.get('fac_id'))
        faculty_access_subject = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)
        sub_access_list = [sub.fa_subject for sub in faculty_access_subject]
        subjects_not_accessible = subject_data.exclude(sub_id__in=[sub.sub_id for sub in sub_access_list])
        teachers_names = teachers_names.filter(fac_id = fac_id)
        context.update({'fac_id': fac_id, 'subject_data': subjects_not_accessible, 'teachers_names': teachers_names})

    selected_subjects = request.POST.getlist('fa_subject')
    
    if request.method == 'POST':
        form = faculty_access_form(request.POST)
        if form.is_valid():
            fac = form.cleaned_data['fa_faculty']
            batch = form.cleaned_data['fa_batch']
            for x in selected_subjects:
                x_obj = Subject.objects.get(sub_id=x)
                Faculty_Access.objects.create(fa_faculty=fac, fa_batch=batch, fa_subject=x_obj, domain_name = domain)
            messages.success(request, "Access given successfully")
            return redirect('faculty_access')
    else:
        form = faculty_access_form()
        context.update({'form':form})
    return render(request, 'faculty_access.html', context)


@admin_login_required
def export_data(request):
    domain = request.get_host()
    model_name = request.GET.get('model_name')
    Context={'title':model_name}
    get_std = request.GET.get('get_std')
    get_batch = request.GET.get('get_batch')
    get_subject = request.GET.get('get_subject')

    if model_name == 'Students':
        student_data = []
        if get_std:
            data = Students.objects.filter(stud_std__std_id=get_std, domain_name = domain)
        elif get_batch:
            data = Students.objects.filter(stud_batch__batch_id=get_batch, domain_name = domain)
        else:
            data = Students.objects.filter(domain_name = domain)

        field_names = ['roll_no', 'student Name','student_lastname','contact','Email','DOB','gender','admission_no','enrollment_no','Guardian Name','Guardian Email','Guardian Number','Address','Std','Batch','Package']
        for x in data:
            temp_data = {}
            temp_data.update({'student_Name':x.stud_name,'student_lastname':x.stud_lastname,'contact':x.stud_contact,'Email':x.stud_email,'DOB':x.stud_dob,'gender':x.stud_gender,'admission_no':x.stud_admission_no,'roll_no':x.stud_roll_no,'enrollment_no':x.stud_enrollment_no,'Guardian_Name':x.stud_guardian_name,'Guardian_Email':x.stud_guardian_email,'Guardian_Number':x.stud_guardian_number,'Address':x.stud_address,'Std': x.stud_std.std_name + x.stud_std.std_board.brd_name,'Batch':x.stud_batch.batch_name,'Package':x.stud_pack.pack_name})
            student_data.append(temp_data)
        Context.update({'data':student_data,'field_names':field_names})

    if model_name == 'attendance':
        attendance_data = []
        if get_std:
            data = Attendance.objects.filter(atten_student__stud_std__std_id=get_std, domain_name = domain)
        elif get_batch:
            data = Attendance.objects.filter(atten_student__stud_batch__batch_id=get_batch, domain_name = domain)
        else:
            data = Attendance.objects.filter(domain_name = domain)

        field_names = ['Roll No','Date','Name','Subject','Tutor','Attendance','Batch','Std','Board']
        for x in data:
            temp_data = {}
            if x.atten_present == True:
                atten_present = "Present"
            else:
                atten_present = "Absent"
            temp_data.update({'Date':x.atten_date,
            'student_roll_no':x.atten_student.stud_roll_no,
            'Student_name':"{} {}".format(x.atten_student.stud_name, x.atten_student.stud_lastname),
            'subject':x.atten_timetable.tt_subject1.sub_name,
            'tutor':x.atten_timetable.tt_tutor1.fac_name,
            'Attendance': atten_present,
            'Batch':x.atten_student.stud_batch.batch_name,
            'Std':x.atten_student.stud_std.std_name,
            'Board':x.atten_student.stud_std.std_board.brd_name})

            attendance_data.append(temp_data)
        Context.update({'attendance_data':attendance_data,'field_names':field_names})  

    if model_name == 'chepter':
        chepter_data = []
        if get_std:
            data = Chepter.objects.filter(chep_std__std_id = get_std, domain_name = domain)
        elif get_subject:
            data = Chepter.objects.filter(chep_sub__sub_id = get_subject, domain_name = domain)
        else:
            data = Chepter.objects.filter(domain_name = domain)

        field_names = ['Chapter Name', 'Subject', 'Std']
        for x in data:
            temp_data = {}
            temp_data.update({
                'Chepter':x.chep_name,
                'Subject':x.chep_sub.sub_name,
                'Std':"{} {}".format(x.chep_std.std_name, x.chep_std.std_board.brd_name)
                })
            
            chepter_data.append(temp_data)
        Context.update({'chepter_data':chepter_data, 'field_names':field_names})

    if model_name == 'chepterwise_test':
        tests_data = []
        if get_std:
            data = Chepterwise_test.objects.filter(test_std__std_id = get_std, domain_name = domain).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage'))
        elif get_subject:
            data = Chepterwise_test.objects.filter(test_sub__sub_id = get_subject, domain_name = domain).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage'))
        else:
            data = Chepterwise_test.objects.filter(domain_name = domain).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage'))

        field_names = ['Test Name', 'Subject', 'Std', 'Questions', 'Total Marks']
        for x in data:
            temp_data = {}
            temp_data.update({'Test':x.test_name, 'Subject':x.test_sub.sub_name, 'Std':"{} {}".format(x.test_std.std_name, x.test_std.std_board.brd_name), 'Questions':x.num_questions, 'Total':x.total_marks})

            tests_data.append(temp_data)
        Context.update({'tests_data':tests_data, 'field_names':field_names})


    if model_name == 'inquiries':
        inquiries_data = []
        data = Inquiries.objects.filter(domain_name = domain).order_by('-inq_date')
        email_ids = list(Students.objects.values_list('stud_email', flat=True))

        field_names = ['Name', 'Phone', 'Subject', 'Std', 'Guardian Phone', 'Email', 'DOB', 'Gender', 'School Name', 'Std & Percentage', 'Guardian Name', 'Guardian Email', 'Guardian Profession', 'Address', 'Date', 'Know From', 'Admission']

        for x in data:
            temp_data = {}
            temp_data.update({'Name':'{} {}'.format(x.inq_name, x.inq_lastname), 'Phone':x.inq_contact, 'Subject':x.inq_subjects, 'Std':x.inq_std, 'Guardian_Phone':x.inq_guardian_number, 'Email': x.inq_email, 'DOB': x.inq_dob, 'Gender': x.inq_gender, 'School':x.inq_schoolname, 'Std_Percentage': x.inq_last_std_and_marks, 'Guardian_name':x.inq_guardian_name, 'Guardian_email':x.inq_guardian_email, 'Guardian_profession':x.inq_guardian_profession, 'Address':x.inq_address, 'Date':x.inq_date, 'Know_from':x.inq_howuknow, 'Admission':x.inq_email})

            inquiries_data.append(temp_data)
        Context.update({'inquiries_data':inquiries_data, 'field_name':field_names, 'email_ids':email_ids})
        

    return render(request, 'export_data.html',Context)




def bulk_upload_questions(request):
    if request.method == 'POST':
        qb_chapter_id = request.POST.get('tq_chapter')  # Corrected variable name
        qb_chapter = Chepter.objects.get(chep_id=qb_chapter_id)

        # Extract all question entries
        questions_data = request.POST.getlist('question[]')
        q_types = request.POST.getlist('q_type[]')
        answers = request.POST.getlist('answer[]')
        weightages = request.POST.getlist('weightage[]')
        options_a = request.POST.getlist('option_a[]')
        options_b = request.POST.getlist('option_b[]')
        options_c = request.POST.getlist('option_c[]')
        options_d = request.POST.getlist('option_d[]')

        # Save each question entry
        for i in range(len(questions_data)):
            question_bank.objects.create(
                qb_chepter=qb_chapter,
                qb_q_type=q_types[i],
                qb_question=questions_data[i],
                qb_answer=answers[i],
                qb_weightage=weightages[i],
                qb_optiona=options_a[i] if q_types[i] == 'MCQ' else None,
                qb_optionb=options_b[i] if q_types[i] == 'MCQ' else None,
                qb_optionc=options_c[i] if q_types[i] == 'MCQ' else None,
                qb_optiond=options_d[i] if q_types[i] == 'MCQ' else None,
            )

        return redirect('show_question_bank')  # Redirect to the same page after submission
    chap_data = Chepter.objects.filter(chep_std__std_id = 13).values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name')
    que_type_choices = question_bank.que_type.choices
    context={'chap_data':chap_data,'que_type_choices':que_type_choices}
    return render(request, 'insert_update/bulk_upload_test_questions.html',context)




@admin_login_required
def show_question_bank(request):

    questions = question_bank.objects.values('qb_id', 'qb_chepter')

    question_answers = question_bank.objects.values('qb_chepter','qb_std', 'qb_subject', 'qb_q_type', 'qb_question', 'qb_answer', 'qb_weightage','qb_optiona','qb_optionb','qb_optionc','qb_optiond')[:50]

    total_questions = question_bank.objects.all().count()

    chepters_names_with_ids = question_bank.objects.values_list('qb_chepter', 'qb_std', 'qb_subject', 'qb_q_type','qb_question','qb_answer','qb_weightage','qb_optiona','qb_optionb','qb_optionc','qb_optiond')
    

    questions = paginatoorrr(questions,request)
    return render(request, 'show_question_bank.html', {'questions': questions, 'total_questions':total_questions, 'question_answers': question_answers})


@admin_login_required
def edit_question_bankk(request):
    domain = request.get_host()
    # Fetch the specific question to edit
    updateid = request.GET.get('updateid')
    question = get_object_or_404(question_bank, qb_id=updateid)
    
    if request.method == 'POST':
        # Update the question details from form data
        chepter_object = Chepter.objects.get(chep_id=request.POST.get('gb_chepter'))
        question.qb_chepter = chepter_object.chep_name
        question.qb_subject = chepter_object.chep_sub
        question.qb_std = chepter_object.chep_std
        question.qb_q_type = request.POST.get('qb_q_type')
        question.qb_question = request.POST.get('qb_question')
        question.qb_answer = request.POST.get('qb_answer')
        question.qb_weightage = request.POST.get('qb_weightage')
        
        # Update options based on question type
        if question.qb_q_type == 'MCQ':
            question.qb_optiona = request.POST.get('qb_optiona')
            question.qb_optionb = request.POST.get('qb_optionb')
            question.qb_optionc = request.POST.get('qb_optionc')
            question.qb_optiond = request.POST.get('qb_optiond')
        else:
            # Clear options if not MCQ
            question.qb_optiona = None
            question.qb_optionb = None
            question.qb_optionc = None
            question.qb_optiond = None
        
        # Save the updated question to the database
        question.save()
        return redirect('show_question_bank')  # Redirect back to the question list page

    # Render edit form with existing question data
    chap_data = Chepter.objects.filter(chep_sub__sub_std__std_id = 13, domain_name = domain).values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name')
    que_type_choices = question_bank.que_type.choices
    context = {
        'question': question,
        'chap_data': chap_data,
        'que_type_choices': que_type_choices,
    }
    return render(request, 'insert_update/edit_question_bank.html', context)


@admin_login_required
def delete_question_bank(request):
    qb_id = request.GET.get('qb_id')
    if qb_id:
        question = get_object_or_404(question_bank, qb_id=qb_id)
        question.delete()

    # Redirect back to the list of questions
    return redirect('show_question_bank')


@admin_login_required
def delete_test_question_answer(request):
    if request.GET.get('delete_id'):
        del_id = request.GET['delete_id']
        try:
            data = Test_questions_answer.objects.get(tq_id=del_id)
            data.delete()
            messages.success(request,"Question Deleted Successfully")
        except data.DoesNotExist:
            messages.error(request,"Question Not Found")

        url = '/adminside/show_test_questions_admin/?test_id={}'.format(request.GET['test_id'])
    return redirect(url)

from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.core.mail import EmailMessage

def render_to_pdf(template_src, context_dict={}):
    template = render_to_string(template_src, context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(template.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@admin_login_required
def generate_payment_slip(request):
    context = {
        'payer_name': 'John Doe',
        'payer_email': 'john@example.com',
        'amount': '500',
        'payment_date': '2024-09-12',
        'payment_method': 'Credit Card',
        'transaction_id': 'TX123456789',
    }
    pdf = render_to_pdf('payment_slip.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


@admin_login_required
def time_slot_function(request):
    domain = request.get_host()
    faculty_records = Faculties.objects.values('fac_id', 'fac_name')
    faculty_data = []
    for record in faculty_records:
        fac_id = record['fac_id']
        fac_name = record['fac_name']
        access_data = Faculty_Access.objects.filter(fa_faculty__fac_id=fac_id, domain_name = domain)

        if access_data:
            faculty_data.append({
                'faculty_name': fac_name,
                'access_details': list(access_data.values('fa_id', 'fa_subject__sub_name', 'fa_batch__batch_name', 'fa_batch__batch_std__std_name')),
            })
    return render(request, 'time_slot.html', {'faculty_data': faculty_data})

@admin_login_required
def institute_main_send_function(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        try:
            df = pd.read_excel(excel_file, engine='openpyxl')
            print(df)
        except Exception as e:
            return render(request, 'show_inquiries.html', {'error': f"Error reading file: {str(e)}"})

        if 'Email' not in df.columns:
            return render(request, 'show_inquiries.html', {'error': 'Excel file must contain "institute email" column.'})
        else:
            email_list = df['Email'].dropna().tolist()
            institute_send_mail.delay(email_list)
            return redirect('inquiry_data')
    return HttpResponse('Hello')


@admin_login_required
def show_mail_templates_function(request):
    domain = request.get_host()
    mail_name = request.GET.get('mail_name','Introduction_mail')
    templates = mail_templates.objects.filter(domain_name = domain,mail_temp_type = mail_name)
    template_variables = mail_variables.objects.filter(mail_variables_type = mail_name)
    context = {
        'templates':templates,
        'title':'mail_templates',
        'active_mail': mail_name,
        'template_variables': template_variables,
    }

    pk = request.GET.get('pk')
    if pk:
        get_object = mail_templates.objects.get(mail_temp_id = pk)
        domain_name = get_object.domain_name
        mail_type = get_object.mail_temp_type
        mail_templates.objects.filter(domain_name=domain_name, mail_temp_type=mail_type).update(mail_temp_selected=0)
        get_object.mail_temp_selected = 1
        get_object.save()

    return render(request, 'show_mail_templates.html', context)


@admin_login_required
def insert_update_mail_templates(request):
    domain = request.get_host()
    templates = mail_templates.objects.filter(domain_name = domain)

    context = {
        'title':'mail_templates',
        'templates':templates,
    }

    if request.GET.get('pk'):
        pk = request.GET.get('pk')
        instance = get_object_or_404(mail_templates, pk=pk)
        if request.method == "POST":
            form = mail_templates_form(request.POST, instance=instance)
            if form.is_valid():
                form.instance.domain_name = domain
                form.save()
                return redirect('show_mail_templates')
            else:
                filled_data = form.data
                return render(request, 'insert_update/mail_templates.html', {'errors': form.errors,'filled_data':filled_data})
        
        update_data = mail_templates.objects.get(mail_temp_id = request.GET['pk'])
        context.update({'update_data':update_data}) 
    


    if request.method == 'POST':
        form = mail_templates_form(request.POST)
        context.update({'form':form})
        print(form)
        if form.is_valid():
           
            if form.instance.mail_temp_type == 'Announcement_mail':
                print("Hello")
            form.instance.domain_name = domain
            form.save()
            return redirect('show_mail_templates')
        else:
            filled_data = form.data
            return render(request, 'insert_update/mail_templates.html', {'errors': form.errors,'filled_data':filled_data})
        
    context['form'] = mail_templates_form()
    return render(request, 'insert_update/mail_templates.html', context)


@admin_login_required
def delete_mail_templates(request):
    domain = request.get_host()
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                mail_templates.objects.filter(mail_temp_id__in=selected_ids, domain_name = domain).delete()
                messages.success(request, 'Template Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('show_mail_templates')



@admin_login_required
def insert_suggestions_function(request):
    domain = request.get_host()
    suggestion = suggestions_improvements.objects.filter(domain_name = domain)
    username = request.session['admin_name']
    context = {
        'title': 'suggestions_improvements',
        'suggestions':suggestion,
        'username':username
    }
    
    if request.method == 'POST':
        si_user = request.POST.get('si_user')
        si_suggestion = request.POST.get('si_suggestion')
        suggestions_improvements.objects.create(si_user_name=username, si_user=si_user, si_suggestion=si_suggestion, domain_name = domain)
    
    return render(request, 'insert_update/suggestions.html', context)
    

@admin_login_required
def show_complaints_functions(request):
    domain = request.get_host()
    complaint_id = request.GET.get('complaint_id')
    if complaint_id:
        complaint = Complaint.objects.get(complaint_id = complaint_id)
        complaint.complaint_handle = True
        complaint.save()
        return redirect('show_complaints')
    complaints_data = Complaint.objects.filter(domain_name = domain, complaint_handle = 0)
    context = {"complaints_data": complaints_data, "title": "Complaints"}
    return render(request, "show_complaint.html", context)


@admin_login_required
def show_notification_function(request):
    domain = request.get_host()
    notification_data = Notification.objects.filter(domain_name = domain, notify_user = 'admin').order_by('-pk')
    context = {'notification_data': notification_data, 'title': 'Notification'}
    return render(request, 'show_notification.html', context)


@admin_login_required
def show_expense_function(request):
    domain = request.get_host()
    expense_data = Expense.objects.filter(domain_name = domain)
    total_amount = 0
    for amount in expense_data:
        total_amount += amount.expense_amount
    context = {'expense_data': expense_data, 'title': 'Expense', 'total_amount': total_amount}
    return render(request, "show_expense.html", context)

@admin_login_required
def add_expense_function(request):
    context = {"title": "Expense"}
    domain = request.get_host()
    if request.method == 'POST':
        form = expense_form(request.POST)
        if form.is_valid():
            form.instance.domain_name = domain
            messages.success(request, 'Expense has been added successfully')
            form.save()
            return redirect('show_expense')

    return render(request, "insert_update/add_expense.html", context)


@admin_login_required
def delete_expense_functions(request):
    domain  = request.get_host()
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Expense.objects.filter(expense_id__in=selected_ids, domain_name = domain).delete()
                messages.success(request, 'Expense Deleted Successfully')
            except Exception as e:
                messages.error(request, f'<i class="fa-solid fa-triangle-exclamation me-2"></i> An error occurred: {str(e)}')

    return redirect('show_expense')


@admin_login_required
def admin_show_group_function(request):
    domain = request.get_host()
    group_data = Groups.objects.filter(domain_name = domain)
    context = {'group_data': group_data, 'title': 'Groups'}
    return render(request, "show_groupps.html", context)


@admin_login_required
def admin_add_group_function(request):
    domain = request.get_host()
    if request.method == 'POST':
        form = group_form(request.POST)
        if form.is_valid():
            form.instance.domain_name = domain
            messages.success(request, "Group added successfully")
            form.save()
            return redirect('show_group')

    return render(request, "insert_update/add_group.html")


@admin_login_required
def admin_delete_group_function(request):
    if request.GET.get('pk'):
        pk = request.GET.get('pk')
        group_data = Groups.objects.get(group_id = pk)
        group_data.delete()
        messages.success(request, "Group deleted successully")
        return redirect('show_group')
    return render(request, "show_group.html")


@admin_login_required
def admin_show_material_function(request):
    context = {}
    domain = request.get_host()
    group_id = request.GET.get('group_id')
    materials_data = Materials.objects.filter(domain_name = domain, material_group_id__group_id = group_id)
    context.update({'materials_data': materials_data, 'title': 'Materials', 'group_id': group_id})
    return render(request, "show_material.html", context)



def generate_pdf_icon(pdf_file):
    # Read the file content into memory
    pdf_data = pdf_file.read()
    # Open the PDF from the memory
    doc = fitz.open(stream=pdf_data, filetype="pdf")
    # Select the first page
    page = doc.load_page(0)
    # Render the page to an image
    pix = page.get_pixmap()  
    # Convert to PIL Image
    image = Image.open(io.BytesIO(pix.tobytes("png")))
    # Save image to BytesIO object
    image_io = io.BytesIO()
    image.save(image_io, format="PNG")
    # Return a ContentFile that can be saved in the ImageField
    return ContentFile(image_io.getvalue(), name=f"{pdf_file.name.split('.')[0]}_icon.png")


@admin_login_required
def admin_add_material_function(request):
    domain = request.get_host()
    group_id = request.GET.get('group_id')
    group_data = Groups.objects.filter(domain_name = domain, group_id = group_id)
    context = {'group_data': group_data}
    if request.method == 'POST':
            group_id = request.POST.get('material_group_id')
            group_obj = Groups.objects.get(group_id = group_id)
            form = materials_form(request.POST, request.FILES)
            if form.is_valid():
                
                check = Materials.objects.filter(material_name = form.data['material_name'], domain_name = domain).count()
                pdf_file = form.cleaned_data['material_file']

                if check >= 1:
                    messages.error(request, '{} is already Exists'.format(form.data['material_name']))
                else:
                    form.instance.domain_name = domain
                    material = form.save(commit=False)
                    # Generate icon for the PDF file
                    material.material_icon.save(
                        pdf_file.name.replace('.pdf', '_icon.png'),
                        generate_pdf_icon(pdf_file),
                        save=False
                    )
                    material.material_name = pdf_file.name
                    material.material_group_id = group_obj
                    material.save()
                    messages.success(request, 'Material Added Successfully')
                    return redirect('show_material')
            else:
                filled_data = form.data
                context.update({'filled_data': filled_data, 'errors': form.errors})
                return render(request, 'insert_update/add_material.html', context)

    return render(request, 'insert_update/add_material.html', context)


@admin_login_required
def admin_delete_material_function(request):
    if request.GET.get('pk'):
        pk = request.GET.get('pk')
        material_data = Materials.objects.get(material_id = pk)
        material_data.delete()
        messages.success(request, "Material Deleted Successfully")
        return redirect('show_material')
    
    return render(request, "show_material.html")


@admin_login_required
def admin_show_pdf(request):
    context={}
    if request.GET.get('pdf'):
        pdf = Materials.objects.get(material_id = request.GET.get('pdf'))
        context.update({
            'pdf':pdf,
        })
    return render(request,'Show_pdf.html', context)    
