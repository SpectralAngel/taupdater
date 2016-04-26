# -*- coding: utf8 -*-
from __future__ import unicode_literals

from bootstrap3_datetime.widgets import DateTimePicker
from bridge.models import Banco, Cotizacion
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Submit
from django import forms
from django.utils.translation import ugettext_lazy as _


class FieldSetFormMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FieldSetFormMixin, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.html5_required = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-7'
        self.field_names = self.fields.keys()

    def set_legend(self, text):
        self.helper.layout = Fieldset(text, *self.field_names)

    def set_action(self, action):
        self.helper.form_action = action


class CobroGenerarForm(FieldSetFormMixin):
    """
    Builds a form that allows the user to generate files to be sent to financial
    institutions for payment.
    """
    banco = forms.ModelChoiceField(Banco.objects.all(),
                                   widget=forms.HiddenInput())
    fecha = forms.DateField(widget=DateTimePicker(
        options={"format": "YYYY-MM-DD"})
    )
    cobrar_colegiacion = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(CobroGenerarForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', _('Generar')))


class CotizacionCobroGenerarForm(FieldSetFormMixin):
    """
    Builds a form that allows the user to generate files that will be sent to
    external institutions to collect payment.
    """
    cotizacion = forms.ModelChoiceField(Cotizacion.objects.all(),
                                        widget=forms.HiddenInput())
    fecha = forms.DateField(widget=DateTimePicker(
        options={"format": "YYYY-MM-DD"})
    )
    cobrar_colegiacion = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(CotizacionCobroGenerarForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', _('Generar')))
