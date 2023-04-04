from django import forms
from edc_base.sites.forms import SiteModelFormMixin

from pre_flourish.models.child.offschedule import ChildOffSchedule


class ChildOffScheduleForm(SiteModelFormMixin, forms.ModelForm):
    class Meta:
        model = ChildOffSchedule
        fields = '__all__'
