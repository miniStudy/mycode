from django.shortcuts import render

# Create your views here.

def firstpage(request):
    context={}	

    if request.GET.get("deviceId"):
        deviceId = request.GET.get('deviceId','1')
        if deviceId != '123':
            request.session['deviceId'] = deviceId
        context.update({'deviceId':deviceId})

    return render(request, "pages/index.html")

