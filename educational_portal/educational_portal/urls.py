"""educational_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from adminside import views as adminview
from django.conf import settings
from django.conf.urls.static import static
from website import views as websiteview
urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminside/', include('adminside.urls')),
    path('', websiteview.firstpage, name="FirstPage"),
    path('summernote/', include('django_summernote.urls')),
    path('studentside/', include('studentside.urls')),
    path('teacherside/', include('teacherside.urls')),
    path('parentsside/', include('parentsside.urls')),
    path('team_ministudy/', include('team_ministudy.urls')),
    path('api/', include('api.apiurls')),]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)