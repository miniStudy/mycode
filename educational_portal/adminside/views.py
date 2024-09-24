from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from adminside.form import *
from adminside.models import *
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import math
import statistics
import random
from django.http import Http404,JsonResponse
from django.db.models import Count,Sum, F, Case, When, Value, IntegerField
from django.core.files.storage import FileSystemStorage
from adminside.send_mail import *
# Create your views here.
# mail integration 
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from adminside.decorators import admin_login_required
from django.db.models import Count, Q
from django.http import Http404
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
import requests

def paginatoorrr(queryset,request):
        paginator = Paginator(queryset, 20)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return page_obj


def send_report_card(request):
    # Define your context
    context = {
        'logo_url': 'https://metrofoods.co.nz/1nobg.png',
        'student': {
            'name': 'Trushal Patel',
            'roll_no': '20'
        },
        'attendance': {
            'overall': '50%',
            'maths': '70%',
            'english': '50%',
            'science': '60%',
            'total_classes': '50',
            'absent_classes': '10'
        },
        'test_results': {
            'overall': '70%',
            'maths': '30%',
            'science': '60%',
            'english': '80%',
            'total_tests': '10',
            'absent_tests': '2',
            'average': '70%'
        },
        'doubts': {
            'solved': '20',
            'asked': '10',
            'verified': '8'
        }
    }
    

    # Generate the PDF
    # pdf = render_to_pdf('reportcardtable.html', context)
    # # Email configuration
    # subject = 'Student Report Card'
    # body = 'Please find attached the report card.'
    # from_email = 'miniStudy <mail@ministudy.in>'
    # to_email = 'tmp1221pmt@gmail.com'

    # # Create EmailMessage instance
    # email = EmailMessage(
    #     subject,
    #     body,
    #     from_email,
    #     [to_email],
    # )

    # # Attach PDF
    # email.attach('report_card.pdf', pdf, 'application/pdf')
    # # Send the email
    # email.send()
    # return HttpResponse("Email sent successfully!")
    return render(request, 'reportcardtable.html',context)

# -----------------------------auth Start---------------------------



