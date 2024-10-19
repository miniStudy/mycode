from django.shortcuts import render,get_object_or_404,redirect
from adminside.models import *
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import math
import statistics
from django.db.models import Sum,Count,Avg, Value
from django.db.models import Count, Case, When, IntegerField
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
from datetime import datetime, timedelta
from django.utils.timezone import now
from team_ministudy.models import *

import logging

logger = logging.getLogger(__name__)
# from .send_mail import *
# Create your views here.


@student_login_required
def student_home(request):
    domain = request.get_host()
    std_id = request.session['stud_std']
    stud_id = request.session['stud_id']
    student_onesignal_player_id = request.session.get('deviceId', 'Error')
    logger.error("============================playerid:{}".format(student_onesignal_player_id))
    if student_onesignal_player_id != 'Error':
        studentsdata = Students.objects.get(stud_id = stud_id)
        studentsdata.stud_onesignal_player_id = student_onesignal_player_id
        logger.error("============================playerid:{}".format(studentsdata.stud_onesignal_player_id))
        studentsdata.save()
    today = datetime.today()
    cusrrent_student = Students.objects.get(stud_id=stud_id)
    
    day = today - timedelta(days=7)
    last_7_days=(day.strftime('%Y-%m-%d'))

    current_doubts = Doubt_section.objects.filter(doubt_date__date__gt=last_7_days, doubt_stud_id__stud_std__std_id = std_id, domain_name = domain).count()

    current_announcements = Announcements.objects.filter(announce_date__date__gt=last_7_days).filter(
        Q(announce_std=None, announce_batch=None) |
        Q(announce_std__std_id=request.session.get('stud_std'), announce_batch=None) |
        Q(announce_std__std_id=request.session.get('stud_std'), announce_batch__batch_id=request.session.get('stud_batch')), domain_name = domain).count()

    day_name = today.strftime('%A')

    today_timetable = Timetable.objects.filter(tt_day=day_name, tt_batch__batch_id = request.session['stud_batch'], tt_subject1__sub_std__std_id = std_id, domain_name = domain)
    

    student_id = request.session['stud_id']
    student_std = request.session['stud_std']
    students_li = Students.objects.filter(stud_std__std_id = student_std, domain_name = domain)
    overall_attendance_li = []
    for x in students_li:
        total_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x.stud_id, domain_name = domain).count()
        present_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x.stud_id, atten_present=True, domain_name = domain).count()
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

        overall_attendance_li.append({'stud_name':x.stud_name, 'stud_lastname':x.stud_lastname, 'overall_attendance_studentwise':overall_attendence_studentwise, 'overall_result':overall_result})


    overall_attendance_li = sorted(overall_attendance_li, key=lambda x: x['overall_result'], reverse=True)
    overall_attendance_li = overall_attendance_li[:5]

    #=============== Test Result Dashboard ===============================================================
    test_result_analysis = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id, domain_name = domain).values('tau_test_id__test_name', 'tau_obtained_marks').order_by('-pk')

    test_counts = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id, domain_name = domain).count()

    test_result_list = []
    test_name_list = []
    for x in test_result_analysis:
        test_name_list.append(x['tau_test_id__test_name'])
        test_result_list.append(x['tau_obtained_marks'])
    
    context = {
        'title':'Home',
        'current_doubts':current_doubts,
        'current_announcements':current_announcements,
        'today_timetable': today_timetable,
        'overall_attendance_li':overall_attendance_li,
        'test_result_analysis':test_result_analysis,
        'test_result_list':test_result_list,
        'test_name_list': test_name_list,
        'test_counts':test_counts,
        'cusrrent_student':cusrrent_student,
    }
    return render(request, 'studentpanel/index.html',context)

