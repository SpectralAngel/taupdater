# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create,
#     modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field
# names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom
# [app_label]'
# into your database.
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Account(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    loan = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'account'

    def __str__(self):

        return self.name


class Affiliate(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    card_id = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    birth_place = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    school = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=50, blank=True, null=True)
    joined = models.DateField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    escalafon = models.CharField(max_length=11, blank=True, null=True)
    inprema = models.CharField(max_length=11, blank=True, null=True)
    payment = models.CharField(max_length=20)
    jubilated = models.DateField(blank=True, null=True)
    reason = models.CharField(max_length=50, blank=True, null=True)
    desactivacion = models.DateField(blank=True, null=True)
    muerte = models.DateField(blank=True, null=True)
    banco = models.IntegerField(blank=True, null=True)
    cuenta = models.CharField(max_length=20, blank=True, null=True)
    departamento = models.ForeignKey('Departamento', blank=True, null=True)
    municipio = models.ForeignKey('Municipio', blank=True, null=True)
    cotizacion = models.ForeignKey('Cotizacion', blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    instituto_id = models.IntegerField(blank=True, null=True)
    banco_completo = models.IntegerField()
    bancario = models.CharField(max_length=255, blank=True, null=True)
    last = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                               null=True)

    class Meta:
        managed = False
        db_table = 'affiliate'


class Alquiler(models.Model):
    cubiculo = models.ForeignKey('Cubiculo', blank=True, null=True)
    dia = models.DateField()
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    inquilino = models.CharField(max_length=100, blank=True, null=True)
    recibo = models.ForeignKey('Recibo', blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=0)
    mora = models.DecimalField(max_digits=10, decimal_places=0, blank=True,
                               null=True)
    impuesto = models.DecimalField(max_digits=10, decimal_places=0, blank=True,
                                   null=True)

    class Meta:
        managed = False
        db_table = 'alquiler'


class Asamblea(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.ForeignKey('Departamento', blank=True, null=True)
    habilitado = models.IntegerField()
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asamblea'


class AutoSeguro(models.Model):
    affiliate = models.ForeignKey(Affiliate, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    month1 = models.IntegerField(blank=True, null=True)
    month2 = models.IntegerField(blank=True, null=True)
    month3 = models.IntegerField(blank=True, null=True)
    month4 = models.IntegerField(blank=True, null=True)
    month5 = models.IntegerField(blank=True, null=True)
    month6 = models.IntegerField(blank=True, null=True)
    month7 = models.IntegerField(blank=True, null=True)
    month8 = models.IntegerField(blank=True, null=True)
    month9 = models.IntegerField(blank=True, null=True)
    month10 = models.IntegerField(blank=True, null=True)
    month11 = models.IntegerField(blank=True, null=True)
    month12 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auto_seguro'
        unique_together = (('affiliate', 'year'),)


class Autorizacion(models.Model):
    affiliate = models.ForeignKey(Affiliate, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    banco = models.ForeignKey('Banco', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'autorizacion'


class Auxilio(models.Model):
    afiliado = models.ForeignKey(Affiliate, blank=True, null=True)
    cobrador = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    cheque = models.CharField(max_length=20, blank=True, null=True)
    banco = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auxilio'


class AyudaFunebre(models.Model):
    afiliado = models.ForeignKey(Affiliate, blank=True, null=True)
    fecha = models.DateTimeField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    cheque = models.CharField(max_length=20, blank=True, null=True)
    pariente = models.CharField(max_length=100, blank=True, null=True)
    banco = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ayuda_funebre'


@python_2_unicode_compatible
class Banco(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    depositable = models.IntegerField()
    asambleista = models.IntegerField()
    parser = models.CharField(max_length=45)
    generator = models.CharField(max_length=45)
    codigo = models.CharField(max_length=45, blank=True, null=True)
    cuenta = models.CharField(max_length=45, blank=True, null=True)
    cuota = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'banco'

    def __str__(self):

        return u'{0}'.format(self.nombre)


class BankAccount(models.Model):
    account = models.ForeignKey(Account, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                 null=True)
    bank_report = models.ForeignKey('BankReport', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bank_account'


class BankReport(models.Model):
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    banco = models.ForeignKey(Banco, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bank_report'


class Beneficiario(models.Model):
    seguro = models.ForeignKey('Seguro', blank=True, null=True)
    nombre = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    cheque = models.CharField(max_length=20)
    banco = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'beneficiario'


class Casa(models.Model):
    nombre = models.CharField(max_length=20)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=11, blank=True, null=True)
    activa = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'casa'


class CobroBancarioBanhcafe(models.Model):
    identidad = models.CharField(max_length=13, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                   null=True)
    consumido = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cobro_bancario_banhcafe'


class Cotizacion(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    jubilados = models.IntegerField()
    bank_main = models.IntegerField()
    alternate = models.IntegerField()
    normal = models.IntegerField()
    ordering = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cotizacion'


class CotizacionTgUser(models.Model):
    cotizacion_id = models.IntegerField()
    tg_user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cotizacion_tg_user'


class Cubiculo(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    inquilino = models.CharField(max_length=255, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    enee = models.CharField(max_length=100)
    interes = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'cubiculo'


class CuentaRetrasada(models.Model):
    account = models.ForeignKey(Account, blank=True, null=True)
    mes = models.IntegerField(blank=True, null=True)
    anio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cuenta_retrasada'
        unique_together = (('anio', 'mes'),)


class CuotaTable(models.Model):
    affiliate = models.ForeignKey(Affiliate)
    year = models.IntegerField()
    month1 = models.IntegerField()
    month2 = models.IntegerField()
    month3 = models.IntegerField()
    month4 = models.IntegerField()
    month5 = models.IntegerField()
    month6 = models.IntegerField()
    month7 = models.IntegerField()
    month8 = models.IntegerField()
    month9 = models.IntegerField()
    month10 = models.IntegerField()
    month11 = models.IntegerField()
    month12 = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cuota_table'
        unique_together = (('affiliate', 'year'),)


class DeduccionBancaria(models.Model):
    afiliado = models.ForeignKey(Affiliate, blank=True, null=True)
    banco = models.ForeignKey(Banco, blank=True, null=True)
    account = models.ForeignKey(Account, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                 null=True)
    detail = models.TextField(blank=True, null=True)
    day = models.DateField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deduccion_bancaria'


class Deduced(models.Model):
    affiliate = models.ForeignKey(Affiliate)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account)
    month = models.IntegerField()
    year = models.IntegerField()
    detail = models.CharField(max_length=150, blank=True, null=True)
    cotizacion_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deduced'


class Deduction(models.Model):
    loan = models.ForeignKey('Loan', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                 null=True)
    account = models.ForeignKey(Account)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deduction'
        unique_together = (('id', 'account'),)


class Departamento(models.Model):
    nombre = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departamento'


class DepartamentoTgUser(models.Model):
    departamento_id = models.IntegerField()
    tg_user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'departamento_tg_user'


class Deposito(models.Model):
    afiliado_id = models.IntegerField(blank=True, null=True)
    banco_id = models.IntegerField(blank=True, null=True)
    concepto = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                null=True)
    posteo = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'deposito'


class DepositoAnonimo(models.Model):
    referencia = models.CharField(max_length=100, blank=True, null=True)
    banco_id = models.IntegerField(blank=True, null=True)
    concepto = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                null=True)

    class Meta:
        managed = False
        db_table = 'deposito_anonimo'


class DetalleBancario(models.Model):
    reporte = models.ForeignKey('ReporteBancario', blank=True, null=True)
    account = models.ForeignKey(Account, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                 null=True)

    class Meta:
        managed = False
        db_table = 'detalle_bancario'


class DetalleProducto(models.Model):
    producto = models.ForeignKey('Producto', blank=True, null=True)
    organizacion = models.ForeignKey('Organizacion', blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'detalle_producto'


class Devolucion(models.Model):
    afiliado = models.ForeignKey(Affiliate, blank=True, null=True)
    concepto = models.CharField(max_length=200, blank=True, null=True)
    fecha = models.DateTimeField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    cheque = models.CharField(max_length=20, blank=True, null=True)
    banco = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devolucion'


class Distribution(models.Model):
    account = models.ForeignKey(Account, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                 null=True)

    class Meta:
        managed = False
        db_table = 'distribution'


class Extra(models.Model):
    affiliate = models.ForeignKey(Affiliate, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                 null=True)
    account = models.ForeignKey(Account, blank=True, null=True)
    months = models.IntegerField(blank=True, null=True)
    retrasada = models.IntegerField(blank=True, null=True)
    mes = models.IntegerField(blank=True, null=True)
    anio = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'extra'


class Filial(models.Model):
    instituto = models.CharField(max_length=255, blank=True, null=True)
    departamento = models.ForeignKey(Departamento, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filial'


class FormaPago(models.Model):
    nombre = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forma_pago'


class GroupPermission(models.Model):
    group = models.ForeignKey('TgGroup')
    permission = models.ForeignKey('Permission')

    class Meta:
        managed = False
        db_table = 'group_permission'


class Indemnizacion(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indemnizacion'


class Inscripcion(models.Model):
    afiliado_id = models.IntegerField(blank=True, null=True)
    asamblea_id = models.IntegerField(blank=True, null=True)
    viatico_id = models.IntegerField(blank=True, null=True)
    enviado = models.IntegerField(blank=True, null=True)
    envio = models.DateField(blank=True, null=True)
    ingresado = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inscripcion'
        unique_together = (('asamblea_id', 'afiliado_id'),)


class Instituto(models.Model):
    municipio = models.ForeignKey('Municipio', blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instituto'


class Loan(models.Model):
    affiliate = models.ForeignKey(Affiliate, blank=True, null=True)
    capital = models.DecimalField(max_digits=10, decimal_places=2)
    letters = models.TextField(blank=True, null=True)
    debt = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=4, decimal_places=2)
    months = models.IntegerField(blank=True, null=True)
    last = models.DateField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    start_date = models.DateField()
    aproved = models.IntegerField(blank=True, null=True)
    offset = models.IntegerField(blank=True, null=True)
    aproval = models.ForeignKey('TgUser', blank=True, null=True)
    casa = models.ForeignKey(Casa, blank=True, null=True)
    fecha_mora = models.DateField()
    cobrar = models.IntegerField(blank=True, null=True)
    acumulado = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                    null=True)
    vence = models.DateField(blank=True, null=True)
    vencidas = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loan'


class Logger(models.Model):
    user = models.ForeignKey('TgUser', blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    day = models.DateTimeField(blank=True, null=True)
    affiliate = models.ForeignKey(Affiliate, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logger'


class Municipio(models.Model):
    departamento = models.ForeignKey(Departamento, blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'municipio'


class Obligation(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()
    account = models.ForeignKey(Account)
    inprema = models.DecimalField(max_digits=10, decimal_places=2)
    filiales = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                   null=True)
    inprema_compliment = models.DecimalField(max_digits=10, decimal_places=2)
    amount_compliment = models.DecimalField(max_digits=10, decimal_places=2)
    alternate = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'obligation'


class Observacion(models.Model):
    affiliate = models.ForeignKey(Affiliate, blank=True, null=True)
    texto = models.TextField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'observacion'


class OldPay(models.Model):
    payed_loan = models.ForeignKey('PayedLoan', blank=True, null=True)
    day = models.DateField()
    capital = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt = models.TextField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'old_pay'


class Organizacion(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'organizacion'


class OtherAccount(models.Model):
    account = models.ForeignKey(Account, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                 null=True)
    other_report = models.ForeignKey('OtherReport', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'other_account'


class OtherReport(models.Model):
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    cotizacion = models.ForeignKey(Cotizacion, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'other_report'


class PagoBancarioBanhcafe(models.Model):
    identidad = models.CharField(max_length=13, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                   null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    referencia = models.IntegerField(blank=True, null=True)
    agencia = models.IntegerField(blank=True, null=True)
    cajero = models.CharField(max_length=10, blank=True, null=True)
    terminal = models.CharField(max_length=10, blank=True, null=True)
    aplicado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pago_bancario_banhcafe'


class PagoFilial(models.Model):
    filial = models.ForeignKey(Filial, blank=True, null=True)
    dia = models.DateField()
    detalle = models.CharField(max_length=255, blank=True, null=True)
    cheque = models.CharField(max_length=255, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                null=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                null=True)

    class Meta:
        managed = False
        db_table = 'pago_filial'


class Pay(models.Model):
    loan = models.ForeignKey(Loan)
    day = models.DateField(blank=True, null=True)
    capital = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt = models.CharField(max_length=100, blank=True, null=True)
    deposito = models.IntegerField()
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pay'


class PayedDeduction(models.Model):
    payed_loan = models.ForeignKey('PayedLoan', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                 null=True)
    account = models.ForeignKey(Account, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payed_deduction'


class PayedLoan(models.Model):
    affiliate = models.ForeignKey(Affiliate)
    capital = models.DecimalField(max_digits=10, decimal_places=2)
    letters = models.TextField(blank=True, null=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=4, decimal_places=2)
    months = models.IntegerField()
    last = models.DateField(blank=True, null=True)
    start_date = models.DateField()
    debt = models.DecimalField(max_digits=10, decimal_places=2)
    casa = models.ForeignKey(Casa, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payed_loan'


class Permission(models.Model):
    permission_name = models.CharField(unique=True, max_length=16)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permission'


class PostReport(models.Model):
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_report'


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto'


class Rechazo(models.Model):
    affiliate = models.ForeignKey(Affiliate, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    day = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rechazo'


class Recibo(models.Model):
    casa = models.ForeignKey(Casa, blank=True, null=True)
    afiliado = models.IntegerField(blank=True, null=True)
    cliente = models.CharField(max_length=100)
    dia = models.DateTimeField()
    impreso = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recibo'


class ReciboCeiba(models.Model):
    casa = models.ForeignKey(Casa, blank=True, null=True)
    afiliado = models.IntegerField(blank=True, null=True)
    cliente = models.CharField(max_length=100)
    dia = models.DateTimeField()
    impreso = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recibo_ceiba'


class ReciboDanli(models.Model):
    casa = models.ForeignKey(Casa, blank=True, null=True)
    afiliado = models.IntegerField(blank=True, null=True)
    cliente = models.CharField(max_length=100)
    dia = models.DateTimeField()
    impreso = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recibo_danli'


class ReciboSps(models.Model):
    casa = models.ForeignKey(Casa, blank=True, null=True)
    afiliado = models.IntegerField(blank=True, null=True)
    cliente = models.CharField(max_length=100)
    dia = models.DateTimeField()
    impreso = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recibo_sps'


class ReciboTga(models.Model):
    casa_id = models.IntegerField(blank=True, null=True)
    afiliado = models.IntegerField(blank=True, null=True)
    cliente = models.CharField(max_length=100)
    dia = models.DateTimeField()
    impreso = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recibo_tga'


class Reintegro(models.Model):
    affiliate_id = models.IntegerField(blank=True, null=True)
    emision = models.DateField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                null=True)
    cheque = models.CharField(max_length=10, blank=True, null=True)
    planilla = models.CharField(max_length=10, blank=True, null=True)
    motivo = models.CharField(max_length=100, blank=True, null=True)
    forma_pago_id = models.IntegerField(blank=True, null=True)
    pagado = models.IntegerField(blank=True, null=True)
    cancelacion = models.DateField(blank=True, null=True)
    cuenta_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reintegro'


class ReportAccount(models.Model):
    name = models.TextField(blank=True, null=True)
    account_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                 null=True)
    post_report = models.ForeignKey(PostReport, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_account'


class ReporteBancario(models.Model):
    banco = models.ForeignKey(Banco, blank=True, null=True)
    day = models.DateField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reporte_bancario'


class ReversionBancariaBanhcafe(models.Model):
    fecha = models.DateTimeField(blank=True, null=True)
    referencia = models.IntegerField(blank=True, null=True)
    agencia = models.IntegerField(blank=True, null=True)
    terminal = models.CharField(max_length=10, blank=True, null=True)
    cajero = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reversion_bancaria_banhcafe'


class Seguro(models.Model):
    afiliado = models.ForeignKey(Affiliate, blank=True, null=True)
    fecha = models.DateTimeField()
    fallecimiento = models.DateTimeField()
    indemnizacion = models.ForeignKey(Indemnizacion, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seguro'


class Sobrevivencia(models.Model):
    afiliado = models.ForeignKey(Affiliate, blank=True, null=True)
    fecha = models.DateTimeField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    cheque = models.CharField(max_length=20, blank=True, null=True)
    banco = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sobrevivencia'


class Solicitud(models.Model):
    affiliate = models.ForeignKey(Affiliate, blank=True, null=True)
    ingreso = models.DateField(blank=True, null=True)
    entrega = models.DateField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    periodo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'solicitud'


class SqlobjectDbVersion(models.Model):
    version = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sqlobject_db_version'


class TgGroup(models.Model):
    group_name = models.CharField(unique=True, max_length=16)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tg_group'


class TgPermission(models.Model):
    permission_name = models.CharField(unique=True, max_length=16)
    description = models.CharField(max_length=255, blank=True, null=True)
    child_name = models.CharField(max_length=255, blank=True, null=True)
    done_constructing = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tg_permission'


class TgUser(models.Model):
    user_name = models.CharField(unique=True, max_length=16)
    email_address = models.CharField(unique=True, max_length=255)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=40, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    casa = models.ForeignKey(Casa, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tg_user'


class UserGroup(models.Model):
    group = models.ForeignKey(TgGroup)
    user = models.ForeignKey(TgUser)

    class Meta:
        managed = False
        db_table = 'user_group'


class Venta(models.Model):
    recibo = models.ForeignKey(Recibo)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    cantidad = models.IntegerField()
    unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'venta'


class VentaCeiba(models.Model):
    recibo = models.ForeignKey(ReciboCeiba, blank=True, null=True)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.IntegerField()
    unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'venta_ceiba'


class VentaDanli(models.Model):
    recibo = models.ForeignKey(ReciboDanli, blank=True, null=True)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.IntegerField()
    unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'venta_danli'


class VentaSps(models.Model):
    recibo = models.ForeignKey(ReciboSps, blank=True, null=True)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.IntegerField()
    unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'venta_sps'


class VentaTga(models.Model):
    recibo_id = models.IntegerField(blank=True, null=True)
    producto_id = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    cantidad = models.IntegerField()
    unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                   null=True)

    class Meta:
        managed = False
        db_table = 'venta_tga'


class Viatico(models.Model):
    asamblea = models.ForeignKey(Asamblea, blank=True, null=True)
    municipio = models.ForeignKey(Municipio, blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                null=True)
    transporte = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, null=True)
    previo = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                 null=True)
    posterior = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                    null=True)

    class Meta:
        managed = False
        db_table = 'viatico'


class Visit(models.Model):
    visit_key = models.CharField(unique=True, max_length=40)
    created = models.DateTimeField(blank=True, null=True)
    expiry = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visit'


class VisitIdentity(models.Model):
    visit_key = models.CharField(unique=True, max_length=40)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visit_identity'
