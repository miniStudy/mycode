from django.shortcuts import render,get_object_or_404,redirect, HttpResponse
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
from team_ministudy.forms import suggestions_improvements_Form
from team_ministudy.models import NewInstitution, suggestions_improvements
from teacherside.tasks import *
from django.contrib.auth.hashers import make_password
from teacherside.tasks import send_notification
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime, timezone as dt_timezone
import random
from django.http import Http404,JsonResponse
from studentside.forms import *
from adminside.form import *
from teacherside.forms import *
from django.db.models import OuterRef, Subquery, BooleanField,Q
from django.core.paginator import Paginator
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import pytz
import fitz  # PyMuPDF
from PIL import Image
import io
from django.core.files.base import ContentFile


# mail integration 
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context, Template
from django.core.mail import EmailMultiAlternatives


from teacherside.decorators import *

ist = pytz.timezone('Asia/Kolkata')


def paginatoorrr(queryset,request):
    paginator = Paginator(queryset, 30)
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
    context = {}
    domain = request.get_host()
    msg = None
    overall_attendance_li = None
    fac_id = request.session['fac_id']
    
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)
    std_access_list=[]
    subject_access_list = []
    for x in faculty_access:
        std_access_list.append(x.fa_batch.batch_std.std_id)
        subject_access_list.append(x.fa_subject.sub_id)

    std_data = Std.objects.filter(std_id__in = std_access_list, domain_name = domain)
    subject_data = Subject.objects.filter(sub_id__in = subject_access_list, domain_name = domain)

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
            overall_attendence_studentwise = (present_attendence_studentwise/total_attendence_studentwise)*100
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
    
    #=====================Count Unverified Doubts=======================================================
    fac_data = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)
    l = []
    for data in fac_data:
        l.append(data.fa_subject.sub_id)
    
    unverified_solution = Doubt_section.objects.filter(doubt_subject__sub_id__in = l, domain_name = domain).annotate(verified_solution=Count(
        Case(
            When(doubt_solution__solution_verified=True, then=1),
            output_field=IntegerField(),
        ))).filter(verified_solution=0).count()
    
    # ----------------------------for chart on dashboard---------------------
    all_students= Students.objects.filter(domain_name = domain).count()
    all_male=Students.objects.filter(stud_gender='Male', domain_name = domain).count()
    all_female=Students.objects.filter(stud_gender='Female', domain_name = domain).count()
    all_other=Students.objects.filter(stud_gender='Other', domain_name = domain).count()
    piechart_category = ['Male','Female','Other']
    piechart_data = [all_male,all_female,all_other]
    stds = Std.objects.filter(domain_name = domain).order_by('-std_board')

    std_list = []
    students_for_that_std = []
    for x in stds:
        n = (x.std_name+' '+x.std_board.brd_name)
        std_list.append(n)
        noss = Students.objects.filter(stud_std__std_id=x.std_id, domain_name = domain).count()
        students_for_that_std.append(noss)
    
    
    context.update({
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
    })
    return render(request, 'teacherpanel/index.html',context)

def teacher_login_page(request):
    domain = request.get_host()
    Institute_data = NewInstitution.objects.get(institute_domain = domain)  
    login=1
    context = {}
    if request.GET.get("deviceId"):
        deviceId = request.GET.get('deviceId','1')
        context.update({'deviceId':deviceId})
        if deviceId != '123':
            request.session['deviceId'] = deviceId
        context.update({'deviceId':deviceId})
    if request.GET.get("version"):
        version = request.GET.get('version','1')  
        context.update({'version':version})
        
    if request.COOKIES.get("fac_email"):
          cookie_email = request.COOKIES['fac_email'].lower()
          cookie_pass = request.COOKIES['fac_password']
          return render(request, 'teacherpanel/master_auth.html',{'login_set':login,'c_email':cookie_email,'c_pass':cookie_pass, 'title': 'login'})
    else:
          return render(request, 'teacherpanel/master_auth.html',{'login_set':login, 'title':'login', 'Institute_data': Institute_data})

def teacher_login_handle(request):
    domain = request.get_host()
    Institute_data = NewInstitution.objects.get(institute_domain = domain)
    if request.method == "POST":
        email = request.POST['email'].lower()
        password = request.POST['password']
        val = Faculties.objects.filter(fac_email=email).count()
        if val==1:
            fac_onesignal_player_id = request.session.get('deviceId', 'Error')
            if fac_onesignal_player_id != 'Error':
                try:
                    faculty = Faculties.objects.get(fac_email=email)
                    faculty.fac_onesignal_player_id = fac_onesignal_player_id
                    faculty.save()
                except Faculties.DoesNotExist:
                    messages.error(request, "Faculties with this OneSignal player ID does not exist.")
            Data = Faculties.objects.filter(fac_email=email, domain_name = domain)
            if Data:
                fac_id = Faculties.objects.get(fac_id = Data[0] .fac_id)
                if check_password(password, fac_id.fac_password):
                    for item in Data:
                        request.session['fac_id'] = item.fac_id
                        request.session['fac_name'] = item.fac_name
                        request.session['fac_profile'] = '{}'.format(item.fac_profile)
                        request.session['fac_logged_in'] = 'yes'
                        request.session['institute_logo'] = Institute_data.institute_logo.url
                        request.session['institute_name'] = Institute_data.institute_name
                        request.session['institute_logo_icon'] = Institute_data.institute_logo_icon.url

                    if request.POST.get("remember"):
                        response = redirect("teacher_home")
                        response.set_cookie('fac_email', email) 
                        response.set_cookie('fac_password', password)   
                        return response
                    
                    messages.success(request, 'Logged In Successfully')
                    return redirect('teacher_home')
                else:
                    messages.error(request, "password Wrong")
                    return redirect('teacher_login')
            else:
                messages.error(request, "Invalid Username & Password.")
                return redirect('teacher_login')

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
          val = Faculties.objects.filter(fac_email=email2).count()
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
                  hashed_password = make_password(password)
                  data = Faculties.objects.get(fac_otp = otp)
                  data.fac_password = hashed_password
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
     domain = request.get_host()
     fac_id = request.session['fac_id']
     faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)
     batch_access_list = []
     std_access_list=[]
     for x in faculty_access:
        batch_access_list.append(x.fa_batch.batch_id)
        std_access_list.append(x.fa_batch.batch_std.std_id)

     timetable_data = Timetable.objects.filter(tt_tutor1__fac_id = fac_id, tt_batch__batch_id__in = batch_access_list, tt_batch__batch_std__std_id__in = std_access_list, domain_name = domain)
     std_data = Std.objects.filter(std_id__in = std_access_list, domain_name = domain)
     batch_data = Batches.objects.filter(batch_id__in = batch_access_list, domain_name = domain)

     context = {
        'timetable_data':timetable_data,
        'title':'Timetable',
        'std_data':std_data,
        'batch_data':batch_data,
     }
     if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:
            timetable_data = timetable_data.filter(tt_batch__batch_std__std_id = get_std, domain_name = domain)
            batch_data = batch_data.filter(batch_std__std_id = get_std, domain_name = domain)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'timetable_data':timetable_data, 'batch_data':batch_data, 'get_std':get_std})

     if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            timetable_data = timetable_data.filter(tt_batch__batch_id = get_batch, domain_name = domain)
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'timetable_data':timetable_data, 'get_batch':get_batch})        

     return render(request, 'teacherpanel/timetable.html', context)

