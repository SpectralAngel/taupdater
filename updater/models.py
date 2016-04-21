# -*- coding: utf8 -*-
from __future__ import unicode_literals

from collections import defaultdict
from decimal import Decimal

import unicodecsv as csv
from bridge.models import Banco, Account, Affiliate
from django.conf import settings
from django.core.files.storage import default_storage as storage
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel


@python_2_unicode_compatible
class BankUpdateFile(TimeStampedModel):
    banco = models.ForeignKey(Banco)
    archivo = models.FileField(upload_to='update//%Y/%m/%d')
    fecha_de_cobro = models.DateField()
    fecha_de_procesamiento = models.DateField()
    procesado = models.BooleanField(default=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    cuenta_colegiacion = models.ForeignKey(Account, blank=True, null=True,
                                           related_name='colegiacion_set')
    cuenta_prestamo = models.ForeignKey(Account, blank=True, null=True,
                                        related_name='prestamo_set')
    cuenta_excedente = models.ForeignKey(Account, blank=True, null=True,
                                         related_name='excedente_set')
    usar_id = models.BooleanField(default=True)
    cobrar_colegiacion = models.BooleanField(default=True)

    def __str__(self):
        return '{0} - {1}'.format(
            self.banco.nombre,
            self.fecha_de_cobro.strftime(u'%Y/%m/%d')
        )

    def process(self):
        """
        Processes the information inside the file to update the payments of a
        :class:`Affiliate`
        :return:
        """
        if self.procesado:
            return

        reader = csv.reader(storage.open(self.archivo.name, 'rU'))

        afiliados = {}
        afiliado_identidad = {}
        pagos = defaultdict(Decimal)

        todos = Affiliate.objects.select_related(
            'cotizacion',
            'banco',
        ).prefetch_related(
            'loan_set',
            'loan_set__pay_set',
            'loan_set__deduction_set',
            'loan_set__deduction_set__account',
            'extra_set',
            'extra_set__account',
        ).filter(card_id__isnull=False)

        for afiliado in todos:
            afiliados[afiliado.id] = afiliado
            identidad = afiliado.card_id.replace('-', '')
            afiliado_identidad[identidad] = afiliado

        for row in reader:

            amount = Decimal(row[2].replace(',', ''))
            try:
                if self.usar_id:
                    afiliado = afiliados[int(row[0])]
                else:
                    identidad = '{0:013d}'.format(int(row[0].replace('-', '')))
                    afiliado = afiliado_identidad[identidad]

                pagos[afiliado] += amount

            except KeyError as key_error:
                error = ErrorLectura()
                error.bank_update_file = self
                error.no_encontrado = row[0]
                error.monto = amount
                error.save()

        for afiliado in pagos:
            afiliado.pagar(self.fecha_de_cobro, self.fecha_de_procesamiento,
                           pagos[afiliado], self.banco, self.cuenta_colegiacion,
                           self.cuenta_prestamo, self.cuenta_excedente,
                           self.cobrar_colegiacion, banco=True)

        self.procesado = True
        self.save()


@python_2_unicode_compatible
class ErrorLectura(TimeStampedModel):
    """
    Registra los errores de parseo correspondientes a un archivo de
    actualizacion bancaria
    """
    bank_update_file = models.ForeignKey(BankUpdateFile)
    no_encontrado = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return _('{0} {1}').format(
            self.bank_update_file.banco.nombre,
            self.no_encontrado
        )
