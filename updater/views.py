# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bridge.models import Banco, build_obligation_map
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.base import RedirectView
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from updater.forms import CobroGenerarForm
from updater.models import BankUpdateFile
import generators

build_obligation_map()


class BankUpdateFileDetailView(LoginRequiredMixin, DetailView):
    model = BankUpdateFile


class BankUpdateFileListView(LoginRequiredMixin, ListView):
    """
    Shows the List of :class:`BankUpdateFiles that have not been processed yet.
    """
    model = BankUpdateFile
    queryset = BankUpdateFile.objects.filter(procesado=False)


class BankUpdateFileProcess(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        bankupdatefile = get_object_or_404(BankUpdateFile, pk=kwargs['pk'])
        bankupdatefile.process()
        messages.info(
            self.request,
            _('Actualización Completada')
        )

        return reverse('bank-update-file-index')


class BancoListView(LoginRequiredMixin, ListView):
    """
    Shows the UI to handle the :class:`Banco`
    """
    model = Banco
    template_name = 'updater/bank_list.html'


class BancoDetailView(LoginRequiredMixin, DetailView):
    """
    Displays the :class:`Banco` data along with the forms to make te billing
    statements
    """
    model = Banco
    template_name = 'updater/bank_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BancoDetailView, self).get_context_data(**kwargs)
        form = CobroGenerarForm(initial={
            'banco': self.object
        })
        form.helper.form_action = 'banco-bill'
        form.set_legend(_('Crear Archivo de Cobro'))

        context['form'] = form

        return context


class BancoBillingView(LoginRequiredMixin, FormView):
    """
    Creates the billing for the specified :class:`Banco`
    """
    form_class = CobroGenerarForm

    def form_valid(self, form):
        banco = form.cleaned_data['banco']
        fecha = form.cleaned_data['fecha']

        gen_class = getattr(generators, banco.generator, generators.Generator)

        generator = gen_class(banco, banco.affiliate_set.all(), fecha)

        return generator.generate()
