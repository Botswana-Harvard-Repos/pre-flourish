from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from ..models import PreFlourishVisit


class PreFlourishVisitForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = PreFlourishVisit
        fields = '__all__'