def mail_send(request):
    # ------------mail sending ---------------
        sub = 'Offer Letter from miniStudy'
        mess = 'Offer Letter'
        email_from = 'miniStudy <mail@ministudy.in>'
        recp_list = ['mail.trushalpatel@gmail.com','sakahisharma88172@gmail.com']
        # send_mail(sub,mess,email_from,recp_list)
        htmly = get_template('Email/sakshi_offer_letter.html')
        # d = {'pname': pname,'qty':qty,'size': ring_size,'clr':ring_color,'uname':fname,'uemail':email,'ucontact':cnumber}
        text_content = ''
        html_content = htmly.render()
        msg = EmailMultiAlternatives(sub, text_content, email_from, recp_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect('Admin Home')


def admin_login_page(request):  
    login=1
    if request.COOKIES.get("admin_email"):
            cookie_email = request.COOKIES['admin_email']
            cookie_pass = request.COOKIES['admin_password']
            return render(request, 'master_auth.html',{'login_set':login,'c_email':cookie_email,'c_pass':cookie_pass})
    else:
            return render(request, 'master_auth.html',{'login_set':login})


def admin_login_handle(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        val = AdminData.objects.filter(admin_email=email,admin_pass=password).count()
        if val==1:
            Data = AdminData.objects.filter(admin_email=email,admin_pass=password)
            for item in Data:
                request.session['admin_id'] = item.admin_id
                request.session['admin_name'] = item.admin_name
                request.session['admin_logged_in'] = 'yes'

            if request.POST.get("remember"):
                response = redirect("Admin Home")
                response.set_cookie('admin_email', email) 
                response.set_cookie('admin_password', password)   
                return response
            
            messages.success(request, 'Logged In Successfully')
            
            return redirect('Admin Home')
        else:
            messages.error(request, "Invalid Username & Password.")
            return redirect('Admin Login')
    else:
        return redirect('Admin Login')



def admin_Forgot_Password(request):  
    login=2
    if request.COOKIES.get("admin_email"):
            cookie_email = request.COOKIES['admin_email']
            return render(request, 'master_auth.html',{'login_set':login,'c_email':cookie_email})
    else:
            return render(request, 'master_auth.html',{'login_set':login})
    
def admin_handle_forgot_password(request):
     if request.method == "POST":
        email2 = request.POST['email']
        val = AdminData.objects.filter(admin_email=email2).count()
        if val!=1:
            messages.error(request, "Email is Wrong")
            url = f"{reverse('Admin_Forgot_Password')}?email={email2}"
            return redirect(url)
     # ------------mail sending ---------------
        sub = 'OTP from EDUPORTAL'
        otp = random.randint(000000,999999)
        mess = 'YOUR OTP IS {}'.format(otp)
        email_from = settings.EMAIL_HOST_USER
        recp_list = [email2,]
        send_mail(sub,mess,email_from,recp_list)
        daata = AdminData.objects.get(admin_email = email2)
        daata.admin_otp = otp
        daata.save()
        messages.success(request, "Otp Sent Successfully")
        url = f"{reverse('Admin_Set_New_Password')}?email={email2}"
        return redirect(url)
     else:
        return redirect('Admin_Forgot_Password')
    
def admin_Set_New_Password(request):  
    login=3      
    if request.GET['email']:
         foremail = request.GET['email']
    return render(request, 'master_auth.html',{'login_set':login,'email':foremail})

def admin_handle_set_new_password(request):
     if request.method == "POST":
        otp = int(request.POST['otp'])
        password = request.POST['password']
        conf_password = request.POST['confirm_password']
        if password == conf_password:
             obj = AdminData.objects.filter(admin_otp = otp).count()
             if obj == 1:
                  data = AdminData.objects.get(admin_otp = otp)
                  data.admin_pass = password
                  data.admin_otp = None
                  data.save()
                  response = redirect("Admin Login")
                  response.set_cookie('admin_password', '')
                  messages.success(request, "Password has been changed Successfully")
                  return response
             else:
                  messages.error(request, "OTP is Wrong")
                  return redirect('Admin Set New Password')
        else:
             messages.error(request, "Password and Confirm Password are not same.")
             return redirect('Admin Set New Password')  
     else:
        messages.error(request, "Method is not Post")
        return redirect('Admin Set New Password')
 
     
def admin_logout(request):
    try:
        del request.session['admin_id']
        del request.session['admin_name']
        del request.session['admin_logged_in']
        messages.success(request, "Logged out Successfully")
        return redirect("Admin Login")
    except:
        pass
    return redirect("Admin Login")     




# -----------------------------------auth End -------------------------
@admin_login_required
def home(request):
    context = {}
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

    # Performance of all standards
    std_data = Std.objects.all()

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
        context.update({'overall_attendance_li':overall_attendance_li})     
    else:
        get_std = 0
        msg = "Please! Select standard for data"
        context.update({'msg':msg})

    context.update({
        'title' : 'Home',
        'all_students':all_students,
        'piechart_category':piechart_category,
        'piechart_data':piechart_data,
        'get_std': get_std,
        'std_list':std_list,
        'students_for_that_std':students_for_that_std,
        'std_data':std_data
    })
    return render(request, 'index.html',context)

@admin_login_required
def show_boards(request):
    data = Boards.objects.all()
    context ={
        'data' : data,
        'title' : 'Boards',

    }
    return render(request, 'show_boards.html',context)

@admin_login_required
def insert_update_boards(request):
    context = {
        'title' : 'Boards',
    }
    if request.GET.get('pk'):
        pk = request.GET['pk']
        instance = get_object_or_404(Boards, pk=pk)
        if request.method == "POST":
            form = brd_form(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('boards')
            else:
                filled_data = form.data
                return render(request, 'insert_update/boards.html', {'errors': form.errors,'filled_data':filled_data})
    
    if request.GET.get('update_id'):
        update_id = request.GET['update_id']
        update_data = Boards.objects.get(brd_id = update_id)
        context2 = {
            'update_data' : update_data

        }
        context.update(context2)
        return render(request, 'insert_update/boards.html',context)

    if request.method == "POST":
        form = brd_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('boards')
        else:
            filled_data = form.data
            print(filled_data)
            return render(request, 'insert_update/boards.html', {'errors': form.errors,'filled_data':filled_data})
    return render(request, 'insert_update/boards.html',context)

@admin_login_required
def delete_boards(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Boards.objects.filter(brd_id__in=selected_ids).delete()
                messages.success(request, '<div class="bg-success text-white p-2 rounded-2 returnmessage mb-2" id="returnmessage"><i class="fa-regular fa-circle-check me-2"></i> Items Deleted Successfully.</div>')
            except Exception as e:
                messages.error(request, f'<div class="bg-danger text-white p-2 rounded-2 returnmessage mb-2" id="returnmessage"><i class="fa-solid fa-triangle-exclamation me-2"></i> An error occurred: {str(e)} </div>')

    return redirect('boards')

# -------------------------Logic for Std-======================

@admin_login_required
def show_stds(request):
    data = Std.objects.all()
    context ={
        'data' : data,
        'title' : 'Stds',
    }
    return render(request, 'show_stds.html',context)

def insert_update_stds(request):
    brddata = Boards.objects.all()
    context = {
        'title' : 'Stds',
        'brddata':brddata,
    }
    if request.GET.get('pk'):
        pk = request.GET['pk']
        instance = get_object_or_404(Std, pk=pk)
        if request.method == "POST":
            form = std_form(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('stds')
            else:
                filled_data = form.data
                return render(request, 'insert_update/stds.html', {'errors': form.errors,'filled_data':filled_data})
    
    if request.GET.get('update_id'):
        update_id = request.GET['update_id']
        update_data = Std.objects.get(std_id = update_id)
        context2 = {
            'update_data' : update_data

        }
        context.update(context2)
        return render(request, 'insert_update/stds.html',context)

    if request.method == "POST":
        form = std_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stds')
        else:
            filled_data = form.data
            print(filled_data)
            return render(request, 'insert_update/stds.html', {'errors': form.errors,'filled_data':filled_data})
    return render(request, 'insert_update/stds.html',context)


def delete_stds(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Std.objects.filter(std_id__in=selected_ids).delete()
                messages.success(request, '<div class="bg-success text-white p-2 rounded-2 returnmessage mb-2" id="returnmessage"><i class="fa-regular fa-circle-check me-2"></i> Items Deleted Successfully.</div>')
            except Exception as e:
                messages.error(request, f'<div class="bg-danger text-white p-2 rounded-2 returnmessage mb-2" id="returnmessage"><i class="fa-solid fa-triangle-exclamation me-2"></i> An error occurred: {str(e)} </div>')

    return redirect('stds')



@admin_login_required
def show_announcements(request):
    data = Announcements.objects.all().order_by('-pk')
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
            data = data.filter(announce_std__std_id = get_std).order_by('-pk')
            batch_data = batch_data.filter(batch_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'batch_data':batch_data,'get_std':get_std})
            

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = data.filter(announce_batch__batch_id = get_batch).order_by('-pk')
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'data':data,'get_batch':get_batch})        
            
    return render(request, 'show_announcements.html',context)



def insert_update_announcements(request):
    std_data = Std.objects.all()
    batch_data = Batches.objects.all()
    # ------------getting students for mail------------------
    students_for_mail = Students.objects.all()

    context = {
        'title' : 'Announcements',
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

                return redirect('admin_announcements')
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
            announcement_mail(form.cleaned_data['announce_title'],form.cleaned_data['announce_msg'],students_email_list)
         
            return redirect('admin_announcements')
        else:
            filled_data = form.data
            context.update({'filled_data ':filled_data,'errors':form.errors})
            return render(request, 'insert_update/announcements.html', context)

    if request.GET.get('pk'):
        update_data = Announcements.objects.get(announce_id = request.GET['pk'])
        context.update({'update_data':update_data})
    return render(request, 'insert_update/announcements.html',context)


def delete_announcements(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Announcements.objects.filter(announce_id__in=selected_ids).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_announcements')







@admin_login_required
def show_subjects(request):
    data = Subject.objects.all().values('sub_id','sub_name','sub_std__std_name','sub_std__std_board__brd_name')
    std_data = Std.objects.all()
   
    context ={
        'data' : data,
        'title' : 'Subjects',
        'std_data' : std_data,
    }
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'get_std':get_std})     
    return render(request, 'show_subjects.html',context)


def insert_update_subjects(request):
    std_data = Std.objects.all()
    
    context = {
        'title' : 'Insert Subjects',
        'std_data':std_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        context.update({'get_std ':get_std,'std_data':std_data}) 


   

 # ================update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Subject, pk=request.GET['pk'])
            form = subject_form(request.POST, instance=instance)
            check = Subject.objects.filter(sub_name = form.data['sub_name'], sub_std__std_id = form.data['sub_std']).count()
            if check >= 1:
                messages.error(request,'{} is already Exists'.format(form.data['sub_name']))
            else:
                if form.is_valid():
                    form.save()
                    return redirect('admin_subjects')
                else:
                    filled_data = form.data
                    context.update({'filled_data ':filled_data,'errors':form.errors})
        
        update_data = Subject.objects.get(sub_id = request.GET['pk'])
        context.update({'update_data':update_data})  
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            form = subject_form(request.POST)
            if form.is_valid():
                check = Subject.objects.filter(sub_name = form.data['sub_name'], sub_std__std_id = form.data['sub_std']).count()
                if check >= 1:
                    messages.error(request,'{} is already Exists'.format(form.data['sub_name']))
                else:    
                    form.save()
                    return redirect('admin_subjects')
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
                return render(request, 'insert_update/subjects.html', context) 
        
    return render(request, 'insert_update/subjects.html',context)                     

def delete_subjects(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Subject.objects.filter(sub_id__in=selected_ids).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_subjects')


@admin_login_required
def show_chepters(request):
    data = Chepter.objects.all().values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name','chep_sub__sub_std__std_id')
    std_data = Std.objects.all()
    subject_data = Subject.objects.all()

    data = paginatoorrr(data, request)
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
            data = Chepter.objects.filter(chep_sub__sub_std__std_id = get_std).values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name','chep_sub__sub_std__std_id')
            data = paginatoorrr(data, request)
            subject_data = subject_data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'get_std':get_std,'std_data':std_data,'subject_data':subject_data}) 


    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        if get_subject == 0:
            pass
        else:    
            data =  Chepter.objects.filter(chep_sub__sub_id = get_subject).values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name','chep_sub__sub_std__std_id')
            data = paginatoorrr(data, request)
            get_subject = Subject.objects.get(sub_id = get_subject)
            context.update({'data':data,'subject_data':subject_data,'get_subject':get_subject}) 


    if request.GET.get('searchhh'):
        searchhh = request.GET['searchhh']
        if searchhh:
            data = Chepter.objects.filter(
            Q(chep_name__icontains=searchhh) |
            Q(chep_sub__sub_name__icontains=searchhh) |
            Q(chep_sub__sub_std__std_name__icontains=searchhh)).values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name','chep_sub__sub_std__std_id')
            data = paginatoorrr(data, request)
            context.update({'data':data,'searchhh':searchhh})      

    return render(request, 'show_chepters.html',context)



def insert_update_chepters(request):
    std_data = Std.objects.all()
    subject_data = Subject.objects.all()
    context = {
        'title' : 'Chepters',
        'std_data':std_data,
        'subject_data':subject_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        context.update({'get_std ':get_std,'std_data':std_data})

    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        subject_data = subject_data.filter(sub_id = get_subject)
        context.update({'get_subject':get_subject,'subject_data':subject_data})     


   

 # ================update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Chepter, pk=request.GET['pk'])
            form = chepter_form(request.POST,request.FILES, instance=instance)
            check = Chepter.objects.filter(chep_name = form.data['chep_name'], chep_std__std_id = form.data['chep_std']).count()
            if check >= 1:
                messages.error(request,'{} is already Exists'.format(form.data['chep_name']))
            else:
                if form.is_valid():
                    form.save()
                    return redirect('admin_chepters')
                else:
                    filled_data = form.data
                    context.update({'filled_data ':filled_data,'errors':form.errors})
        
        update_data = Chepter.objects.get(chep_id = request.GET['pk'])
        context.update({'update_data':update_data})  
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            form = chepter_form(request.POST, request.FILES)
            if form.is_valid():
                check = Chepter.objects.filter(chep_name = form.data['chep_name'], chep_std__std_id = form.data['chep_std']).count()
                if check >= 1:
                    messages.error(request,'{} is already Exists'.format(form.data['chep_name']))
                else:    
                    form.save()
                    return redirect('admin_chepters')
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
                return render(request, 'insert_update/add_chepters.html', context) 
        
    return render(request, 'insert_update/add_chepters.html',context)                

        
        

def delete_chepters(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Chepter.objects.filter(chep_id__in=selected_ids).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_chepters')




@admin_login_required
def show_faculties(request):
    faculties = Faculties.objects.all()
    faculties = paginatoorrr(faculties,request)
    faculty_data = Faculties.objects.all()
    faculty_access_data = Faculty_Access.objects.all()
    context = {
        'faculty_data':faculty_data,
        'faculty_access_data':faculty_access_data,
        'title': 'Faculties'
    }

    return render(request, 'show_faculties.html', context)

@admin_login_required
def view_faculty_access(request):
    if request.GET.get('fac_id'):
        fac_id = request.GET.get('fac_id')
        faculty_data = Faculties.objects.get(fac_id = fac_id)
        faculty_access_data = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)
        context = {
            'faculty_data':faculty_data,
            'faculty_access_data':faculty_access_data,
            'title': 'Access'
        }
        return render(request, 'view_faculty_access.html', context)

@admin_login_required
def delete_faculty_access(request):
    if request.GET.get('fac_access_id'):
        fac_access_id = request.GET.get('fac_access_id')

        faculty_access_del = get_object_or_404(Faculty_Access, fa_id=fac_access_id)
        faculty_access_del.delete()
        messages.success(request, "Access deleted successfully")
        url = '/adminside/view_faculty_access/?fac_id={}'.format(request.GET['fac_id']) 
        return redirect(url)


@admin_login_required
def insert_update_faculties(request):
    context = {
        'title': 'Faculties',
    }

    # Update Logic
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Faculties, pk=request.GET['pk'])
            form = faculty_form(request.POST, instance=instance)
            check = Faculties.objects.filter(fac_email=form.data['fac_email']).exclude(pk=request.GET['pk']).count()
            if check >= 1:
                messages.error(request, '{} is already Exists'.format(form.data['fac_email']))
            else:
                if form.is_valid():
                    form.save()
                    return redirect('admin_faculties')
                else:
                    filled_data = form.data
                    context.update({'filled_data': filled_data, 'errors': form.errors})

        update_data = Faculties.objects.get(fac_id=request.GET['pk'])
        context.update({'update_data': update_data})
    else:
        # Insert Logic
        if request.method == 'POST':
            form = faculty_form(request.POST)
            if form.is_valid():
                check = Faculties.objects.filter(fac_email=form.data['fac_email']).count()
                if check >= 1:
                    messages.error(request, '{} is already Exists'.format(form.data['fac_email']))
                else:
                    form.save()
                    return redirect('admin_faculties')
            else:
                filled_data = form.data
                context.update({'filled_data': filled_data, 'errors': form.errors})

    return render(request, 'insert_update/faculties.html', context)



@admin_login_required
def delete_faculties(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Faculties.objects.filter(fac_id__in=selected_ids).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_faculties')

@admin_login_required
def show_timetable(request):
    data = Timetable.objects.all()
    std_data = Std.objects.all()
    batch_data = Batches.objects.all()
   
    context = {
        'data': data,
        'title': 'Timetable',
        'std_data': std_data,
        'batch_data': batch_data,
    }
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std != 0:  
            data = data.filter(tt_batch__batch_std__std_id=get_std)
            batch_data = batch_data.filter(batch_std__std_id=get_std)
            get_std = Std.objects.get(std_id=get_std)
            context.update({'data': data, 'batch_data': batch_data, 'get_std': get_std})

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch != 0:
            data = data.filter(tt_batch__batch_id=get_batch)
            get_batch = Batches.objects.get(batch_id=get_batch)
            context.update({'data': data, 'get_batch': get_batch})        
            
    return render(request, 'show_timetable.html', context)

def insert_update_timetable(request):
    std_data = Std.objects.all()
    batch_data = Batches.objects.all()
    faculty_data = Faculties.objects.all()
    subject_data = Subject.objects.all()
    tt_students_for_mail = Students.objects.all()

    context = {
        'title': 'Timetable',
        'std_data': std_data,
        'batch_data': batch_data,
        'subject_data':subject_data,
        'faculty_data':faculty_data,
        'DaysChoice': Timetable.DaysChoice,
    }

    print(Timetable.DaysChoice)

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id=get_std)
        subject_data = Subject.objects.filter(sub_std__std_id = get_std)
        batch_data = batch_data.filter(batch_std__std_id=get_std)
        tt_students_for_mail = tt_students_for_mail.filter(stud_std=get_std)
        context.update({'get_std': get_std, 'std_data': std_data, 'batch_data': batch_data, 'subject_data':subject_data}) 

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        batch_data = batch_data.filter(batch_id=get_batch)
        tt_students_for_mail = tt_students_for_mail.filter(stud_batch=get_batch)
        context.update({'get_batch': get_batch, 'batch_data': batch_data})

    if request.method == 'POST':
        # Update logic
        if request.GET.get('pk'):
            instance = get_object_or_404(Timetable, pk=request.GET['pk'])
            form = timetable_form(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('admin_timetable')
            else:
                filled_data = form.data
                context.update({'filled_data': filled_data, 'errors': form.errors})

        # Insert logic
        form = timetable_form(request.POST)
        if form.is_valid():
            form.save()
            # ---------------------sendmail Logic===================================
            tt_students_email_list = []
            for x in tt_students_for_mail:
                tt_students_email_list.append(x.stud_email)
            print(tt_students_email_list)    
            timetable_mail(tt_students_email_list)
            return redirect('admin_timetable')
    
        else:
            filled_data = form.data
            context.update({'filled_data': filled_data, 'errors': form.errors})
            return render(request, 'insert_update/timetable.html', context)

    if request.GET.get('pk'):
        update_data = Timetable.objects.get(tt_id=request.GET['pk'])
        context.update({'update_data': update_data})
    return render(request, 'insert_update/timetable.html', context)



def delete_timetable(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Timetable.objects.filter(tt_id__in=selected_ids).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_timetable')

@admin_login_required
def show_attendance(request):
    data = Attendance.objects.all().values('atten_id','atten_timetable__tt_day','atten_timetable__tt_time1','atten_date','atten_timetable__tt_subject1','atten_timetable__tt_tutor1__fac_name','atten_present','atten_student__stud_name','atten_student__stud_lastname')
    std_data = Std.objects.all()
    batch_data = Batches.objects.all()
    stud_data = Students.objects.all()
    subj_data = Subject.objects.all()
    
    data = paginatoorrr(data, request)
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
            data = Attendance.objects.filter(atten_timetable__tt_batch__batch_std__std_id = get_std).values('atten_id','atten_timetable__tt_day','atten_timetable__tt_time1','atten_date','atten_timetable__tt_subject1','atten_timetable__tt_tutor1__fac_name','atten_present','atten_student__stud_name','atten_student__stud_lastname')
            data = paginatoorrr(data, request)
            batch_data = batch_data.filter(batch_std__std_id = get_std)
            stud_data = stud_data.filter(stud_std__std_id = get_std)
            subj_data = subj_data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'batch_data':batch_data,'get_std':get_std,'stud_data':stud_data,'sub_data':subj_data})
            

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = Attendance.objects.filter(atten_timetable__tt_batch__batch_id = get_batch).values('atten_id','atten_timetable__tt_day','atten_timetable__tt_time1','atten_date','atten_timetable__tt_subject1','atten_timetable__tt_tutor1__fac_name','atten_present','atten_student__stud_name','atten_student__stud_lastname')
            data = paginatoorrr(data, request)
            stud_data = stud_data.filter(stud_batch__batch_id = get_batch)
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'data':data,'get_batch':get_batch,'stud_data':stud_data}) 

    if request.GET.get('get_student'):
        get_student = int(request.GET['get_student'])
        if get_student == 0:
            pass
        else:
            data = Attendance.objects.filter(atten_student__stud_id = get_student).values('atten_id','atten_timetable__tt_day','atten_timetable__tt_time1','atten_date','atten_timetable__tt_subject1','atten_timetable__tt_tutor1__fac_name','atten_present','atten_student__stud_name','atten_student__stud_lastname')
            data = paginatoorrr(data, request)
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
            sub_attendance = round((sub_one/sub_all) * 100, 2)
            subject_wise_attendance.append(sub_attendance)
            subjects.append(sub_name)
            
    combined_data = zip(subject_wise_attendance, subjects)

    context.update({'combined_data': combined_data})
    return render(request, 'show_attendance.html',context)


@admin_login_required
def show_events(request):
    events = Event.objects.all().values('event_id', 'event_name')
    events_imgs = Event_Image.objects.all()
    selected_events = Event.objects.first()
    context = {
        'events':events,
        'events_imgs':events_imgs,
        'selected_events':selected_events,
        'title' : 'Events',
    }
    if request.GET.get('event_id'):
        event_id = request.GET['event_id']
        selected_events = Event.objects.get(event_id = event_id)
        events_imgs = Event_Image.objects.filter(event__event_id = event_id)
        context.update({'selected_events':selected_events,'events_imgs':events_imgs})
    return render(request, 'show_events.html',context)

@admin_login_required
def insert_events(request):
    title = 'Insert Events'
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        event_desc = request.POST.get('event_desc')
        event_images = request.FILES.getlist('event_img')
        print(event_images)
        event = Event(event_name=event_name, event_date=event_date, event_desc=event_desc)
        event.save()
        
        fs = FileSystemStorage(location='media/uploads/events/')
        for image in event_images:
            filename = fs.save(image.name, image)
            Event_Image.objects.create(event=event, event_img=filename)
        return redirect('show_events')
    return render(request, 'insert_update/events_insert_admin.html', {'title':title})

def delete_event(request):
    if request.GET.get('event_id'):
        event_id = request.GET.get('event_id')
        event_data_del = get_object_or_404(Event, event_id=event_id)
        event_data_del.delete()
        messages.success(request, "Event deleted successfully")
        return redirect('show_events')

@admin_login_required
def show_tests(request):
    data = Chepterwise_test.objects.annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage')).values('test_sub__sub_name','num_questions','total_marks','test_std__std_name','test_std__std_board__brd_name','test_name','test_id')
    std_data = Std.objects.all()
    subject_data = Subject.objects.all()
    data = paginatoorrr(data, request)
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
            data = Chepterwise_test.objects.filter(test_sub__sub_std__std_id = get_std).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage')).values('test_sub__sub_name','num_questions','total_marks','test_std__std_name','test_std__std_board__brd_name','test_name','test_id')
            data = paginatoorrr(data, request)
            subject_data = subject_data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'get_std':get_std,'std_data':std_data,'subject_data':subject_data}) 


    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        if get_subject == 0:
            pass
        else:    
            data = Chepterwise_test.objects.filter(test_sub__sub_id = get_subject).annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage')).values('test_sub__sub_name','num_questions','total_marks','test_std__std_name','test_std__std_board__brd_name','test_name','test_id')
            data = paginatoorrr(data, request)
            get_subject = Subject.objects.get(sub_id = get_subject)
            context.update({'data':data,'subject_data':subject_data,'get_subject':get_subject}) 

    return render(request, 'show_tests.html',context)


