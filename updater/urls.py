# -*- coding: utf-8 -*-
from django.conf.urls import url

from updater import views

urlpatterns = [
    url(
        r'^bank/update/(?P<pk>\d+)$',
        views.BankUpdateFileDetailView.as_view(),
        name='bank-update-file'
    ),
    url(
        r'^$',
        views.BankUpdateFileListView.as_view(),
        name='bank-update-file-index'
    ),

    url(
        r'^bank/update/(?P<pk>\d+)/procesar$',
        views.BankUpdateFileProcess.as_view(),
        name='bank-update-file-process'
    ),

    url(
        r'^bank/list$',
        views.BancoListView.as_view(),
        name='banco-list'
    ),

    url(
        r'^bank/(?P<pk>\d+)$',
        views.BancoDetailView.as_view(),
        name='banco-detail'
    ),
]
