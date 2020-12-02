"""test_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static
from django.http import HttpResponseRedirect
from django.urls import path, include

from test_platform import settings
from stud_teach.views import user_info, views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tests/', include("stud_teach.urls")),
    path('login/', user_info.login_user, name='login'),
    path('logout/', user_info.logout_user, name='logout'),
    path('register/', user_info.register, name='register'),
    path('profile/', user_info.profile, name='profile'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
