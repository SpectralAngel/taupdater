# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.base import RedirectView
from django.utils.translation import ugettext_lazy as _

from updater.models import BankUpdateFile


class BankUpdateFileDetailView(DetailView):
    model = BankUpdateFile


class BankUpdateFileListView(ListView):
    model = BankUpdateFile
    queryset = BankUpdateFile.objects.filter(procesado=False)


class BankUpdateFileProcess(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):

        bankupdatefile = get_object_or_404(BankUpdateFile, pk=kwargs['pk'])
        bankupdatefile.process()
        messages.info(
            self.request,
            _(u'Actualización Completada')
        )

        return reverse('bank-update-file-index')