@teacher_login_required
def teacher_attendance(request):
    domain = request.get_host()
    fac_id = request.session['fac_id']
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)
    batch_access_list = []
    std_access_list=[]
    for x in faculty_access:
        batch_access_list.append(x.fa_batch.batch_id)
        std_access_list.append(x.fa_batch.batch_std.std_id)

    data = Attendance.objects.filter(domain_name = domain).values('atten_timetable__tt_day','atten_timetable__tt_time1','atten_timetable__tt_subject1__sub_name','atten_timetable__tt_tutor1__fac_name','atten_present','atten_student__stud_name','atten_student__stud_lastname','atten_date', 'atten_student__stud_roll_no').order_by('-atten_date', '-atten_timetable__tt_time1')
    data = paginatoorrr(data,request)
    std_data = Std.objects.filter(std_id__in = std_access_list, domain_name = domain)   
    batch_data = Batches.objects.filter(batch_id__in = batch_access_list, domain_name = domain)
    stud_data = Students.objects.filter(domain_name = domain)
    subj_data = Subject.objects.filter(domain_name = domain)    
    today = datetime.now(ist)
    today_records = Attendance.objects.filter(atten_date__contains=today, domain_name = domain)
     
     
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
               data = Attendance.objects.filter(atten_timetable__tt_batch__batch_std__std_id = get_std, domain_name = domain).values('atten_timetable__tt_day','atten_timetable__tt_time1','atten_timetable__tt_subject1__sub_name','atten_timetable__tt_tutor1__fac_name','atten_present','atten_student__stud_name','atten_student__stud_lastname','atten_date', 'atten_student__stud_roll_no').order_by('-atten_date', '-atten_timetable__tt_time1')
               data = paginatoorrr(data,request)
               batch_data = batch_data.filter(batch_std__std_id = get_std, domain_name = domain)
               stud_data = stud_data.filter(stud_std__std_id = get_std, domain_name = domain)
               subj_data = subj_data.filter(sub_std__std_id = get_std, domain_name = domain)
               get_std = Std.objects.get(std_id = get_std)
               context.update({'data':data,'batch_data':batch_data,'get_std':get_std, 'stud_data':stud_data,'sub_data':subj_data})
     
    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = Attendance.objects.filter(atten_timetable__tt_batch__batch_id = get_batch, domain_name = domain).values('atten_timetable__tt_day','atten_timetable__tt_time1','atten_timetable__tt_subject1__sub_name','atten_timetable__tt_tutor1__fac_name','atten_present','atten_student__stud_name','atten_student__stud_lastname','atten_date', 'atten_student__stud_roll_no').order_by('-atten_date', '-atten_timetable__tt_time1')
            data = paginatoorrr(data,request)
            stud_data = stud_data.filter(stud_batch__batch_id = get_batch, domain_name = domain)
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
            atten_date = datetime.strptime(atten_date, '%Y-%m-%d').date()
            data = Attendance.objects.filter(atten_date__date=atten_date, domain_name = domain).values('atten_timetable__tt_day','atten_timetable__tt_time1','atten_timetable__tt_subject1__sub_name','atten_timetable__tt_tutor1__fac_name','atten_present','atten_student__stud_name','atten_student__stud_lastname','atten_date', 'atten_student__stud_roll_no').order_by('-atten_date', '-atten_timetable__tt_time1')
            data = paginatoorrr(data,request)
            try:
                atten_obj = Attendance.objects.get(atten_date=atten_date)
                get_date = atten_obj.atten_date
            except ObjectDoesNotExist:
                get_date = None
            context.update({'data': data, 'get_date': get_date})                     


    attendance_present = Attendance.objects.filter(atten_present = True, domain_name = domain).count()
    attendance_all = Attendance.objects.filter(domain_name = domain).count()
    if attendance_all>0:
        overall_attendance = round((attendance_present/attendance_all) * 100,2)
        context.update({'overall_attendance':overall_attendance})

    sub_list = subj_data.all().values('sub_name').distinct()
    subject_wise_attendance = []
    subjects = []
    for x in sub_list:
        sub_name = x['sub_name']
        sub_one = Attendance.objects.filter(atten_present = True,atten_timetable__tt_subject1__sub_name=sub_name, domain_name = domain).count()
        sub_all = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = sub_name, domain_name = domain).count()
        if sub_all>0:
            sub_attendance = round((sub_one/sub_all) * 100,2)
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

    if request.GET.get('searchhh'):
        searchhh = request.GET['searchhh']
        if searchhh:
            data = Attendance.objects.filter(
            Q(atten_timetable__tt_day__icontains=searchhh) |
            Q(atten_timetable__tt_time1__icontains=searchhh) |
            Q(atten_timetable__tt_subject1__sub_name__icontains=searchhh) |
            Q(atten_timetable__tt_tutor1__fac_name__icontains=searchhh) |
            Q(atten_present__icontains=searchhh) |
            Q(atten_student__stud_name__icontains=searchhh) |
            Q(atten_student__stud_lastname__icontains=searchhh) |
            Q(atten_date__icontains=searchhh), domain_name = domain).values('atten_id','atten_timetable__tt_day','atten_timetable__tt_time1','atten_date','atten_timetable__tt_subject1__sub_name','atten_timetable__tt_tutor1__fac_name','atten_present','atten_student__stud_name','atten_student__stud_lastname', 'atten_student__stud_roll_no').order_by('-atten_date', '-atten_timetable__tt_time1')
            data = paginatoorrr(data, request)
            context.update({'data':data,'searchhh':searchhh})  

    return render(request, 'teacherpanel/attendance.html',context)

def teacher_edit_attendance(request):
    context = {'title' : 'Attendance'}
    domain = request.get_host()
    if request.GET.get('get_std') and request.GET.get('get_batch'):
        get_std = request.GET['get_std']     
        get_batch = request.GET['get_batch']
        tt_id = request.GET['tt_id']
        std_data = Std.objects.get(std_id=get_std)
        batch_data = Batches.objects.get(batch_id=get_batch) 
        timetable_data = Timetable.objects.filter(tt_batch__batch_id = get_batch, tt_batch__batch_std__std_id = get_std,  domain_name = domain)
        students_data = Students.objects.filter(stud_std__std_id = get_std, stud_batch__batch_id = get_batch, domain_name = domain)
        get_hour = request.GET.get('hour','')     
        get_date = request.GET.get('date','')
        get_minute = request.GET.get('minute','')
        date_obj = datetime.strptime(get_date, '%Y-%m-%d')
        get_data = Attendance.objects.filter(atten_date__hour=get_hour, atten_date__date=date_obj,atten_timetable__tt_id=tt_id, domain_name = domain)
        context.update({
          'std_data':std_data,
          'batch_data':batch_data,
          'students_data':students_data,
          'timetable_data':timetable_data,
          'get_data':get_data,
          'get_date':get_date,
          'get_hour':get_hour})
    else:
        messages.error(request, 'Please! Select Standard And Batch')
        return redirect('teacher_attendance')
    return render(request, 'teacherpanel/teacher_edit_attendance.html', context)



@teacher_login_required
def insert_update_attendance(request):
     domain = request.get_host()
     if request.GET.get('get_std') and request.GET.get('get_batch'):
        get_std = request.GET['get_std']     
        get_batch = request.GET['get_batch']
        std_data = Std.objects.get(std_id=get_std)
        batch_data = Batches.objects.get(batch_id=get_batch) 
        timetable_data = Timetable.objects.filter(tt_batch__batch_id = get_batch, domain_name = domain)
        students_data = Students.objects.filter(stud_std__std_id = get_std, stud_batch__batch_id = get_batch, domain_name = domain)

        context = {
          'title' : 'Attendance',
          'std_data':std_data,
          'batch_data':batch_data,
          'students_data':students_data,
          'timetable_data':timetable_data,
        }

     else:
        messages.error(request, "Please! Select Standard And Batch")
        return redirect('teacher_attendance')  
     return render(request, 'teacherpanel/insert_attendence.html', context)

@teacher_login_required
def handle_attendance(request):
     domain = request.get_host()
     url = '/teacherside/teacher_attendance/'
     if request.method == 'POST':
        std_data = request.POST.get('std_data')
        batch_data = request.POST.get('batch_data')

        url = '/teacherside/teacher_attendance/?get_std={}&get_batch={}'.format(std_data, batch_data)

        atten_timetable = request.POST.get('atten_timetable')
        atten_tt = Timetable.objects.get(tt_id = atten_timetable)
        selected_items = request.POST.getlist('selection_attendance')
        students_all = Students.objects.filter(stud_batch__batch_id = batch_data, stud_std__std_id = std_data, domain_name = domain)
        if selected_items:
          selected_ids = [int(id) for id in selected_items]
        
        present_list = []
        absent_list = []
        parent_present_li = []
        parent_absent_li = []
        student_present_name_list = []
        student_absent_name_list = []
        telegram_student_present_list = []
        telegram_student_absent_list = []
        telegram_parent_present_list = []
        telegram_parent_absent_list = []
        onesignal_player_id_list = []

        for i in students_all:
            if i.stud_id in selected_ids:
                att = Attendance.objects.create(atten_timetable=atten_tt, atten_student=i, atten_present=1, domain_name = domain)        
                present_list.append(i.stud_email)
                parent_present_li.append(i.stud_guardian_email)
                student_present_name_list.append(i.stud_name)

                telegram_student_present_list.append(i.stud_telegram_studentchat_id)
                telegram_parent_present_list.append(i.stud_telegram_parentschat_id)
            else:
                att = Attendance.objects.create(atten_timetable=atten_tt, atten_student=i, atten_present=0, domain_name = domain)
                absent_list.append(i.stud_email)
                parent_absent_li.append(i.stud_guardian_email)
                student_absent_name_list.append(i.stud_name)

                telegram_student_absent_list.append(i.stud_telegram_studentchat_id)
                telegram_parent_absent_list.append(i.stud_telegram_studentchat_id)

            if i.stud_onesignal_player_id:
                onesignal_player_id_list.append(i.stud_onesignal_player_id)
        
        date = datetime.now()

        htmly = mail_templates.objects.get(mail_temp_type = 'Attendance_mail', mail_temp_selected=1).mail_temp_html
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
        'title': "Attendance Result",
        'name': student_present_name_list,
        'status': 'Present',
        'date': date,
        })
        htmly = Template(htmly)
        html_content = htmly.render(Context(context_data))     
        attendance_student_present_mail.delay(present_list, html_content)
        attendance_student_present_mail.delay(parent_present_li, html_content)

        htmly = mail_templates.objects.get(mail_temp_type = 'Attendance_mail', mail_temp_selected=1).mail_temp_html
        context_data = {
        'title': "Attendance Result",
        'name': student_absent_name_list,
        'status': 'Absent',
        'date': date,
        }
        htmly = Template(htmly)
        html_content = htmly.render(Context(context_data))     
        attendance_student_absent_mail.delay(absent_list, html_content)
        attendance_student_absent_mail.delay(parent_absent_li, html_content)


        #------------------------- Telegram Message -----------------------------------------
        attendance_telegram_message_student('Present', date, telegram_student_present_list)
        attendance_telegram_message_student('Absent', date, telegram_student_absent_list)

        attendance_telegram_message_parent('Present', date, telegram_parent_present_list)
        attendance_telegram_message_parent('Absent', date, telegram_parent_absent_list)

        #---------------------------Notification send ---------------------------------------
        title = 'Attendance Update'
        noti_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        for student in students_all:
            status = 'Present' if student.stud_id in selected_ids else 'Absent'
            if student.stud_onesignal_player_id:
                mess = f"Your attendance status for {noti_date} is {status}."
                # notification = Notification(
                # notify_title=title,
                # notify_notification=mess,
                # notify_user = 'student',
                # domain_name=domain)
                # notification.save()
                for player_id in onesignal_player_id_list:
                    send_notification(player_id,title,mess, request)
        messages.success(request, "Attendance has been submitted!")    
     return redirect(url)


