from django.shortcuts import render, redirect
from adminside.models import *
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import random
import statistics
from django.db.models import Sum,Count
from django.db.models import Count, Case, When, IntegerField
from django.db.models import OuterRef, Subquery, BooleanField,Q
from parentsside.decorators import *

# mail integration 
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives

# Create your views here.
# Shivam is on testing

@parent_login_required
def parent_home(request):
    student_id = request.session['parent_id']
    student = Students.objects.get(stud_id = student_id)
    student_std = student.stud_std.std_id
    students_li = Students.objects.filter(stud_std__std_id = student_std).values('stud_id', 'stud_name', 'stud_lastname')
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
        if student_id == x['stud_id']: 
            current_student_overall_test_result = overall_result

        overall_attendance_li.append({'stud_name':x['stud_name'], 'stud_lastname':x['stud_lastname'], 'overall_attendance_studentwise':overall_attendence_studentwise, 'overall_result':overall_result})


    overall_attendance_li = sorted(overall_attendance_li, key=lambda x: x['overall_result'], reverse=True)
    overall_attendance_li = overall_attendance_li[:5]


        #=============== Test Result Dashboard ===============================================================
    test_result_analysis = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id).values('tau_obtained_marks', 'tau_test_id__test_name').order_by('-pk')

    test_counts = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id).count()

    test_result_list = []
    test_name_list = []
    for x in test_result_analysis:
        test_name_list.append(x['tau_test_id__test_name'])
        test_result_list.append(x['tau_obtained_marks'])

    context = {
        'title': 'Home',
        'overall_attendance_li':overall_attendance_li,
        'test_result_list':test_result_list,
        'test_name_list': test_name_list,
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
    event_data = Event.objects.all().values('event_id','event_name')
    event_imgs = Event_Image.objects.all().values('event_id','event_img')
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



@parent_login_required
def show_parentside_report_card(request):
    student_id = request.session['parent_id']

    # ===============Overall Attendance==================
    student = Students.objects.get(stud_id = student_id)
    student_std = student.stud_std.std_id

    total_attendence = Attendance.objects.filter(atten_student__stud_id = student_id).count()
    
    present_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=True).count()

    absent_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=False).count()
    
    if total_attendence > 0:
        overall_attendence = (present_attendence/total_attendence)*100
    else:
        overall_attendence = 0



    # ==================Test Report and Attendance Report============
    students_li = Students.objects.filter(stud_std__std_id = student_std).values('stud_id', 'stud_name')
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
        if student_id == x['stud_id']: 
            current_student_overall_test_result = overall_result

        overall_attendance_li.append({'stud_name':x['stud_name'], 'overall_attendance_studentwise':overall_attendence_studentwise, 'overall_result':overall_result})

    
    overall_attendance_li = sorted(overall_attendance_li, key=lambda x: x['overall_result'], reverse=True)
    overall_attendance_li = overall_attendance_li[:5]
    


   # ===================SubjectsWise Attendance============================
    subjects_li = Subject.objects.filter(sub_std__std_id = student_std).values('sub_name').distinct()
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

    subjects_data = Subject.objects.filter(sub_std=student_std)
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
    class_average_result = round(statistics.mean(overall_results),2)
    

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

    return render(request, 'parentpanel/report_card.html', context)


@parent_login_required
def show_parentside_payment(request):
    student_id = request.session['parent_id']
    student_data = Students.objects.get(stud_id = student_id)

    discount_amount = Discount.objects.filter(discount_stud_id__stud_id = student_id) 
    if discount_amount:
        fees_to_paid = int(student_data.stud_pack.pack_fees) - int(discount_amount[0].discount_amount)
    else:
        fees_to_paid = int(student_data.stud_pack.pack_fees)

    # ===========================Paid Fees========================================

    fees_collection = Fees_Collection.objects.filter(fees_stud_id__stud_id = student_id).values('fees_stud_id__stud_name', 'fees_stud_id__stud_lastname', 'fees_paid', 'fees_date', 'fees_mode')
    if fees_collection:
        paid_fees = Fees_Collection.objects.filter(fees_stud_id__stud_id = student_id).aggregate(tol_amount=Sum('fees_paid'))
        paid_fees = int(paid_fees['tol_amount'])
    else:
        paid_fees = 0

    # ==========================Remaining_Fees====================================

    remaining_fees = fees_to_paid - paid_fees
   
    # ===========================Cheque Fees======================================

    cheque_data = Cheque_Collection.objects.filter(cheque_stud_id__stud_id = student_id, cheque_paid = False).values('cheque_paid', 'cheque_amount', 'cheque_date', 'cheque_expiry', 'cheque_paid', 'cheque_bounce')

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
    return render(request, 'parentpanel/fee_payment.html', context)

@parent_login_required
def show_parentside_announcement(request):
    title = 'Announcement'
    student_id = request.session['parent_id']
    student = Students.objects.get(stud_id = student_id)
    announcements_data = Announcements.objects.filter(
    Q(announce_std=None, announce_batch=None) |
    Q(announce_std__std_id=student.stud_std.std_id, announce_batch=None) |
    Q(announce_std__std_id=student.stud_std.std_id, announce_batch__batch_id=student.stud_batch.batch_id)
).order_by('-pk')[:50].values('announce_title','announce_id','announce_msg','announce_date')

    return render(request, 'parentpanel/announcement.html', {"announcements_data":announcements_data, 'title':title})

@parent_login_required
def show_parentside_timetable(request):
    student_id = request.session['parent_id']
    student = Students.objects.get(stud_id = student_id)
    title = 'Timetable'
    timetable_data = Timetable.objects.filter(tt_batch__batch_id = student.stud_batch.batch_id).values('tt_day','tt_subject1','tt_time1','tt_tutor1__fac_name')
    return render(request, 'parentpanel/timetable.html', {'timetable_data':timetable_data, 'title':title})