from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .pre_flourish_caregiver_locator_model_wrapper import PreFlourishCaregiverLocatorModelWrapper


class PreFlourishCaregiverLocatorModelWrapperMixin:

    locator_model_wrapper_cls = PreFlourishCaregiverLocatorModelWrapper

    @property
    def locator_model_obj(self):
        """Returns a caregiver locator model instance or None.
        """
        try:
            return self.caregiver_locator_cls.objects.get(
                **self.caregiver_locator_options)
        except ObjectDoesNotExist:
            return None

    @property
    def caregiver_locator(self):
        """"Returns a wrapped saved or unsaved caregiver locator
        """
        model_obj = self.locator_model_obj or self.caregiver_locator_cls(
            **self.create_caregiver_locator_options)
        return PreFlourishCaregiverLocatorModelWrapper(model_obj=model_obj)

    @property
    def caregiver_locator_cls(self):
        return django_apps.get_model('pre_flourish.caregiverlocator')

    @property
    def create_caregiver_locator_options(self):
        """Returns a dictionary of options to create a new
        unpersisted caregiver locator model instance.
        """
        options = dict(
            screening_identifier=self.object.screening_identifier, )
        return options

    @property
    def caregiver_locator_options(self):
        """Returns a dictionary of options to get an existing
         caregiver locator model instance.
        """
        options = dict(
            screening_identifier=self.object.screening_identifier, )
        return options