def student_login_page(request): 
    login=1
    if request.COOKIES.get("stud_email"):
            cookie_email = request.COOKIES['stud_email']
            cookie_pass = request.COOKIES['stud_password']
            return render(request, 'studentpanel/master_auth.html',{'login_set':login,'c_email':cookie_email,'c_pass':cookie_pass, 'title':'login'})
    else:
            return render(request, 'studentpanel/master_auth.html',{'login_set':login, 'title':'login'})

def student_login_handle(request):
    domain = request.get_host()
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        val = Students.objects.filter(stud_email=email,stud_pass=password, domain_name = domain).count()
        if val==1:
            Data = Students.objects.filter(stud_email=email,stud_pass=password, domain_name = domain)
            for item in Data:
                request.session['stud_id'] = item.stud_id
                request.session['stud_name'] = item.stud_name
                request.session['stud_batch'] = item.stud_batch.batch_id
                request.session['stud_std'] = item.stud_std.std_id
                request.session['stud_profile'] = '{}'.format(item.stud_profile)
                request.session['stud_logged_in'] = 'yes'

            if request.POST.get("remember"):
                response = redirect("Student_home")
                response.set_cookie('stud_email', email) 
                response.set_cookie('stud_password', password)   
                return response
            
            messages.success(request, 'Logged In Successfully')
            
            if NewInstitution.objects.get(institute_lock = False):
                return redirect('Student_home')
            else:
                return redirect('Lock_Page')
        else:
            messages.error(request, "Invalid Username & Password.")
            return redirect('Student_Login')
    else:
        return redirect('Student_Login')

def student_Forgot_Password(request): 
    login=2
    if request.COOKIES.get("student_email"):
            cookie_email = request.COOKIES['stud_email']
            return render(request, 'master_auth.html',{'login_set':login,'c_email':cookie_email, 'title':'Forget Password'})
    else:
            return render(request, 'studentpanel/master_auth.html',{'login_set':login, 'title':'Forget Password'})
    
def student_handle_forgot_password(request):
    domain = request.get_host()
    if request.method == "POST":
        email2 = request.POST['email']
        val = AdminData.objects.filter(admin_email=email2, domain_name = domain).count()
        if val!=1:
            messages.error(request, "Email is Wrong")
            url = f"{reverse('Student_Forgot_Password')}?email={email2}"
            return redirect(url)
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
    title = 'New Password'
    login=3      
    if request.GET.get('email'):
         foremail = request.GET['email']
    return render(request, 'studentpanel/master_auth.html',{'login_set':login,'email':foremail, 'title':title})

def student_handle_set_new_password(request):
    domain = request.get_host()
    if request.method == "POST":
        otp = int(request.POST['otp'])
        password = request.POST['password']
        conf_password = request.POST['confirm_password']
        if password == conf_password:
             obj = Students.objects.filter(stud_otp = otp, domain_name = domain).count()
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
    domain = request.get_host()
    title = 'Update Profile'
    student_id = request.session['stud_id']
    student_obj = Students.objects.get(stud_id = student_id)
    if request.method == 'POST':
        form = update_form(request.POST, instance=student_obj)
        if form.is_valid():
            form.instance.domain_name = domain
            form.save()
            messages.success(request, 'Your information updated successfully')
            return redirect('Student_Profile')
        else:
            messages.error(request, 'error')
    else:
        form = update_form(instance=student_obj)
    return render(request, 'studentpanel/updateinfo.html', {'form':form, 'student_obj':student_obj, 'title':title})

@student_login_required
def student_announcement(request):
    domain = request.get_host()
    title = 'Announcements'
    announcements_data = Announcements.objects.filter(
    Q(announce_std=None, announce_batch=None) |
    Q(announce_std__std_id=request.session.get('stud_std'), announce_batch=None) |
    Q(announce_std__std_id=request.session.get('stud_std'), announce_batch__batch_id=request.session.get('stud_batch')), domain_name = domain).values('announce_title', 'announce_id', 'announce_msg', 'announce_date').order_by('-pk')[:50]

    return render(request, 'studentpanel/announcements.html', {"announcements_data":announcements_data, 'title':title})


