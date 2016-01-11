from django.db import models
from django.conf import settings


class ModelInstanceCounter(object):

    def __init__(self, producer, app_and_field={}):

        self.producer = producer
        self.app_and_field = app_and_field
        self.result = {}
        self.model_list = []

    def _set(self):
        # for app_label, key_field in self.app_and_field.iteritems():
        # check if app_label is in settings.INSTALLED_APPS
        app_labels = []
        if self.app_and_field['app_label'] in settings.INSTALLED_APPS:
            app_labels.append(self.app_and_field['app_label'])
        else:
            # if not do a search with the string
            for app in settings.INSTALLED_APPS:
                if self.app_and_field['app_label'] in app:
                    app_labels.append(app)
        app_labels.sort()
        self.model_list = {}

        for app_label in app_labels:
            key_field = self.app_and_field['key_field']
            self. model_list[app_label] = [{'verbose_name': model._meta.verbose_name, 'object_name': model._meta.object_name, 'model':model}
                                    for model in models.get_models()
                                    if (model._meta.app_label in app_label)
                                    and key_field in
                                    [field.name for field in model._meta.fields]
                                    and '_audit_id' not in
                                    [field.name for field in model._meta.fields]]
        for app_label, result in self.model_list.iteritems():
            counts = []
            for r in result:
                counts.append([r['verbose_name'], r['object_name'].lower(), r['model'].objects.filter(hostname_created=self.producer).count()])
            counts.sort()
            self.result[app_label] = counts

    def get(self):
        if not self.result:
            self._set()

        return self.result
