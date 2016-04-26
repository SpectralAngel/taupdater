# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from updater.models import BankUpdateFile, ErrorLectura, ErrorLecturaCotizacion, \
    CotizacionUpdateFile


class BankUpdateFileAdmin(admin.ModelAdmin):
    list_display = ['banco', 'fecha_de_cobro', 'fecha_de_procesamiento',
                    'procesado']
    ordering = ['banco', 'fecha_de_cobro', 'fecha_de_procesamiento',
                'procesado']


class ErrorLecturaAdmin(admin.ModelAdmin):
    list_display = ['bank_update_file', 'no_encontrado', 'monto']


class CotizacionUpdateFileAdmin(admin.ModelAdmin):
    list_display = ['cotizacion', 'fecha_de_cobro', 'fecha_de_procesamiento',
                    'procesado']
    ordering = ['cotizacion', 'fecha_de_cobro', 'fecha_de_procesamiento',
                'procesado']


class ErrorLecturaCotizacionAdmin(admin.ModelAdmin):
    list_display = ['cotizacion_update_file', 'no_encontrado', 'monto']


admin.site.register(BankUpdateFile, BankUpdateFileAdmin)
admin.site.register(ErrorLectura, ErrorLecturaAdmin)
admin.site.register(CotizacionUpdateFile, CotizacionUpdateFileAdmin)
admin.site.register(ErrorLecturaCotizacion, ErrorLecturaCotizacionAdmin)
