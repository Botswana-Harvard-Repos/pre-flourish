import imp
import re

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

# from ...model_wrappers import MaternalDatasetModelWrapper

from ...model_wrappers import PreflourishCaregiverLocatorModelWrapper

class PreFlourishCaregiverLocatorListBoardView(
        NavbarViewMixin, EdcBaseViewMixin,
        ListboardFilterViewMixin, SearchFormViewMixin,
        ListboardView):
    listboard_template = 'pre_flourish_caragiver_locator_listboard_template'
    listboard_url = 'pre_flourish_caregiver_locator_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"
    model = 'flourish_caregiver.caregiverlocator'
    model_wrapper_cls = PreflourishCaregiverLocatorModelWrapper
    # listboard_view_filters = ListboardViewFilters()
    navbar_name = 'pre_flourish_dashboard'
    # navbar_selected_item = 'pre_flourish_caregiver_locator'
    # ordering = '-locatorlog__locatorlogentry__report_datetime'
    paginate_by = 10
    search_form_url = 'pre_flourish_caregiver_locator_listboard_url'
    protocol = 'Tshilo Dikotla'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # def get_queryset(self):

    #     participants = super(PreFlourishMaternalDatasetListBoardView, self).get_queryset().filter(
    #         protocol=self.protocol)

    #     return participants

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            maternal_locator_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('screening_identifier'):
            options.update(
                {'screening_identifier': kwargs.get('screening_identifier')})
        if kwargs.get('study_maternal_identifier'):
            options.update(
                {'study_maternal_identifier': kwargs.get('study_maternal_identifier')})
        return options

    def extra_search_options(self, search_term):
        breakpoint()
        q = Q()
        if search_term:
            q = Q(study_maternal_identifier__iexact=search_term)
        return q
