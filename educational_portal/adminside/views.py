from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from adminside.form import *
from adminside.models import *
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import math
import random
from django.http import Http404,JsonResponse
from django.db.models import Count,Sum
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
import requests


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

    print(std_list)
    print(students_for_that_std)
    context={
        'title' : 'Home',
        'all_students':all_students,
        'piechart_category':piechart_category,
        'piechart_data':piechart_data,
        'std_list':std_list,
        'students_for_that_std':students_for_that_std,
    }
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
    data = Subject.objects.all()
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
    data = Chepter.objects.all()
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
            data = data.filter(chep_sub__sub_std__std_id = get_std)
            subject_data = subject_data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'get_std':get_std,'std_data':std_data}) 


    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        if get_subject == 0:
            pass
        else:    
            data = data.filter(chep_sub__sub_id = get_subject)
            get_subject = Subject.objects.get(sub_id = get_subject)
            context.update({'data':data,'subject_data':subject_data,'get_subject':get_subject}) 


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
    context = {
        'faculties': faculties,
        'title': 'Faculties',
    }

    return render(request, 'show_faculties.html', context)

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
            context.update({'data':data,'batch_data':batch_data,'get_std':get_std,'stud_data':stud_data,'sub_data':subj_data})
            

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
            sub_attendance = round((sub_one/sub_all) * 100, 2)
            subject_wise_attendance.append(sub_attendance)
            subjects.append(sub_name)
            
    combined_data = zip(subject_wise_attendance, subjects)

    context.update({'combined_data': combined_data})
    return render(request, 'show_attendance.html',context)


@admin_login_required
def show_events(request):
    events = Event.objects.all()
    events_imgs = Event_Image.objects.all()
    selected_events = Event.objects.all()[:1]
    context = {
        'events':events,
        'events_imgs':events_imgs,
        'selected_events':selected_events,
        'title' : 'Events',
    }
    if request.GET.get('event_id'):
        event_id = request.GET['event_id']
        selected_events = Event.objects.filter(event_id = event_id)
        events_imgs = Event_Image.objects.filter(event__event_id = event_id)
        context.update({'selected_events':selected_events,'events_imgs':events_imgs})
    return render(request, 'show_events.html',context)

@admin_login_required
def insert_events(request):
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
    return render(request, 'insert_update/events_insert_admin.html')


@admin_login_required
def show_tests(request):
    data = Chepterwise_test.objects.annotate(num_questions=Count('test_questions_answer'),total_marks=Sum('test_questions_answer__tq_weightage'))
    std_data = Std.objects.all()
    subject_data = Subject.objects.all()
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

    return render(request, 'show_tests.html',context)



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
                    return redirect('admin_tests')
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
        print(test_id)
        context.update({'test_id': test_id})

    if request.method == 'POST':
        form = TestQuestionsAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace 'success_url' with your actual success URL
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
            data = data.filter(pack_std__std_id = get_std)
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
def show_students(request):
    data = Students.objects.all()
    std_data = Std.objects.all()
    batch_data = Batches.objects.all()
   
    context ={
        'data' : data,
        'title' : 'Students',
        'std_data' : std_data,
        'batch_data':batch_data,
    }
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(stud_std__std_id = get_std)
            batch_data = batch_data.filter(batch_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            context.update({'data':data,'batch_data':batch_data,'get_std':get_std})
            

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = data.filter(stud_batch__batch_id = get_batch)
            get_batch = Batches.objects.get(batch_id = get_batch)
            context.update({'data':data,'get_batch':get_batch})        
            
    return render(request, 'show_students.html',context)




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
            data = data.filter(batch_std__std_id = get_std)
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
    materials = Chepterwise_material.objects.all()
    selected_sub=None

    context = {'standard_data':standard_data, 'subjects_data':subjects_data, 'materials':materials, 'title' : 'Materials',}
    if request.GET.get('std_id'):
        std_id = int(request.GET.get('std_id'))
        subjects_data = Subject.objects.filter(sub_std__std_id = std_id)
        materials = Chepterwise_material.objects.filter(cm_chepter__chep_sub__sub_std__std_id = std_id)
        context.update({'materials': materials,'subjects_data': subjects_data, 'std':std_id})

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
            sub_attendance = round((sub_one/sub_all) * 100, 2)
            subject_wise_attendance.append(sub_attendance)
            subjects.append(sub_name)
            
    combined_data = zip(subject_wise_attendance, subjects)

    context.update({'combined_data': combined_data})
    return render(request, 'show_report_card_admin.html', context)



def fees_collection_admin(request):
    fees_collections_data = Fees_Collection.objects.all()
    cheque_collections_data = Cheque_Collection.objects.filter(cheque_paid=False)


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
    

    context={
        'fees_collections_data':fees_collections_data,
        'cheque_collections_data':cheque_collections_data,
        'total_amount_fees_paid':total_amount_fees_paid,
        'total_fees_amount_after_discount':total_fees_amount_after_discount,
        'total_pending_fees':total_pending_fees
    }
    return render(request, 'fees_collection_admin.html', context)

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


def add_fees_collection_admin(request):
    context={}
    return render(request, 'insert_update/add_fees_collection_admin.html', context)

def update_cheques_admin(request):
    context={}
    return render(request, 'update_cheques_admin.html', context)

def payments_history_admin(request):
    context={}
    return render(request, 'payments_history_admin.html', context)