def insert_update_tests(request):
    std_data = Std.objects.all()
    subject_data = Subject.objects.all()
    chap_data = Chepter.objects.all().values('chep_name','chep_id','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name')
    context = {
        'title': 'Tests',
        'std_data': std_data,
        'subject_data': subject_data,
        'chap_data': chap_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id=get_std)
        subject_data = subject_data.filter(sub_std__std_id=get_std)
        chap_data = Chepter.objects.filter(chep_std__std_id = get_std).values('chep_name','chep_id','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name')
        context.update({'get_std': get_std, 'std_data': std_data,'subject_data':subject_data,'chap_data':chap_data})

    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        subject_data = subject_data.filter(sub_id=get_subject)
        chap_data = Chepter.objects.filter(chep_sub__sub_id = get_subject).values('chep_name','chep_id','chep_sub__sub_name','chep_sub__sub_std__std_name','chep_sub__sub_std__std_board__brd_name')

        context.update({'get_subject': get_subject, 'subject_data': subject_data,'chap_data':chap_data})

    # Update Logic
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Chepterwise_test, pk=request.GET['pk'])
            form = tests_form(request.POST, instance=instance)
            check = Chepterwise_test.objects.filter(
                test_name=form.data['test_name'], test_std__std_id=form.data['test_std']
            ).count()
            if check >= 1:
                messages.error(request, '{} already exists'.format(form.data['test_name']))
            else:
                if form.is_valid():
                    form.save()
                    return redirect('admin_tests')
                else:
                    filled_data = form.data
                    context.update({'filled_data': filled_data, 'errors': form.errors})
        
        update_data = Chepterwise_test.objects.get(test_id=request.GET['pk'])
        context.update({'update_data': update_data})

    else:
        # Insert Logic
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
                        two_mark_count = int(request.POST.get('two_mark_questions', 0))
                        three_mark_count = int(request.POST.get('three_mark_questions', 0))
                        four_mark_count = int(request.POST.get('four_mark_questions', 0))
                        chap_object = Chepter.objects.get(chep_id = request.POST.get('test_chap'))

                        # Function to get questions by weightage
                        def get_questions_by_weightage(weightage, count):
                            return question_bank.objects.filter(
                                qb_chepter=chap_object,
                                qb_weightage=weightage
                            ).order_by('?')[:count]

                        # Retrieve questions based on weightage
                        one_mark_questions = get_questions_by_weightage(1, one_mark_count)
                        two_mark_questions = get_questions_by_weightage(2, two_mark_count)
                        three_mark_questions = get_questions_by_weightage(3, three_mark_count)
                        four_mark_questions = get_questions_by_weightage(4, four_mark_count)

                        # Insert the generated questions into Test_questions_answer
                        for question in one_mark_questions:
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

                    return redirect('admin_tests')
            else:
                filled_data = form.data
                context.update({'filled_data': filled_data, 'errors': form.errors})
                return render(request, 'insert_update/add_tests.html', context)
    return render(request, 'insert_update/add_tests.html', context)



