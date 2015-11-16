from django.contrib import admin

from updater.models import BankUpdateFile


class BankUpdateFileAdmin(admin.ModelAdmin):
    list_display = ['banco', 'fecha_de_cobro', 'fecha_de_procesamiento',
                    'procesado']
    ordering = ['banco', 'fecha_de_cobro', 'fecha_de_procesamiento',
                'procesado']

admin.site.register(BankUpdateFile, BankUpdateFileAdmin)
