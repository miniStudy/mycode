from django.shortcuts import render,get_object_or_404,redirect
from adminside.form import *
from adminside.models import *
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import math
import random
from django.http import Http404,JsonResponse
# Create your views here.
# mail integration 
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from adminside.decorators import admin_login_required

# -----------------------------auth Start---------------------------

def mail_send(request):
    # ------------mail sending ---------------
        sub = 'Offer Letter from miniStudy'
        mess = 'Offer Letter'
        email_from = 'miniStudy <mail@ministudy.in>'
        recp_list = ['mail.trushalpatel@gmail.com']
        # send_mail(sub,mess,email_from,recp_list)
        htmly = get_template('Email/joining_letter.html')
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
    context={
        'title' : 'Home' 
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
        'title' : 'Std',
    }
    return render(request, 'show_stds.html',context)

def insert_update_stds(request):
    brddata = Boards.objects.all()
    context = {
        'title' : 'Std',
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
    
    context = {
        'title' : 'Insert Announcements',
        'std_data':std_data,
        'batch_data':batch_data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        batch_data = batch_data.filter(batch_std__std_id = get_std)
        context.update({'get_std ':get_std,'std_data':std_data,'batch_data':batch_data}) 


    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        batch_data = batch_data.filter(batch_id = get_batch)
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
            context.update({'data':data,'get_std':get_std})     
    return render(request, 'show_subjects.html',context)





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

    context = {
        'title': 'Insert Timetable',
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
        context.update({'get_std': get_std, 'std_data': std_data, 'batch_data': batch_data, 'subject_data':subject_data}) 

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        batch_data = batch_data.filter(batch_id=get_batch)
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
            sub_attendance = (sub_one/sub_all) * 100
            subject_wise_attendance.append(sub_attendance)
            subjects.append(sub_name)
            
    combined_data = zip(subject_wise_attendance, subjects)

    context.update({'combined_data': combined_data})
    return render(request, 'show_attendance.html',context)


@admin_login_required
def insert_events(request):
    if request.method == 'POST':
        form = event_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = event_form()
    return render(request, 'event.html', {'form':form})


def hello_world():
    print("hello wolrd")




@admin_login_required
def show_tests(request):
    data = Chepterwise_test.objects.all()

    context ={
        'data' : data,
        'title' : 'Tests',
    }

    return render(request, 'show_tests.html',context)


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
