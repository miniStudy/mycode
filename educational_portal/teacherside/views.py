from django.shortcuts import render,get_object_or_404,redirect
from adminside.models import *
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import math
import datetime
import statistics
from datetime import datetime
from django.utils import timezone
from django.db.models.functions import TruncHour, TruncMinute, TruncDate
from django.db.models import Sum,Count, Max, Min, Avg, F
from django.db.models import Count, Case, When, IntegerField

import random
from django.http import Http404,JsonResponse
from studentside.forms import *
from adminside.form import *
from teacherside.forms import *
from django.db.models import OuterRef, Subquery, BooleanField,Q
from django.core.paginator import Paginator

import fitz  # PyMuPDF
from PIL import Image
import io
from django.core.files.base import ContentFile


# mail integration 
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives

from teacherside.decorators import *

def paginatoorrr(queryset,request):
    paginator = Paginator(queryset, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


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


@teacher_login_required
def teacher_home(request):
    msg = None
    overall_attendance_li = None
    fac_id = request.session['fac_id']
    
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)
    std_access_list=[]
    for x in faculty_access:
        std_access_list.append(x.fa_batch.batch_std.std_id)

    std_data = Std.objects.filter(std_id__in = std_access_list)


    if request.GET.get('get_std'):
        get_std = request.GET.get('get_std')

        get_std = Std.objects.get(std_id = get_std)
        students_li = Students.objects.filter(stud_std = get_std).values('stud_id','stud_name','stud_lastname')
        overall_attendance_li = []
        for x in students_li:
            total_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x['stud_id']).count()
            present_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x['stud_id'], atten_present=True).count()
            if total_attendence_studentwise > 0:
                overall_attendence_studentwise = (present_attendence_studentwise/total_attendence_studentwise)*100
            else:
                overall_attendence_studentwise = 0
            

            total_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x['stud_id']).aggregate(total_sum_marks=Sum('tau_total_marks'))['total_sum_marks'] or 0
            
            
            obtained_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x['stud_id']).aggregate(total_obtained_marks=Sum('tau_obtained_marks'))['total_obtained_marks'] or 0
            

            if total_marks == 0:
                overall_result = 0
            else:
                overall_result = round((obtained_marks/total_marks)*100,2)

            overall_attendance_li.append({'stud_name':x['stud_name'], 'stud_lastname':x['stud_lastname'], 'overall_attendance_studentwise':overall_attendence_studentwise, 'overall_result':overall_result})


        overall_attendance_li = sorted(overall_attendance_li, key=lambda x: x['overall_result'], reverse=True)
        overall_attendance_li = overall_attendance_li[:5]        
    else:
        get_std = 0
        msg = "Please! Select standard for data"
    #=====================Count Unverified Doubts=======================================================
    fac_data = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)
    l = []
    for data in fac_data:
        l.append(data.fa_subject.sub_id)
    
    unverified_solution = Doubt_section.objects.filter(doubt_subject__sub_id__in = l).annotate(verified_solution=Count(
        Case(
            When(doubt_solution__solution_verified=True, then=1),
            output_field=IntegerField(),
        ))).filter(verified_solution=0).count()
    
    # ----------------------------for chart on dashboard---------------------
    all_students= Students.objects.filter().count()
    all_male=Students.objects.filter(stud_gender='Male').count()
    all_female=Students.objects.filter(stud_gender='Female').count()
    all_other=Students.objects.filter(stud_gender='Other').count()
    piechart_category = ['Male','Female','Other']
    piechart_data = [all_male,all_female,all_other]
    stds = Std.objects.all().order_by('-std_board')

    std_list = []
    students_for_that_std = []
    for x in stds:
        n = (x.std_name+' '+x.std_board.brd_name)
        std_list.append(n)
        noss = Students.objects.filter(stud_std__std_id=x.std_id).count()
        students_for_that_std.append(noss)
    
    
    context={
        'title':'Home',
        'unverified_solution':unverified_solution,
        'std_data':std_data,
        'get_std': get_std,
        'msg': msg,
        'overall_attendance_li':overall_attendance_li,
        'all_students':all_students,
        'piechart_category':piechart_category,
        'piechart_data':piechart_data,
        'std_list':std_list,
        'students_for_that_std':students_for_that_std,
    }
    return render(request, 'teacherpanel/index.html',context)

def teacher_login_page(request):  
    login=1
    if request.COOKIES.get("fac_email"):
          cookie_email = request.COOKIES['fac_email']
          cookie_pass = request.COOKIES['fac_password']
          return render(request, 'teacherpanel/master_auth.html',{'login_set':login,'c_email':cookie_email,'c_pass':cookie_pass, 'title': 'login'})
    else:
          return render(request, 'teacherpanel/master_auth.html',{'login_set':login, 'title':'login'})

