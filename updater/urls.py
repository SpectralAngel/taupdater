# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
        name='banco-update-list'
    ),

    url(
        r'^bank/(?P<pk>\d+)$',
        views.BancoDetailView.as_view(),
        name='banco-update-detail'
    ),

    url(
        r'^bank/bill$',
        views.BancoBillingView.as_view(),
        name='banco-bill'
    ),

    url(
        r'^bank/client$',
        views.BancoClientView.as_view(),
        name='banco-client'
    ),

    url(
        r'^cotizacion/files$',
        views.CotizacionUpdateFileList.as_view(),
        name='cotizacion-file-index'
    ),

    url(
        r'^cotizacion/update/(?P<pk>\d+)/procesar$',
        views.CotizacionUpdateFileProcessView.as_view(),
        name='cotizacion-update-file-process'
    ),

    url(
        r'^cotizacion/list$',
        views.CotizacionListView.as_view(),
        name='cotizacion-update-list'
    ),

    url(
        r'^cotizacion/(?P<pk>\d+)$',
        views.CotizacionDetailView.as_view(),
        name='cotizacion-update-detail'
    ),

    url(
        r'^cotizacion/bill$',
        views.CotizacionBillingView.as_view(),
        name='cotizacion-bill'
    ),

    url(
        r'^cotizacion/(?P<pk>\d+)retrasadas/crear$',
        views.RetrasadasCrearView.as_view(),
        name='retrasadas-crear'
    ),

    url(
        r'^banco/comparaciones$',
        views.ComparacionBancoListView.as_view(),
        name='compracion-banco-list'
    ),

    url(
        r'^banco/comparacion/(?P<pk>\d+)$',
        views.ComparacionBancoDetailView.as_view(),
        name='comparacion-banco-detail'
    ),

    url(
        r'^banco/comparacion/(?P<pk>\d+)/procesar$',
        views.ComparacionBancoProcessView.as_view(),
        name='comparacion-banco-process'
    ),
]