@admin_login_required
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

    return redirect('admin_tests')

@admin_login_required
def show_test_questions_admin(request):
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
            'title' : 'Tests',
        }
        return render(request, 'show_test_questions_admin.html',context)
    else:
        return redirect('admin_tests') 

@admin_login_required
def insert_update_test_questions(request):
    chep_data = Chepter.objects.all()
    context = {
        'chep_data': chep_data,
        'que_type': Test_questions_answer.que_type,
        'title' : 'Tests',
    }

    if request.GET.get('test_id'):
        test_id = request.GET['test_id']
        test_data = Chepterwise_test.objects.get(test_id = request.GET['test_id'])
        chep_data = chep_data.filter(chep_sub__sub_id = test_data.test_sub.sub_id)
        context.update({'test_id': test_id,'chep_data': chep_data})

    if request.method == 'POST':
        form = TestQuestionsAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            testt_id = form.cleaned_data['tq_name']
            chep_id = form.cleaned_data['tq_chepter']
            testt_id = testt_id.test_id
            chep_id = chep_id.chep_id
            form.save()
            url = '/adminside/insert_update_test_question_admin/?test_id={}&chep_id={}'.format(testt_id,chep_id)
            return redirect(url) 
        else:
            context.update({'form': form,'errors':form.errors})
            return render(request, 'insert_update/add_test_questions.html', context)
    else:
        form = TestQuestionsAnswerForm()
        context.update({'form': form})
        return render(request, 'insert_update/add_test_questions.html', context)


