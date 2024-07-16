from django.shortcuts import render

# Create your views here.
def teacher_home(request):
     return render(request, 'teacherpanel/index.html')