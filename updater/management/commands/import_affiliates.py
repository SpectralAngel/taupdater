# -*- coding: utf8 -*-
from datetime import datetime

from bridge.models import Affiliate
from django.core.management.base import BaseCommand
import unicodecsv as csv


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        reader = csv.reader(open(options['file'], 'rU'))

        afiliados = []

        for line in reader:
            afiliado = Affiliate()
            afiliado.first_name = line[0]
            afiliado.last_name = line[1]
            afiliado.card_id = line[2]
            afiliado.joined = datetime.strptime(line[3], '%d/%m/%Y')
            afiliados.append(afiliado)

        Affiliate.objects.bulk_create(afiliados)