@student_login_required
def show_subjects(request):
    domain = request.get_host()
    title = 'Subjects'
    stud_standard = request.session.get('stud_std')
    subjects = Subject.objects.filter(sub_std__std_id = stud_standard, domain_name = domain)
    return render(request, 'studentpanel/subjects.html', {'subjects':subjects, 'title':title})


@student_login_required
def show_chepters(request):
    domain = request.get_host()
    title = 'Chepters'
    if request.GET.get('sub_id'):
        id = request.GET['sub_id']  
        chepters = Chepter.objects.filter(chep_sub__sub_id = id, domain_name = domain)
    return render(request, 'studentpanel/chepters.html', {'chepters':chepters, 'title':title})


@student_login_required
def show_materials(request):
    domain = request.get_host()
    title = 'Materials'
    student_std = request.session['stud_std']
    student_id = request.session['stud_id']
    student = Students.objects.get(stud_id=student_id)
    subjects = student.stud_pack.pack_subjects.filter(domain_name = domain)
              
    materials = Chepterwise_material.objects.filter(cm_chepter__chep_std__std_id = student_std, domain_name = domain).values('cm_filename', 'cm_chepter__chep_sub__sub_id', 'cm_file', 'cm_chepter__chep_sub__sub_name','cm_chepter__chep_sub__sub_id','cm_file_icon')
    selected_sub=None
    if request.GET.get('sub_id'):
        id = request.GET['sub_id']
        materials = materials.filter(cm_chepter__chep_sub__sub_id = id, domain_name = domain).values('cm_filename', 'cm_chepter__chep_sub__sub_id', 'cm_file', 'cm_chepter__chep_sub__sub_name','cm_chepter__chep_sub__sub_id','cm_file_icon')
        selected_sub = Subject.objects.get(sub_id=id)

    return render(request, 'studentpanel/materials.html',{'materials':materials, 'subjects':subjects,'selected_sub':selected_sub, 'title':title})

@student_login_required
def show_timetables(request):
    domain = request.get_host()
    title = 'Timetable'
    student_batch = request.session['stud_batch']
    timetable_data = Timetable.objects.filter(tt_batch__batch_id = student_batch, domain_name = domain)
    return render(request, 'studentpanel/timetable.html', {'timetable_data':timetable_data, 'title':title})


@student_login_required
def show_attendence(request):
    domain = request.get_host()
    title = 'Attendance'
    student_id = request.session['stud_id']
    student_name = request.session['stud_name']
    student_std = request.session['stud_std']

    attendence_data = Attendance.objects.filter(atten_student__stud_id = student_id, domain_name = domain).values('atten_timetable__tt_day', 'atten_timetable__tt_subject1__sub_name', 'atten_date', 'atten_present')

    total_days = Attendance.objects.filter(atten_student__stud_id = student_id, domain_name = domain).count()
    present_days = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=True, domain_name = domain).count()

    if total_days > 0:
        attendence_prec = round((present_days / total_days) * 100, 2)
    else:
        attendence_prec = 0
    
    subject_attendance = []
    subjects = Subject.objects.filter(sub_std__std_id = student_std, domain_name = domain).values('sub_name').distinct()
    for subject in subjects:
        subject = subject['sub_name']
        total_days_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = subject, atten_student__stud_id = student_id, domain_name = domain).count()
        present_days_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = subject, atten_student__stud_id = student_id, atten_present=True, domain_name = domain).count()
        if total_days_subwise > 0:
            attendence_prec_subwise = round((present_days_subwise / total_days_subwise) * 100, 2)
            subject_attendance.append({
            'subject': subject,
            'attendence_prec_subwise': attendence_prec_subwise,
        })
        
    absent_days = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=False, domain_name = domain).count()
    attendence_data = attendence_data.order_by('-pk')
    return render(request, 'studentpanel/attendence.html', {'student_name':student_name, 'attendence_data':attendence_data, 'attendence_prec':attendence_prec, 'subject_attendance':subject_attendance,'total_days':total_days, 'absent_days':absent_days, 'title':title})

