# -*- coding: utf8 -*-
from __future__ import unicode_literals

from decimal import Decimal

import unicodecsv
from bridge.models import CobroBancarioBanhcafe
from django.http import StreamingHttpResponse


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def filter_rows(rows):
    rows = [l for l in rows if
            l[0] is not None and l[1] is not None and l[2] is not None and
            l[3] is not None]
    return rows


def create_csv_response(rows, nombre):
    writer = unicodecsv.writer(Echo())
    response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                     content_type="text/csv")
    response[
        'Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(
        nombre
    )
    return response


def create_text_response(rows, nombre):
    response = StreamingHttpResponse(content_type="text")
    response[
        'Content-Disposition'] = 'attachment; filename="{0}.txt"'.format(
        nombre
    )
    [response.write(row) for row in rows]
    return response


class Generator(object):
    def __init__(self, banco, afiliados, fecha):
        self.afiliados = afiliados
        self.fecha = fecha
        self.banco = banco

    def generate(self):
        """
        Creates the file ready to download with the deduction data
        :return: A StreamingHttpResponse that contains the generated File
        """

        rows = ([str(a.id),
                 "{0} {1}".format(a.first_name, a.last_name),
                 a.cardID,
                 a.get_monthly(self.fecha, True),
                 a.cuenta]
                for a in self.afiliados)

        rows = filter_rows(rows)

        return create_csv_response(rows, self.banco)

    def davivienda(self):
        rows = ([a.id,
                 a.cardID.replace('-', ''),
                 "{0} {1}".format(a.first_name, a.last_name),
                 a.get_monthly(self.fecha, True),
                 0,
                 0,
                 a.get_monthly(self.fecha, True),
                 ]
                for a in self.afiliados)
        rows = filter_rows(rows)

        return create_csv_response(rows, self.banco.nombre)

    def cobros(self):
        rows = ([a.id,
                 a.card_id.replace('-', ''),
                 "{0} {1}".format(a.fist_name, a.last_name),
                 str(a.get_monthly(self.fecha)),
                 a.phone,
                 a.email,
                 a.get_monthly(),
                 ]
                for a in self.afiliados)
        rows = filter_rows(rows)

        return create_csv_response(rows, self.banco.nombre)


class Occidente(Generator):
    def __init__(self, banco, afiliados, fecha):

        super(Occidente, self).__init__(banco, afiliados, fecha)
        self.format = "{0:012d}{1:18}{2:12d}{3:<30}{4:<20}{5:04d}{6:02d}{7:02d}{8:013d} \n"
        month = self.fecha.month + 3
        year = self.fecha.year
        if month > 12:
            month -= 12
            year += 1
        self.fecha_cuota = self.fecha
        self.fecha = self.fecha.replace(year=year, month=month)

    def generate(self):
        """
        Creates the file ready to download with the deduction data
        :return: A StreamingHttpResponse that contains the generated File
        """
        rows = []

        for afiliado in self.afiliados:
            row = self.format.format(
                int(self.banco.cuenta),
                int(self.banco.codigo),
                int(afiliado.cuenta),
                afiliado.card_id,
                afiliado.id,
                self.fecha.year,
                self.fecha.month,
                self.fecha.day,
                int(afiliado.get_monthly(
                    self.fecha_cuota, True
                ) * Decimal("100"))
            )
            rows.append(row)

        return create_text_response(rows, self.banco.nombre)


