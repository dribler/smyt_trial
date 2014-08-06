# -*- coding: utf-8 -*-
__author__ = 'Vershinin M.S.'
from django.conf.urls import patterns, url

urlpatterns = patterns('main.views',
                       url(r'^$', 'home'),
                       url(r'^model/(\w+)/$', 'model'))