@teacher_login_required
def edit_handle_attendance(request):
     domain = request.get_host()
     url = '/teacherside/teacher_attendance/'
     if request.method == 'POST':
        get_std = request.POST.get('get_std')
        get_batch = request.POST.get('get_batch')

        url = '/teacherside/teacher_attendance/?get_std={}&get_batch={}'.format(get_std, get_batch)
        get_date = request.POST.get('get_date')
        get_hour = request.POST.get('get_hour')
        get_date = datetime.strptime(get_date, '%Y-%m-%d')
        atten_timetable = request.POST.get('atten_timetable')
        atten_tt = Timetable.objects.get(tt_id = atten_timetable)
        selected_items = request.POST.getlist('selection_attendance')
        if selected_items:
          selected_ids = [int(id) for id in selected_items]
        current_all_attendance = Attendance.objects.filter(atten_date__hour=get_hour, atten_date__date=get_date,atten_timetable__tt_id = atten_timetable, domain_name = domain)  
        for i in current_all_attendance:
            if i.atten_student.stud_id in selected_ids:
                instance = Attendance.objects.get(atten_date__hour=get_hour, atten_date__date=get_date, atten_student__stud_id=i.atten_student.stud_id, domain_name = domain)  
                instance.atten_present = 1
                instance.save()
            else:
                instance = Attendance.objects.get(atten_date__hour=get_hour, atten_date__date=get_date, atten_student__stud_id=i.atten_student.stud_id, domain_name = domain)
                instance.atten_present = 0
                instance.save()

        messages.success(request, "Attendance has been updated!")
     return redirect(url)


@teacher_login_required
def teacher_syllabus(request):
    domain = request.get_host()
    fac_id = request.session['fac_id'] 
 
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)
    subjects_list = []
    batches_list = []
    for x in faculty_access:
        subjects_list.append(x.fa_subject.sub_id)
        batches_list.append(x.fa_batch.batch_id)

        
    syllabus_data = Syllabus.objects.filter(syllabus_batch__batch_id__in = batches_list, syllabus_chapter__chep_sub__sub_id__in = subjects_list, domain_name = domain)
    context = {'syllabus_data': syllabus_data}

    # if request.GET.get('chep_id'):
    #     chep_id = request.GET.get('chep_id')
    #     status_id = request.GET.get('status')

    #     # Get objects from the database
    #     chep_obj = Chepter.objects.get(chep_id=chep_id)
    #     get_batch = request.GET.get('get_batch')
    #     Last_obj = Syllabus.objects.filter(domain_name=domain, fac_syllabus__fac_id=fac_id, syllabus_batch__batch_id = get_batch).last()

    #     if Last_obj is not None:
    #         # Assuming Last_obj.syllabus_date is a datetime field, it should already have timezone info.
    #         provided_date = Last_obj.syllabus_date

    #         # Current date and time with timezone information
    #         today_date = timezone.now()

    #         # Calculate the difference in days
    #         difference_in_days = (today_date - provided_date).days

    #         # Update or create the Syllabus entry
    #         Syllabus.objects.update_or_create(
    #             syllabus_chapter=chep_obj,
    #             defaults={
    #                 'syllabus_status': status_id,
    #                 'syllabus_chapter': chep_obj,
    #                 'domain_name': domain,
    #                 'fac_syllabus': fac_object,
    #                 'Completion_time': difference_in_days,
    #                 'syllabus_batch': get_batch
    #             },
    #         )
    #     else:
    #         # Create without Completion_time if no Last_obj is found
    #         Syllabus.objects.update_or_create(
    #             syllabus_chapter=chep_obj,
    #             defaults={
    #                 'syllabus_status': status_id,
    #                 'syllabus_chapter': chep_obj,
    #                 'domain_name': domain,
    #                 'fac_syllabus': fac_object,
    #                 'syllabus_batch': get_batch
    #             },
    #         )
    
    
    
    subjects = Subject.objects.filter(sub_id__in = subjects_list, domain_name = domain)
    batches = Batches.objects.filter(batch_id__in = batches_list, domain_name = domain)
    

    if request.GET.get('get_batch'):
        get_batch = request.GET.get('get_batch')
        get_batch = Batches.objects.get(batch_id = get_batch)
        subjects = subjects.filter(sub_std__std_id = get_batch.batch_std.std_id)
        syllabus_data = syllabus_data.filter(syllabus_batch__batch_id = get_batch.batch_id)
        context.update({'get_batch': get_batch, 'subjects': subjects, 'syllabus_data': syllabus_data})

    if request.GET.get('get_subject'):
        get_subject = request.GET.get('get_subject')
        get_subject = Subject.objects.get(sub_id = get_subject)
        syllabus_data = syllabus_data.filter(syllabus_chapter__chep_sub__sub_id = get_subject.sub_id)
        context.update({'get_subject': get_subject, 'syllabus_data': syllabus_data})

    context.update({
        'title':'Syllabus',
        'subjects':subjects,
        'batches': batches,
        
    })
    return render(request, 'teacherpanel/syllabus.html', context) 

@teacher_login_required  
def insert_update_syllabus(request):
    context = {}
    domain = request.get_host()
    fac_id = request.session['fac_id']
 
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)
    subjects_list = []
    batches_list = []
    standard_list = []
    for x in faculty_access:
        subjects_list.append(x.fa_subject.sub_id)
        batches_list.append(x.fa_batch.batch_id)
        standard_list.append(x.fa_batch.batch_std.std_id)

    chepter_data = Chepter.objects.filter(chep_std__std_id__in = standard_list, domain_name = domain)
    batch_data = Batches.objects.filter(batch_id__in = batches_list, domain_name = domain)
    fac_data = Faculties.objects.get(fac_id = fac_id, domain_name = domain)

    if request.GET.get('get_batch') and request.GET.get('get_subject'):
        get_batch = request.GET.get('get_batch')
        get_subject = request.GET.get('get_subject')
        chepter_data = chepter_data.filter(chep_sub__sub_id = get_subject, domain_name = domain)
        batch_data = batch_data.filter(batch_id = get_batch, domain_name = domain)
        context.update({'chepter_data': chepter_data})

    context.update({'chepter_data': chepter_data, 'batch_data': batch_data, 'fac_data': fac_data, 'title':'Syllabus'})


    if request.method == 'POST':
        chep_id = request.POST.get('syllabus_chapter')
        status_id = request.POST.get('syllabus_status')
        print(status_id)
        fac_syllabus = request.POST.get('fac_syllabus')
        fac_object = Faculties.objects.get(fac_id = fac_syllabus)
        # Get objects from the database
        chep_obj = Chepter.objects.get(chep_id=chep_id)
        get_batch = request.POST.get('syllabus_batch')
        batch_obj = Batches.objects.get(batch_id = get_batch)
        Last_obj = Syllabus.objects.filter(domain_name=domain, fac_syllabus__fac_id=fac_id, syllabus_batch__batch_id = get_batch).last()

        if Last_obj is not None:
            # Assuming Last_obj.syllabus_date is a datetime field, it should already have timezone info.
            provided_date = Last_obj.syllabus_date

            # Current date and time with timezone information
            today_date = timezone.now()

            # Calculate the difference in days
            difference_in_days = (today_date - provided_date).days

            # Update or create the Syllabus entry
            Syllabus.objects.update_or_create(
                syllabus_chapter=chep_obj,
                defaults={
                    'syllabus_status': status_id,
                    'syllabus_chapter': chep_obj,
                    'domain_name': domain,
                    'fac_syllabus': fac_object,
                    'Completion_time': difference_in_days,
                    'syllabus_batch': batch_obj
                },
            )
        else:
            # Create without Completion_time if no Last_obj is found
            Syllabus.objects.update_or_create(
                syllabus_chapter=chep_obj,
                defaults={
                    'syllabus_status': status_id,
                    'syllabus_chapter': chep_obj,
                    'domain_name': domain,
                    'fac_syllabus': fac_object,
                    'syllabus_batch': batch_obj
                },
            )
        
        title = "Syllabus Completion Update"
        message = (
        f"The syllabus for chapter '{chep_obj.chep_name}' "
        f"in batch '{batch_obj.batch_name}' has been successfully completed."
)
        player_ids = AdminData.objects.filter(domain_name = domain).values('admin_onesignal_player_id')
        notification = Notification(
        notify_title=title,
        notify_notification=message,
        notify_user = 'admin',
        domain_name=domain)
        notification.save()
        for playerid in player_ids:
            if playerid['admin_onesignal_player_id']:
                send_notification(playerid['admin_onesignal_player_id'],title,message, request)
        return redirect('teacher_syllabus')
    return render(request, 'teacherpanel/insert_update_syllabus.html', context)