def teacher_login_handle(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        val = Faculties.objects.filter(fac_email=email,fac_password=password).count()
        if val==1:
            Data = Faculties.objects.filter(fac_email=email,fac_password=password)
            for item in Data:
               request.session['fac_id'] = item.fac_id
               request.session['fac_name'] = item.fac_name
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
            return redirect('teacher_login')
    else:
        return redirect('teacher_login')

def teacher_forget_password(request):  
    login=2
    if request.COOKIES.get("fac_email"):
          cookie_email = request.COOKIES['fac_email']
          return render(request, 'teacherpanel/master_auth.html',{'login_set':login,'c_email':cookie_email, 'title':'Forget Password'})
    else:
          return render(request, 'teacherpanel/master_auth.html',{'login_set':login, 'title':'Forget Password'})
    
def teacher_handle_forget_password(request):
     if request.method == "POST":
          email2 = request.POST['email']
          val = AdminData.objects.filter(admin_email=email2).count()
          if val!=1:
            messages.error(request, "Email is Wrong")
            url = f"{reverse('teacher_forget_password')}?email={email2}"
            return redirect(url)  
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
    return render(request, 'teacherpanel/master_auth.html',{'login_set':login,'email':foremail, 'title':'New Password'})

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

@teacher_login_required
def teacher_timetable(request):
     timetable_data = Timetable.objects.all()

     context = {
        'timetable_data':timetable_data,
        'title':'Timetable',
     }
     return render(request, 'teacherpanel/timetable.html', context)

@teacher_login_required
def teacher_attendance(request):
     fac_id = request.session['fac_id']
     faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)
     batch_access_list = []
     std_access_list=[]
     for x in faculty_access:
        batch_access_list.append(x.fa_batch.batch_id)
        std_access_list.append(x.fa_batch.batch_std.std_id)

     data = Attendance.objects.all().values('atten_timetable__tt_day','atten_timetable__tt_time1','atten_timetable__tt_subject1','atten_timetable__tt_tutor1__fac_name','atten_present','atten_student__stud_name','atten_student__stud_lastname','atten_date')
     data = paginatoorrr(data,request)
     std_data = Std.objects.filter(std_id__in = std_access_list)   
     batch_data = Batches.objects.filter(batch_id__in = batch_access_list)
     stud_data = Students.objects.all()
     subj_data = Subject.objects.all()
     
     
     today = timezone.localdate()

     
     today_records = Attendance.objects.filter(atten_date__contains=today)
     
     
     distinct_data = today_records.annotate(date=TruncDate('atten_date'),
        hour=TruncHour('atten_date'), minute=TruncMinute('atten_date')).values('date', 'hour', 'minute','atten_timetable').distinct()
     li = []
     for x in distinct_data:
        date_hour = x['hour'].hour
        date_minute = x['minute'].minute
        date_data = x['minute'].date()
        date_str = date_data.strftime('%Y-%m-%d')
        subjectt = Timetable.objects.get(tt_id = x['atten_timetable'])
        li.append({'hour':date_hour,'date':date_str, 'minute':date_minute,'tt_id':x['atten_timetable'],'subject':subjectt})
   
   

     context ={
          'data' : data,
          'title' : 'Attendance',
          'std_data' : std_data,
          'batch_data':batch_data,
          'stud_data':stud_data,
          'sub_data':subj_data,
          'li':li,
    }
    
     if request.GET.get('get_std'):
          get_std = int(request.GET['get_std'])
          if get_std == 0:
               pass
          else:    
               data = Attendance.objects.filter(atten_timetable__tt_batch__batch_std__std_id = get_std).values('atten_timetable__tt_day','atten_timetable__tt_time1','atten_timetable__tt_subject1','atten_timetable__tt_tutor1__fac_name','atten_present','atten_student__stud_name','atten_student__stud_lastname','atten_date')
               data = paginatoorrr(data,request)
               batch_data = batch_data.filter(batch_std__std_id = get_std)
               stud_data = stud_data.filter(stud_std__std_id = get_std)
               subj_data = subj_data.filter(sub_std__std_id = get_std)
               get_std = Std.objects.get(std_id = get_std)
               context.update({'data':data,'batch_data':batch_data,'get_std':get_std, 'stud_data':stud_data,'sub_data':subj_data})
     
     if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = Attendance.objects.filter(atten_timetable__tt_batch__batch_id = get_batch).values('atten_timetable__tt_day','atten_timetable__tt_time1','atten_timetable__tt_subject1','atten_timetable__tt_tutor1__fac_name','atten_present','atten_student__stud_name','atten_student__stud_lastname','atten_date')
            data = paginatoorrr(data,request)
            stud_data = stud_data.filter(stud_batch__batch_id = get_batch)
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'data':data,'get_batch':get_batch,'stud_data':stud_data}) 

     if request.GET.get('get_student'):
        get_student = int(request.GET['get_student'])
        if get_student == 0:
            pass
        else:
            data = data.filter(atten_student__stud_id = get_student)
            get_student = Students.objects.get(stud_id = get_student)
            context.update({'data':data,'get_student':get_student})                     


     attendance_present = Attendance.objects.filter(atten_present = True).count()
     attendance_all = Attendance.objects.all().count()
     if attendance_all>0:
        overall_attendance = round((attendance_present/attendance_all) * 100,2)
        context.update({'overall_attendance':overall_attendance})

     sub_list = subj_data.all().values('sub_name').distinct()
     subject_wise_attendance = []
     subjects = []
     for x in sub_list:
        sub_name = x['sub_name']
        sub_one = Attendance.objects.filter(atten_present = True,atten_timetable__tt_subject1__sub_name=sub_name).count()
        sub_all = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = sub_name).count()
        if sub_all>0:
            sub_attendance = round((sub_one/sub_all) * 100,2)
            subject_wise_attendance.append(sub_attendance)
            subjects.append(sub_name)
            
     combined_data = zip(subject_wise_attendance, subjects)

     context.update({'combined_data': combined_data})
     return render(request, 'teacherpanel/attendance.html',context)

def teacher_edit_attendance(request):
    if request.GET.get('get_std') and request.GET.get('get_batch'):
        get_std = request.GET['get_std']     
        get_batch = request.GET['get_batch']
        tt_id = request.GET['tt_id']
        std_data = Std.objects.get(std_id=get_std)
        batch_data = Batches.objects.get(batch_id=get_batch) 
        timetable_data = Timetable.objects.filter(tt_batch__batch_id = get_batch)
        students_data = Students.objects.filter(stud_std__std_id = get_std, stud_batch__batch_id = get_batch)
        get_hour = request.GET.get('hour','')     
        get_date = request.GET.get('date','')
        get_minute = request.GET.get('minute','')
        date_obj = datetime.strptime(get_date, '%Y-%m-%d')
        get_data = Attendance.objects.filter(atten_date__hour=get_hour, atten_date__date=date_obj,atten_timetable__tt_id=tt_id)
        context = {
          'std_data':std_data,
          'batch_data':batch_data,
          'students_data':students_data,
          'timetable_data':timetable_data,
          'title': 'Insert Attendence',
          'get_data':get_data,
          'get_date':get_date,
          'get_hour':get_hour,
     
          }
    else:
        messages.error(request, 'Please! Select Standard And Batch')
        return redirect('teacher_attendance')
    return render(request, 'teacherpanel/teacher_edit_attendance.html', context)




@teacher_login_required
def insert_update_attendance(request):
     if request.GET.get('get_std') and request.GET.get('get_batch'):
        get_std = request.GET['get_std']     
        get_batch = request.GET['get_batch']
        std_data = Std.objects.get(std_id=get_std)
        batch_data = Batches.objects.get(batch_id=get_batch) 
        timetable_data = Timetable.objects.filter(tt_batch__batch_id = get_batch)
        students_data = Students.objects.filter(stud_std__std_id = get_std, stud_batch__batch_id = get_batch)

        context = {
          'std_data':std_data,
          'batch_data':batch_data,
          'students_data':students_data,
          'timetable_data':timetable_data,
          'title': 'Insert Attendence',
     
          }
     else:
        messages.error(request, "Please! Select Standard And Batch")
        return redirect('teacher_attendance')  
     return render(request, 'teacherpanel/insert_attendence.html', context)