class Atlantida(Generator):
    def __init__(self, banco, afiliados, fecha):

        super(Atlantida, self).__init__(banco, afiliados, fecha)
        self.cformat = "{0:<16}{1:2}{2:1}{3:05d}{4:8}{5:15}{6:40}"
        self.cformat += "{7:3}{8:40}{9:19}{10:12}{11:2}{12:03d}{13:16}\n"

        self.format = "{0:05d}{1:<16}{2:<16}{3:03d}{4:016d}{5:3}{6:<40}"
        self.format += "{7:<9}{8:<9}\n"

    def clients(self):

        clients = []

        for afiliado in self.afiliados:
            if not afiliado.autorizacion:
                continue

            nombre_afiliado = "{0} {1}".format(afiliado.first_name,
                                               afiliado.last_name)
            if len(nombre_afiliado) > 40:
                nombre_afiliado = nombre_afiliado[:39]

            clients.append(self.cformat.format(
                afiliado.id,
                "01",
                "A",
                int(self.banco.codigo),
                0,
                afiliado.cardID,
                afiliado.get_email(),
                "LPS",
                nombre_afiliado,
                afiliado.cuenta,
                afiliado.get_phone(),
                "AH",
                1,
                ""
            ))

        return create_text_response(clients, self.banco.nombre)

    def generate(self):
        charges = []

        for afiliado in self.afiliados:
            if not afiliado.autorizacion:
                continue
            charges.append(self.format.format(
                int(self.banco.codigo),
                afiliado.id,
                "",
                1,
                int(afiliado.get_monthly(self.fecha, True) * Decimal(
                    "100")),
                "LPS",
                "Cuota de Aportaciones COPEMH",
                '',
                '',
            ))

        return create_text_response(charges, self.banco.nombre)


class INPREMA(Generator):
    def __init__(self, afiliados, fecha, append=False):

        super(INPREMA, self).__init__(None, afiliados, fecha)
        self.format = "{0:4d}{1:02d}{2:13}00011{3:013}\n"
        self.append = append

    def generate(self):
        identidad = 0
        rows = []

        for afiliado in self.afiliados:
            if afiliado.cardID is None or afiliado.cardID == '0':
                identidad += 1
                continue

            rows.append(
                (
                    self.fecha.year,
                    self.fecha.month,
                    afiliado.card_id.replace('-', ''),
                    11,
                    afiliado.get_monthly(self.fecha)
                )
            )

        return create_csv_response(rows, self.banco)


class Banhcafe(Generator):

    def generate(self):
        CobroBancarioBanhcafe.objects.all().delete()
        for afiliado in self.afiliados:
            cobro = CobroBancarioBanhcafe(
                cantidad=afiliado.get_monthly(),
                identidad=afiliado.cardID.replace('-', '')
            )
            cobro.save()


class Pais(Generator):
    def __init__(self, banco, afiliados, fecha):
        super(Pais, self).__init__(banco, afiliados, fecha)

    def generate(self):
        rows = ([str(a.id),
                 a.cardID.replace('-', ''),
                 "{0} {1}".format(a.firstName, a.lastName),
                 str(a.cuenta),
                 str(a.bancario),
                 str(a.get_monthly(self.fecha, True)),
                 str(a.last)] for a in self.afiliados
                if a.autorizacion)

        return create_csv_response(rows, self.banco)


class Ficensa(Generator):
    def __init__(self, banco, afiliados, fecha):

        super(Ficensa, self).__init__(banco, afiliados, fecha)
        self.format = "{0}{1:13}APO{02:8d}{3:<40}{4:<20}{5:08d} {6:015d}\n"

    def generator(self):

        charges = []

        for afiliado in self.afiliados:
            nombre_afiliado = "{0} {1}".format(afiliado.first_name,
                                               afiliado.last_name)
            if len(nombre_afiliado) > 40:
                nombre_afiliado = nombre_afiliado[:39]

            charges.append(self.format.format(
                self.fecha.strftime("%Y%m"),
                afiliado.card_id.replace('-', ''),
                int(afiliado.get_monthly(self.fecha, True) * Decimal(
                    "100")),
                nombre_afiliado,
                'Aportaciones',
                afiliado.id,
                int(afiliado.cuenta),
            )
            )

        return create_text_response(charges, self.banco.nombre)


class UPN(Generator):
    def __init__(self, afiliados, fecha):
        super(UPN, self).__init__(None, afiliados, fecha)
        self.afiliados = afiliados

    def generate(self):
        line = ([a.cardID,
                 "{0} {1}".format(a.first_name, a.last_name),
                 a.escalafon,
                 a.get_monthly(self.fecha, True)] for a in self.afiliados)

        rows = filter_rows(line)

        return create_csv_response(rows, self.banco.nombre)


class Trabajadores(Generator):
    def generate(self):
        line = ([a.id,
                 "{0} {1}".format(a.first_name, a.last_name),
                 a.cardID,
                 a.get_monthly(self.fecha, True, True),
                 '50',
                 a.cuenta
                 ] for a in self.afiliados)

        rows = filter_rows(line)

        return create_csv_response(rows, self.banco.nombre)
