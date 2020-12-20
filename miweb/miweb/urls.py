"""miweb URL Configuration

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
from django.urls import path, re_path
from unica_app.views import call_model
from django.views.generic import TemplateView
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from unica_app.views import test_if_logged
from unica_app.models import Quota
from unica_app.models import EmailHistorico
from unica_app.views import consultList
from unica_app.views import quotaagregate
from unica_app.views import quota_info, database
from unica_app import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
app_name = 'unica_app'

urlpatterns = [
            path('admin/', admin.site.urls),
            path('quotaagregate/', quotaagregate.as_view()),
            path('quota_info/', quota_info.as_view()),
            path('api-token-auth/', obtain_jwt_token),
            path('test_if_logged',test_if_logged.as_view()),
            re_path(r'process_email',call_model.as_view()),
            path('history/<int:param1>/', consultList.as_view()),
            path('query/', database.as_view())
            ]
