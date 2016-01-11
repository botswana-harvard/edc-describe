from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from edc.dashboard.section.classes import site_sections

from ..classes import ModelSelector
from ..forms import ModelSelectorForm

from ..classes import ModelDataInspector


@login_required
def model_data_inspector_view(request, **kwargs):

    section_name = 'reports'
    template = 'model_data_inspector.html'
    app_label = kwargs.get('app_label')
    model_name = kwargs.get('model_name')
    report_title = ''
    form = ModelSelectorForm()
    context = {
        'sections': site_sections.get_indexed_section_tuples(),
        'form': form,
        'table': '',
        'section_name': section_name,
        'selected_section': section_name,
        'report_title': report_title,
        'report': '',
        'report_name': kwargs.get('report_name'),
        }

    if request.method == 'POST' or (app_label and model_name):
        form = ModelSelectorForm(request.POST or {'app_label': app_label, 'model_name': model_name})
        if form.is_valid():
            app_label = form.cleaned_data.get('app_label') or app_label
            model_name = form.cleaned_data.get('model_name') or model_name
            model_selector = ModelSelector(app_label, model_name)
            model_data_inspector = ModelDataInspector(app_label, model_name)
            if model_data_inspector.get_model():
                summary = model_data_inspector.summarize()
                group = model_data_inspector.group()
                group_m2m = model_data_inspector.group_m2m()
                context = {
                    'sections': site_sections.get_indexed_section_tuples(),
                    'selected_section': section_name,
                    'form': form,
                    'app_label': model_selector.get_app_label(),
                    'model_name': model_selector.get_model_name(),
                    'app_labels': model_selector.get_app_labels(),
                    'model_names': model_selector.get_model_names(),
                    'summary_fields': summary['fields'],
                    'group_fields': group['fields'],
                    'group_m2m_fields': group_m2m['fields'],
                    'fields': model_data_inspector.get_model()._meta.fields,
                    'section_name': section_name,
                    'report_title': model_selector.get_model()._meta.verbose_name,
                    'cumulative_frequency': 0,
                    }
    else:
        form = ModelSelectorForm()
        model_selector = None
    return render_to_response(template, context, context_instance=RequestContext(request))