# ============================================packages logic====================================
@admin_login_required
def show_packages(request):
    data = Packs.objects.prefetch_related('pack_subjects').all()
    std_data = Std.objects.all()
    print(data)
    data = paginatoorrr(data, request)

    context ={
        'data' : data,
        'title' : 'Packages',
        'std_data' : std_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = Packs.objects.prefetch_related('pack_subjects').filter(pack_std__std_id = get_std)
            data = paginatoorrr(data, request)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'get_std':get_std})     
    return render(request, 'show_packages.html',context)




def insert_update_packages(request):
    std_data = Std.objects.all()
    subjects_data = Subject.objects.all()

    context = {
        'title' : 'Packages',
        'std_data':std_data,
        'subjects_data':subjects_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        subjects_data = subjects_data.filter(sub_std__std_id = get_std)
        context.update({'get_std ':get_std,'std_data':std_data, 'subjects_data':subjects_data}) 


   

 # ================update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Packs, pk=request.GET['pk'])
            form = pack_form(request.POST, instance=instance)
            check = Packs.objects.filter(pack_name = form.data['pack_name'], pack_std__std_id = form.data['pack_std']).count()
            if check >= 1:
                messages.error(request,'{} is already Exists'.format(form.data['pack_name']))
            else:
                if form.is_valid():
                    form.save()
                    return redirect('admin_packages')
                else:
                    filled_data = form.data
                    context.update({'filled_data ':filled_data,'errors':form.errors})
        
        update_data = Packs.objects.get(pack_id = request.GET['pk'])
        context.update({'update_data':update_data})  
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            form = pack_form(request.POST)
            if form.is_valid():
                check = Packs.objects.filter(pack_name = form.data['pack_name'], pack_std__std_id = form.data['pack_std']).count()
                if check >= 1:
                    messages.error(request,'{} is already Exists'.format(form.data['pack_name']))
                else:    
                    form.save()
                    return redirect('admin_packages')
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
                return render(request, 'insert_update/packages.html', context) 
        
    return render(request, 'insert_update/package.html',context)



@admin_login_required
def delete_admin_package(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Packs.objects.filter(batch_id__in=selected_ids).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_packages')

@admin_login_required
@require_GET  # Ensure that only GET requests are allowed
def show_students(request):
    context = {'title': 'Students'}
    std_data = Std.objects.all()
    get_std_id = request.GET.get('get_std')
    get_batch_id = request.GET.get('get_batch')

    if get_std_id and get_batch_id:
        data = Students.objects.filter(stud_batch__batch_id=get_batch_id).values(
            'stud_id', 'stud_name', 'stud_lastname', 'stud_username', 'stud_contact', 
            'stud_email', 'stud_dob', 'stud_std__std_name', 'stud_std__std_board__brd_name', 
            'stud_batch__batch_name', 'stud_std__std_id', 'stud_batch__batch_id', 
            'stud_pack__pack_name', 'stud_guardian_email', 'stud_guardian_name', 
            'stud_guardian_number', 'stud_address', 'stud_guardian_profession', 'stud_gender'
        )

        batch_data = Batches.objects.filter(batch_std__std_id=get_std_id)
        get_batch = Batches.objects.get(batch_id=get_batch_id)
        get_std = Std.objects.get(std_id=get_std_id)

        data = paginatoorrr(data,request)
        context.update({
            'data': data,
            'std_data': std_data,
            'batch_data': batch_data,
            'get_batch': get_batch,
            'get_std': get_std,
        })

    elif get_std_id:
        data = Students.objects.filter(stud_std__std_id=get_std_id).values(
            'stud_id', 'stud_name', 'stud_lastname', 'stud_username', 'stud_contact', 
            'stud_email', 'stud_dob', 'stud_std__std_name', 'stud_std__std_board__brd_name', 
            'stud_batch__batch_name', 'stud_std__std_id', 'stud_batch__batch_id', 
            'stud_pack__pack_name', 'stud_guardian_email', 'stud_guardian_name', 
            'stud_guardian_number', 'stud_address', 'stud_guardian_profession', 'stud_gender'
        )

        batch_data = Batches.objects.filter(batch_std__std_id=get_std_id)
        get_std = Std.objects.get(std_id=get_std_id)

        data = paginatoorrr(data,request)
        context.update({
            'data': data,
            'std_data': std_data,
            'batch_data': batch_data,
            'get_std': get_std,
        })

    else:
        data = Students.objects.values(
            'stud_id', 'stud_name', 'stud_lastname', 'stud_username', 'stud_contact', 
            'stud_email', 'stud_dob', 'stud_std__std_name', 'stud_std__std_board__brd_name', 
            'stud_batch__batch_name', 'stud_std__std_id', 'stud_batch__batch_id', 
            'stud_pack__pack_name', 'stud_guardian_email', 'stud_guardian_name', 
            'stud_guardian_number', 'stud_address', 'stud_guardian_profession', 'stud_gender'
        )
        
        batch_data = Batches.objects.all()
        data = paginatoorrr(data,request)
        
        context.update({
            'data': data,
            'std_data': std_data,
            'batch_data': batch_data,
        })

    return render(request, 'show_students.html', context)



def insert_update_students(request):
    std_data = Std.objects.all()
    batch_data = Batches.objects.all()
    pack_data = Packs.objects.all()

    context = {
        'title' : 'Students',
        'std_data':std_data,
        'batch_data':batch_data,
        'pack_data':pack_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        batch_data = batch_data.filter(batch_std__std_id = get_std)
        pack_data = pack_data.filter(pack_std__std_id = get_std)
        context.update({'get_std ':get_std,'std_data':std_data,'batch_data':batch_data,'pack_data':pack_data}) 


    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        batch_data = batch_data.filter(batch_id = get_batch)
        context.update({'get_batch ':get_batch,'batch_data':batch_data})

    if request.method == 'POST':

        # ================update Logic============================
        if request.GET.get('pk'):
            instance = get_object_or_404(Students, pk=request.GET['pk'])
            form = student_form(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Insert student successfully')
                return redirect('students_dataAdmin')
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})

        # ===================insert_logic===========================
        form = student_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students_dataAdmin')
        else:
            filled_data = form.data
            context.update({'filled_data ':filled_data,'errors':form.errors})
            return render(request, 'insert_update/add_student.html', context)

    if request.GET.get('pk'):
        update_data = Students.objects.get(stud_id = request.GET['pk'])
        context.update({'update_data':update_data})
    
    if request.GET.get('inq_id'):
        inq_id = request.GET.get('inq_id')
        inquires_admission_data = Inquiries.objects.get(inq_id=inq_id)
        context.update({'inquires_admission_data':inquires_admission_data})
    return render(request, 'insert_update/add_student.html',context)


def delete_students(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Students.objects.filter(stud_id__in=selected_ids).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('students_dataAdmin')





@admin_login_required
def show_inquiries(request):
    title = "Inquiries"
    inquiries_data = Inquiries.objects.all()

    context = {
        "title":title,
        "inquiries_data":inquiries_data
    }
    return render(request, 'show_inquiries.html', context)


# ------------------------------------------batches data-----------------------------------------

@admin_login_required
def show_batches(request):
    data = Batches.objects.all()
    std_data = Std.objects.all()
    data = paginatoorrr(data, request)
    context ={
        'data' : data,
        'title' : 'Batches',
        'std_data' : std_data,
    }
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = Batches.objects.filter(batch_std__std_id = get_std)
            data = paginatoorrr(data, request)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'get_std':get_std})     
    return render(request, 'show_batches.html',context)


@admin_login_required
def insert_update_batches(request):
    std_data = Std.objects.all()
    
    context = {
        'title' : 'Batches',
        'std_data':std_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        context.update({'get_std ':get_std,'std_data':std_data}) 


   

 # ================update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Batches, pk=request.GET['pk'])
            form = batch_form(request.POST, instance=instance)
            check = Batches.objects.filter(batch_name = form.data['batch_name'], batch_std__std_id = form.data['batch_std']).count()
            if check >= 1:
                messages.error(request,'{} is already Exists'.format(form.data['batch_name']))
            else:
                if form.is_valid():
                    form.save()
                    return redirect('admin_batches')
                else:
                    filled_data = form.data
                    context.update({'filled_data ':filled_data,'errors':form.errors})
        
        update_data = Batches.objects.get(batch_id = request.GET['pk'])
        context.update({'update_data':update_data})  
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            form = batch_form(request.POST)
            if form.is_valid():
                check = Batches.objects.filter(batch_name = form.data['batch_name'], batch_std__std_id = form.data['batch_std']).count()
                if check >= 1:
                    messages.error(request,'{} is already Exists'.format(form.data['batch_name']))
                else:    
                    form.save()
                    return redirect('admin_batches')
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
                return render(request, 'insert_update/batches.html', context) 
        
    return render(request, 'insert_update/batches.html',context)                     



@admin_login_required
def delete_admin_batches(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Batches.objects.filter(batch_id__in=selected_ids).delete()
                messages.success(request, 'Items Deleted Successfully')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    return redirect('admin_batches')




def show_admin_materials(request):
    standard_data = Std.objects.all()
    subjects_data = Subject.objects.all()
    materials = Chepterwise_material.objects.all().values('cm_id','cm_filename','cm_chepter__chep_sub__sub_id','cm_file','cm_file_icon','cm_chepter__chep_sub__sub_std__std_id')
    selected_sub=None

    context = {'standard_data':standard_data, 'subjects_data':subjects_data, 'materials':materials, 'title' : 'Materials',}
    if request.GET.get('std_id'):
        std_id = int(request.GET.get('std_id'))
        subjects_data = Subject.objects.filter(sub_std__std_id = std_id)
        materials = [material for material in materials if material['cm_chepter__chep_sub__sub_std__std_id'] == std_id]
        selected_std = Std.objects.get(std_id=std_id)
        context.update({'materials': materials,'subjects_data': subjects_data, 'std':std_id,'selected_std':selected_std})

    if request.GET.get('sub_id'):
        sub_id = request.GET.get('sub_id')
        materials = Chepterwise_material.objects.filter(cm_chepter__chep_sub__sub_id = sub_id)
        selected_sub = Subject.objects.get(sub_id=sub_id)
        context.update({'materials': materials, 'selected_sub':selected_sub})

    return render(request, 'show_materials.html', context)



def show_admin_profile(request):
    admin_data = AdminData.objects.all()
    context = {
        'admin_data':admin_data,
        'title' : 'Profile',
    }
    return render(request, 'show_profile.html', context)


def Student_doubts_adminside(request):

    Total_doubts = Doubt_section.objects.count()
    Total_solutions = Doubt_solution.objects.count()

    unverified_doubts_count = Doubt_section.objects.annotate(
    verified_solution_count=Count('doubt_solution', filter=Q(doubt_solution__solution_verified=True))
    ).filter(verified_solution_count = 0).count()

    verified_doubts_count = Doubt_solution.objects.filter(solution_verified=1).count()

    doubts_zero_solution = Doubt_section.objects.annotate(
        zero_solution_count = Count('doubt_solution')
    ).filter(zero_solution_count=0).count()

    context = {
        'title' : 'Doubts',
        'Total_doubts':Total_doubts,
        'Total_solutions':Total_solutions,
        'unverified_doubts_count':unverified_doubts_count,
        'verified_doubts_count':verified_doubts_count,
        'doubts_zero_solution':doubts_zero_solution,
    }
    return render(request, 'show_doubts_admin.html', context)


def adminside_report_card(request):
    data = Attendance.objects.all()
    std_data = Std.objects.all()
    batch_data = Batches.objects.all()
    stud_data = Students.objects.all()
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
        students_li = Students.objects.filter(stud_std__std_id = student_std)
        overall_attendance_li = []
        for x in students_li:
            total_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x.stud_id).count()
            present_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x.stud_id, atten_present=True).count()
            # print("==============================================",total_attendence_studentwise)
            if total_attendence_studentwise > 0:
                overall_attendence_studentwise = (present_attendence_studentwise/total_attendence_studentwise)*100
            else:
                overall_attendence_studentwise = 0
            

            total_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x.stud_id).aggregate(total_sum_marks=Sum('tau_total_marks'))['total_sum_marks'] or 0
            
            
            obtained_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x.stud_id).aggregate(total_obtained_marks=Sum('tau_obtained_marks'))['total_obtained_marks'] or 0
            

            if total_marks == 0:
                overall_result = 0
            else:
                overall_result = round((obtained_marks/total_marks)*100,2)
            if student_id == x.stud_id: 
                current_student_overall_test_result = overall_result
                context.update({'current_student_overall_test_result':current_student_overall_test_result})

            overall_attendance_li.append({'stud_name':x.stud_name, 'overall_attendance_studentwise':overall_attendence_studentwise, 'overall_result':overall_result})
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
        nobody = 0
        context.update({'nobody':nobody, 'noreport_card':noreport_card})
    return render(request, 'show_report_card_admin.html', context)



