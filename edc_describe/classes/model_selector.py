from django.db.models import get_model, get_models
from django.conf import settings


class ModelSelector(object):

    def __init__(self, app_label, model_name):

        self._app_label = None
        self._model_name = None
        self._app_labels = None
        self._model_names = None

        self.set_app_label(app_label)
        self.set_model_name(model_name)
        self.set_model()
        self.set_app_labels()
        self.set_model_names()

    def set_app_label(self, value):
        if value not in settings.INSTALLED_APPS:
            self._app_label = value
        if not self._app_label:
            raise AttributeError('Attribute app_label may not be None.')

    def get_app_label(self):
        return self._app_label

    def set_model_name(self, value):
        self._model_name = value.replace('_', '')  # make it object_name
        if not self._model_name:
            raise AttributeError('Attribute model_name may not be None.')

    def get_model_name(self):
        return self._model_name

    def set_model(self):
        self._model = get_model(self.get_app_label(), self.get_model_name())
        if not self._model:
            AttributeError(
                'Could not get model for app_label={0}, model_name={1}.'.format(
                    self.get_app_label(), self.get_model_name()))

    def get_model(self):
        return self._model

    def set_app_labels(self):
        self._app_labels = [
            model._meta.app_label for model in get_models() if model._meta.app_label not in [
                'contenttypes', 'admin', 'auth', 'sites', 'sessions', 'south']]
        self._app_labels = list(set(self._app_labels))
        self._app_labels.sort()

    def get_app_labels(self):
        return self._app_labels

    def set_model_names(self):
        self._model_names = [
            {'module_name': model._meta.module_name, 'verbose_name': model._meta.verbose_name}
            for model in get_models() if model._meta.app_label == self.get_app_label() and
            model._meta.verbose_name[-5:] != 'audit']

    def get_model_names(self):
        return self._model_names