@teacher_login_required
def handle_attendance(request):
     if request.method == 'POST':
        std_data = request.POST.get('std_data')
        batch_data = request.POST.get('batch_data')
        atten_timetable = request.POST.get('atten_timetable')
        atten_tt = Timetable.objects.get(tt_id = atten_timetable)
        selected_items = request.POST.getlist('selection_attendance')
        students_all = Students.objects.filter(stud_batch__batch_id = batch_data, stud_std__std_id = std_data)
        if selected_items:
          selected_ids = [int(id) for id in selected_items]
        for i in students_all:
            if i.stud_id in selected_ids:
                Attendance.objects.create(atten_timetable=atten_tt, atten_student=i, atten_present=1)
            else:
                Attendance.objects.create(atten_timetable=atten_tt, atten_student=i, atten_present=0) 

        messages.success(request, "Attendance has been submitted!")    
     return redirect('teacher_attendance')

@teacher_login_required
def edit_handle_attendance(request):
     if request.method == 'POST':
        get_date = request.POST.get('get_date')
        get_hour = request.POST.get('get_hour')
        get_date = datetime.strptime(get_date, '%Y-%m-%d')
        atten_timetable = request.POST.get('atten_timetable')
        atten_tt = Timetable.objects.get(tt_id = atten_timetable)
        selected_items = request.POST.getlist('selection_attendance')
        if selected_items:
          selected_ids = [int(id) for id in selected_items]
        current_all_attendance = Attendance.objects.filter(atten_date__hour=get_hour, atten_date__date=get_date,atten_timetable__tt_id = atten_timetable)  
        for i in current_all_attendance:
            if i.atten_student.stud_id in selected_ids:
                instance = Attendance.objects.get(atten_date__hour=get_hour, atten_date__date=get_date, atten_student__stud_id=i.atten_student.stud_id)  
                instance.atten_present = 1
                instance.save()
            else:
                instance = Attendance.objects.get(atten_date__hour=get_hour, atten_date__date=get_date, atten_student__stud_id=i.atten_student.stud_id)
                instance.atten_present = 0
                instance.save()

        messages.success(request, "Attendance has been updated!")
     return redirect('teacher_attendance')


@teacher_login_required
def teacher_syllabus(request):
    fac_id = request.session['fac_id']
    if request.GET.get('chep_id'):
        chep_id = request.GET.get('chep_id')
        status_id = request.GET.get('status')
        chep_obj = Chepter.objects.get(chep_id=chep_id)
        Syllabus.objects.update_or_create(syllabus_chapter=chep_obj, defaults={'syllabus_status':status_id, 'syllabus_chapter':chep_obj})

    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)
    subjects_list = []
    for x in faculty_access:
        subjects_list.append(x.fa_subject.sub_id)
    
    subjects = Subject.objects.filter(sub_id__in = subjects_list)
    chepters = Chepter.objects.filter().annotate(status=F('syllabus__syllabus_status')).values('chep_sub__sub_id', 'chep_name','chep_id', 'status')


    context = {
        'title':'Syllabus',
        'subjects':subjects,
        'chepters':chepters,
    }
    return render(request, 'teacherpanel/syllabus.html', context) 
   

@teacher_login_required
def teacher_doubts(request):
    fac_id = request.session['fac_id']
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)
    subjects_list = []
    for x in faculty_access:
        subjects_list.append(x.fa_subject.sub_id)

    doubts_data = Doubt_section.objects.filter(doubt_subject__sub_id__in = subjects_list).annotate(count_solution=Count('doubt_solution'), verified_solution=Count(
        Case(
            When(doubt_solution__solution_verified=True, then=1),
            output_field=IntegerField(),
        ))).order_by('-pk')[:30]
     
    context = {
        'title':'Doubts',
        'doubts_data':doubts_data
    }
    return render(request, 'teacherpanel/doubts.html', context)


@teacher_login_required
def show_teacher_solution_verified(request):
     if request.GET.get('doubt_id'):
          doubt_id = request.GET.get('doubt_id')
          doubts_solution = Doubt_solution.objects.filter(solution_doubt_id__doubt_id = doubt_id)

          teacher_id = request.session['fac_id']
          fac_id = Faculties.objects.get(fac_id = teacher_id)
          if request.method == 'POST':
              verification = request.POST.get('verification')
              solution_id = request.POST.get('solution_id')
              sol_id = Doubt_solution.objects.get(solution_id = solution_id)
              sol_id.solution_verified = verification
              sol_id.solution_verified_by_teacher = fac_id
              sol_id.save()
          return render(request, 'teacherpanel/show_solution.html', {'doubts_solution':doubts_solution, 'doubt_id': doubt_id, 'title':'Doubts Solution',})


@teacher_login_required
def teacher_events(request):
    event_data = Event.objects.all().values('event_id','event_name')
    event_imgs = Event_Image.objects.all()
    selected_events = Event.objects.first()
    context={
        'event_data':event_data,
        'event_imgs':event_imgs,
        'selected_events':selected_events,
        'title':'Events',
    }

    if request.GET.get('event_id'):
        event_id = request.GET['event_id']
        selected_events = Event.objects.get(event_id = event_id)
        event_imgs = Event_Image.objects.filter(event__event_id = event_id)
        
        context.update({'selected_events':selected_events, 'events_img':event_imgs})
    return render(request, 'teacherpanel/events.html', context)


