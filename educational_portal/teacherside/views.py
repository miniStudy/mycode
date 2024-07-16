from django.shortcuts import render, redirect
from adminside.models import Faculties
from django.contrib import messages
import random
from django.urls import reverse
from django.conf import settings
# mail integration 
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives

# Create your views here.

def teacher_home(request):
     return render(request, 'teacherpanel/index.html')

def teacher_login_page(request):  
    login=1
    if request.COOKIES.get("fac_email"):
          cookie_email = request.COOKIES['fac_email']
          cookie_pass = request.COOKIES['fac_password']
          return render(request, 'teacherpanel/master_auth.html',{'login_set':login,'c_email':cookie_email,'c_pass':cookie_pass})
    else:
          return render(request, 'teacherpanel/master_auth.html',{'login_set':login})

def teacher_login_handle(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        val = Faculties.objects.filter(fac_email=email,fac_password=password).count()
        if val==1:
            Data = Faculties.objects.filter(fac_email=email,fac_password=password)
            for item in Data:
               request.session['fac_id'] = item.fac_id
               request.session['fac_logged_in'] = 'yes'

            if request.POST.get("remember"):
               response = redirect("teacher_home")
               response.set_cookie('fac_email', email) 
               response.set_cookie('fac_password', password)   
               return response
            
            messages.success(request, 'Logged In Successfully')
            
            return redirect('teacher_home')
        else:
            messages.error(request, "Invalid Username & Password.")
            return redirect('Student_Login')
    else:
        return redirect('teacher_login')

def teacher_forget_password(request):  
    login=2
    if request.COOKIES.get("fac_email"):
          cookie_email = request.COOKIES['fac_email']
          return render(request, 'master_auth.html',{'login_set':login,'c_email':cookie_email})
    else:
          return render(request, 'teacherpanel/master_auth.html',{'login_set':login})
    
def teacher_handle_forget_password(request):
     if request.method == "POST":
          email2 = request.POST['email']

     # ------------mail sending ---------------
          sub = 'OTP from EDUPORTAL'
          otp = random.randint(000000,999999)
          mess = 'YOUR OTP IS {}'.format(otp)
          email_from = settings.EMAIL_HOST_USER
          recp_list = [email2,]
          send_mail(sub,mess,email_from,recp_list)
          otp_data = Faculties.objects.get(fac_email = email2)
          otp_data.fac_otp = otp
          otp_data.save()
          messages.success(request, "Otp Sent Successfully")
          url = f"{reverse('teacher_set_new_password')}?email={email2}"
          return redirect(url)

     else:
          return redirect('teacher_forget_password')
    
def teacher_set_new_password(request):  
    login=3      
    if request.GET.get('email'):
         foremail = request.GET['email']
    return render(request, 'teacherpanel/master_auth.html',{'login_set':login,'email':foremail})

def teacher_handle_set_new_password(request):
     if request.method == "POST":
        otp = int(request.POST['otp'])
        password = request.POST['password']
        conf_password = request.POST['confirm_password']
        if password == conf_password:
             obj = Faculties.objects.filter(fac_otp = otp).count()
             if obj == 1:
                  data = Faculties.objects.get(fac_otp = otp)
                  data.fac_password = password
                  data.fac_otp = otp
                  data.save()
                  response = redirect("teacher_login")
                  response.set_cookie('fac_password', password)
                  messages.success(request, "Password has been changed Successfully")
                  return response
             
             else:
                  messages.error(request, "OTP is Wrong")
                  return redirect('Student_Set_New_Password')
        else:
             messages.error(request, "Password and Confirm Password are not same.")
             return redirect('teacher_set_new_password')  
     else:
        messages.error(request, "Method is not Post")
        return redirect('teacher_set_new_password')
 

def teacher_logout_page(request):
    try:
        del request.session['fac_id']
        del request.session['fac_logged_in']
        messages.success(request, "Logged out Successfully")
        return redirect("teacher_login")
    except:
        pass
    return redirect("teacher_login")