@student_login_required
def show_event(request):
    domain = request.get_host()
    event_data = Event.objects.filter(domain_name = domain).values('event_id', 'event_name')
    event_imgs = Event_Image.objects.filter(domain_name = domain)
    selected_events = Event.objects.filter(domain_name = domain).first()
    context={
        'event_data':event_data,
        'event_imgs':event_imgs,
        'selected_events':selected_events,
        'title': 'Events'
    }
    if request.GET.get('event_id'):
        event_id = request.GET['event_id']
        selected_events = Event.objects.get(event_id = event_id)
        event_imgs = Event_Image.objects.filter(event__event_id = event_id, domain_name = domain)
        context.update({'selected_events':selected_events, 'event_imgs':event_imgs})

    return render(request, 'studentpanel/event.html', context)

from django.db.models import Avg

@student_login_required
def show_test(request):
    domain = request.get_host()
    student_id = request.session['stud_id']
    
    test_analysis_data = Test_attempted_users.objects.filter(tau_stud_id__stud_id=student_id, domain_name = domain)

    average_marks = Test_attempted_users.objects.filter(domain_name = domain).values('tau_test_id').annotate(average_marks=Avg('tau_obtained_marks'))
    avg_marks_dict = {item['tau_test_id']: item['average_marks'] for item in average_marks}

    test_details = []
    for data in test_analysis_data:
        test_details.append({
            'test_name': data.tau_test_id.test_name,
            'sub_name': data.tau_test_id.test_sub.sub_name,
            'total_marks': data.tau_total_marks,
            'time_taken': data.tau_completion_time,
            'obtained_marks': data.tau_obtained_marks,
            'date': data.tau_date,
            'avg_marks': round(avg_marks_dict.get(data.tau_test_id.test_id, 0),2)
        })

    context = {
        'title': 'Tests',
        'test_analysis_data': test_details  # Pass the detailed test data to the context
    }
    return render(request, 'studentpanel/test.html', context)


