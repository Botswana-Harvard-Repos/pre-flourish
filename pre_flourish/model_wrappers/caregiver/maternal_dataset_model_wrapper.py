from django.apps import apps as django_apps
from django.conf import settings
from django.db.models import Q
from edc_model_wrapper import ModelWrapper
from flourish_caregiver.models import LocatorLogEntry
from flourish_dashboard.model_wrappers import SubjectConsentModelWrapper, LocatorLogEntryModelWrapper
from flourish_dashboard.model_wrappers.bhp_prior_screening_model_wrapper_mixin import BHPPriorScreeningModelWrapperMixin
from flourish_dashboard.model_wrappers.caregiver_locator_model_wrapper_mixin import CaregiverLocatorModelWrapperMixin
from flourish_dashboard.model_wrappers.consent_model_wrapper_mixin import ConsentModelWrapperMixin
from flourish_follow.models import LogEntry, InPersonContactAttempt

from pre_flourish.model_wrappers.caregiver.maternal_screening_model_wrapper_mixin import \
    MaternalScreeningModelWrapperMixin


class MaternalDatasetModelWrapper(ConsentModelWrapperMixin,
                                  CaregiverLocatorModelWrapperMixin,
                                  BHPPriorScreeningModelWrapperMixin,
                                  MaternalScreeningModelWrapperMixin,
                                  ModelWrapper):
    consent_model_wrapper_cls = SubjectConsentModelWrapper

    model = 'flourish_caregiver.maternaldataset'
    querystring_attrs = [
        'screening_identifier', 'subject_identifier',
        'study_maternal_identifier', 'study_child_identifier']
    next_url_attrs = ['study_maternal_identifier', 'screening_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'maternal_dataset_listboard_url')

    @property
    def screening_identifier(self):
        if self.object:
            return self.object.screening_identifier
        return None

    @property
    def consent_version(self):
        version = None
        try:
            consent_version_obj = self.consent_version_cls.objects.get(
                screening_identifier=self.bhp_prior_screening.screening_identifier)
        except self.consent_version_cls.DoesNotExist:
            version = '1'
        else:
            version = consent_version_obj.version
        return version

    @property
    def log_entries(self):
        locator_log = getattr(self.object, 'locatorlog')
        wrapped_entries = []
        log_entries = LocatorLogEntry.objects.filter(
            locator_log=locator_log)
        for log_entry in log_entries:
            wrapped_entries.append(
                LocatorLogEntryModelWrapper(log_entry))

        return wrapped_entries

    @property
    def call_or_home_visit_success(self):
        """Returns true if the call or home visit was a success.
        """
        log_entries = LogEntry.objects.filter(
            ~Q(phone_num_success='none_of_the_above'),
            study_maternal_identifier=self.object.study_maternal_identifier,
            phone_num_success__isnull=False)
        home_visit_logs = InPersonContactAttempt.objects.filter(
            ~Q(successful_location='none_of_the_above'),
            study_maternal_identifier=self.object.study_maternal_identifier,
            successful_location__isnull=False)
        if log_entries:
            return True
        elif home_visit_logs:
            return True
        return False

    @property
    def locator_exists(self):
        locator_log = getattr(self.object, 'locatorlog')
        exists = False
        if (LocatorLogEntry.objects.filter(locator_log=locator_log, log_status='exist') or
                self.locator_model_obj):
            exists = True
        return exists

    @property
    def log_entry(self):
        locator_log = getattr(self.object, 'locatorlog')
        log_entry = LocatorLogEntry(locator_log=locator_log)
        return LocatorLogEntryModelWrapper(log_entry)

    @property
    def contact_attempts(self):
        return False

    @property
    def screening_report_datetime(self):
        if self.bhp_prior_screening_model_obj:
            return self.bhp_prior_screening_model_obj.report_datetime

    @property
    def multiple_births(self):
        """Returns value of births if the mother has twins/triplets.
        """
        if self.object:
            child_dataset_cls = django_apps.get_model(
                'flourish_child.childdataset')
            children = child_dataset_cls.objects.filter(
                study_maternal_identifier=self.object.study_maternal_identifier)
            return children.count()
        return 0

    @property
    def is_td_onstudy(self):
        """Returns true if participant is TD prior and is still onstudy
        """
        child_dataset_cls = django_apps.get_model(
            'flourish_child.childdataset')
        if self.object and self.object.protocol == 'Tshilo Dikotla':
            try:
                child_datase_obj = child_dataset_cls.objects.get(
                    study_maternal_identifier=self.object.study_maternal_identifier)
            except child_dataset_cls.DoesNotExist:
                pass
            else:
                return child_datase_obj.infant_offstudy_complete == 0
        return False

    @property
    def screening(self):
        """"Returns a wrapped saved or unsaved bhp prior screening
        """
        model_obj = self.bhp_prior_screening_model_obj or self.bhp_prior_screening_cls(
            **self.create_bhp_prior_screening_options)
        return self.prior_screening_model_wrapper_cls(model_obj=model_obj)

    @property
    def screening_model_obj(self):
        """Returns a bhp prior model instance or None.
        """
        try:
            return self.bhp_prior_screening_cls.objects.get(
                **self.bhp_prior_screening_options)
        except ObjectDoesNotExist:
            return None

    @property
    def create_screening_options(self):
        """Returns a dictionary of options to create a new
        unpersisted bhp prior screening model instance.
        """
        options = dict(
            screening_identifier=self.object.screening_identifier, )
        return options
