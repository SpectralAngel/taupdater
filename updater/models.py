# -*- coding: utf8 -*-
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_extensions.db.models import TimeStampedModel
from sqlobject import sqlhub
from actaf import database, parsers
from bridge.models import Banco


@python_2_unicode_compatible
class BankUpdateFile(TimeStampedModel):
    banco = models.ForeignKey(Banco)
    archivo = models.FileField(upload_to='update//%Y/%m/%d')
    fecha_de_cobro = models.DateField()
    fecha_de_procesamiento = models.DateField()
    procesado = models.BooleanField(default=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return u'{0} - {1}'.format(
            self.banco.nombre,
            self.fecha_de_cobro.strftime(u'%Y/%m/%d')
        )

    def process(self):
        if self.procesado:
            return

        banco = database.Banco.get(self.banco.id)

        accounts = {}
        for account in database.get_accounts():
            accounts[account] = {'number': 0, 'amount': Decimal()}

        Parser = getattr(parsers, banco.parser)
        parser = Parser(self.fecha_de_procesamiento, self.archivo.name, banco)
        parsed = parser.output()

        obligacion = database.get_obligation(self.fecha_de_procesamiento.year,
                                             self.fecha_de_procesamiento.month)
        jubilados = database.get_compliment(
            self.fecha_de_procesamiento.year,
            self.fecha_de_procesamiento.month,
            True
        )

        alternativos = database.get_compliment(
            self.fecha_de_procesamiento.year,
            self.fecha_de_procesamiento.month,
            False
        )

        updater = parsers.ActualizadorBancario(
            obligacion,
            accounts,
            self.fecha_de_procesamiento,
            banco,
            self.fecha_de_cobro,
            jubilados,
            alternativos
        )

        updater.registrar_cuenta(database.get_loan_account(), 'prestamo')
        updater.registrar_cuenta(database.get_cuota_account(), 'cuota')
        updater.registrar_cuenta(database.get_incomplete_account(),
                                 'incomplete')
        updater.registrar_cuenta(database.get_exceding_account(), 'excedente')
        updater.registrar_cuenta(database.get_inprema_account(), 'complemento')

        conn = sqlhub.getConnection()
        transaction = conn.transaction()
        sqlhub.processConnection = transaction
        try:
            [updater.update(i, banco.cuota) for i in parsed]
            transaction.commit()
        except Exception:
            transaction.rollback()
            transaction.begin()
            raise

        self.procesado = True
        self.save()