@student_login_required
def show_test_questions(request, id):
    domain = request.get_host()
    domain = None
    student_id = Students.objects.get(stud_id=request.session['stud_id'])
    test = Chepterwise_test.objects.get(test_id=id)

    # Check if test start time is in session
    if 'start_time' not in request.session:
        request.session['start_time'] = str(now())
    start_time = datetime.fromisoformat(request.session['start_time'])

    # Calculate remaining time
    test_duration = timedelta(minutes=int(test.test_time))  
    elapsed_time = now() - start_time
    remaining_time = test_duration - elapsed_time

    # If time is up, redirect to submission
    if remaining_time <= timedelta(0):
        return redirect('/studentside/Student_Test_Submission/')

    if request.GET.get('que_id'):
        que_id = request.GET.get('que_id')
        test_question = Test_questions_answer.objects.filter(tq_id=que_id, domain_name = domain)

        if request.GET.get('ans'):
            quen_id = request.GET.get('current_q_id')
            quen_id = Test_questions_answer.objects.get(tq_id=quen_id)
            answer = request.GET.get('ans')
            test_attempted = 1
            data = Test_submission.objects.filter(ts_stud_id=student_id, ts_que_id=quen_id, domain_name = domain).count()
            if data == 0:
                Test_submission.objects.create(ts_stud_id=student_id, ts_que_id=quen_id, ts_ans=answer, ts_attempted=test_attempted, domain_name = domain)
            else:
                Test_submission.objects.filter(ts_stud_id=student_id, ts_que_id=quen_id, domain_name = domain).update(ts_ans=answer, ts_attempted=1)
        else:
            not_attemp = 0
    else:
        test_question = Test_questions_answer.objects.filter(tq_name__test_id=id, domain_name = domain)[:1]

    subquery = Test_submission.objects.filter(ts_que_id=OuterRef('pk'), domain_name = domain).values('ts_attempted')[:1]
    test_questions_all = Test_questions_answer.objects.filter(tq_name__test_id=id, domain_name = domain).annotate(ts_attempted=Subquery(subquery, output_field=BooleanField()))
    all_q_list = []
    if test_questions_all.exists():
        current_q_id = test_question[0].tq_id
        for x in test_questions_all:
            all_q_list.append(x.tq_id)

        index_posi = all_q_list.index(current_q_id)
        if all_q_list[index_posi] != all_q_list[-1]:
            next_id = all_q_list[index_posi + 1]
        else:
            next_id = all_q_list[0]

        if all_q_list[index_posi] != all_q_list[0]:
            prev_id = all_q_list[index_posi - 1]
        else:
            prev_id = None

        tq_idd = test_question[0].tq_id
        get_answer = Test_submission.objects.filter(ts_stud_id__stud_id=student_id.stud_id, ts_que_id__tq_id=tq_idd, domain_name = domain)
        if get_answer.exists():
            get_answer = get_answer[0].ts_ans
        else:
            get_answer = None

        if request.GET.get('clear_id'):
            clear_id = request.GET['clear_id']
            Test_submission.objects.get(ts_stud_id__stud_id=student_id.stud_id, ts_que_id__tq_id=clear_id, domain_name = domain).delete()
            return redirect('/studentside/Student_Test_Q/{}/?que_id={}'.format(id, clear_id))

        context = {
            'test_questions_all': test_questions_all,
            'test_question': test_question,
            'test_id': id,
            'next_id': next_id,
            'prev_id': prev_id,
            'get_answer': get_answer,
            'student_id': student_id,
            'remaining_time': remaining_time.total_seconds(),  # Pass remaining time in seconds
            'title': 'Test Questions',
        }   
        return render(request, 'studentpanel/testque.html', context)
    else:
        no_que = "No questions available right now!"
    context = {
        'test_questions_all': test_questions_all,
        'test_question': test_question,
        'test_id': id,
        'no_que': no_que,
        'student_id': student_id,
        'remaining_time': remaining_time.total_seconds()  # Pass remaining time in seconds
    }
    return render(request, 'studentpanel/testque.html', context)

@student_login_required
def Student_Test_Submission(request):
    domain = request.get_host()
    if request.POST.get("test_id"):
        test_id = request.POST['test_id'] 
        student_id = request.POST['student_id'] 
        total_attemped_que = Test_submission.objects.filter(ts_que_id__tq_name__test_id = test_id, ts_stud_id__stud_id = student_id, ts_attempted=1, domain_name = domain).count()
        total_test_marks = Chepterwise_test.objects.filter(test_id = test_id, domain_name = domain).annotate(totaltest_marks = Sum('test_questions_answer__tq_weightage'))
    return redirect('Student_Test')
        
@student_login_required
def show_syllabus(request):
    domain = request.get_host()
    student_std = request.session['stud_std']
    student_id = request.session['stud_id']
    syllabus_data = Syllabus.objects.filter(syllabus_chapter__chep_std__std_id = student_std, domain_name = domain)
    student = Students.objects.get(stud_id=student_id)
    subjects = student.stud_pack.pack_subjects.filter(domain_name = domain)
    chepters = Chepter.objects.filter(chep_sub__sub_std__std_id = student_std, domain_name = domain).annotate(status=Case(When(syllabus__syllabus_status = None, then=Value(0)), default=1, output_filed=IntegerField())).values('chep_sub__sub_id','chep_name', 'status')
    context = {
        'subjects':subjects,
        'chepters':chepters, 
        'syllabus_data':syllabus_data,
        'title':'Syllabus',
    }
    return render(request, 'studentpanel/syllabus.html', context)