@teacher_login_required
def teacher_doubts(request):
    context = {}
    domain = request.get_host()
    fac_id = request.session['fac_id']
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)
    subjects_list = []
    for x in faculty_access:
        subjects_list.append(x.fa_subject.sub_id)

    doubts_data = Doubt_section.objects.filter(doubt_faculty__fac_id = fac_id, domain_name = domain).annotate(count_solution=Count('doubt_solution'), verified_solution=Count(
        Case(
            When(doubt_solution__solution_verified=True, then=1),
            output_field=IntegerField(),
        ))).order_by('-pk')

    if request.GET.get('get_verified'):
        get_verified = request.GET.get('get_verified')
        verify_check = request.GET.get('verify_check')
        doubts_data = doubts_data.filter(verified_solution = get_verified)
        context.update({'doubts_data': doubts_data, 'verify_check': verify_check})

    doubts_data = doubts_data[:30]
    context['doubts_data'] = doubts_data

    context.update({
        'title':'Doubts',
        'doubts_data':doubts_data
    })
    return render(request, 'teacherpanel/doubts.html', context)


@teacher_login_required
def show_teacher_solution_verified(request):
    fac_name = request.session['fac_name']
    domain = request.get_host()
    if request.GET.get('doubt_id'):
        doubt_id = request.GET.get('doubt_id')
        doubts_solution = Doubt_solution.objects.filter(solution_doubt_id__doubt_id = doubt_id, domain_name = domain)

        teacher_id = request.session['fac_id']
        fac_id = Faculties.objects.get(fac_id = teacher_id)
        if request.method == 'POST':
            verification = request.POST.get('verification')
            solution_id = request.POST.get('solution_id')
            sol_id = Doubt_solution.objects.get(solution_id = solution_id)
            sol_id.solution_verified = verification
            sol_id.solution_verified_by_teacher = fac_id
            sol_id.save()
        return render(request, 'teacherpanel/show_solution.html', {'doubts_solution':doubts_solution, 'doubt_id': doubt_id,'title':'Doubts Solution', 'fac_name': fac_name})

@teacher_login_required
def teacher_add_solution_function(request):
    title = 'Doubts'
    context = {}
    teacher_data = Faculties.objects.get(fac_id = request.session['fac_id'])
    if request.GET.get('doubt_id'):
        doubt_id = request.GET.get('doubt_id')
        doubt_data = Doubt_section.objects.get(doubt_id = doubt_id)
        context.update({'doubt_data': doubt_data, 'title': title})
    domain = request.get_host()
    if request.method == 'POST':
        form = teacher_solution_form(request.POST)
        if form.is_valid():
            doubt_id = form.cleaned_data['solution_doubt_id']
            id = doubt_id.doubt_id
            form.instance.solution_teacher_id = teacher_data.fac_name
            form.instance.solution_verified = True
            form.instance.solution_verified_by_teacher = teacher_data
            count_sol = Doubt_solution.objects.filter(solution_teacher_id = teacher_data.fac_name, solution_doubt_id__doubt_id=id, domain_name = domain).count()

            if count_sol == 1:
                messages.error(request, "Cannot add more than one solution!")
                return redirect('/teacherside/teacher_doubts/?doubt_id={}'.format(id))
            else:
                form.instance.domain_name = domain
                form.save()
                messages.success(request, "You'r solution has been added!")

                doubt = Doubt_section.objects.get(doubt_id = id)
                playerid = doubt.doubt_stud_id.stud_onesignal_player_id
                student_name = doubt.doubt_stud_id.stud_name
                fac_name = teacher_data.fac_name

                title = "Your Doubt Has Been Answered!"
                message = f"Hello {student_name}, your doubt has been answered by the {fac_name}. Check it out!"
                notification = Notification(
                notify_title=title,
                notify_notification=message,
                notify_user = 'student',
                domain_name=domain)
                notification.save()
                send_notification(playerid, title, message, request)

                return redirect('/teacherside/teacher_doubts/?doubt_id={}'.format(id))
        else:
            print('hello wolrd')    
    form = teacher_solution_form()   
    context.update({'form':form})
    return render(request, 'teacherpanel/add_solution.html', context)

def teacher_edit_solution_function(request):
    domain = request.get_host()
    teacher_data = Faculties.objects.get(fac_id = request.session['fac_id'])
    solution_id = request.GET.get('solution_id')
    instance = Doubt_solution.objects.get(solution_id=solution_id)
    context = {'solution_id': solution_id, 'instance':instance, 'title': 'Doubts'}
    if request.POST.get('solution'):
        form = teacher_solution_form(request.POST, instance=instance)
        if form.is_valid():
            id = form.cleaned_data['solution_doubt_id']
            form.instance.domain_name = domain
            form.instance.solution_teacher_id = teacher_data.fac_name
            form.save()
            return redirect('/teacherside/teacher_solution_verify/?doubt_id={}'.format(id.doubt_id))
    else:
        form = teacher_solution_form(instance=instance)
        context.update({'form': form})
    return render(request, 'teacherpanel/edit_solution.html', context)


@teacher_login_required
def teacher_events(request):
    domain = request.get_host()
    event_data = Event.objects.filter(domain_name = domain).values('event_id','event_name')
    event_imgs = Event_Image.objects.filter(domain_name = domain)
    selected_events = Event.objects.filter(domain_name = domain).first()
    context={
        'event_data':event_data,
        'event_imgs':event_imgs,
        'selected_events':selected_events,
        'title':'Events',
    }

    if request.GET.get('event_id'):
        event_id = request.GET['event_id']
        selected_events = Event.objects.get(event_id = event_id)
        event_imgs = Event_Image.objects.filter(event__event_id = event_id, domain_name = domain)
        
        context.update({'selected_events':selected_events, 'events_img':event_imgs})
    return render(request, 'teacherpanel/events.html', context)


@teacher_login_required
def teacher_test(request):
    domain = request.get_host()
    fac_id = request.session['fac_id']
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)
    subjects_list = []
    std_list = []
    for x in faculty_access:
        std_list.append(x.fa_batch.batch_std.std_id)
        subjects_list.append(x.fa_subject.sub_id)


    data = Chepterwise_test.objects.filter(test_std__std_id__in = std_list, domain_name = domain).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage'))
    data = paginatoorrr(data,request)

    std_data = Std.objects.filter(std_id__in = std_list, domain_name = domain)
    subject_data = Subject.objects.filter(sub_id__in = subjects_list, domain_name = domain)
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
            data = Chepterwise_test.objects.filter(test_sub__sub_std__std_id = get_std, domain_name = domain).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage'))
            data = paginatoorrr(data,request)
            subject_data = subject_data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'get_std':get_std, 'subject_data':subject_data, 'std_data':std_data}) 


    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        if get_subject == 0:
            pass
        else:    
            data = Chepterwise_test.objects.filter(test_sub__sub_id = get_subject, domain_name = domain).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage'))
            data = paginatoorrr(data,request)
            get_subject = Subject.objects.get(sub_id = get_subject)
            context.update({'data':data,'subject_data':subject_data,'get_subject':get_subject})

    if request.GET.get('searchhh'):
        searchhh = request.GET['searchhh']
        if searchhh:
            data = Chepterwise_test.objects.filter(
            Q(test_name__icontains=searchhh) |
            Q(test_sub__sub_name__icontains=searchhh) |
            Q(test_std__std_name__icontains=searchhh), domain_name = domain).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage'))
            data = paginatoorrr(data, request)
            context.update({'data':data,'searchhh':searchhh})  

    return render(request, 'teacherpanel/show_tests.html',context)