def fees_collection_admin(request):
    cheque_collections_data = Cheque_Collection.objects.filter(cheque_paid=False)
    std_data = Std.objects.all()
    Context = {'std_data':std_data}
             
    students_data = Students.objects.annotate(
    amount_paid=Coalesce(Sum('fees_collection__fees_paid'), Value(0)),
    discountt=Case(
        When(discount__discount_amount=None, then=Value(0)),
        default=F('discount__discount_amount'),output_field=IntegerField()
    )).values('stud_id','amount_paid','discountt','stud_std__std_name','stud_std__std_board__brd_name','stud_name','stud_lastname','stud_pack__pack_fees')

    students_data = paginatoorrr(students_data, request)
    # -------------filter--------------------------------------------
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            students_data = Students.objects.filter(stud_std__std_id = get_std).annotate(
            amount_paid=Coalesce(Sum('fees_collection__fees_paid'), Value(0)),
            discountt=Case(
                When(discount__discount_amount=None, then=Value(0)),
                default=F('discount__discount_amount'),output_field=IntegerField()
            )).values('stud_id','amount_paid','discountt','stud_std__std_name','stud_std__std_board__brd_name','stud_name','stud_lastname','stud_pack__pack_fees')
            students_data = paginatoorrr(students_data, request)
            get_std = Std.objects.get(std_id = get_std)
            Context.update({'get_std':get_std,'students_data':students_data}) 
    # ------------------end filter-------------------------------------

    #=================Total Amount Fees Paid============================================
    total_amount_fees_paid = Fees_Collection.objects.all().aggregate(total_amu_paid = Sum('fees_paid'))
    
    if total_amount_fees_paid['total_amu_paid'] != None:
        total_amount_fees_paid = total_amount_fees_paid['total_amu_paid']
    else:
        total_amount_fees_paid = 0

    #==================Total Fees Amount After Discount=================================
    total_discount_amount = Discount.objects.all().aggregate(discount_amount=Sum('discount_amount'))
    if total_discount_amount['discount_amount'] != None:
        total_discount_amount = total_discount_amount['discount_amount']
    else:
        total_discount_amount = 0

    total_fees_amount = Students.objects.all().aggregate(fees_amount=Sum('stud_pack__pack_fees'))
    if total_fees_amount['fees_amount'] != None:
        total_fees_amount = total_fees_amount['fees_amount']
    else:
        total_fees_amount = 0

    total_fees_amount_after_discount = (total_fees_amount-total_discount_amount)
    
    #===================Total Pending Fees==============================================
    total_pending_fees = total_fees_amount_after_discount - total_amount_fees_paid
    

    Context.update({
        'title':'Payments',
        'std_data':std_data,
        'cheque_collections_data':cheque_collections_data,
        'total_amount_fees_paid':total_amount_fees_paid,
        'total_fees_amount_after_discount':total_fees_amount_after_discount,
        'total_pending_fees':total_pending_fees,
        'students_data':students_data,
   
    })
    return render(request, 'fees_collection_admin.html', Context)