@teacher_login_required
def teacher_test(request):
    fac_id = request.session['fac_id']
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)
    subjects_list = []
    std_list = []
    for x in faculty_access:
        std_list.append(x.fa_batch.batch_std.std_id)
        subjects_list.append(x.fa_subject.sub_id)


    data = Chepterwise_test.objects.filter(test_std__std_id__in = std_list).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage'))
    data = paginatoorrr(data,request)

    std_data = Std.objects.filter(std_id__in = std_list)
    subject_data = Subject.objects.filter(sub_id__in = subjects_list)
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
            data = Chepterwise_test.objects.filter(test_sub__sub_std__std_id = get_std).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage'))
            data = paginatoorrr(data,request)
            subject_data = subject_data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'get_std':get_std, 'subject_data':subject_data, 'std_data':std_data}) 


    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        if get_subject == 0:
            pass
        else:    
            data = Chepterwise_test.objects.filter(test_sub__sub_id = get_subject).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage'))
            data = paginatoorrr(data,request)
            get_subject = Subject.objects.get(sub_id = get_subject)
            context.update({'data':data,'subject_data':subject_data,'get_subject':get_subject}) 

    return render(request, 'teacherpanel/show_tests.html',context)


@teacher_login_required
def teacher_insert_offline_marks(request):
    context = {}

    if request.GET.get('test_id'):
        test_id = request.GET.get('test_id')
        context.update({'test_id':test_id})

    if request.GET.get('std_id'):
        std_id = request.GET.get('std_id')
        batch_data = Batches.objects.filter(batch_std__std_id = std_id)
        students_data = Students.objects.filter(stud_std__std_id = std_id)
        context.update({'std_id':std_id, 'batch_data':batch_data, 'students_data':students_data})
    else:
        messages.error(request, 'Please! Select Standard')
        return redirect('teacher_test')
    
    if request.GET.get('batch_id'):
        batch_id = request.GET.get('batch_id')
        students_data = Students.objects.filter(stud_batch__batch_id = batch_id)
        batch_id = Batches.objects.get(batch_id=batch_id)
        context.update({'students_data':students_data, 'batch_id':batch_id})
    
    return render(request, 'teacherpanel/offline_marks.html',context)

