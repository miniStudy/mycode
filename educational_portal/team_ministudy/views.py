from django.shortcuts import render, redirect, get_object_or_404
from team_ministudy.models import *
from team_ministudy.forms import *

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
                form = form.data
                return render(request, 'ministudy/insert_update_institute.html', {'update_form': form})

    if request.method == 'POST':
        institute_name = request.POST['institute_name']
        institute_email = request.POST['institute_email']
        institute_contact = request.POST['institute_contact']
        institute_domain = request.POST['institute_domain']
        institute_logo = request.FILES['institute_logo']

        NewInstitution.objects.create(institute_name = institute_name, institute_email = institute_email, institute_contact = institute_contact, institute_logo = institute_logo, institute_domain = institute_domain)
        return redirect('show_institute')
    return render(request, 'ministudy/insert_update_institute.html')

