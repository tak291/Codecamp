# -*- coding: utf-8 -*-
"""
URLs for customerdataapi.
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from customerdataapi.views import CustomerDataViewSet

ROUTER = DefaultRouter()
ROUTER.register(r'customerdata', CustomerDataViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(ROUTER.urls)),
    url(r'^$', TemplateView.as_view(template_name="customerdataapi/base.html")),
]
