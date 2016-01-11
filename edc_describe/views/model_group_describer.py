from django.conf import settings

from .base_model_group_describer import base_model_group_describer


def model_group_describer(request, **kwargs):

    if not 'APP_NAME' in dir(settings):
        raise KeyError('Cannot find key \'APP_NAME\' in settings file. e.g APP_NAME=\'maikalelo\'')
    if not 'SUBJECT_APP_LIST' in dir(settings):
        raise KeyError('Cannot find key \'SUBJECT_APP_LIST\' in settings file. e.g SUBJECT_APP_LIST=[\'maikalelo_maternal\',]')
    return base_model_group_describer(request, app_name=settings.APP_NAME, app_list=settings.SUBJECT_APP_LIST, **kwargs)