def add_cheques_admin(request):
    students = Students.objects.all()
    banks = Banks.objects.all()

    context={
        'title' : 'Add Cheques',
        'students':students,
        'banks':banks,    
             }   

 # ================update Logic==================================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Cheque_Collection, pk=request.GET['pk'])
            form = Cheque_Collection_form(request.POST, instance=instance)
            if form.is_valid():
                
                if form.cleaned_data['cheque_paid']==True:
                    studid = form.cleaned_data['cheque_stud_id']
                    cheque_amt = form.cleaned_data['cheque_amount']
                    cheque_amt = form.cleaned_data['cheque_amount']
                    fees_mode = 'CHECK'
                    cheque_date = form.cleaned_data['cheque_date']
                    abcd = Fees_Collection.objects.create(fees_stud_id = studid,fees_paid=cheque_amt,fees_mode=fees_mode,fees_date=cheque_date)
                    print(abcd)
                    

                form.save()
                return redirect('fees_collection_admin')
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
        
        update_data = Cheque_Collection.objects.get(cheque_id = request.GET['pk'])
        context.update({'update_data':update_data})  
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            form = Cheque_Collection_form(request.POST)
            if form.is_valid():
                check = Cheque_Collection.objects.filter(cheque_number = form.data['cheque_number']).count()
                if check >= 1:
                    messages.error(request,'{} is already Exists'.format(form.data['cheque_number']))
                else:    
                    form.save()
                    return redirect('fees_collection_admin')
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
                return render(request, 'insert_update/add_cheques_admin.html', context)          
            
    return render(request, 'insert_update/add_cheques_admin.html', context)


def delete_cheques_admin(request):
    if request.GET.get('delete_cheque'):
        del_id = request.GET['delete_cheque']
        print(del_id)
        try:
            check_data = Cheque_Collection.objects.get(cheque_id=del_id)
            check_data.delete()
        except Cheque_Collection.DoesNotExist:
            raise Http404("Cheque not found")
    return redirect('fees_collection_admin') 


