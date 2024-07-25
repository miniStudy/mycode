from django.shortcuts import render, redirect
from adminside.models import *
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import random
from parentsside.decorators import *

# mail integration 
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives

# Create your views here.

@parent_login_required
def parent_home(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'parentpanel/index.html', context)

def parent_login_page(request):
    title = 'Login' 
    login=1
    if request.COOKIES.get("stud_guardian_email"):
          cookie_email = request.COOKIES['stud_guardian_email']
          cookie_pass = request.COOKIES['stud_guardian_password']
          return render(request, 'parentpanel/master_auth.html',{'login_set':login,'c_email':cookie_email,'c_pass':cookie_pass, 'title':title})
    else:
          return render(request, 'parentpanel/master_auth.html',{'login_set':login, 'title':title})

def parent_login_handle(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        val = Students.objects.filter(stud_guardian_email=email,stud_guardian_password=password).count()
        if val==1:
            Data = Students.objects.filter(stud_guardian_email=email,stud_guardian_password=password)
            for item in Data:
               request.session['parent_id'] = item.stud_id
               request.session['parent_logged_in'] = 'yes'

            if request.POST.get("remember"):
               response = redirect("parent_home")
               response.set_cookie('stud_guardian_email', email) 
               response.set_cookie('stud_guardian_password', password)   
               return response
            
            messages.success(request, 'Logged In Successfully')
            
            return redirect('parent_home')
        else:
            messages.error(request, "Invalid Username & Password.")
            return redirect('parent_login')
    else:
        return redirect('teacher_login')

def parent_forget_password(request):
    title = 'Forget Password'  
    login=2
    if request.COOKIES.get("stud_guardian_email"):
          cookie_email = request.COOKIES['stud_guardian_email']
          return render(request, 'parentpanel/master_auth.html',{'login_set':login,'c_email':cookie_email, 'title':title})
    else:
          return render(request, 'parentpanel/master_auth.html',{'login_set':login, 'title':title})
    
def parent_handle_forget_password(request):
     if request.method == "POST":
          email2 = request.POST['email']

     # ------------mail sending ---------------
          sub = 'OTP from EDUPORTAL'
          otp = random.randint(000000,999999)
          mess = 'YOUR OTP IS {}'.format(otp)
          email_from = settings.EMAIL_HOST_USER
          recp_list = [email2,]
          send_mail(sub,mess,email_from,recp_list)
          otp_data = Students.objects.get(stud_guardian_email = email2)
          otp_data.stud_guardian_otp = otp
          otp_data.save()
          messages.success(request, "Otp Sent Successfully")
          url = f"{reverse('parent_set_new_password')}?email={email2}"
          return redirect(url)

     else:
          return redirect('parent_forget_password')
    
def parent_set_new_password(request):  
    login=3      
    # if request.GET.get('email'):
    #     foremail = request.GET['email']
    return render(request, 'parentpanel/master_auth.html',{'login_set':login})

def parent_handle_set_new_password(request):
     if request.method == "POST":
        otp = int(request.POST['otp'])
        password = request.POST['password']
        conf_password = request.POST['confirm_password']
        if password == conf_password:
             obj = Students.objects.filter(stud_guardian_otp = otp).count()
             if obj == 1:
                  data = Students.objects.get(stud_guardian_otp = otp)
                  data.stud_guardian_password = password
                  data.stud_guardian_otp = None
                  data.save()
                  response = redirect("parent_login")
                  response.set_cookie('stud_guardian_password', password)
                  messages.success(request, "Password has been changed Successfully")
                  return response
             
             else:
                  messages.error(request, "OTP is Wrong")
                  return redirect('parent_set_new_password')
        else:
             messages.error(request, "Password and Confirm Password are not same.")
             return redirect('parent_set_new_password')  
     else:
        messages.error(request, "Method is not Post")
        return redirect('parent_set_new_password')
 

def parent_logout_page(request):
    try:
        del request.session['parent_id']
        del request.session['parent_logged_in']
        messages.success(request, "Logged out Successfully")
        return redirect("parent_login")
    except:
        pass
    return redirect("parent_login")

@parent_login_required
def show_parent_events(request):
    event_data = Event.objects.all()
    event_imgs = Event_Image.objects.all()
    selected_events = Event.objects.all()[:1]
    context={
        'event_data':event_data,
        'event_imgs':event_imgs,
        'selected_events':selected_events,
        'title': 'Events'
    }

    if request.GET.get('event_id'):
        event_id = request.GET['event_id']
        selected_events = Event.objects.filter(event_id = event_id)
        event_imgs = Event_Image.objects.filter(event__event_id = event_id)
        
        context.update({'selected_events':selected_events, 'events_img':event_imgs})

    return render(request, 'parentpanel/events.html', context)

@parent_login_required
def show_parent_profile(request):
    title = 'Profile'
    parent_id = request.session['parent_id']
    parent_profile = Students.objects.filter(stud_id = parent_id)
    return render(request, 'parentpanel/parent_profile.html', {'parent_profile':parent_profile, 'title':title})