# -*- coding: utf-8 -*-
"""
URLs for customerdataapi.
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic.base import View
from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework.views import APIView
from . import views

from customerdataapi.views import CustomerDataViewSet


ROUTER = DefaultRouter()
ROUTER.register(r'customerdata', CustomerDataViewSet)



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(ROUTER.urls)),
    url(r'^$', TemplateView.as_view(template_name="customerdataapi/pay.html")),
    url(r'payments/paypal/', include("paypal.standard.ipn.urls")),
    #Adding url for paypal payments.
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^paypal/accepted', TemplateView.as_view(template_name="customerdataapi/accepted.html")),
    url(r'^paypal/cancel', TemplateView.as_view(template_name="customerdataapi/cancel.html")),
]
