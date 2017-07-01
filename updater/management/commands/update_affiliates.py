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
        for archivo in options['file']:
            with open(archivo, 'rU') as source:
                reader = csv.reader(source)

                for line in reader:
                    afiliado = Affiliate.objects.get(pk=int(line[0]))
                    afiliado.joined = datetime.strptime(line[4], '%d/%m/%Y')
                    afiliado.save()