@teacher_login_required
def teacher_save_offline_marks(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_id')
        test_id = request.POST.get('test_id')
        marks = request.POST.getlist('marks')
        test_data = Test_questions_answer.objects.filter(tq_name__test_id = test_id)
        test_id = Chepterwise_test.objects.get(test_id=test_id)
        sum = 0
        count = 0
        for x in test_data:
            sum = sum + x.tq_weightage
            count += 1

        for student_id, mark in zip(student_ids, marks):
            student = Students.objects.get(pk=student_id)
            test_attempt = Test_attempted_users(
                tau_test_id=test_id,
                tau_stud_id=student,
                tau_completion_time=test_id.test_time,  # Update with actual completion time
                tau_attempted_questions=count,  # Update with actual number of attempted questions
                tau_correct_ans=0,  # Update with actual number of correct answers
                tau_total_marks=sum,  # Update with actual total marks
                tau_obtained_marks=mark
            )
            test_attempt.save()
    messages.success(request, 'Marks have been successfully saved.')
    return redirect('teacher_test')

@teacher_login_required
def view_attemp_students(request):
    if request.GET.get('test_id'):
        test_id = request.GET.get('test_id')
        students_attemp_data = Test_attempted_users.objects.filter(tau_test_id__test_id = test_id)

        students_count = students_attemp_data.count()

        marks_aggregates = students_attemp_data.aggregate(max_marks=Max('tau_obtained_marks'), min_marks=Min('tau_obtained_marks'), avg_marks=Avg('tau_obtained_marks'))
        avg_marks = marks_aggregates['avg_marks']
        if avg_marks is not None:
            avg_marks = round(avg_marks,2)
    
    return render(request, 'teacherpanel/students_view.html', {'students_attemp_data':students_attemp_data, 'students_count':students_count, 'marks_aggregates':marks_aggregates, 'avg_marks':avg_marks})

@teacher_login_required
def insert_update_tests(request):
    std_data = Std.objects.all()
    subject_data = Subject.objects.select_related().all()
    chap_data = Chepter.objects.all().values('chep_name','chep_id','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name')
    context = {
        'title' : 'Tests',
        'std_data':std_data,
        'subject_data':subject_data,
        'chap_data':chap_data
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        chap_data = Chepter.objects.filter(chep_std__std_id = get_std).values('chep_name','chep_id','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name')
        context.update({'get_std': get_std, 'std_data': std_data, 'chap_data':chap_data})

    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        subject_data = subject_data.filter(sub_id = get_subject)
        chap_data = Chepter.objects.filter(chep_sub__sub_id = get_subject).values('chep_name','chep_id','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name')
        context.update({'get_subject': get_subject, 'subject_data': subject_data, 'chap_data':chap_data})     

    
    # ================update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Chepterwise_test, pk=request.GET['pk'])
            form = tests_form(request.POST, instance=instance)
            check = Chepterwise_test.objects.filter(test_name=form.data['test_name'], test_std__std_id=form.data['test_std']).count()
            if check >= 1:
                messages.error(request, '{} is already Exists'.format(form.data['test_name']))
            else:
                if form.is_valid():
                    form.save()
                    return redirect('teacher_test')
                else:
                    filled_data = form.data
                    context.update({'filled_data': filled_data, 'errors': form.errors})
        
        update_data = Chepterwise_test.objects.get(test_id=request.GET['pk'])
        context.update({'update_data': update_data})  

    else:
        if request.method == 'POST':
            form = tests_form(request.POST, request.FILES)
            if form.is_valid():
                check = Chepterwise_test.objects.filter(
                    test_name=form.data['test_name'], test_std__std_id=form.data['test_std']
                ).count()
                if check >= 1:
                    messages.error(request, '{} already exists'.format(form.data['test_name']))
                else:
                    test_instance = form.save()

                    # Check for auto-generate test
                    if request.POST.get('auto_generate_test'):
                        one_mark_count = int(request.POST.get('one_mark_questions', 0))
                        print(one_mark_count)
                        two_mark_count = int(request.POST.get('two_mark_questions', 0))
                        three_mark_count = int(request.POST.get('three_mark_questions', 0))
                        four_mark_count = int(request.POST.get('four_mark_questions', 0))
                        chap_object = Chepter.objects.filter(chep_id = request.POST.get('test_chap'))

                        # Function to get questions by weightage
                        def get_questions_by_weightage(weightage, count):
                            return question_bank.objects.filter(
                                qb_chepter=chap_object,
                                qb_weightage=weightage
                            ).order_by('?')[:count]

                        # Retrieve questions based on weightage
                        one_mark_questions = get_questions_by_weightage(1, one_mark_count)
                        print(one_mark_questions)
                        two_mark_questions = get_questions_by_weightage(2, two_mark_count)
                        three_mark_questions = get_questions_by_weightage(3, three_mark_count)
                        four_mark_questions = get_questions_by_weightage(4, four_mark_count)

                        # Insert the generated questions into Test_questions_answer
                        for question in one_mark_questions:
                            print(question)
                            Test_questions_answer.objects.create(     
                                tq_name=test_instance,
                                tq_chepter=question.qb_chepter,
                                tq_q_type=Test_questions_answer.que_type.Question_Answer,
                                tq_question=question.qb_question,
                                tq_answer=question.qb_answer,
                                tq_weightage=1,
                                tq_hint=question.qb_hint,
                                tq_optiona=question.qb_optiona,
                                tq_optionb=question.qb_optionb,
                                tq_optionc=question.qb_optionc,
                                tq_optiond=question.qb_optiond
                            )

                        for question in two_mark_questions:
                            Test_questions_answer.objects.create(
                                tq_name=test_instance,
                                tq_chepter=question.qb_chepter,
                                tq_q_type=Test_questions_answer.que_type.Question_Answer,
                                tq_question=question.qb_question,
                                tq_answer=question.qb_answer,
                                tq_weightage=2,
                                tq_hint=question.qb_hint,
                                tq_optiona=question.qb_optiona,
                                tq_optionb=question.qb_optionb,
                                tq_optionc=question.qb_optionc,
                                tq_optiond=question.qb_optiond
                            )

                        for question in three_mark_questions:
                            Test_questions_answer.objects.create(
                                tq_name=test_instance,
                                tq_chepter=question.qb_chepter,
                                tq_q_type=Test_questions_answer.que_type.Question_Answer,
                                tq_question=question.qb_question,
                                tq_answer=question.qb_answer,
                                tq_weightage=3,
                                tq_hint=question.qb_hint,
                                tq_optiona=question.qb_optiona,
                                tq_optionb=question.qb_optionb,
                                tq_optionc=question.qb_optionc,
                                tq_optiond=question.qb_optiond
                            )

                        for question in four_mark_questions:
                            Test_questions_answer.objects.create(
                                tq_name=test_instance,
                                tq_chepter=question.qb_chepter,
                                tq_q_type=Test_questions_answer.que_type.Question_Answer,
                                tq_question=question.qb_question,
                                tq_answer=question.qb_answer,
                                tq_weightage=4,
                                tq_hint=question.qb_hint,
                                tq_optiona=question.qb_optiona,
                                tq_optionb=question.qb_optionb,
                                tq_optionc=question.qb_optionc,
                                tq_optiond=question.qb_optiond
                            )
                    return redirect('teacher_test')
            else:
                filled_data = form.data
                context.update({'filled_data': filled_data, 'errors': form.errors})
                return render(request, 'teacherpanel/insert_update_tests.html', context) 
    return render(request, 'teacherpanel/insert_update_tests.html', context)

@teacher_login_required
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

    return redirect('teacher_test')

@teacher_login_required
def show_test_questions_teacher(request):
    if request.GET.get('test_id'):
        Test_Questions_data = Test_questions_answer.objects.filter(tq_name = request.GET['test_id'])
        No_of_q = Test_Questions_data.count()
        total_marks = 0
        for x in Test_Questions_data:
            total_marks += x.tq_weightage
        test_info = Chepterwise_test.objects.get(test_id = request.GET['test_id'])

        if request.GET.get('que_id'):
            que_id = request.GET.get('que_id')
            test_question = Test_questions_answer.objects.filter(tq_id = que_id) 
        else:
            test_question = Test_questions_answer.objects.filter(tq_name__test_id = request.GET['test_id'])[:1]


        context = {
            'Test_Questions_data':Test_Questions_data,
            'test_info':test_info,
            'test_question':test_question,
            'total_marks':total_marks,
            'no_of_q':No_of_q,
            'title':'Tests',
        }
        return render(request, 'teacherpanel/show_test_questions_teacher.html',context)
    else:
        return redirect('teacher_test') 

@teacher_login_required
def insert_update_test_questions_teacher(request):
    chep_data = Chepter.objects.all()
    context = {
        'chep_data': chep_data,
        'que_type': Test_questions_answer.que_type,
    }

    if request.GET.get('test_id'):
        test_id = request.GET['test_id']
        print(test_id)
        test_data = Chepterwise_test.objects.get(test_id = test_id)
        chep_data = chep_data.filter(chep_sub__sub_id = test_data.test_sub.sub_id)
        context.update({'test_id': test_id,'chep_data':chep_data})

    if request.method == 'POST':
        form = TestQuestionsAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('teacher_test')  # Replace 'success_url' with your actual success URL
        else:
            context.update({'form': form,'errors':form.errors})
            return render(request, 'teacherpanel/insert_update_add_test_questions.html', context)
    else:
        form = TestQuestionsAnswerForm()
        context.update({'form': form})
        return render(request, 'teacherpanel/insert_update_add_test_questions.html', context)


@teacher_login_required
def teacher_announcement(request):
    fac_id = request.session['fac_id']
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)
    batch_access_list = []
    std_access_list=[]
    for x in faculty_access:
        batch_access_list.append(x.fa_batch.batch_id)
        std_access_list.append(x.fa_batch.batch_std.std_id)

    data = Announcements.objects.all().values('announce_id','announce_title','announce_msg','announce_date')
    data = paginatoorrr(data,request)
    std_data = Std.objects.filter(std_id__in = std_access_list)
    batch_data = Batches.objects.filter(batch_id__in = batch_access_list)
   
    context ={
        'data' : data,
        'title' : 'Announcements',
        'std_data' : std_data,
        'batch_data':batch_data,
    }
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = Announcements.objects.filter(announce_std__std_id = get_std).values('announce_id','announce_title','announce_msg','announce_date')
            data = paginatoorrr(data,request)
            batch_data = batch_data.filter(batch_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'batch_data':batch_data,'get_std':get_std})
            

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = Announcements.objects.filter(announce_batch__batch_id = get_batch).values('announce_id','announce_title','announce_msg','announce_date')
            data = paginatoorrr(data,request)
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'data':data,'get_batch':get_batch})        
            
    return render(request, 'teacherpanel/show_announcements.html',context)


