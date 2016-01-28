# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from updater.views import BankUpdateFileDetailView, BankUpdateFileListView, \
    BankUpdateFileProcess

urlpatterns = [
    url(
        r'bank/update/^(?P<pk>\d+)$',
        BankUpdateFileDetailView.as_view(),
        name='bank-update-file'
    ),
    url(
        r'^$',
        BankUpdateFileListView.as_view(),
        name='bank-update-file-index'
    ),

    url(
        r'^bank/update/(?P<pk>\d+)/procesar$',
        BankUpdateFileProcess.as_view(),
        name='bank-update-file-process'
    ),
]
