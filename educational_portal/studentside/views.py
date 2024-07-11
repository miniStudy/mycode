from django.shortcuts import render,get_object_or_404,redirect
from adminside.models import *
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import math
from django.db.models import Sum,Count
import random
from django.http import Http404,JsonResponse
from .forms import *
from django.db.models import OuterRef, Subquery, BooleanField,Q
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
            messages.success(request, 'Your information updated successfully')
            return redirect('Student_Profile')
        else:
            messages.error(request, 'error')
    else:
        form = update_form(instance=student_obj)
    return render(request, 'studentpanel/updateinfo.html', {'form':form, 'student_obj':student_obj})

@student_login_required
def student_announcement(request):
    announcements_data = Announcements.objects.filter(
    Q(announce_std=None, announce_batch=None) |
    Q(announce_std__std_id=request.session.get('stud_std'), announce_batch=None) |
    Q(announce_std__std_id=request.session.get('stud_std'), announce_batch__batch_id=request.session.get('stud_batch'))
).order_by('-pk')[:50]

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
    selected_sub=None
    print(materials)
    if request.GET.get('sub_id'):
        id = request.GET['sub_id']
        materials = materials.filter(cm_chepter__chep_sub__sub_id = id)
        selected_sub = Subject.objects.get(sub_id=id)

    return render(request, 'studentpanel/materials.html',{'materials':materials, 'subjects':subjects,'selected_sub':selected_sub})

@student_login_required
def show_timetables(request):
    student_batch = request.session['stud_batch']
    timetable_data = Timetable.objects.filter(tt_batch__batch_id = student_batch)
    return render(request, 'studentpanel/timetable.html', {'timetable_data':timetable_data})


@student_login_required
def show_attendence(request):
    student_id = request.session['stud_id']
    student_name = request.session['stud_name']
    student_std = request.session['stud_std']

    attendence_data = Attendance.objects.filter(atten_student__stud_id = student_id)

    total_days = Attendance.objects.filter(atten_student__stud_id = student_id).count()
    present_days = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=True).count()

    if total_days > 0:
        attendence_prec = round((present_days / total_days) * 100, 2)
    else:
        attendence_prec = 0
    
    subject_attendance = []
    subjects = Subject.objects.filter(sub_std__std_id = student_std).values('sub_name').distinct()
    for subject in subjects:
        subject = subject['sub_name']
        total_days_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = subject).count()
        present_days_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = subject, atten_present=True).count()
        if total_days_subwise > 0:
            attendence_prec_subwise = round((present_days_subwise / total_days_subwise) * 100, 2)
            subject_attendance.append({
            'subject': subject,
            'attendence_prec_subwise': attendence_prec_subwise,
        })
        
    absent_days = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=False).count()
    attendence_data = attendence_data.order_by('-pk')
    return render(request, 'studentpanel/attendence.html', {'student_name':student_name, 'attendence_data':attendence_data, 'attendence_prec':attendence_prec, 'subject_attendance':subject_attendance,'total_days':total_days, 'absent_days':absent_days})

@student_login_required
def show_event(request):
    event_data = Event.objects.all()
    event_imgs = Event_Image.objects.all()
    selected_events = Event.objects.all()[:1]
    context={
        'event_data':event_data,
        'event_imgs':event_imgs,
        'selected_events':selected_events
    }

    if request.GET.get('event_id'):
        event_id = request.GET['event_id']
        selected_events = Event.objects.filter(event_id = event_id)
        event_imgs = Event_Image.objects.filter(event__event_id = event_id)
        
        context.update({'selected_events':selected_events, 'events_img':event_imgs})

    return render(request, 'studentpanel/event.html', context)

@student_login_required
def show_test(request):
    standard_id = request.session['stud_std']
    test_names = Chepterwise_test.objects.filter(test_std__std_id = standard_id)
    return render(request, 'studentpanel/test.html', {'test_names':test_names})