def add_fees_collection_admin(request):
    students = Students.objects.all()
    context={
        'title' : 'Add Fees',
        'students':students,    
    }
    # ================update Logic==================================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Fees_Collection, pk=request.GET['pk'])
            form = fees_collection_form(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('fees_collection_admin')
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
        
        update_data = Fees_Collection.objects.get(fees_id = request.GET['pk'])
        context.update({'update_data':update_data})  
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            form = fees_collection_form(request.POST)
            if form.is_valid():   
                form.save()
                return redirect('fees_collection_admin')
            else:
                filled_data = form.data
                context.update({'filled_data ':filled_data,'errors':form.errors})
                return render(request, 'insert_update/add_fees_collection_admin.html', context)
    return render(request, 'insert_update/add_fees_collection_admin.html', context)

def admin_fees_collection_delete(request):
    if request.GET.get('delete_payment'):
        del_id = request.GET['delete_payment']
        print(del_id)
        try:
            fees_data = Fees_Collection.objects.get(fees_id=del_id)
            fees_data.delete()
        except Fees_Collection.DoesNotExist:
            messages.error(request, 'Error in Deleting Data') 
            raise Http404("Cheque not found")
              
    return redirect('fees_collection_admin') 

def payments_history_admin(request):
    fees_collections_data = Fees_Collection.objects.all()
    context = {
        'fees_collections_data':fees_collections_data,
    }
    return render(request, 'payments_history_admin.html', context)

def faculty_access_show(request):
    standard_data = Std.objects.all()
    batch_data = Batches.objects.all()
    subject_data = Subject.objects.all()
    teachers_names = Faculties.objects.all()
    context = {
        'standard_data':standard_data,
        'batch_data':batch_data,
        'subject_data':subject_data,
        'teachers_names':teachers_names,
        'title': 'Faculty-Access',
    }
    if request.GET.get('get_std'):
        get_std = request.GET.get('get_std')
        batch_data = Batches.objects.filter(batch_std__std_id = get_std)
        subject_data = Subject.objects.filter(sub_std__std_id = get_std)
        selected_standard = Std.objects.get(std_id = get_std)
        context.update({'batch_data':batch_data, 'subject_data':subject_data, 'selected_standard':selected_standard})



    selected_subjects = request.POST.getlist('fa_subject')
    
    if request.method == 'POST':
        form = faculty_access_form(request.POST)
        if form.is_valid():
            fac = form.cleaned_data['fa_faculty']
            batch = form.cleaned_data['fa_batch']
            for x in selected_subjects:
                x_obj = Subject.objects.get(sub_id=x)
                Faculty_Access.objects.create(fa_faculty=fac, fa_batch=batch, fa_subject=x_obj)
            messages.success(request, "Access given successfully")
            return redirect('faculty_access')
    else:
        form = faculty_access_form()
        context.update({'form':form})
    return render(request, 'faculty_access.html', context)



def export_data(request):
    model_name = request.GET.get('model_name')
    Context={'title':model_name}
    get_std = request.GET.get('get_std')
    get_batch = request.GET.get('get_batch')
    get_subject = request.GET.get('get_subject')

    if model_name == 'Students':
        student_data = []
        if get_std:
            data = Students.objects.filter(stud_std__std_id=get_std)
        elif get_batch:
            data = Students.objects.filter(stud_batch__batch_id=get_batch)
        else:
            data = Students.objects.all()

        field_names = ['student Name','student_lastname','contact','Email','DOB','gender','admission_no','roll_no','enrollment_no','Guardian Name','Guardian Email','Guardian Number','Address','Std','Batch','Package']
        for x in data:
            temp_data = {}
            temp_data.update({'student_Name':x.stud_name,'student_lastname':x.stud_lastname,'contact':x.stud_contact,'Email':x.stud_contact,'DOB':x.stud_dob,'gender':x.stud_gender,'admission_no':x.stud_admission_no,'roll_no':x.stud_roll_no,'enrollment_no':x.stud_enrollment_no,'Guardian_Name':x.stud_guardian_name,'Guardian_Email':x.stud_guardian_email,'Guardian_Number':x.stud_guardian_number,'Address':x.stud_address,'Std': x.stud_std.std_name + x.stud_std.std_board.brd_name,'Batch':x.stud_batch.batch_name,'Package':x.stud_pack.pack_name})
            student_data.append(temp_data)
        Context.update({'data':student_data,'field_names':field_names})



    if model_name == 'Students':
        student_data = []
        if get_std:
            data = Students.objects.filter(stud_std__std_id=get_std)
        elif get_batch:
            data = Students.objects.filter(stud_batch__batch_id=get_batch)
        else:
            data = Students.objects.all()

        field_names = ['student Name','student_lastname','contact','Email','DOB','gender','admission_no','roll_no','enrollment_no','Guardian Name','Guardian Email','Guardian Number','Address','Std','Batch','Package']
        for x in data:
            temp_data = {}
            temp_data.update({'student_Name':x.stud_name,'student_lastname':x.stud_lastname,'contact':x.stud_contact,'Email':x.stud_contact,'DOB':x.stud_dob,'gender':x.stud_gender,'admission_no':x.stud_admission_no,'roll_no':x.stud_roll_no,'enrollment_no':x.stud_enrollment_no,'Guardian_Name':x.stud_guardian_name,'Guardian_Email':x.stud_guardian_email,'Guardian_Number':x.stud_guardian_number,'Address':x.stud_address,'Std': x.stud_std.std_name + x.stud_std.std_board.brd_name,'Batch':x.stud_batch.batch_name,'Package':x.stud_pack.pack_name})
            student_data.append(temp_data)
        Context.update({'data':student_data,'field_names':field_names})

    if model_name == 'attendance':
        all_data = []
        if get_std:
            data = Attendance.objects.filter(atten_student__stud_std__std_id=get_std)
        elif get_batch:
            data = Attendance.objects.filter(atten_student__stud_batch__batch_id=get_batch)
        else:
            data = Attendance.objects.all()

        field_names = ['Date','Student Roll No','Student Name','Subject','Time','Tutor','Attendance','Batch','Std','Board']
        for x in data:
            temp_data = {}
            temp_data.update({'Date':x.atten_date,'student_roll_no':x.stud_lastname,'Student_name':x.stud_contact,'subject':x.stud_contact,'time':x.stud_dob,'tutor':x.stud_gender,'Attendance':x.stud_admission_no,'Batch':x.stud_roll_no,'Std':x.stud_enrollment_no,'Board':x.stud_guardian_name})
            student_data.append(temp_data)
        Context.update({'data':student_data,'field_names':field_names})   
        
    return render(request, 'export_data.html',Context)




def bulk_upload_questions(request):
    if request.method == 'POST':
        qb_chapter_id = request.POST.get('tq_chapter')  # Corrected variable name
        qb_chapter = Chepter.objects.get(chep_id=qb_chapter_id)

        # Extract all question entries
        questions_data = request.POST.getlist('question[]')
        q_types = request.POST.getlist('q_type[]')
        answers = request.POST.getlist('answer[]')
        weightages = request.POST.getlist('weightage[]')
        options_a = request.POST.getlist('option_a[]')
        options_b = request.POST.getlist('option_b[]')
        options_c = request.POST.getlist('option_c[]')
        options_d = request.POST.getlist('option_d[]')

        # Save each question entry
        for i in range(len(questions_data)):
            question_bank.objects.create(
                qb_chepter=qb_chapter,
                qb_q_type=q_types[i],
                qb_question=questions_data[i],
                qb_answer=answers[i],
                qb_weightage=weightages[i],
                qb_optiona=options_a[i] if q_types[i] == 'MCQ' else None,
                qb_optionb=options_b[i] if q_types[i] == 'MCQ' else None,
                qb_optionc=options_c[i] if q_types[i] == 'MCQ' else None,
                qb_optiond=options_d[i] if q_types[i] == 'MCQ' else None,
            )

        return redirect('show_question_bank')  # Redirect to the same page after submission
    chap_data = Chepter.objects.filter(chep_std__std_id = 13).values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name')
    que_type_choices = question_bank.que_type.choices
    Context={'chap_data':chap_data,'que_type_choices':que_type_choices}
    return render(request, 'insert_update/bulk_upload_test_questions.html',Context)





def show_question_bank(request):
    # Fetch all questions from the question_bank model
    questions = question_bank.objects.all().values('qb_id','qb_chepter__chep_name','qb_q_type','qb_question','qb_answer','qb_weightage','qb_optiona','qb_optionb','qb_optionc','qb_optiond')
    total_questions = question_bank.objects.count()
    questions = paginatoorrr(questions,request)
    return render(request, 'show_question_bank.html', {'questions': questions, 'total_questions':total_questions})


def edit_question_bankk(request):
    # Fetch the specific question to edit
    updateid = request.GET.get('updateid')
    question = get_object_or_404(question_bank, qb_id=updateid)
    
    if request.method == 'POST':
        # Update the question details from form data
        question.qb_chepter = Chepter.objects.get(chep_id=request.POST.get('qb_chepter'))
        question.qb_q_type = request.POST.get('qb_q_type')
        question.qb_question = request.POST.get('qb_question')
        question.qb_answer = request.POST.get('qb_answer')
        question.qb_weightage = request.POST.get('qb_weightage')
        
        # Update options based on question type
        if question.qb_q_type == 'MCQ':
            question.qb_optiona = request.POST.get('qb_optiona')
            question.qb_optionb = request.POST.get('qb_optionb')
            question.qb_optionc = request.POST.get('qb_optionc')
            question.qb_optiond = request.POST.get('qb_optiond')
        else:
            # Clear options if not MCQ
            question.qb_optiona = None
            question.qb_optionb = None
            question.qb_optionc = None
            question.qb_optiond = None
        
        # Save the updated question to the database
        question.save()
        return redirect('show_question_bank')  # Redirect back to the question list page

    # Render edit form with existing question data
    chap_data = Chepter.objects.filter(chep_sub__sub_std__std_id = 13).values('chep_id','chep_name','chep_sub__sub_name','chep_sub__sub_std__std_name')
    que_type_choices = question_bank.que_type.choices
    context = {
        'question': question,
        'chap_data': chap_data,
        'que_type_choices': que_type_choices,
    }
    return render(request, 'insert_update/edit_question_bank.html', context)



def delete_question_bank(request):
    qb_id = request.GET.get('qb_id')
    if qb_id:
        question = get_object_or_404(question_bank, qb_id=qb_id)
        question.delete()

    # Redirect back to the list of questions
    return redirect('show_question_bank')

def delete_test_question_answer(request):
    if request.GET.get('delete_id'):
        del_id = request.GET['delete_id']
        print(del_id)
        try:
            data = Test_questions_answer.objects.get(tq_id=del_id)
            data.delete()
            messages.success(request,"Question Deleted Successfully")
        except data.DoesNotExist:
            messages.error(request,"Question Not Found")

        url = '/adminside/show_test_questions_admin/?test_id={}'.format(request.GET['test_id'])
    return redirect(url)




from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.core.mail import EmailMessage

def render_to_pdf(template_src, context_dict={}):
    template = render_to_string(template_src, context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(template.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_payment_slip(request):
    context = {
        'payer_name': 'John Doe',
        'payer_email': 'john@example.com',
        'amount': '500',
        'payment_date': '2024-09-12',
        'payment_method': 'Credit Card',
        'transaction_id': 'TX123456789',
    }
    pdf = render_to_pdf('payment_slip.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
