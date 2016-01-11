from django.conf.urls import url, patterns

from .views import model_data_inspector_view, model_instance_counter

urlpatterns = patterns('',
    url(r'^(?P<app_label>\w+)/(?P<model_name>\w+)/$',
        model_data_inspector_view,
        name="model_data_inspector_url_name"
        ),

    url(r'^(?P<app_label>\w+)/$',
        model_data_inspector_view,
        name="model_data_inspector_url_name"
        ),

    url(r'^counter/',
        model_instance_counter,
        name="model_instance_counter_url_name"
        ),

    url(r'',
        model_data_inspector_view,
        name="model_data_inspector_url_name"
        ),
    )
