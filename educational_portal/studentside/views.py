from django.shortcuts import render,get_object_or_404,redirect
from adminside.models import *
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import math
import random
from django.http import Http404,JsonResponse
from .forms import update_form
# Create your views here.
# mail integration 
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from studentside.decorators import student_login_required
# Create your views here.


@student_login_required
def student_home(request):
     return render(request, 'studentpanel/index.html')

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

@student_login_required
def student_info_update(request):
    student_id = request.session['stud_id']
    student_obj = Students.objects.get(stud_id = student_id)
    if request.method == 'POST':
        form = update_form(request.POST, instance=student_obj)
        if form.is_valid():
            form.save()
            return redirect('Student_InfoUpdate')
        else:
            messages.error(request, 'error')
    return render(request, 'studentpanel/updateinfo.html', {'student_obj':student_obj})

@student_login_required
def student_announcement(request):
    # datas = Announcements.objects.get(announce_std__std_id=request.session.get('stud_id'))
    announcement = Announcements.objects.all()
    
    announce_1 = announcement.filter(announce_std=None, announce_batch=None)

    announce_2 = announcement.filter(announce_std__std_id=request.session.get('stud_std'), announce_batch=None)

    announce_3 = announcement.filter(announce_std__std_id=request.session.get('stud_std'), announce_batch__batch_id=request.session.get('stud_batch'))

    announcements_data = announce_1.union(announce_2, announce_3)
   
    return render(request, 'studentpanel/announcements.html', {"announcements_data":announcements_data})

@student_login_required
def show_subjects(request):
    stud_standard = request.session.get('stud_std')
    subjects = Subject.objects.filter(sub_std__std_id = stud_standard)
    return render(request, 'studentpanel/subjects.html', {'subjects':subjects})

@student_login_required
def show_chepters(request):
    if request.GET.get('sub_id'):
        id = request.GET['sub_id']  
        chepters = Chepter.objects.filter(chep_sub__sub_id = id)
    return render(request, 'studentpanel/chepters.html', {'chepters':chepters})

@student_login_required
def show_materials(request):
    student_std = request.session['stud_std']
    subjects = Subject.objects.filter(sub_std__std_id = student_std)
    materials = Chepterwise_material.objects.filter(cm_chepter__chep_std__std_id = student_std)

    if request.GET.get('sub_id'):
        id = request.GET['sub_id']
        materials = Chepterwise_material.objects.filter(cm_chepter__chep_sub__sub_id = id)

    return render(request, 'studentpanel/materials.html',{'materials':materials, 'subjects':subjects})

@student_login_required
def show_timetables(request):
    student_batch = request.session['stud_batch']
    timetable_data = Timetable.objects.filter(tt_batch__batch_id = student_batch)
    return render(request, 'studentpanel/timetable.html', {'timetable_data':timetable_data})


@student_login_required
def show_attendence(request):
    student_id = request.session['stud_id']
    student_name = request.session['stud_name']

    attendence_data = Attendance.objects.filter(atten_student__stud_id = student_id)

    total_days = Attendance.objects.filter(atten_student__stud_id = student_id).count()
    present_days = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=True).count()

    if total_days > 0:
        attendence_prec = round((present_days / total_days) * 100, 2)
    else:
        attendence_prec = 0
    
    subject_attendance = []
    subjects = Subject.objects.all().values('sub_name').distinct()
    for subject in subjects:
        subject = subject['sub_name']
        total_days_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = subject).count()
        present_days_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = subject, atten_present=True).count()
        if total_days_subwise > 0:
            attendence_prec_subwise = round((present_days_subwise / total_days_subwise) * 100, 2)
        else:
            attendence_prec_subwise = 0

        subject_attendance.append({
            'subject': subject,
            'attendence_prec_subwise': attendence_prec_subwise,
        })
    
    absent_days = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=False).count()
    
    return render(request, 'studentpanel/attendence.html', {'student_name':student_name, 'attendence_data':attendence_data, 'attendence_prec':attendence_prec, 'subject_attendance':subject_attendance,'total_days':total_days, 'absent_days':absent_days})

@student_login_required
def show_event(request):
    event_data = Event.objects.all()
    return render(request, 'studentpanel/event.html', {'event_data':event_data})

@student_login_required
def show_test(request):
    standard_id = request.session['stud_std']
    test_names = Chepterwise_test.objects.filter(test_std__std_id = standard_id)
    return render(request, 'studentpanel/test.html', {'test_names':test_names})

@student_login_required
def show_test_questions(request, id):
    
    
    if request.GET.get('que_id'):
        que_id = request.GET.get('que_id')
        test_question = Test_questions_answer.objects.filter(tq_id = que_id) 
    else:
        test_question = Test_questions_answer.objects.filter(tq_name__test_id = id)[:1]   
    
    
    test_questions_all = Test_questions_answer.objects.filter(tq_name__test_id = id)
    all_q_list = []
    if test_questions_all.exists():
        current_q_id = test_question[0].tq_id
        for x in test_questions_all:
            all_q_list.append(x.tq_id)


        index_posi = all_q_list.index(current_q_id)
        if all_q_list[index_posi] != all_q_list[-1]:
            next_id = all_q_list[index_posi+1]
        else:
            next_id = None

        if all_q_list[index_posi] != all_q_list[0]:
            prev_id = all_q_list[index_posi-1]
        else:
            prev_id = None
    
        return render(request, 'studentpanel/testque.html', {'test_questions_all':test_questions_all, 'test_question':test_question, 'test_id':id,'next_id':next_id, 'prev_id':prev_id})
    else:
        no_que = "There are no anymore questions!"
    
    return render(request, 'studentpanel/testque.html', {'test_questions_all':test_questions_all, 'test_question':test_question, 'no_que':no_que})