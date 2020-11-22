"""DDiag URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from .views import *

urlpatterns = [
    path('', diagnose, name='home'),
    path('result/', diagnose, name='redirect_example'),
    path('insert/', insert_view, name='insert'),
    path('insert_result/', insert_view, name='redirect_insert'),
    path('update/', update_view, name='update'),
    path('update_result/', update_view, name='redirect_update'),
    path('delete/<int:patientID>', delete_view, name='delete'),
    path('verify/', verify_view, name='verify'),
    path('verify_result/', verify_view, name='redirect_verify'),
    path('admin/', admin.site.urls),
]
