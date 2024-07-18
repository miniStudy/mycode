from django.shortcuts import render,get_object_or_404,redirect
from adminside.models import *
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import math
from django.db.models import Sum,Count
from django.db.models import Count, Case, When, IntegerField
import random
from django.http import Http404,JsonResponse
from studentside.forms import *
from adminside.form import *
from teacherside.forms import *
from django.db.models import OuterRef, Subquery, BooleanField,Q

# mail integration 
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives



def teacher_home(request):
     return render(request, 'teacherpanel/index.html')

def teacher_test(request):
     return render(request, 'teacherpanel/index.html')


def teacher_materials(request):
     return render(request, 'teacherpanel/index.html')


def teacher_timetable(request):
     timetable_data = Timetable.objects.all()

     context = {
          'timetable_data':timetable_data
     }
     return render(request, 'teacherpanel/timetable.html', context)


def teacher_attendance(request):
     data = Attendance.objects.all()
     std_data = Std.objects.all()
     batch_data = Batches.objects.all()
     stud_data = Students.objects.all()
     subj_data = Subject.objects.all()
     

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
               context.update({'attendance_data':data,'batch_data':batch_data,'get_std':get_std, 'stud_data':stud_data,'sub_data':subj_data})
     
     if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = data.filter(atten_timetable__tt_batch__batch_id = get_batch)
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


     attendance_present = data.filter(atten_present = True).count()
     attendance_all = data.all().count()
     if attendance_all>0:
        overall_attendance = round((attendance_present/attendance_all) * 100,2)
        context.update({'overall_attendance':overall_attendance})

     sub_list = subj_data.all().values('sub_name').distinct()
     subject_wise_attendance = []
     subjects = []
     for x in sub_list:
        sub_name = x['sub_name']
        sub_one = data.filter(atten_present = True,atten_timetable__tt_subject1__sub_name=sub_name).count()
        sub_all = data.filter(atten_timetable__tt_subject1__sub_name = sub_name).count()
        if sub_all>0:
            sub_attendance = round((sub_one/sub_all) * 100,2)
            subject_wise_attendance.append(sub_attendance)
            subjects.append(sub_name)
            
     combined_data = zip(subject_wise_attendance, subjects)

     context.update({'combined_data': combined_data})
     return render(request, 'teacherpanel/attendance.html',context)

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
     
          }
     else:
        messages.error(request, "Please! Select Standard And Batch")
        return redirect('teacher_attendance')  
     return render(request, 'teacherpanel/insert_attendence.html', context)

def handle_attendance(request):
     if request.method == 'POST':
        atten_timetable = request.POST.get('atten_timetable')
        atten_tt = Timetable.objects.get(tt_id = atten_timetable)
        selected_items = request.POST.getlist('selection')
        if selected_items:
          selected_ids = [int(id) for id in selected_items]
        for i in selected_ids:
            stud = Students.objects.get(stud_id = i)
            Attendance.objects.create(atten_timetable=atten_tt, atten_student=stud, atten_present=1)
            messages.success(request, "Attendance has been submitted!")
     return redirect('teacher_attendance')


def teacher_syllabus(request):
     subjects = Subject.objects.filter()
     chepters = Chepter.objects.filter()
     return render(request, 'teacherpanel/syllabus.html', {'subjects':subjects,'chepters':chepters}) 


def teacher_announcement(request):
     return render(request, 'teacherpanel/index.html')     
     return render(request, 'teacherpanel/index.html')       


def teacher_doubts(request):
     doubts_data = Doubt_section.objects.all()
     context = {
         'doubts_data':doubts_data
     }
     return render(request, 'teacherpanel/doubts.html', context)     

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
          return render(request, 'teacherpanel/show_solution.html', {'doubts_solution':doubts_solution, 'doubt_id': doubt_id})


def teacher_events(request):
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

    return render(request, 'teacherpanel/events.html', context)


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
          return render(request, 'teacherpanel/master_auth.html',{'login_set':login,'c_email':cookie_email})
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







def teacher_test(request):
    data = Chepterwise_test.objects.annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage'))
    std_data = Std.objects.all()
    subject_data = Subject.objects.all()
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
            data = data.filter(test_sub__sub_std__std_id = get_std)
            subject_data = subject_data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'get_std':get_std,'std_data':std_data}) 


    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        if get_subject == 0:
            pass
        else:    
            data = data.filter(test_sub__sub_id = get_subject)
            get_subject = Subject.objects.get(sub_id = get_subject)
            context.update({'data':data,'subject_data':subject_data,'get_subject':get_subject}) 

    return render(request, 'teacherpanel/show_tests.html',context)



def insert_update_tests(request):
    std_data = Std.objects.all()
    subject_data = Subject.objects.all()
    context = {
        'title' : 'Tests',
        'std_data':std_data,
        'subject_data':subject_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        context.update({'get_std': get_std, 'std_data': std_data})

    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        subject_data = subject_data.filter(sub_id = get_subject)
        context.update({'get_subject': get_subject, 'subject_data': subject_data})     

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
        # ===================insert_logic===========================
        if request.method == 'POST':
            form = tests_form(request.POST, request.FILES)
            if form.is_valid():
                check = Chepterwise_test.objects.filter(test_name=form.data['test_name'], test_std__std_id=form.data['test_std']).count()
                if check >= 1:
                    messages.error(request, '{} is already Exists'.format(form.data['test_name']))
                else:    
                    form.save()
                    return redirect('teacher_test')
            else:
                filled_data = form.data
                context.update({'filled_data': filled_data, 'errors': form.errors})
                return render(request, 'teacherpanel/insert_update_tests.html', context) 
        
    return render(request, 'teacherpanel/insert_update_tests.html', context)




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
        }
        return render(request, 'teacherpanel/show_test_questions_teacher.html',context)
    else:
        return redirect('teacher_test') 

def insert_update_test_questions_teacher(request):
    chep_data = Chepter.objects.all()
    context = {
        'chep_data': chep_data,
        'que_type': Test_questions_answer.que_type,
    }

    if request.GET.get('test_id'):
        test_id = request.GET['test_id']
        print(test_id)
        context.update({'test_id': test_id})

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







def teacher_announcement(request):
    data = Announcements.objects.all()
    std_data = Std.objects.all()
    batch_data = Batches.objects.all()
   
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
            data = data.filter(announce_std__std_id = get_std)
            batch_data = batch_data.filter(batch_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'batch_data':batch_data,'get_std':get_std})
            

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = data.filter(announce_batch__batch_id = get_batch)
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'data':data,'get_batch':get_batch})        
            
    return render(request, 'teacherpanel/show_announcements.html',context)



def announcements_insert_update_teacher(request):
    std_data = Std.objects.all()
    batch_data = Batches.objects.all()
    # ------------getting students for mail------------------
    students_for_mail = Students.objects.all()

    context = {
        'title' : 'Insert Announcements',
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