@student_login_required
def show_test_questions(request, id):
    student_id = Students.objects.get(stud_id = request.session['stud_id'])
    if request.GET.get('que_id'):
        que_id = request.GET.get('que_id')
        test_question = Test_questions_answer.objects.filter(tq_id = que_id)
        

        if request.GET.get('ans'):
            quen_id = request.GET.get('current_q_id')
            quen_id = Test_questions_answer.objects.get(tq_id=quen_id)
            answer = request.GET.get('ans')
            test_attempted = 1
            data = Test_submission.objects.filter(ts_stud_id=student_id, ts_que_id=quen_id).count()
            if data == 0:
               Test_submission.objects.create(ts_stud_id=student_id, ts_que_id=quen_id, ts_ans=answer, ts_attempted=test_attempted)
            else:
                Test_submission.objects.filter(ts_stud_id=student_id, ts_que_id=quen_id).update(ts_ans=answer,ts_attempted=1)
   
        else:
            not_attemp = 0
    else:
        test_question = Test_questions_answer.objects.filter(tq_name__test_id = id)[:1]   
    
    subquery = Test_submission.objects.filter(ts_que_id = OuterRef('pk')).values('ts_attempted')[:1]
    test_questions_all = Test_questions_answer.objects.filter(tq_name__test_id = id).annotate(ts_attempted=Subquery(subquery,output_field = BooleanField()))
    all_q_list = []
    if test_questions_all.exists():
        current_q_id = test_question[0].tq_id
        for x in test_questions_all:
            all_q_list.append(x.tq_id)


        index_posi = all_q_list.index(current_q_id)
        if all_q_list[index_posi] != all_q_list[-1]:
            next_id = all_q_list[index_posi+1]
        else:
            next_id = all_q_list[0]
        
        if all_q_list[index_posi] != all_q_list[0]:
            prev_id = all_q_list[index_posi-1]
        else:
            prev_id = None

    #<===============================Check-Answers================================================>
        tq_idd = test_question[0].tq_id
        get_answer = Test_submission.objects.filter(ts_stud_id__stud_id = student_id.stud_id, ts_que_id__tq_id = tq_idd)
        if get_answer.exists():
            get_answer = get_answer[0].ts_ans
            # print(get_answer)
        else:
            get_answer = None
        
    # <=======================================Clear Selection Logic==============================>
        if request.GET.get('clear_id'):
            clear_id = request.GET['clear_id']
            Test_submission.objects.get(ts_stud_id__stud_id = student_id.stud_id, ts_que_id__tq_id = clear_id).delete()
            return redirect('/studentside/Student_Test_Q/{}/?que_id={}'.format(id,clear_id))
        context = {
            'test_questions_all':test_questions_all,
            'test_question':test_question,
            'test_id':id,
            'next_id':next_id,
            'prev_id':prev_id,
            'get_answer':get_answer,
            'student_id':student_id
        }
        return render(request, 'studentpanel/testque.html', context)
    else:
        no_que = "No questions available right now!"
    context = {
            'test_questions_all':test_questions_all,
            'test_question':test_question,
            'test_id':id,
            'no_que':no_que,
            'student_id':student_id
        }
    return render(request, 'studentpanel/testque.html', context)

def Student_Test_Submission(request):
    if request.POST.get("test_id"):
        test_id = request.POST['test_id'] 
        student_id = request.POST['student_id'] 
        total_attemped_que = Test_submission.objects.filter(ts_que_id__tq_name__test_id = test_id, ts_stud_id__stud_id = student_id, ts_attempted=1).count()
        print("----",total_attemped_que)
        total_test_marks = Chepterwise_test.objects.filter(test_id = test_id).annotate(totaltest_marks = Sum('test_questions_answer__tq_weightage'))
        print(total_test_marks[0].totaltest_marks)
    return redirect('Student_Test')
        

def show_syllabus(request):
    student_std = request.session['stud_std']
    subjects = Subject.objects.filter(sub_std__std_id = student_std)
    chepters = Chepter.objects.filter(chep_sub__sub_std__std_id = student_std)
    return render(request, 'studentpanel/syllabus.html', {'subjects':subjects,'chepters':chepters})

def student_inquiries_data(request):
    standard_data = Std.objects.all()
    if request.method == 'POST':
        form = student_inquiries(request.POST)
        print(form)
        if form.is_valid():
            form.save()
        else:
            print("Form is not valid")
    else:
        form = student_inquiries()
    return render(request, 'studentpanel/inquiries.html', {'form':form, 'standard_data':standard_data})


def student_profile(request):
    student_id = request.session['stud_id']
    student_profile = Students.objects.filter(stud_id = student_id)
    return render(request, 'studentpanel/myprofile.html', {'student_profile':student_profile})

def Student_doubt_section(request):
    student_id = request.session['stud_id']
    doubt_data = Doubt_section.objects.filter(doubt_stud_id__stud_id = student_id)

    context = {
        'doubt_data':doubt_data,
    }
    return render(request, 'studentpanel/doubt.html', context)

def Student_doubt_solution_section(request):
    student_id = request.session['stud_id']
    if request.GET.get('doubt_id'):
        doubt_id = request.GET.get('doubt_id')
        doubt_solution = Doubt_solution.objects.filter(solution_doubt_id__doubt_id = doubt_id)

    if request.method == 'POST':
        solu = request.POST.get('solution')
        Doubt_solution(solution=solu, solution_doubt_id=doubt_id, solution_stud_id=student_id).save()
    
    context = {
        'doubt_solution':doubt_solution
    }

    return render(request, 'studentpanel/solution.html', context)