@teacher_login_required
def announcements_insert_update_teacher(request):
    std_data = Std.objects.all()
    batch_data = Batches.objects.all()
    # ------------getting students for mail------------------
    students_for_mail = Students.objects.all()

    context = {
        'title' : 'Insert Announcements',
        'std_data':std_data,
        'batch_data':batch_data,
        'title':'Announcements',
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

        # ================update Logic============================
        if request.GET.get('pk'):
            instance = get_object_or_404(Announcements, pk=request.GET['pk'])
            form = announcement_form(request.POST, instance=instance)       
            if form.is_valid():
                form.save()

                return redirect('teacher_announcement')
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})

        # ===================insert_logic===========================
        form = announcement_form(request.POST)
        if form.is_valid():
            form.save()
            # ---------------------sendmail Logic===================================
            students_email_list = []
            for x in students_for_mail:
                students_email_list.append(x.stud_email)
            print(students_email_list)    
            # announcement_mail(form.cleaned_data['announce_title'],form.cleaned_data['announce_msg'],students_email_list)
         
            return redirect('teacher_announcement')
        else:
            filled_data = form.data
            context.update({'filled_data ':filled_data,'errors':form.errors})
            return render(request, 'teacherpanel/announcements_insert_update_teacher.html', context)

    if request.GET.get('pk'):
        update_data = Announcements.objects.get(announce_id = request.GET['pk'])
        context.update({'update_data':update_data})
    return render(request, 'teacherpanel/announcements_insert_update_teacher.html',context)


@teacher_login_required
def announcements_delete_teacher(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Announcements.objects.filter(announce_id__in=selected_ids).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('teacher_announcement')


@teacher_login_required
def teacher_materials(request):
    fac_id = request.session['fac_id']
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id).values('fa_faculty__fac_id','fa_subject__sub_id','fa_batch__batch_std__std_id')
    subject_access_list = []
    std_access_list=[]
    for x in faculty_access:
        subject_access_list.append(x['fa_subject__sub_id'])
        std_access_list.append(x['fa_batch__batch_std__std_id'])

    standard_data = Std.objects.filter(std_id__in = std_access_list).values('std_id','std_name','std_board__brd_name')
    subjects_data = Subject.objects.filter(sub_id__in = subject_access_list).values('sub_id','sub_name','sub_std__std_name','sub_std__std_id','sub_std__std_board__brd_name')
    materials = Chepterwise_material.objects.filter(cm_chepter__chep_sub__sub_id__in = subject_access_list).values('cm_chepter__chep_sub__sub_id', 'cm_file', 'cm_file_icon', 'cm_filename', 'cm_chepter__chep_sub__sub_name', 'cm_id')
    selected_sub=None

    context = {'standard_data':standard_data, 'subjects_data':subjects_data, 'materials':materials, "title":'Materials'}
    if request.GET.get('std_id'):
        std_id = int(request.GET.get('std_id'))
        subjects_data = Subject.objects.filter(sub_std__std_id = std_id).values('sub_id','sub_name','sub_std__std_name','sub_std__std_id','sub_std__std_board__brd_name')
        materials = Chepterwise_material.objects.filter(cm_chepter__chep_sub__sub_std__std_id = std_id).values('cm_chepter__chep_sub__sub_id', 'cm_file', 'cm_file_icon', 'cm_filename', 'cm_chepter__chep_sub__sub_name', 'cm_id')
        std_data = Std.objects.get(std_id = std_id)
        context.update({'materials': materials,'subjects_data': subjects_data, 'std':std_data})

    if request.GET.get('sub_id'):
        sub_id = request.GET.get('sub_id')
        materials = Chepterwise_material.objects.filter(cm_chepter__chep_sub__sub_id = sub_id).values('cm_chepter__chep_sub__sub_id', 'cm_file', 'cm_file_icon', 'cm_filename', 'cm_chepter__chep_sub__sub_name', 'cm_id')
        selected_sub = Subject.objects.get(sub_id=sub_id)
        context.update({'materials': materials, 'selected_sub':selected_sub})

    return render(request, 'teacherpanel/show_materials.html', context)