@teacher_login_required
def teacher_insert_offline_marks(request):
    domain= request.get_host()
    context = {}

    if request.GET.get('test_id'):
        test_id = request.GET.get('test_id')
        test_data = Chepterwise_test.objects.get(test_id = test_id)

        total_marks = 0
        for marks in Test_questions_answer.objects.filter(tq_name__test_id = test_id):
            total_marks += marks.tq_weightage

        context.update({'test_id':test_id, 'test_data': test_data, 'title': 'Tests', 'total_marks': total_marks})

    if request.GET.get('std_id'):
        std_id = request.GET.get('std_id')
        batch_data = Batches.objects.filter(batch_std__std_id = std_id, domain_name = domain)
        students_data = Students.objects.filter(stud_std__std_id = std_id, domain_name = domain)
        context.update({'std_id':std_id, 'batch_data':batch_data, 'students_data':students_data})
    else:
        messages.error(request, 'Please! Select Standard')
        return redirect('teacher_tests')
    
    if request.GET.get('batch_id'):
        batch_id = request.GET.get('batch_id')
        students_data = Students.objects.filter(stud_batch__batch_id = batch_id, domain_name = domain)
        batch_id = Batches.objects.get(batch_id=batch_id)
        context.update({'students_data':students_data, 'batch_id':batch_id})
    
    
    return render(request, 'teacherpanel/offline_marks.html',context)

@teacher_login_required
def teacher_save_offline_marks(request):
    domain = request.get_host()
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_id')
        test_id = request.POST.get('test_id')
        marks = request.POST.getlist('marks')
        date = request.POST.get('tau_date')
        test_data = Test_questions_answer.objects.filter(tq_name__test_id = test_id, domain_name = domain)
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
                tau_obtained_marks=mark,
                tau_date = date,
                domain_name = domain,
            )

            test_attempt.save()

        student_email_ids = []
        parent_email_ids = []
        student_names = []
        onesignal_player_ids = []
        student_marks = []

        if not date:
            test_date = datetime.now().date() 
            
        test = Test_attempted_users.objects.filter(tau_test_id__test_id=test_id.test_id, domain_name = domain).first()

        if test:
            test_name = test.tau_test_id.test_name
            total_marks = test.tau_total_marks
            

            for i, stud_id in enumerate(student_ids):
                student_email = Students.objects.get(stud_id=stud_id)
                student_names.append(student_email.stud_name)
                student_email_ids.append(student_email.stud_email)
                parent_email_ids.append(student_email.stud_guardian_email)
                onesignal_player_ids.append(student_email.stud_onesignal_player_id)
                student_marks.append(marks[i])
            
            htmly = mail_templates.objects.get(mail_temp_type = 'Student_marks_mail', mail_temp_selected=1, domain_name = domain).mail_temp_html   
            marks_mail.delay(student_names, student_marks, test_date, test_name, total_marks, student_email_ids, htmly)
            marks_mail.delay(student_names, student_marks, test_date, test_name, total_marks, parent_email_ids, htmly)
            

            title = "Marks Update"
            for index, player_id in enumerate(onesignal_player_ids):
                student_name = Students.objects.get(stud_id=student_ids[index]).stud_name
                student_score = student_marks[index]
                mess = (
                f"Dear {student_name}, your score for the test '{test_name}' is {student_score}/{total_marks}. "
                f"Keep up the hard work! Exam date: {date}.")
                notification = Notification(
                notify_title=title,
                notify_notification=mess,
                notify_user = 'student',
                domain_name=domain)
                notification.save()
                send_notification(player_id, title, mess, request)

        else:
            print("No test found for the given test ID.")

            test_attempt.save()        
    messages.success(request, 'Marks have been successfully saved.')
    return redirect('teacher_tests')

@teacher_login_required
def view_attemp_students(request):
    domain = request.get_host()
    if request.GET.get('test_id'):
        test_id = request.GET.get('test_id')
        students_attemp_data = Test_attempted_users.objects.filter(tau_test_id__test_id = test_id, domain_name = domain)

        students_count = students_attemp_data.count()

        marks_aggregates = students_attemp_data.aggregate(max_marks=Max('tau_obtained_marks'), min_marks=Min('tau_obtained_marks'), avg_marks=Avg('tau_obtained_marks'))
        avg_marks = marks_aggregates['avg_marks']
        if avg_marks is not None:
            avg_marks = round(avg_marks,2)
    
    return render(request, 'teacherpanel/students_view.html', {'students_attemp_data':students_attemp_data, 'students_count':students_count, 'marks_aggregates':marks_aggregates, 'avg_marks':avg_marks})

@teacher_login_required
def insert_update_tests(request):
    domain = request.get_host()
    std_data = Std.objects.filter(domain_name = domain)
    subject_data = Subject.objects.select_related().filter(domain_name = domain)
    chap_data = Chepter.objects.filter(domain_name = domain).values('chep_name','chep_id','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name')
    context = {
        'title' : 'Tests',
        'std_data':std_data,
        'subject_data':subject_data,
        'chap_data':chap_data
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        chap_data = Chepter.objects.filter(chep_std__std_id = get_std, domain_name = domain).values('chep_name','chep_id','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name')
        context.update({'get_std': get_std, 'std_data': std_data, 'chap_data':chap_data})

    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        subject_data = subject_data.filter(sub_id = get_subject)
        chap_data = Chepter.objects.filter(chep_sub__sub_id = get_subject, domain_name = domain).values('chep_name','chep_id','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name')
        context.update({'get_subject': get_subject, 'subject_data': subject_data, 'chap_data':chap_data})     

    
    # ================update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Chepterwise_test, pk=request.GET['pk'])
            form = tests_form(request.POST, instance=instance)
            check = Chepterwise_test.objects.filter(test_name=form.data['test_name'], test_std__std_id=form.data['test_std'], domain_name = domain).count()
            if check >= 1:
                messages.error(request, '{} is already Exists'.format(form.data['test_name']))
            else:
                if form.is_valid():
                    form.instance.domain_name = domain
                    form.save()
                    return redirect('teacher_test')
                else:
                    filled_data = form.data
                    context.update({'filled_data': filled_data, 'errors': form.errors})
        
        update_data = Chepterwise_test.objects.get(test_id=request.GET['pk'])
        context.update({'update_data': update_data})  

    else:
        if request.method == 'POST':
            test_std = request.POST.get('test_std')
            test_sub = request.POST.get('test_sub')
            url = '/teacherside/teacher_tests/?get_std={}&get_subject={}'.format(test_std, test_sub)
            form = tests_form(request.POST, request.FILES)
            if form.is_valid():
                check = Chepterwise_test.objects.filter(domain_name = domain, 
                    test_name=form.data['test_name'], test_std__std_id=form.data['test_std']
                ).count()
                if check >= 1:
                    messages.error(request, '{} already exists'.format(form.data['test_name']))
                else:
                    form.instance.domain_name = domain
                    if request.POST.get('test_chap'):
                        chap_object = Chepter.objects.get(chep_id = request.POST.get('test_chap'))
                        if chap_object.chep_std.std_name != '10':
                                messages.error(request, "In demo application, our AI is only available for 10 standard!")
                                return redirect('teacher_tests')
                    test_instance = form.save()
                    

                    # Check for auto-generate test
                    if request.POST.get('auto_generate_test'):
                        one_mark_count = int(request.POST.get('one_mark_questions', 0))
                        print(one_mark_count)
                        two_mark_count = int(request.POST.get('two_mark_questions', 0))
                        three_mark_count = int(request.POST.get('three_mark_questions', 0))
                        four_mark_count = int(request.POST.get('four_mark_questions', 0))
                        chap_object = Chepter.objects.get(chep_id = request.POST.get('test_chap'), domain_name = domain)

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
                            Test_questions_answer.objects.create(  domain_name = domain,   
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
                                tq_optiond=question.qb_optiond
                            )

                        for question in two_mark_questions:
                            chep_id = Chepter.objects.get(chep_name = question.qb_chepter, domain_name = domain)
                            Test_questions_answer.objects.create(domain_name = domain,
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
                                tq_optiond=question.qb_optiond
                            )

                        for question in three_mark_questions:
                            chep_id = Chepter.objects.get(chep_name = question.qb_chepter, domain_name = domain)
                            Test_questions_answer.objects.create(domain_name = domain,
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
                                tq_optiond=question.qb_optiond
                            )

                        for question in four_mark_questions:
                            chep_id = Chepter.objects.get(chep_name = question.qb_chepter, domain_name = domain)
                            Test_questions_answer.objects.create(domain_name = domain,
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
                                tq_optiond=question.qb_optiond
                            )
                    return redirect(url)
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

    return redirect('teacher_tests')

@teacher_login_required
def show_test_questions_teacher(request):
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
            'title':'Tests',
        }
        return render(request, 'teacherpanel/show_test_questions_teacher.html',context)
    else:
        return redirect('teacher_tests') 

