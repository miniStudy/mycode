from django.shortcuts import render
from team_ministudy.models import *
# Create your views here.

def firstpage(request):
    context={}	
    domain  = request.get_host()
    Institute_data = NewInstitution.objects.get(institute_domain = domain)
    request.session['institute_logo'] = Institute_data.institute_logo.url

    if request.GET.get("deviceId"):
        deviceId = request.GET.get('deviceId','1')
        if deviceId != '123':
            
            request.session['deviceId'] = deviceId
        context.update({'deviceId':deviceId})

    return render(request, "pages/index.html",context)