@teacher_login_required
def teacher_insert_update_materials(request):
    chepter_data = Chepter.objects.all().values('chep_name','chep_id','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name')
    context = {
        'title': 'Materials',
        'chepter_data': chepter_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        chepter_data = chepter_data.filter(chep_std__std_id=get_std)
        context.update({'get_std': get_std, 'chepter_data': chepter_data})

    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        chepter_data = chepter_data.filter(chep_sub__sub_id=get_subject)
        context.update({'get_subject': get_subject, 'chepter_data': chepter_data})

    # ================Update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Chepterwise_material, pk=request.GET['pk'])
            form = teacher_materials_form(request.POST, request.FILES, instance=instance)
            check = Chepterwise_material.objects.filter(
                cm_filename=form.data['cm_filename'],
                cm_chepter__chep_name=form.data['cm_chepter']
            ).exclude(pk=request.GET['pk']).count()

            if check >= 1:
                messages.error(request, '{} is already Exists'.format(form.data['cm_filename']))
            else:
                if form.is_valid():
                    material = form.save(commit=False)
                    pdf_file = form.cleaned_data['cm_file']
                    
                    # Generate icon for the PDF file
                    material.cm_file_icon.save(
                        pdf_file.name.replace('.pdf', '_icon.png'),
                        generate_pdf_icon(pdf_file),
                        save=False
                    )
                    material.save()
                    
                    chap_obj = form.cleaned_data['cm_chepter']
                    url = '/teacherside/teacher_materials/?std_id={}&sub_id={}'.format(
                        chap_obj.chep_sub.sub_std.std_id,
                        chap_obj.chep_sub.sub_id
                    )
                    return redirect(url)
                else:
                    filled_data = form.data
                    context.update({'filled_data': filled_data, 'errors': form.errors})

        update_data = Chepterwise_material.objects.get(cm_id=request.GET['pk'])
        context.update({'update_data': update_data})
    else:
        # ===================Insert Logic===========================
        if request.method == 'POST':
            form = teacher_materials_form(request.POST, request.FILES)
            if form.is_valid():
                chap_obj = form.cleaned_data['cm_chepter'] 

                url='/teacherside/teacher_materials/?std_id={}&sub_id={}'.format(chap_obj.chep_sub.sub_std.std_id,chap_obj.chep_sub.sub_id)
                    
                check = Chepterwise_material.objects.filter(cm_filename = form.data['cm_filename'], cm_chepter__chep_name = form.data['cm_chepter']).count()
                pdf_file = form.cleaned_data['cm_file']
                chap_obj = form.cleaned_data['cm_chepter']
                url = '/teacherside/teacher_materials/?std_id={}&sub_id={}'.format(
                    chap_obj.chep_sub.sub_std.std_id,
                    chap_obj.chep_sub.sub_id
                )

                check = Chepterwise_material.objects.filter(
                    cm_filename=form.data['cm_filename'],
                    cm_chepter__chep_name=form.data['cm_chepter']
                ).count()

                if check >= 1:
                    messages.error(request, '{} is already Exists'.format(form.data['cm_filename']))
                else:
                    material = form.save(commit=False)
                    # Generate icon for the PDF file
                    material.cm_file_icon.save(
                        pdf_file.name.replace('.pdf', '_icon.png'),
                        generate_pdf_icon(pdf_file),
                        save=False
                    )
                    material.save()
                    return redirect(url)
            else:
                filled_data = form.data
                context.update({'filled_data': filled_data, 'errors': form.errors})
                return render(request, 'teacherpanel/insert_update_materials_teacher.html', context)

    return render(request, 'teacherpanel/insert_update_materials_teacher.html', context)


@teacher_login_required
def materials_delete_teacher(request):
    if request.method == 'GET':
        selected_items = request.GET.get('delete_material_id')
        if selected_items:
            try:
                Chepterwise_material.objects.get(cm_id=selected_items).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('teacher_materials')

@teacher_login_required
def teacher_view_profile(request):
    teacher_id = request.session['fac_id']
    teacher_profile = Faculties.objects.filter(fac_id = teacher_id)
    teacher_access = Faculty_Access.objects.filter(fa_faculty__fac_id = teacher_id)
    context = {
        'teacher_profile' : teacher_profile,
        'title': 'Profile',
        'teacher_access':teacher_access,
    }
    return render(request, 'teacherpanel/myprofile.html', context)


@teacher_login_required
def teacher_profile_update(request):
    teacher_id = request.session['fac_id']
    teacher_obj = Faculties.objects.get(fac_id = teacher_id)
    if request.method == 'POST':
        form = teacher_update_form(request.POST, instance=teacher_obj)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information updated successfully')
            return redirect('teacher_profile')
        else:
            messages.error(request, 'error')
    else:
        form = teacher_update_form(instance=teacher_obj)
    context={
        'form':form,
        'teacher_obj':teacher_obj,
        'title': 'Update Profile',
    }
    return render(request, 'teacherpanel/updateprofile.html',context)


def report_card_show(request):
    fac_id = request.session['fac_id']
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)
    subject_access_list = []
    std_access_list = []
    batch_access_list = []
    for x in faculty_access:
        subject_access_list.append(x.fa_subject.sub_id)
        std_access_list.append(x.fa_batch.batch_std.std_id)
        batch_access_list.append(x.fa_batch.batch_id)

    data = Attendance.objects.all()
    std_data = Std.objects.filter(std_id__in = std_access_list)
    batch_data = Batches.objects.filter(batch_id__in = batch_access_list)
    stud_data = Students.objects.all().values('stud_std__std_id', 'stud_batch__batch_id', 'stud_id', 'stud_name', 'stud_lastname')
    subj_data = Subject.objects.all()

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
        print(student_std) 
    
    
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
            my_package = Packs.objects.prefetch_related('pack_subjects').get(pack_id = get_student.stud_pack.pack_id)
            pack_subject_list = []
            for subject in my_package.pack_subjects.all():
                pack_subject_list.append(subject.sub_id)
                print(subject.sub_id)
            print(pack_subject_list)
            context.update({'data':data,'get_student':get_student})

        student_id = get_student.stud_id

    if ((request.GET.get('get_std')) and (request.GET.get('get_batch')) and (request.GET.get('get_student'))):    
        # ===============Overall Attendance==================

        # student_data = Students.objects.filter(stud_std__std_id = student_std)
        # print(student_data)
        total_attendence = Attendance.objects.filter(atten_student__stud_id = student_id).count()
        
        present_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=True).count()

        absent_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=False).count()
        
        if total_attendence > 0:
            overall_attendence = (present_attendence/total_attendence)*100
        else:
            overall_attendence = 0



        # ==================Test Report and Attendance Report============
        students_li = Students.objects.filter(stud_std__std_id = student_std).values('stud_id', 'stud_name','stud_lastname')
        overall_attendance_li = []
        for x in students_li:
            total_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x['stud_id']).count()
            present_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x['stud_id'], atten_present=True).count()
            # print("==============================================",total_attendence_studentwise)
            if total_attendence_studentwise > 0:
                overall_attendence_studentwise = (present_attendence_studentwise/total_attendence_studentwise)*100
            else:
                overall_attendence_studentwise = 0
            

            total_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x['stud_id']).aggregate(total_sum_marks=Sum('tau_total_marks'))['total_sum_marks'] or 0
            
            
            obtained_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x['stud_id']).aggregate(total_obtained_marks=Sum('tau_obtained_marks'))['total_obtained_marks'] or 0
            

            if total_marks == 0:
                overall_result = 0
            else:
                overall_result = round((obtained_marks/total_marks)*100,2)
            if student_id == x['stud_id']: 
                current_student_overall_test_result = overall_result
                context.update({'current_student_overall_test_result':current_student_overall_test_result})

            overall_attendance_li.append({'stud_name':x['stud_name'], 'overall_attendance_studentwise':overall_attendence_studentwise, 'overall_result':overall_result})
        overall_attendance_li = sorted(overall_attendance_li, key=lambda x: x['overall_result'], reverse=True)
        overall_attendance_li = overall_attendance_li[:5]
        
        # ===================SubjectsWise Attendance============================
        subjects_li = Subject.objects.filter(sub_std__std_id = student_std, sub_id__in = pack_subject_list).values('sub_name').distinct()
        print(subjects_li)
        overall_attendance_subwise = []
        for x in subjects_li:
            x = x['sub_name']
            total_attendence_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = x, atten_student__stud_id=student_id).count()

            present_attendence_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = x, atten_present=True,atten_student__stud_id=student_id).count()

            if total_attendence_subwise > 0:
                attendance_subwise = (present_attendence_subwise/total_attendence_subwise)*100
            else:
                attendance_subwise = 0
            overall_attendance_subwise.append({'sub_name': x, 'attendance_subwise':attendance_subwise})

        # ======================SubjectWise TestResult==============================
        subjects_data = Subject.objects.filter(sub_std=student_std, sub_id__in = pack_subject_list )
        final_average_marks_subwise = []
        for x in subjects_data:
            total_marks_subwise = Test_attempted_users.objects.filter(tau_test_id__test_sub__sub_name = x.sub_name, tau_stud_id__stud_id=student_id).aggregate(total_sum_marks_subwise=Sum('tau_total_marks'))['total_sum_marks_subwise'] or 0
        

            obtained_marks_subwise = Test_attempted_users.objects.filter(tau_test_id__test_sub__sub_name = x.sub_name, tau_stud_id__stud_id=student_id).aggregate(obtained_sum_marks_subwise=Sum('tau_obtained_marks'))['obtained_sum_marks_subwise'] or 0
            
            
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

        total_test_conducted = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id).count()

        absent_in_test = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id,tau_obtained_marks = 0).count()


        # =============Doubts and Solution Counts================================

        doubt_asked = Doubt_section.objects.filter(doubt_stud_id__stud_id = student_id).count()

        solutions_gives = Doubt_section.objects.filter(doubt_stud_id__stud_id = student_id).annotate(verified_solution=Count(
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

        doubt_solved_byme = Doubt_solution.objects.filter(solution_stud_id__stud_id = student_id, solution_verified = True).count()
        # print(student_data)
        context.update({
            'title': 'Report-Card',
            'logo_url': 'https://metrofoods.co.nz/1nobg.png',
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
        context.update({'noreport_card':noreport_card})
    return render(request, 'teacherpanel/report_card.html', context)


def today_learning_show(request):
    fac_id = request.session['fac_id']
    fac_data = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)

    std_access = []
    batch_access = []
    for x in fac_data:
        std_access.append(x.fa_batch.batch_std.std_id)
        batch_access.append(x.fa_batch.batch_id)
    
    standard_access_data = Std.objects.filter(std_id__in = std_access)
    batch_access_data = Batches.objects.filter(batch_id__in = batch_access)

    today_learn_data = Today_Teaching.objects.filter(today_teaching_batches_id__batch_id__in = batch_access, today_teaching_batches_id__batch_std__std_id__in = std_access)

    context = {
        'today_learn_data':today_learn_data,
        'standard_access_data':standard_access_data,
        'batch_access_data':batch_access_data,
        'title': 'Class-Overview'
    }

    if request.GET.get('get_std'):
        get_std = request.GET['get_std']
        if get_std == 0:
            pass
        else:
            today_learn_data = today_learn_data.filter(today_teaching_batches_id__batch_std__std_id = get_std)
            batch_access_data = batch_access_data.filter(batch_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'today_learn_data':today_learn_data,'batch_access_data':batch_access_data,'get_std':get_std})

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            today_learn_data = today_learn_data.filter(today_teaching_batches_id__batch_id = get_batch)
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'today_learn_data':today_learn_data,'get_batch':get_batch}) 

    return render(request, 'teacherpanel/today_learn.html', context)