@teacher_login_required
def insert_update_test_questions_teacher(request):
    domain = request.get_host()
    chep_data = Chepter.objects.filter(domain_name = domain)
    context = {
        'chep_data': chep_data,
        'que_type': Test_questions_answer.que_type,
    }

    if request.GET.get('test_id'):
        test_id = request.GET['test_id']
        test_data = Chepterwise_test.objects.get(test_id = test_id)
        chep_data = chep_data.filter(chep_sub__sub_id = test_data.test_sub.sub_id)
        context.update({'test_id': test_id,'chep_data':chep_data})

    if request.method == 'POST':
        form = TestQuestionsAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            testt_id = form.cleaned_data['tq_name']
            testt_id = testt_id.test_id
            form.instance.domain_name = domain
            form.save()
            url = '/teacherside/show_test_questions_teacher/?test_id={}'.format(testt_id)
            messages.success(request, 'Question Added Successfully')
            return redirect(url)  # Replace 'success_url' with your actual success URL
        else:
            context.update({'form': form,'errors':form.errors})
            return render(request, 'teacherpanel/insert_update_add_test_questions.html', context)
    else:
        form = TestQuestionsAnswerForm()
        context.update({'form': form})
        return render(request, 'teacherpanel/insert_update_add_test_questions.html', context)


@teacher_login_required
def teacher_announcement(request):
    domain = request.get_host()
    fac_id = request.session['fac_id']
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)
    batch_access_list = []
    std_access_list=[]
    for x in faculty_access:
        batch_access_list.append(x.fa_batch.batch_id)
        std_access_list.append(x.fa_batch.batch_std.std_id)
    

    data = Announcements.objects.filter(domain_name = domain).values('announce_id','announce_title','announce_msg','announce_date').order_by('-announce_id')
    data = paginatoorrr(data,request)
    std_data = Std.objects.filter(std_id__in = std_access_list, domain_name = domain)
    batch_data = Batches.objects.filter(batch_id__in = batch_access_list, domain_name = domain)
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
            data = Announcements.objects.filter(announce_std__std_id = get_std, domain_name = domain).values('announce_id','announce_title','announce_msg','announce_date').order_by('-announce_id')
            data = paginatoorrr(data,request)
            batch_data = batch_data.filter(batch_std__std_id = get_std, domain_name = domain)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'batch_data':batch_data,'get_std':get_std})
            

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = Announcements.objects.filter(announce_batch__batch_id = get_batch, domain_name = domain).values('announce_id','announce_title','announce_msg','announce_date').order_by('-announce_id')
            data = paginatoorrr(data,request)
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'data':data,'get_batch':get_batch})        
            
    return render(request, 'teacherpanel/show_announcements.html',context)


@teacher_login_required
def announcements_insert_update_teacher(request):
    domain = request.get_host()
    std_data = Std.objects.filter(domain_name = domain)
    batch_data = Batches.objects.filter(domain_name = domain)
    # ------------getting students for mail------------------
    students_for_mail = Students.objects.filter(domain_name = domain)

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
        announce_std = request.POST.get('announce_std')
        announce_batch = request.POST.get('announce_batch')
        url = '/teacherside/teacher_announcement/?get_std={}&get_batch={}'.format(announce_std, announce_batch)
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
            # ---------------------sendmail Logic===================================
            students_email_list = []
            onesignal_player_id_list = []
            for x in students_for_mail:
                students_email_list.append(x.stud_email)
                if x.stud_onesignal_player_id:
                    onesignal_player_id_list.append(x.stud_onesignal_player_id)
            # announcement_mail(form.cleaned_data['announce_title'],form.cleaned_data['announce_msg'],students_email_list)
            title = 'New Announcement'
            mess = f"{form.cleaned_data['announce_title']}: {form.cleaned_data['announce_msg']}"
            notification = Notification(
            notify_title=title,
            notify_notification=mess,
            notify_user = 'student',
            domain_name=domain)
            notification.save()
            for player_id in onesignal_player_id_list:
                send_notification(player_id,title,mess, request)
            return redirect(url)
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
                messages.success(request, 'Announcements Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('teacher_announcement')


@teacher_login_required
def teacher_materials(request):
    domain = request.get_host()
    fac_id = request.session['fac_id']
    context={}
    return render(request, 'teacherpanel/show_materials.html', context)

@teacher_login_required
def teacher_insert_update_materials(request):
    domain = request.get_host()
    context={}
    return render(request, 'teacherpanel/insert_update_materials_teacher.html', context)


@teacher_login_required
def materials_delete_teacher(request):
    if request.method == 'GET':
        selected_items = request.GET.get('delete_material_id')
        if selected_items:
            try:
                Chepterwise_material.objects.get(cm_id=selected_items).delete()
                messages.success(request, 'Materials Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('teacher_materials')

@teacher_login_required
def teacher_view_profile(request):
    domain = request.get_host()
    teacher_id = request.session['fac_id']
    teacher_profile = Faculties.objects.get(fac_id = teacher_id, domain_name = domain)
    teacher_access = Faculty_Access.objects.filter(fa_faculty__fac_id = teacher_id, domain_name = domain)
    context = {
        'teacher_profile' : teacher_profile,
        'title': 'Profile',
        'teacher_access':teacher_access,
    }
    return render(request, 'teacherpanel/myprofile.html', context)


@teacher_login_required
def teacher_profile_update(request):
    domain = request.get_host()
    teacher_id = request.session['fac_id']
    teacher_obj = Faculties.objects.get(fac_id = teacher_id)
    if request.method == 'POST':
        form = teacher_update_form(request.POST, request.FILES, instance=teacher_obj)
        if form.is_valid():
            form.instance.domain_name = domain
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

@teacher_login_required
def report_card_show(request):
    domain = request.get_host()
    fac_id = request.session['fac_id']
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)
    subject_access_list = []
    std_access_list = []
    batch_access_list = []
    for x in faculty_access:
        subject_access_list.append(x.fa_subject.sub_id)
        std_access_list.append(x.fa_batch.batch_std.std_id)
        batch_access_list.append(x.fa_batch.batch_id)

    data = Attendance.objects.filter(domain_name = domain)
    std_data = Std.objects.filter(std_id__in = std_access_list, domain_name = domain)
    batch_data = Batches.objects.filter(batch_id__in = batch_access_list, domain_name = domain)
    stud_data = Students.objects.filter(domain_name = domain).values('stud_std__std_id', 'stud_batch__batch_id', 'stud_id', 'stud_name', 'stud_lastname')
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
        total_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, domain_name = domain).count()
        
        present_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=True, domain_name = domain).count()

        absent_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=False, domain_name = domain).count()
        
        if total_attendence > 0:
            overall_attendence = round((present_attendence/total_attendence)*100,2)
        else:
            overall_attendence = 0



        # ==================Test Report and Attendance Report============
        students_li = Students.objects.filter(stud_std__std_id = student_std, domain_name = domain).values('stud_id', 'stud_name','stud_lastname')
        overall_attendance_li = []
        for x in students_li:
            total_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x['stud_id'], domain_name = domain).count()
            present_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x['stud_id'], atten_present=True, domain_name = domain).count()
            # print("==============================================",total_attendence_studentwise)
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
                context.update({'current_student_overall_test_result':current_student_overall_test_result})

            overall_attendance_li.append({'stud_name':x['stud_name'], 'overall_attendance_studentwise':overall_attendence_studentwise, 'overall_result':overall_result})
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

@teacher_login_required
def today_learning_show(request):
    domain = request.get_host()
    fac_id = request.session['fac_id']
    fac_data = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)

    std_access = []
    batch_access = []
    for x in fac_data:
        std_access.append(x.fa_batch.batch_std.std_id)
        batch_access.append(x.fa_batch.batch_id)
    
    standard_access_data = Std.objects.filter(std_id__in = std_access, domain_name = domain)
    batch_access_data = Batches.objects.filter(batch_id__in = batch_access, domain_name = domain)

    today_learn_data = Today_Teaching.objects.filter(today_teaching_batches_id__batch_id__in = batch_access, today_teaching_batches_id__batch_std__std_id__in = std_access, domain_name = domain).order_by('-today_teaching_id')

    context = {
        'today_learn_data':today_learn_data,
        'standard_access_data':standard_access_data,
        'batch_access_data':batch_access_data,
        'title': 'Class-Overview'
    }

    if request.GET.get('get_std'):
        get_std = request.GET.get('get_std')
        if get_std == 0:
            pass
        else:
            today_learn_data = today_learn_data.filter(today_teaching_batches_id__batch_std__std_id = get_std, domain_name = domain)
            batch_access_data = batch_access_data.filter(batch_std__std_id = get_std, domain_name = domain)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'today_learn_data':today_learn_data,'batch_access_data':batch_access_data,'get_std':get_std})

    if request.GET.get('get_batch'):
        get_batch = request.GET.get('get_batch')
        if get_batch == 0:
            pass
        else:
            today_learn_data = today_learn_data.filter(today_teaching_batches_id__batch_id = get_batch, domain_name = domain)
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'today_learn_data':today_learn_data,'get_batch':get_batch}) 

    return render(request, 'teacherpanel/today_learn.html', context)