def student_inquiries_data(request):
    title = 'Inquiries'
    domain = request.get_host()
    standard_data = Std.objects.filter(domain_name = domain)
    package_data = Packs.objects.filter(domain_name = domain)
    subjects = Subject.objects.filter(domain_name=domain)
    unique_subjects = {subject.sub_name: subject for subject in subjects}.values()
    subjects_data = list(unique_subjects)

    if request.method == 'POST':
        form = student_inquiries(request.POST)
        if form.is_valid():
            selected_subjects = request.POST.getlist('stud_pack[]')
            form.instance.inq_subjects = ', '.join(selected_subjects)
            form.instance.domain_name = domain
            student_name = form.cleaned_data['inq_name']
            student_email = form.cleaned_data['inq_email']
            form.save()
            admin_emails = AdminData.objects.values_list('admin_email', flat=True)
            # admin_email_send(admin_emails, student_name, student_email, selected_subjects)
            messages.success(request, "Inquiry saved successfully!")
            return redirect('Student_Inquiries')
        else:
            messages.error(request, "Form is not valid!")
            return redirect('Student_Inquiries')
    else:
        form = student_inquiries()

    return render(
        request, 
        'studentpanel/inquiries.html', 
        {'form': form, 'standard_data': standard_data, 'package_data': package_data, 'subjects_data': subjects_data, 'title': title}
    )

@student_login_required
def student_profile(request):
    domain = request.get_host()
    title = 'Profile'
    student_id = request.session['stud_id']
    student_profile = Students.objects.get(stud_id = student_id)
    return render(request, 'studentpanel/myprofile.html', {'student':student_profile, 'title':title})

@student_login_required
def Student_doubt_section(request):
    domain = request.get_host()
    student_id = request.session['stud_id']
    current_stud = Students.objects.get(stud_id = student_id) 
    doubt_data = Doubt_section.objects.filter(
    doubt_subject__sub_std__std_id = current_stud.stud_std.std_id, domain_name = domain).annotate(count_solution=Count('doubt_solution'),verified_solution=Count(
        Case(
            When(doubt_solution__solution_verified=True, then=1),
            output_field=IntegerField(),
        ))).values('doubt_id', 'doubt_date', 'doubt_doubt', 'doubt_subject__sub_name', 'doubt_stud_id__stud_name', 'doubt_stud_id__stud_lastname', 'verified_solution', 'count_solution')   .order_by('-pk')[:30]
    
    context = {
        'doubt_data':doubt_data,
        'title': 'Doubts'
    }
    return render(request, 'studentpanel/doubt.html', context)


@student_login_required
def Student_add_doubts(request):
    domain = request.get_host()
    student_id = request.session['stud_id']
    student = Students.objects.get(stud_id=student_id)
    subjects_li = student.stud_pack.pack_subjects.filter(domain_name = domain)

    context = {
    'student_id':student_id,
    'subjects':subjects_li,
    'title': 'Doubts'
    }

    if request.method == 'POST':
        form = doubts_form(request.POST)
        if form.is_valid():
            form.instance.domain_name = domain
            form.save()
            return redirect('Student_Doubt') 
    form = doubts_form()   
    context.update({'form':form}) 

    return render(request, 'studentpanel/add_doubts.html', context)