def today_learning_insert_update(request):
    fac_id = request.session['fac_id']
    fac_data = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)

    std_access = []
    batch_access = []
    for x in fac_data:
        std_access.append(x.fa_batch.batch_std.std_id)
        batch_access.append(x.fa_batch.batch_id)
    
    standard_access_data = Std.objects.filter(std_id__in = std_access)
    batch_access_data = Batches.objects.filter(batch_id__in = batch_access)
    today_learning_data = Today_Teaching.objects.filter(today_teaching_batches_id__batch_id__in = batch_access)

    context = {
        'standard_access_data':standard_access_data,
        'batch_access_data':batch_access_data,
        'today_learning_data':today_learning_data
    }
    
    if request.GET.get('get_std'):
        get_std = request.GET['get_std']
        if get_std == 0:
            pass
        else:
            batch_access_data = batch_access_data.filter(batch_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'batch_access_data':batch_access_data,'get_std':get_std})

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            get_batch = Batches.objects.get(batch_id = get_batch) 
            context.update({'get_batch':get_batch}) 

    if request.method == 'POST':
        # ================update Logic============================
        if request.GET.get('pk'):
            instance = get_object_or_404(Today_Teaching, pk=request.GET['pk'])
            form = teacher_todaylearn_form(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Updated Sucessfully!')
                return redirect('today_learning')
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})

        # ===================insert_logic===========================
        form = teacher_todaylearn_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Add Sucessfully!')
            return redirect('today_learning')
        else:
            filled_data = form.data
            context.update({'filled_data ':filled_data,'errors':form.errors})
            return render(request, 'teacherpanel/today_learn_insert_update.html', context)

    if request.GET.get('pk'):
        update_data = Today_Teaching.objects.get(today_teaching_id = request.GET['pk'])
        context.update({'update_data':update_data})
    

    return render(request, 'teacherpanel/today_learn_insert_update.html', context)



def today_learning_delete(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Today_Teaching.objects.filter(today_teaching_id__in=selected_ids).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    return redirect('today_learning')


def show_question_paper(request):
    if request.GET.get('test_id'):
        test_id = request.GET.get('test_id')
        tests_data = Chepterwise_test.objects.filter(test_id = test_id).annotate(total_marks=Sum('test_questions_answer__tq_weightage'))

        questions_data = Test_questions_answer.objects.filter(tq_name__test_id = test_id)
    context = {
        'tests_data':tests_data,
        'questions_data':questions_data
    }
    return render(request, 'teacherpanel/show_question_paper.html', context)





def delete_test_question_answer_teacher(request):
    if request.GET.get('delete_id'):
        del_id = request.GET['delete_id']
        print(del_id)
        try:
            data = Test_questions_answer.objects.get(tq_id=del_id)
            data.delete()
            messages.success(request,"Question Deleted Successfully")
        except data.DoesNotExist:
            messages.error(request,"Question Not Found")

        url = '/teacherside/show_test_questions_teacher/?test_id={}'.format(request.GET['test_id'])
    return redirect(url)