@teacher_login_required
def today_learning_insert_update(request):
    title = 'Class-Overview'
    domain = request.get_host()
    fac_id = request.session['fac_id']
    fac_data = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)

    std_access = []
    batch_access = []
    subject_access = []
    for x in fac_data:
        std_access.append(x.fa_batch.batch_std.std_id)
        batch_access.append(x.fa_batch.batch_id)
        subject_access.append(x.fa_subject.sub_id)
    
    chepters_data = Chepter.objects.filter(chep_sub__sub_id__in = subject_access, domain_name = domain)
    standard_access_data = Std.objects.filter(std_id__in = std_access, domain_name = domain)
    batch_access_data = Batches.objects.filter(batch_id__in = batch_access, domain_name = domain)

    context = {
        'standard_access_data':standard_access_data,
        'batch_access_data':batch_access_data,
        'chepters_data':chepters_data,
        'title': title
    }
    
    if request.GET.get('get_std'):
        get_std = request.GET['get_std']
        if get_std == 0:
            pass
        else:
            batch_access_data = batch_access_data.filter(batch_std__std_id = get_std, domain_name = domain)
            chepters_data = chepters_data.filter(chep_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'batch_access_data':batch_access_data,'get_std':get_std, 'chepters_data': chepters_data})

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'get_batch':get_batch}) 

    if request.method == 'POST':
        today_teaching_batches_id = request.POST.get('today_teaching_batches_id')
        get_std = request.POST.get('get_std')
        url = '/teacherside/today_learning/?get_std={}&get_batch={}'.format(get_std or '', today_teaching_batches_id)
        # ================update Logic============================
        if request.GET.get('pk'):
            instance = get_object_or_404(Today_Teaching, pk=request.GET['pk'])
            form = teacher_todaylearn_form(request.POST, instance=instance)
            if form.is_valid():
                form.instance.domain_name = domain
                form.save()
                messages.success(request, 'Today learning Updated sucessfully!')
                return redirect(url)
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})

        # ===================insert_logic===========================
        form = teacher_todaylearn_form(request.POST)
        if form.is_valid():
            form.instance.domain_name = domain
            form.save()

            batch = Batches.objects.get(batch_id = request.POST.get('today_teaching_batches_id'))
            students = Students.objects.filter(stud_batch__batch_id = batch.batch_id).values('stud_onesignal_player_id', 'guardian_onesignal_player_id')
            title = "Today's Learning Update"
            mess = form.instance.today_teaching_desc

            for playerid in students:
                if playerid['stud_onesignal_player_id']:
                    send_notification(playerid['stud_onesignal_player_id'], title, mess, request)
                
                if playerid['guardian_onesignal_player_id']:
                    send_notification(playerid['guardian_onesignal_player_id'], title, mess, request)

            messages.success(request, 'Today learning Added Sucessfully!')
            return redirect(url)
        else:
            filled_data = form.data
            context.update({'filled_data ':filled_data,'errors':form.errors})
            return render(request, 'teacherpanel/today_learn_insert_update.html', context)

    if request.GET.get('pk'):
        update_data = Today_Teaching.objects.get(today_teaching_id = request.GET['pk'])
        context.update({'update_data':update_data})
    

    return render(request, 'teacherpanel/today_learn_insert_update.html', context)


