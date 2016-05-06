# -*- coding: utf8 -*-
from __future__ import unicode_literals

from collections import defaultdict
from decimal import Decimal, InvalidOperation

import unicodecsv as csv
from bridge.models import Banco, Account, Affiliate, Cotizacion
from bridge.utils import Zero
from django.conf import settings
from django.core.files.storage import default_storage as storage
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
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
            self.fecha_de_cobro.strftime(str('%Y/%m/%d'))
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
            'loan_set__casa',
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
                print(key_error)
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


@python_2_unicode_compatible
class CotizacionUpdateFile(TimeStampedModel):
    cotizacion = models.ForeignKey(Cotizacion)
    archivo = models.FileField(upload_to='update/%Y/%m/%d')
    fecha_de_cobro = models.DateField()
    fecha_de_procesamiento = models.DateField()
    procesado = models.BooleanField(default=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    cuenta_colegiacion = models.ForeignKey(Account, blank=True, null=True,
                                           related_name='colegiacion_cotizacion_set')
    cuenta_prestamo = models.ForeignKey(Account, blank=True, null=True,
                                        related_name='prestamo_cotizacion_set')
    cuenta_excedente = models.ForeignKey(Account, blank=True, null=True,
                                         related_name='excedente_cotizacion_set')
    usar_id = models.BooleanField(default=True)
    cobrar_colegiacion = models.BooleanField(default=True)

    def __str__(self):
        return '{0} - {1}'.format(
            self.cotizacion.nombre,
            self.fecha_de_cobro.strftime(str('%Y/%m/%d'))
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
        ).prefetch_related(
            'loan_set',
            'loan_set__pay_set',
            'loan_set__casa',
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
                           pagos[afiliado], self.cotizacion,
                           self.cuenta_colegiacion, self.cuenta_prestamo,
                           self.cuenta_excedente, self.cobrar_colegiacion,
                           banco=False)
        self.procesado = True
        self.save()


@python_2_unicode_compatible
class ErrorLecturaCotizacion(TimeStampedModel):
    """
    Registra los errores de parseo correspondientes a un archivo de
    actualizacion bancaria
    """
    cotizacion_update_file = models.ForeignKey(CotizacionUpdateFile)
    no_encontrado = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return _('{0} {1}').format(
            self.cotizacion_update_file.cotizacion.nombre,
            self.no_encontrado
        )


@python_2_unicode_compatible
class ComparacionBanco(TimeStampedModel):
    """
    Registra un archivo para verificar las diferencias entre lo ingresado a los
    estados de cuenta y lo que en realidad se pago.
    """
    banco = models.ForeignKey(Banco)
    fecha_inicial = models.DateField()
    fecha_final = models.DateField()
    archivo = models.FileField(upload_to='compare/%Y/%m/%d')
    usar_id = models.BooleanField(default=True)

    def __str__(self):
        return self.banco.nombre

    def get_absolute_url(self):

        return reverse('comparacion-banco-detail', args=[self.id])

    def process(self):

        self.diferenciabanco_set.all().delete()
        self.errorcomparacionbanco_set.all().delete()

        reader = csv.reader(storage.open(self.archivo.name, 'rU'))

        afiliados = {}
        afiliado_identidad = {}
        pagos = defaultdict(Decimal)

        todos = Affiliate.objects.select_related(
            'banco',
        ).prefetch_related(
            'deduccionbancaria_set'
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
                print(key_error)
                error = ErrorComparacionBanco()
                error.comparacion = self
                error.no_encontrado = row[0]
                error.monto = amount
                error.save()

            except ValueError as value_error:
                print(value_error)
                error = ErrorComparacionBanco()
                error.comparacion = self
                error.no_encontrado = row[0]
                error.monto = amount
                error.save()

            except InvalidOperation as value_error:
                print(value_error)
                error = ErrorComparacionBanco()
                error.comparacion = self
                error.no_encontrado = '{0} {1}'.format(row[0], row[1])
                error.save()

        for afiliado in pagos:
            pago = pagos[afiliado]
            deducciones = afiliado.deduccionbancaria_set.filter(
                day__range=(self.fecha_inicial, self.fecha_final)
            ).aggregate(
                total=Sum('amount')
            )['total']
            if deducciones is None:
                deducciones = Zero

            diferencia = pago - deducciones
            if diferencia != Zero:
                registro = DiferenciaBanco(archivo=self, afiiado=afiliado,
                                           diferencia=diferencia,
                                           deducciones=deducciones,
                                           monto_en_archivo=pago)
                registro.save()

    def total(self):

        return self.diferenciabanco_set.aggregate(
            total=Sum('diferencia')
        )['total']


class ErrorComparacionBanco(TimeStampedModel):
    """
    Registra los errores de lectura que se han encontrado en la comparación de
    los datos de un banco
    """
    comparacion = models.ForeignKey(ComparacionBanco)
    no_encontrado = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return _('{0} {1}').format(
            self.comparacion.banco.nombre,
            self.no_encontrado
        )


@python_2_unicode_compatible
class DiferenciaBanco(TimeStampedModel):
    """
    Registra las diferencias que se encontraron en las deducciones de un
    afiliado y los que se encuentra en el archivo
    """
    archivo = models.ForeignKey(ComparacionBanco)
    afiiado = models.ForeignKey(Affiliate)
    diferencia = models.DecimalField(max_digits=10, decimal_places=2)
    deducciones = models.DecimalField(max_digits=10, decimal_places=2)
    monto_en_archivo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return _('{0} {1} {2}').format(
            self.afiiado.first_name,
            self.afiiado.last_name,
            self.diferencia
        )


@python_2_unicode_compatible
class BancoFaltante(TimeStampedModel):
    """
    Registers those who need to be charged again
    """
    archivo = models.FileField(upload_to='complemento/%Y/%m/%d')
    banco = models.ForeignKey(Banco)
    fecha_de_cobro = models.DateField()
    cobrar_colegiacion = models.BooleanField(default=True)

    def __str__(self):

        return self.banco.nombre

    def afiliados(self):
        reader = csv.reader(storage.open(self.archivo.name, 'rU'))

        afiliaciones = []

        for line in reader:
            afiliaciones.append(int(line[0]))

        return Affiliate.objects.filter(
            id__in=afiliaciones
        )
