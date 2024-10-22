from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from team_ministudy.models import *
from team_ministudy.forms import *
from datetime import timedelta
from django.utils.timezone import now

# Create your views here.

def show_institute_function(request):
    institute_data = NewInstitution.objects.all()
    context = {'institute_data': institute_data}
    return render(request, 'ministudy/show_institute.html', context)


def insert_update_institute_function(request):
    if request.GET.get('pk'):
        pk = request.GET['pk']
        instance = get_object_or_404(NewInstitution, pk=pk)
        if request.method == "POST":
            form = Institute_Form(request.POST, instance = instance)
            if form.is_valid():
                form.save()
                return redirect('show_institute')
            else:
                return render(request, 'ministudy/insert_update_institute.html')
        else:
            return render(request, 'ministudy/insert_update_institute.html')

    if request.GET.get('update_id'):
        update_id = request.GET.get('update_id')
        update_data = get_object_or_404(NewInstitution, institute_id=update_id)
        context = {'update_data': update_data}
        return render(request, 'ministudy/insert_update_institute.html', context)
    
    if request.method == 'POST':
        institute_name = request.POST['institute_name']
        institute_email = request.POST['institute_email']
        institute_contact = request.POST['institute_contact']
        institute_domain = request.POST['institute_domain']
        institute_logo = request.FILES['institute_logo']

        NewInstitution.objects.create(institute_name = institute_name, institute_email = institute_email, institute_contact = institute_contact, institute_logo = institute_logo, institute_domain = institute_domain)
        return redirect('show_institute')
    return render(request, 'ministudy/insert_update_institute.html')

def show_ministudy_payment_function(request):
    ministudy_payment_data = MinistudyPayment.objects.all()
    context = {'ministudy_payment_data': ministudy_payment_data}
    return render(request, 'ministudy/show_ministudy_pay.html', context)

def insert_update_ministudy_payment_function(request):
    students_data = Students.objects.all()
    update_data = None
    if request.GET.get('pk'):
        instance = get_object_or_404(MinistudyPayment, pk=request.GET['pk'])
        if request.method == 'POST':
            form = Ministudy_Payment_Form(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('show_ministudy_payment')
            else:
                return render(request, 'ministudy/insert_update_ministudy_pay.html')

    if request.GET.get('update_id'):
        update_id = request.GET.get('update_id')
        update_data = MinistudyPayment.objects.get(ministudypay_id = update_id)
        return render(request, 'ministudy/insert_update_ministudy_pay.html', {'update_data': update_data, 'students_data': students_data})
    else:
        if request.method == 'POST':
            form = Ministudy_Payment_Form(request.POST)
            if form.is_valid():
                form.save()
                return redirect('show_ministudy_payment')
            else:
                return render(request, 'ministudy/insert_update_ministudy_pay.html')
    return render(request, 'ministudy/insert_update_ministudy_pay.html', {'students_data': students_data, 'update_data': update_data})



def institute_lock_function():
    unlocked_institutes = NewInstitution.objects.filter(institute_lock=False)
    for institute in unlocked_institutes:
        lock_date = institute.institute_joining_date + timedelta(days=15)
        
        if now() >= lock_date:
            institute.institute_lock = True
            institute.save()


def remove_institute_function(request):
    if request.GET.get('remove_id'):
        institute_id = request.GET.get('remove_id')
        remove_data = NewInstitution.objects.get(institute_id = institute_id)
        remove_data = NewInstitution.objects.get(institute_id=institute_id)
        Boards.objects.filter(domain_name=remove_data.institute_domain).delete()
        remove_data.delete()  
        messages.success(request, 'Institute deleted successfully!')
        return redirect('show_institute')
    return redirect('show_institute')