@teacher_login_required
def today_learning_delete(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Today_Teaching.objects.filter(today_teaching_id__in=selected_ids).delete()
                messages.success(request, 'Today learning Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    return redirect('today_learning')

@teacher_login_required
def show_question_paper(request):
    domain = request.get_host()
    tests_data = None  # Initialize with a default value
    questions_data = None 
    if request.GET.get('test_id'):
        test_id = request.GET.get('test_id')
        tests_data = Chepterwise_test.objects.filter(test_id = test_id, domain_name = domain).annotate(total_marks=Sum('test_questions_answer__tq_weightage'))

        questions_data = Test_questions_answer.objects.filter(tq_name__test_id = test_id, domain_name = domain)
    context = {
        'tests_data':tests_data,
        'questions_data':questions_data
    }
    return render(request, 'teacherpanel/show_question_paper.html', context)

@teacher_login_required
def delete_test_question_answer_teacher(request):
    if request.GET.get('delete_id'):
        del_id = request.GET['delete_id']
        try:
            data = Test_questions_answer.objects.get(tq_id=del_id)
            data.delete()
            messages.success(request,"Question Deleted Successfully")
        except data.DoesNotExist:
            messages.error(request,"Question Not Found")

        url = '/teacherside/show_test_questions_teacher/?test_id={}'.format(request.GET['test_id'])
    return redirect(url)


@teacher_login_required
def teacher_export_data(request):
    domain = request.get_host()
    model_name = request.GET.get('model_name')
    Context={'title':model_name}
    fac_id = request.session['fac_id']
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id, domain_name = domain)
    subjects_list = [x.fa_subject.sub_id for x in faculty_access]
    std_list = [x.fa_batch.batch_std.std_id for x in faculty_access]

    
    if model_name == 'chepterwise_test':
        tests_data = []
        
        data = Chepterwise_test.objects.filter(test_std__std_id__in = std_list ,domain_name = domain).annotate(
            num_questions=Count('test_questions_answer'),
            total_marks=Sum('test_questions_answer__tq_weightage')
        )

        field_names = ['Test Name', 'Subject', 'Std', 'Questions', 'Total Marks']
        for x in data:
            temp_data = {}
            temp_data.update({'Test':x.test_name, 'Subject':x.test_sub.sub_name, 'Std':"{} {}".format(x.test_std.std_name, x.test_std.std_board.brd_name), 'Questions':x.num_questions, 'Total':x.total_marks})

            tests_data.append(temp_data)
        Context.update({'tests_data':tests_data, 'field_names':field_names})


    
    if model_name == 'attendance':
        attendance_data = []
        
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

    return render(request, 'export_data.html',Context)


@csrf_exempt  # Skip CSRF verification for API testing (enable CSRF protection for production)
def send_whatsapp_message_test_marks(user_name, phone, campaign_name='miniStudy_test', source='MiniStudy', template_params=None):
    # Default template parameters if none are provided
    if template_params is None:
        template_params = ['Trushal Patel', 'MiniStudy', '05-10-2024', 'Polynomials', '20', '25']  # Default values

    # User details
    api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3MDBlYTNjODQ4NGQ2MGI4NDhhZDczMiIsIm5hbWUiOiJtaW5pU3R1ZHlfd2hhdHNhcHAiLCJhcHBOYW1lIjoiQWlTZW5zeSIsImNsaWVudElkIjoiNjY5ZTMwOGZmYmE3OTE3ZjE1MGRmNTMyIiwiYWN0aXZlUGxhbiI6Ik5PTkUiLCJpYXQiOjE3MjgxMTMyMTJ9.aZSCryj6KAkD5ETSkYsmiGwOzs87-wwz70fs6D9kBcg' # Replace with your actual API key
    
    # Media details
    media = {
        "url": "https://metrofoods.co.nz/logoo.png",  # Optional: URL for media (if needed)
        "filename": "1nobg.png"  # Optional: Filename for the media
    }

    # Prepare the payload for the request
    data = {
        "apiKey": api_key,
        "campaignName": campaign_name,
        "destination": phone,
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



@csrf_exempt  # Skip CSRF verification for API testing (enable CSRF protection for production)
def send_whatsapp_message_announcement(user_name, phone, campaign_name='miniStudy_announcement', source='MiniStudy', template_params=None):
    # Default template parameters if none are provided
    if template_params is None:
        template_params = ['Trushal Patel', 'This is announcement for you']  # Default values

    # User details
    api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3MDBlYTNjODQ4NGQ2MGI4NDhhZDczMiIsIm5hbWUiOiJtaW5pU3R1ZHlfd2hhdHNhcHAiLCJhcHBOYW1lIjoiQWlTZW5zeSIsImNsaWVudElkIjoiNjY5ZTMwOGZmYmE3OTE3ZjE1MGRmNTMyIiwiYWN0aXZlUGxhbiI6Ik5PTkUiLCJpYXQiOjE3MjgxMTMyMTJ9.aZSCryj6KAkD5ETSkYsmiGwOzs87-wwz70fs6D9kBcg' # Replace with your actual API key
    
    # Media details
    media = {
        "url": "https://metrofoods.co.nz/logoo.png",  # Optional: URL for media (if needed)
        "filename": "1nobg.png"  # Optional: Filename for the media
    }

    # Prepare the payload for the request
    data = {
        "apiKey": api_key,
        "campaignName": campaign_name,
        "destination": phone,
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



@csrf_exempt  # Skip CSRF verification for API testing (enable CSRF protection for production)
def send_whatsapp_message_payment(user_name, phone, campaign_name='miniStudy_payment', source='MiniStudy', template_params=None):
    # Default template parameters if none are provided
    if template_params is None:
        template_params = ['Trushal Patel', 'UPI', '5000', '25-10-2024']  # Default values

    # User details
    api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3MDBlYTNjODQ4NGQ2MGI4NDhhZDczMiIsIm5hbWUiOiJtaW5pU3R1ZHlfd2hhdHNhcHAiLCJhcHBOYW1lIjoiQWlTZW5zeSIsImNsaWVudElkIjoiNjY5ZTMwOGZmYmE3OTE3ZjE1MGRmNTMyIiwiYWN0aXZlUGxhbiI6Ik5PTkUiLCJpYXQiOjE3MjgxMTMyMTJ9.aZSCryj6KAkD5ETSkYsmiGwOzs87-wwz70fs6D9kBcg' # Replace with your actual API key
    
    # Media details
    media = {
        "url": "https://metrofoods.co.nz/logoo.png",  # Optional: URL for media (if needed)
        "filename": "1nobg.png"  # Optional: Filename for the media
    }

    # Prepare the payload for the request
    data = {
        "apiKey": api_key,
        "campaignName": campaign_name,
        "destination": phone,
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



@csrf_exempt  # Skip CSRF verification for API testing (enable CSRF protection for production)
def send_whatsapp_message_event(user_name, phone, campaign_name='miniStudy_event', source='MiniStudy', template_params=None):
    # Default template parameters if none are provided
    if template_params is None:
        template_params = ['Trushal Patel', 'Event Name', '12-10-2024']  # Default values

    # User details
    api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3MDBlYTNjODQ4NGQ2MGI4NDhhZDczMiIsIm5hbWUiOiJtaW5pU3R1ZHlfd2hhdHNhcHAiLCJhcHBOYW1lIjoiQWlTZW5zeSIsImNsaWVudElkIjoiNjY5ZTMwOGZmYmE3OTE3ZjE1MGRmNTMyIiwiYWN0aXZlUGxhbiI6Ik5PTkUiLCJpYXQiOjE3MjgxMTMyMTJ9.aZSCryj6KAkD5ETSkYsmiGwOzs87-wwz70fs6D9kBcg' # Replace with your actual API key
    
    # Media details
    media = {
        "url": "https://metrofoods.co.nz/logoo.png",  # Optional: URL for media (if needed)
        "filename": "1nobg.png"  # Optional: Filename for the media
    }

    # Prepare the payload for the request
    data = {
        "apiKey": api_key,
        "campaignName": campaign_name,
        "destination": phone,
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



@teacher_login_required
def insert_suggestions_function(request):
    domain = request.get_host()
    suggestion = suggestions_improvements.objects.filter(domain_name = domain)
    username = request.session['fac_name']


    context = {
        'title': 'suggestions_improvements',
        'suggestions':suggestion,
        'username':username
    }
    
    if request.method == 'POST':
        si_user = request.POST.get('si_user')
        si_suggestion = request.POST.get('si_suggestion')
        suggestions_improvements.objects.create(si_user_name=username, si_user=si_user, si_suggestion=si_suggestion, domain_name = domain)
    
    return render(request, 'teacherpanel/insert_suggestions.html', context)




@teacher_login_required
def teacher_chatbox(request):
    context={"title": "Chatbox"}
    domain = request.get_host()
    teacher_id = request.session['fac_id']
    teacher_object = Faculties.objects.get(fac_id = teacher_id)
    
    Persons = Chatbox.objects.filter(chatbox_receiver=teacher_object.fac_email, domain_name = domain).values('chatbox_sender').distinct()
    if request.GET.get('selected_person'):
        selected_person = Students.objects.get(stud_guardian_email = request.GET.get('selected_person'))
        chatbox_data = Chatbox.objects.filter( 
        Q(chatbox_sender=teacher_object.fac_email,chatbox_receiver = selected_person.stud_guardian_email) |
        Q(chatbox_receiver=teacher_object.fac_email, chatbox_sender = selected_person.stud_guardian_email)
        )
        chatbox_data = chatbox_data.filter(domain_name = domain)
        context.update({'selected_person':selected_person,'chatbox_data':chatbox_data})

    else:
        if Persons:
            selected_person = Students.objects.get(stud_guardian_email = Persons[0]['chatbox_sender'])
            chatbox_data = Chatbox.objects.filter( 
            Q(chatbox_sender=teacher_object.fac_email,chatbox_receiver = selected_person.stud_guardian_email) |
            Q(chatbox_receiver=teacher_object.fac_email, chatbox_sender = selected_person.stud_guardian_email)
            )
            chatbox_data = chatbox_data.filter(domain_name = domain)
            context.update({'selected_person':selected_person,'chatbox_data':chatbox_data})

    Unique_persons = []
    for x in Persons:
        a = Students.objects.get(stud_guardian_email=x['chatbox_sender'])
        person_dict = {
            'GuardianName': a.stud_guardian_name,
            'StudentName' : a.stud_name,
            'StudentBatch' : a.stud_batch,
            'GuardianEmail' : a.stud_guardian_email,
        }
        Unique_persons.append(person_dict)
    context.update({
        'Unique_persons':Unique_persons,
        'faculty':teacher_object,
    })
    return render(request, 'teacherpanel/show_chatbox.html',context)


@teacher_login_required
def insert_chatbox_teacher(request):
    domain_name = request.get_host()
    teacher_id = request.session['fac_id']
    teacher_name = request.session['fac_name']
    teacher_object = Faculties.objects.get(fac_id = teacher_id)
    receiver = request.POST.get('chatbox_receiver')
    chat = request.POST.get('chatbox_chat')  
    Chatbox.objects.create(chatbox_sender = teacher_object.fac_email,chatbox_receiver=receiver,chatbox_chat=chat,domain_name = domain_name)
    parent_obj = Students.objects.get(stud_guardian_email = receiver)
    if parent_obj.guardian_onesignal_player_id:
        title = f"{teacher_name}"
        msg = chat
        playerid = parent_obj.guardian_onesignal_player_id
        send_notification(playerid, title, msg, request)    
    return redirect('/teacherside/teacher_chatbox?selected_person={}'.format(receiver))


@teacher_login_required
def show_notification_teacher_function(request):
    domain = request.get_host()
    notification_data = Notification.objects.filter(domain_name = domain, notify_user = 'teacher').order_by('-pk')
    context = {'notification_data': notification_data, 'title': 'Notification'}
    return render(request, 'teacherpanel/show_notification.html', context)


@teacher_login_required
def teacher_show_group_function(request):
    domain = request.get_host()
    fac_id = request.session['fac_id']
    faculty = Faculties.objects.get(fac_id = fac_id)
    group_data = Materials_access.objects.filter(materialaccess_email = faculty.fac_email, domain_name = domain)
    context = {'group_data': group_data, 'title': 'Materials'}
    return render(request, "teacherpanel/show_groupps.html", context)


@teacher_login_required
def teacher_add_group_function(request):
    context = {'title': 'Materials'}
    domain = request.get_host()
    if request.method == 'POST':
        form = group_form(request.POST)
        if form.is_valid():
            form.instance.domain_name = domain
            messages.success(request, "Group added successfully")
            form.save()
            return redirect('teacher_show_group')
    return render(request, "teacherpanel/add_group.html", context)


@teacher_login_required
def teacher_delete_group_function(request):
    if request.GET.get('pk'):
        pk = request.GET.get('pk')
        group_data = Groups.objects.get(group_id = pk)
        group_data.delete()
        messages.success(request, "Group deleted successully")
        return redirect('show_group')
    return render(request, "teacherpanel/show_group.html")


teacher_login_required
def teacher_show_material_function(request):
    context = {}
    domain = request.get_host()
    group_id = request.GET.get('group_id')
    materials_data = Materials.objects.filter(domain_name = domain, material_group_id__group_id = group_id)
    context.update({'materials_data': materials_data, 'title': 'Materials', 'group_id': group_id})
    return render(request, "teacherpanel/show_material.html", context)


@teacher_login_required
def teacher_add_material_function(request):
    domain = request.get_host()
    group_id = request.GET.get('group_id')
    group_data = Groups.objects.filter(domain_name = domain, group_id = group_id)
    context = {'group_data': group_data, 'title': Materials}
    if request.method == 'POST':
            group_id = request.POST.get('material_group_id')
            group_obj = Groups.objects.get(group_id = group_id)
            form = materials_form(request.POST, request.FILES)
            if form.is_valid():
                
                check = Materials.objects.filter(material_name = form.cleaned_data['material_name'], domain_name = domain).count()
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
                context.update({'filled_data': filled_data, 'errors': form.errors, 'title': 'Materials'})
                return render(request, 'teacherpanel/add_material.html', context)

    return render(request, 'teacherpanel/add_material.html', context)

@teacher_login_required
def teacher_delete_material_function(request):
    if request.GET.get('pk'):
        pk = request.GET.get('pk')
        material_data = Materials.objects.get(material_id = pk)
        material_data.delete()
        messages.success(request, "Material Deleted Successfully")
        return redirect('show_material')
    
    return render(request, "teacherpanel/show_material.html")

@teacher_login_required
def teacher_show_pdf(request):
    context={"title": "Materials"}
    if request.GET.get('pdf'):
        pdf = Materials.objects.get(material_id = request.GET.get('pdf'))
        context.update({
            'pdf':pdf,
        })
    return render(request,'teacherpanel/show_pdf.html', context)  