@student_login_required
def Student_doubt_solution_section(request):
    domain = request.get_host()
    student_id = request.session['stud_id']
    context = {'student_id':student_id, 'title': 'Doubts'}
    if request.GET.get('doubt_id'):
        doubt_id = request.GET.get('doubt_id')
        doubt_solution = Doubt_solution.objects.filter(solution_doubt_id__doubt_id = doubt_id, domain_name = domain)
        context.update({'doubt_solution':doubt_solution,'doubt_id':doubt_id})
  
    if request.method == 'POST':
        form = solution_form(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['solution_stud_id']
            doubt_id = form.cleaned_data['solution_doubt_id']
            a = doubt_id.doubt_id
            count_sol = Doubt_solution.objects.filter(solution_stud_id = student_id, solution_doubt_id__doubt_id=a, domain_name = domain).count()

            if count_sol == 1:
                messages.error(request, "Cannot add more than one solution!")
                return redirect('/studentside/Student_Show_Solution/?doubt_id={}'.format(a))
            else:
                form.instance.domain_name = domain
                form.save()
                messages.success(request, "You'r solution has been added!")
                return redirect('/studentside/Student_Show_Solution/?doubt_id={}'.format(a))
        else:
            print('hello wolrd')    
    form = solution_form()   
    context.update({'form':form}) 

    return render(request, 'studentpanel/solution.html', context)

@student_login_required
def Student_show_solution_section(request):
    domain = request.get_host()
    title = 'Doubts'
    stud_id = request.session['stud_id']
    if request.GET.get('doubt_id'):
        doubt_id = request.GET.get('doubt_id')
        doubts_solution = Doubt_solution.objects.filter(solution_doubt_id__doubt_id = doubt_id, domain_name = domain)
        return render(request, 'studentpanel/show_solution.html', {'doubts_solution':doubts_solution, 'stud_id':stud_id, 'title':title}) 
    else:
        return render(request, 'studentpanel/show_solution.html', {'title':title}) 

@student_login_required
def Student_edit_solution(request,id):
    domain = request.get_host()
    title = 'Doubts'
    solution_id = Doubt_solution.objects.get(solution_id=id)
    if request.POST.get('solution'):
        form = solution_form(request.POST, instance=solution_id)
        if form.is_valid():
            form.instance.domain_name = domain
            form.save()
            return redirect('Student_Doubt')
    else:
        form = solution_form(instance=solution_id)
    return render(request, 'studentpanel/edit_solution.html',{'form':form, 'solution_id':solution_id, 'sol_id':id, 'title':title})


def student_analysis_view(request): 
    domain = request.get_host()
    student_id = request.session['stud_id']
    student_std = request.session['stud_std']

    # ===============Overall Attendance==================
    student = Students.objects.get(stud_id = student_id)

    total_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, domain_name = domain).count()
    
    present_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=True, domain_name = domain).count()

    absent_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=False, domain_name = domain).count()
    
    if total_attendence > 0:
        overall_attendence = round((present_attendence/total_attendence)*100,2)
    else:
        overall_attendence = 0



    # ==================Test Report and Attendance Report============
    students_li = Students.objects.filter(stud_std__std_id = student_std, domain_name = domain).values('stud_id', 'stud_name')
    overall_attendance_li = []
    current_student_overall_test_result = None
    for x in students_li:
        total_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x['stud_id'], domain_name = domain).count()
        present_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x['stud_id'], atten_present=True, domain_name = domain).count()
        if total_attendence_studentwise > 0:
            overall_attendence_studentwise = round((present_attendence_studentwise/total_attendence_studentwise)*100,2)
        else:
            overall_attendence_studentwise = 0
        

        total_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x['stud_id'], domain_name = domain).aggregate(total_sum_marks=Sum('tau_total_marks'))['total_sum_marks'] or 0
        
        
        obtained_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x['stud_id'], domain_name = domain).aggregate(total_obtained_marks=Sum('tau_obtained_marks'))['total_obtained_marks'] or 0
        

        if total_marks == 0:
            overall_result = 0
        else:
            overall_result = round((obtained_marks/total_marks)*100,2)
        
        
        if student_id == x['stud_id']: 
            current_student_overall_test_result = overall_result

        overall_attendance_li.append({'stud_name':x['stud_name'], 'overall_attendance_studentwise':overall_attendence_studentwise, 'overall_result':overall_result})

    
    overall_attendance_li = sorted(overall_attendance_li, key=lambda x: x['overall_result'], reverse=True)
    overall_attendance_li = overall_attendance_li[:5]
    


   # ===================SubjectsWise Attendance============================
    
    student = Students.objects.get(stud_id=student_id)
    subjects_li = student.stud_pack.pack_subjects.filter(domain_name = domain)
    overall_attendance_subwise = []

    for x in subjects_li:
        x = x.sub_name
        total_attendence_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = x, atten_student__stud_id=student_id, domain_name = domain).count()

        present_attendence_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = x, atten_present=True,atten_student__stud_id=student_id, domain_name = domain).count()

        if total_attendence_subwise > 0:
            attendance_subwise = round((present_attendence_subwise/total_attendence_subwise)*100,2)
        else:
            attendance_subwise = 0
        overall_attendance_subwise.append({'sub_name': x, 'attendance_subwise':attendance_subwise})
    
    # ======================SubjectWise TestResult==============================

    student = Students.objects.get(stud_id=student_id)
    subjects_li = student.stud_pack.pack_subjects.filter(domain_name = domain)
    final_average_marks_subwise = []

    for x in subjects_li:
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
        ))).values('verified_solution')
    
    my_solve_doubts = 0
    for x in solutions_gives:
        if x['verified_solution'] > 0:
            my_solve_doubts += 1
        else:
            print("no verified")

    doubt_solved_byme = Doubt_solution.objects.filter(solution_stud_id__stud_id = student_id, solution_verified = True, domain_name = domain).count()

    

    context = {
        'title': 'Report-Card',
        'logo_url': 'https://metrofoods.co.nz/1nobg.png',
        'student':student,
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
        'current_student_overall_test_result':current_student_overall_test_result,
        'my_solve_doubts':my_solve_doubts,
        'total_test_conducted':total_test_conducted,
        'absent_in_test':absent_in_test,

    }

    return render(request, 'studentpanel/student_analysis.html', context)

