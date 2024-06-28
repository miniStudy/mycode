from django.shortcuts import render,get_object_or_404,redirect
from adminside.models import *
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import math
import random
from django.http import Http404,JsonResponse
# Create your views here.
# mail integration 
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from studentside.decorators import student_login_required
# Create your views here.


def student_home(request):
     return render(request, 'studentpanel/studenthome.html')

def student_login_page(request):  
    login=1
    if request.COOKIES.get("stud_email"):
            cookie_email = request.COOKIES['stud_email']
            cookie_pass = request.COOKIES['stud_password']
            return render(request, 'studentpanel/master_auth.html',{'login_set':login,'c_email':cookie_email,'c_pass':cookie_pass})
    else:
            return render(request, 'studentpanel/master_auth.html',{'login_set':login})

def student_login_handle(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        val = Students.objects.filter(stud_email=email,stud_pass=password).count()
        if val==1:
            Data = Students.objects.filter(stud_email=email,stud_pass=password)
            for item in Data:
                request.session['stud_id'] = item.stud_id
                request.session['stud_name'] = item.stud_name
                request.session['stud_batch'] = item.stud_batch.batch_id
                request.session['stud_std'] = item.stud_std.std_id
                request.session['stud_logged_in'] = 'yes'

            if request.POST.get("remember"):
                response = redirect("Student_home")
                response.set_cookie('stud_email', email) 
                response.set_cookie('stud_password', password)   
                return response
            
            messages.success(request, 'Logged In Successfully')
            
            return redirect('Student_home')
        else:
            messages.error(request, "Invalid Username & Password.")
            return redirect('Student_Login')
    else:
        return redirect('Student_Login')

def student_Forgot_Password(request):  
    login=2
    if request.COOKIES.get("student_email"):
            cookie_email = request.COOKIES['stud_email']
            return render(request, 'master_auth.html',{'login_set':login,'c_email':cookie_email})
    else:
            return render(request, 'studentpanel/master_auth.html',{'login_set':login})
    
def student_handle_forgot_password(request):
     if request.method == "POST":
        email2 = request.POST['email']

     # ------------mail sending ---------------

        sub = 'OTP from EDUPORTAL'
        otp = random.randint(000000,999999)
        mess = 'YOUR OTP IS {}'.format(otp)
        email_from = settings.EMAIL_HOST_USER
        recp_list = [email2,]
        send_mail(sub,mess,email_from,recp_list)
        daata = Students.objects.get(stud_email = email2)
        daata.stud_otp = otp
        daata.save()
        messages.success(request, "Otp Sent Successfully")
        url = f"{reverse('Student_Set_New_Password')}?email={email2}"
        return redirect(url)
     else:
        return redirect('Student_Forgot_Password')
    
def student_Set_New_Password(request):  
    login=3      
    if request.GET.get('email'):
         foremail = request.GET['email']
    return render(request, 'studentpanel/master_auth.html',{'login_set':login,'email':foremail})

def student_handle_set_new_password(request):
     if request.method == "POST":
        otp = int(request.POST['otp'])
        password = request.POST['password']
        conf_password = request.POST['confirm_password']
        if password == conf_password:
             obj = Students.objects.filter(stud_otp = otp).count()
             if obj == 1:
                  data = Students.objects.get(stud_otp = otp)
                  data.stud_pass = password
                  data.stud_otp = otp
                  data.save()
                  response = redirect("Student_Login")
                  response.set_cookie('stud_password', password)
                  messages.success(request, "Password has been changed Successfully")
                  return response
             
             else:
                  messages.error(request, "OTP is Wrong")
                  return redirect('Student_Set_New_Password')
        else:
             messages.error(request, "Password and Confirm Password are not same.")
             return redirect('Student_Set_New_Password')  
     else:
        messages.error(request, "Method is not Post")
        return redirect('Student_Set_New_Password')
 
     
def student_logout(request):
    try:
        del request.session['stud_id']
        del request.session['stud_name']
        del request.session['stud_logged_in']
        messages.success(request, "Logged out Successfully")
        return redirect("Student_Login")
    except:
        pass
    return redirect("Student_Login")

def student_announcement(request):
    # datas = Announcements.objects.get(announce_std__std_id=request.session.get('stud_id'))
    announcement = Announcements.objects.all()
    announce_1 = announcement.filter(announce_std=None, announce_batch=None)

    announce_2 = announcement.filter(announce_std__std_id=request.session.get('stud_std'), announce_batch=None)

    announce_3 = announcement.filter(announce_std__std_id=request.session.get('stud_std'), announce_batch__batch_id=request.session.get('stud_batch'))

    announcements_data = announce_1.union(announce_2, announce_3)

    
    return render(request, 'studentpanel/announcements.html', {"announcements_data":announcements_data})