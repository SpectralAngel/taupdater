# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bridge.models import Banco, build_obligation_map, Cotizacion, CuotaTable, \
    CuentaRetrasada, Obligation, Extra, obligation_map
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models.aggregates import Min, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.base import RedirectView, View
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from updater.forms import CobroGenerarForm, CotizacionCobroGenerarForm
from updater.models import BankUpdateFile, CotizacionUpdateFile, \
    ComparacionBanco, BancoFaltante
from updater import generators

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
        ).exclude(
            cuenta__exact='',
            active=False,
        ),
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


class CotizacionListView(LoginRequiredMixin, ListView):
    """
    Shows a list of :class:`Cotizacion`
    """
    model = Cotizacion
    template_name = 'updater/cotizacion_list.html'


class CotizacionDetailView(LoginRequiredMixin, DetailView):
    """
    Shows the UI to create payments for :class:`Cotizacion`
    """
    model = Cotizacion
    template_name = 'updater/cotizacion_detail.html'

    def get_context_data(self, **kwargs):
        """
        Adds the form that will create the payment file
        """
        context = super(CotizacionDetailView, self).get_context_data(**kwargs)
        form = CotizacionCobroGenerarForm(initial={
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
            cotizacion.affiliate_set.exclude(
                card_id__isnull=True,
                card_id__iexact='',
                active=False,
            ).prefetch_related(
                'extra_set',
                'loan_set',
            ),
            fecha,
            cobrar_colegiacion
        )

        return generator.generate()


class CotizacionUpdateFileList(LoginRequiredMixin, ListView):
    """
    Displays a list of :class:`CotizacionUpdateFile` that are not yet processed
    """
    model = CotizacionUpdateFile
    paginate_by = 10
    queryset = CotizacionUpdateFile.objects.order_by('-fecha_de_procesamiento')


class CotizacionUpdateFileProcessView(LoginRequiredMixin, RedirectView):
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


class CotizacionUpdateFileCompareView(LoginRequiredMixin, RedirectView):
    """
    Applies the payments file to the :class:`Affiliate`s every payment
    corresponds to.
    """
    permanent = False

    @transaction.atomic
    def get_redirect_url(self, *args, **kwargs):
        cotizacionupdatefile = get_object_or_404(CotizacionUpdateFile,
                                                 pk=kwargs['pk'])
        cotizacionupdatefile.compare()
        messages.info(
            self.request,
            _('Comparación Completada')
        )

        return reverse('cotizacion-file-index')


class CotizacionUpdateFileDetailView(LoginRequiredMixin, DetailView):
    """
    Displays the information associated to a :class:`CotizacionUpdateFile`
    """
    model = CotizacionUpdateFile
    queryset = CotizacionUpdateFile.objects.select_related(
        'cotizacion'
    ).prefetch_related(
        'errorcomparacioncotizacion_set',
        'errorlecturacotizacion_set',
    )


class RetrasadasCrearView(LoginRequiredMixin, RedirectView):
    """
    Calculates the delayed payments for the every :class:`Affiliate`.
    """
    permanent = False

    @transaction.atomic
    def get_redirect_url(self, *args, **kwargs):
        cotizacion = get_object_or_404(Cotizacion, pk=kwargs['pk'])
        years = {}
        first_year = CuotaTable.objects.aggregate(
            minimo=Min('year')
        )['minimo']
        current_year = timezone.now().year
        current_month = timezone.now().month

        for n in range(first_year, current_year + 1):
            years[n] = {}
            for m in range(1, 13):
                if n == current_year and m >= current_month:
                    break
                years[n][m] = {}

                try:
                    years[n][m]['cuenta'] = CuentaRetrasada.objects.filter(
                        mes=m,
                        anio=n,
                    ).first().account
                    years[n][m]['obligacion'] = Obligation.objects.filter(
                        month=m,
                        year=n,
                    ).aggregate(
                        total=Sum('amount')
                    )['amount']
                except:
                    print(n, m)

        extras = []

        for afiliado in cotizacion.affiliate_set.all():
            cuota = afiliado.get_delayed()
            if cuota:
                mes = cuota.delayed()
                anio = cuota.year
                cuenta = years[anio][mes]['cuenta']
                if afiliado.active:
                    monto = obligation_map[anio][mes]['active']
                elif afiliado.jubilated is not None and afiliado.jubilated.year < anio:
                    monto = obligation_map[anio][mes]['retired']
                else:
                    monto = obligation_map[anio][mes]['active']

                extra = Extra()
                extra.affiliate = afiliado
                extra.mes = mes
                extra.anio = anio
                extra.amount = monto
                extra.retrasada = True
                extra.account = cuenta
                extras.append(extra)

        Extra.objects.bulk_create(extras)

        messages.info(
            self.request,
            _('Calculo de retrasadas completado')
        )

        return reverse('cotizacion-update-detail', args=[cotizacion.id])


class ComparacionBancoListView(LoginRequiredMixin, ListView):
    """
    Shows a list of file available to make comparisons
    """
    model = ComparacionBanco


class ComparacionBancoDetailView(LoginRequiredMixin, DetailView):
    """
    Shows the data for a :class:`ComparacionBanco`
    """
    model = ComparacionBanco


class ComparacionBancoProcessView(LoginRequiredMixin, RedirectView):
    """
    Applies the payments file to the :class:`Affiliate`s every payment
    corresponds to.
    """
    permanent = False

    @transaction.atomic
    def get_redirect_url(self, *args, **kwargs):
        comparacion = get_object_or_404(ComparacionBanco, pk=kwargs['pk'])
        comparacion.process()
        messages.info(
            self.request,
            _('Actualización Completada')
        )

        return comparacion.get_absolute_url()


class BancoFaltanteListView(LoginRequiredMixin, ListView):
    """
    Shows a list of the files that have failure from charging
    """
    model = BancoFaltante


class BancoFaltanteCobroView(LoginRequiredMixin, View):
    """
    Applies the payments file to the :class:`Affiliate`s every payment
    corresponds to.
    """

    def dispatch(self, *args, **kwargs):
        self.faltante = get_object_or_404(BancoFaltante, pk=kwargs['pk'])

        return super(BancoFaltanteCobroView, self).dispatch(*args, **kwargs)

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        afiliados = self.faltante.afiliados()
        print(afiliados)
        banco = self.faltante.banco

        gen_class = getattr(generators, banco.generator, generators.Generator)
        generator = gen_class(
            banco,
            afiliados,
            self.faltante.fecha_de_cobro,
            self.faltante.cobrar_colegiacion,
        )

        return generator.generate()


class BancoFaltanteClientView(LoginRequiredMixin, View):
    """
    Applies the payments file to the :class:`Affiliate`s every payment
    corresponds to.
    """

    def dispatch(self, *args, **kwargs):
        self.faltante = get_object_or_404(BancoFaltante, pk=kwargs['pk'])

        return super(BancoFaltanteClientView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        afiliados = self.faltante.afiliados()
        banco = self.faltante.banco

        gen_class = getattr(generators, banco.generator, generators.Generator)
        generator = gen_class(
            banco,
            afiliados,
            self.faltante.fecha_de_cobro,
            self.faltante.cobrar_colegiacion,
        )

        return generator.clients()