def student_fees_collection_view(request):
    domain = request.get_host()
    student_id = request.session['stud_id']
    student_data = Students.objects.get(stud_id = student_id)

    discount_amount = Discount.objects.filter(discount_stud_id__stud_id = student_id, domain_name = domain) 
    if discount_amount:
        fees_to_paid = int(student_data.stud_pack.pack_fees) - int(discount_amount[0].discount_amount)
    else:   
        fees_to_paid = int(student_data.stud_pack.pack_fees)

    # ===========================Paid Fees========================================

    fees_collection = Fees_Collection.objects.filter(fees_stud_id__stud_id = student_id, domain_name = domain)
    if fees_collection:
        paid_fees = Fees_Collection.objects.filter(fees_stud_id__stud_id = student_id, domain_name = domain).aggregate(tol_amount=Sum('fees_paid'))
        paid_fees = int(paid_fees['tol_amount'])
    else:
        paid_fees = 0

    # ==========================Remaining_Fees====================================

    remaining_fees = fees_to_paid - paid_fees
   
    # ===========================Cheque Fees======================================

    cheque_data = Cheque_Collection.objects.filter(cheque_stud_id__stud_id = student_id, cheque_paid = False, domain_name = domain)

    context = {
        'title': 'Payments',
        'fees_collection':fees_collection, 
        'fees_to_paid':fees_to_paid, 
        'paid_fees':paid_fees,
        'student_data':student_data, 
        'remaining_fees':remaining_fees,
        'cheque_data':cheque_data,
        'discount_amount':discount_amount

    }
    return render(request, 'studentpanel/fees_collection.html', context)



# ============================coming soon function========================
def comming_soon_page(request):
    context={}
    return render(request, 'studentpanel/coming-soon.html', context)


def today_study_page(request):
    domain = request.get_host()
    student_standard = request.session['stud_std']
    student_batch = request.session['stud_batch']
    todays_study_data = Today_Teaching.objects.filter(today_teaching_chap_id__chep_std__std_id = student_standard, today_teaching_batches_id__batch_id = student_batch, domain_name = domain).order_by('-today_teaching_chap_id')[:3]

    context = {
        'title': 'Today-Learning',
        'todays_study_data':todays_study_data
    }
    return render(request, 'studentpanel/today-study.html', context)