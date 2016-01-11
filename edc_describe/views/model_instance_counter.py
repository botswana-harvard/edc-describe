from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from ..classes import ModelInstanceCounter
from ..forms import ModelInstanceCounterForm


@login_required
def model_instance_counter(request, **kwargs):

    section_name = kwargs.get('section_name')
    report_title = 'Model Instance Counts'
    template = 'model_instance_counter.html'

    if request.method == 'POST':

        form = ModelInstanceCounterForm(request.POST)

        if form.is_valid():

            producer = form.cleaned_data['producer']
            app_label = form.cleaned_data['app_label']
            key_field = form.cleaned_data['key_field']

            app_and_field = {'app_label': app_label, 'key_field': key_field}

            counter = ModelInstanceCounter(producer, app_and_field)

            context = {
                'form': form,
                'app_label': app_label,
                'key_field': key_field,
                'producer': producer,
                'result': counter.get(),
                'section_name': section_name,
                'app_name': settings.APP_NAME,
                'report_title': report_title,
                }

        return render_to_response(template, context, context_instance=RequestContext(request))

    else:

        form = ModelInstanceCounterForm(request.GET)
        app_label = request.GET.get('app_label', None)
        key_field = request.GET.get('key_field', None)
        producer = request.GET.get('producer', None)

    return render_to_response(template, {
                'form': form,
                'app_label': app_label,
                'key_field': key_field,
                'producer': producer,
                'result': {},
                'section_name': section_name,
                'app_name': settings.APP_NAME,
                'report_title': report_title,
                }, context_instance=RequestContext(request))
