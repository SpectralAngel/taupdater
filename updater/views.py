# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bridge.models import Banco, build_obligation_map, Cotizacion
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.base import RedirectView
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from updater.forms import CobroGenerarForm, CotizacionCobroGenerarForm
from updater.models import BankUpdateFile, CotizacionUpdateFile
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
    """
    Applies the payments file to the :class:`Affiliate`s every payment
    corresponds to.
    """
    permanent = False

    @transaction.atomic
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

        form = CobroGenerarForm(
            prefix='clients',
            initial={'banco': self.object}
        )
        form.helper.form_action = 'banco-client'
        form.set_legend(_('Crear Archivo de Clientes'))

        context['clients_form'] = form

        return context


def build_generator(banco, cobrar_colegiacion, fecha):
    gen_class = getattr(generators, banco.generator, generators.Generator)
    generator = gen_class(
        banco,
        banco.affiliate_set.filter(
            cuenta__isnull=False,
        ).exclude(cuenta__exact=''),
        fecha,
        cobrar_colegiacion
    )
    return generator


class BancoBillingView(LoginRequiredMixin, FormView):
    """
    Creates the billing for the specified :class:`Banco`
    """
    form_class = CobroGenerarForm

    def form_valid(self, form):
        banco = form.cleaned_data['banco']
        fecha = form.cleaned_data['fecha']
        cobrar_colegiacion = form.cleaned_data['cobrar_colegiacion']

        generator = build_generator(banco, cobrar_colegiacion, fecha)

        return generator.generate()


class BancoClientView(LoginRequiredMixin, FormView):
    """
    Creates the billing for the specified :class:`Banco`
    """
    form_class = CobroGenerarForm
    prefix = 'clients'

    def form_valid(self, form):
        banco = form.cleaned_data['banco']
        fecha = form.cleaned_data['fecha']
        cobrar_colegiacion = form.cleaned_data['cobrar_colegiacion']

        generator = build_generator(banco, cobrar_colegiacion, fecha)

        return generator.clients()


class CotizacionDetail(LoginRequiredMixin, DetailView):
    """
    Shows the UI to create payments for :class:`Cotizacion`
    """
    model = Cotizacion

    def get_context_data(self, **kwargs):
        """
        Adds the form that will create the payment file
        """
        context = super(CotizacionDetail, self).get_context_data(**kwargs)
        form = CobroGenerarForm(initial={
            'cotizacion': self.object
        })
        form.helper.form_action = 'cotizacion-bill'
        form.set_legend(_('Crear Archivo de Cobro'))

        context['form'] = form

        return context


class CotizacionBillingView(LoginRequiredMixin, FormView):
    """
    Creates the billing for an specific :class:`Cotizacion`
    """
    form_class = CotizacionCobroGenerarForm

    def form_valid(self, form):
        cotizacion = form.cleaned_data['cotizacion']
        fecha = form.cleaned_data['fecha']
        cobrar_colegiacion = form.cleaned_data['cobrar_colegiacion']

        gen_class = getattr(generators, cotizacion.generator,
                            generators.Generator)
        generator = gen_class(
            cotizacion,
            cotizacion.affiliate_set.all(),
            fecha,
            cobrar_colegiacion
        )

        return generator.clients()


class CotizacionUpdateFileList(LoginRequiredMixin, ListView):
    """
    Displays a list of :class:`CotizacionUpdateFile` that are not yet processed
    """
    model = CotizacionUpdateFile
    queryset = CotizacionUpdateFile.objects.filter(procesado=False)


class CotizacionUpdateFileProcess(LoginRequiredMixin, RedirectView):
    """
    Applies the payments file to the :class:`Affiliate`s every payment
    corresponds to.
    """
    permanent = False

    @transaction.atomic
    def get_redirect_url(self, *args, **kwargs):
        cotizacionupdatefile = get_object_or_404(CotizacionUpdateFile,
                                                 pk=kwargs['pk'])
        cotizacionupdatefile.process()
        messages.info(
            self.request,
            _('Actualización Completada')
        )

        return reverse('cotizacion-file-index')
