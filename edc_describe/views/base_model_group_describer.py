from datetime import datetime, time

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext

from ..forms import DateRangeForm

""" is this used??"""


@login_required
def base_model_group_describer(request, **kwargs):

    """"Given an app and a foreignkey field, such as visit, select a
    list of models and calculate basic frequencies by gender and site"""

    app_list = kwargs.get('app_list')
    section_name = kwargs.get('section_name')
    common_foreign_key_field_name = kwargs.get('common_foreign_key_field_name')
    report_title = 'Data Summary for Models with Key Field \'%s\'' % common_foreign_key_field_name
    template = 'model_group_describer.html'
    months = []
    years = []
    model_reports = {}
    # model_list = []
    model_reports_ordered_keys = []
    # to group on gender and site...
    gender = 'registered_subject__gender'
    site_name = 'registered_subject__study_site__site_name'
    model_list_title = "Membership Form and Additional Entry Models (w/ RegisteredSubject FK)"
    # but, to group on gender and site for models with a visit model foreignkey...
    if not common_foreign_key_field_name == 'registered_subject' and 'visit' in common_foreign_key_field_name:
        gender = common_foreign_key_field_name + '__appointment__' + gender
        site_name = common_foreign_key_field_name + '__appointment__' + site_name
        model_list_title = "Scheduled Entry Models (w/ Subject Visit FK)"
    # get all models with a registered_subject fk
    model_list = [{'name': model._meta.module_name, 'model':model}
                for model in models.get_models()
                if (model._meta.app_label in app_list)
                and common_foreign_key_field_name in
                [field.name for field in model._meta.fields]
                and '_audit_id' not in
                [field.name for field in model._meta.fields]
               ]
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            # get all models with a registered_subject fk
            model_list = [{'name': model._meta.module_name, 'model':model}
                        for model in models.get_models()
                        if (model._meta.app_label in app_list)
                        and common_foreign_key_field_name in
                        [field.name for field in model._meta.fields]
                        and '_audit_id' not in
                        [field.name for field in model._meta.fields]
                       ]
            for dct in model_list:
                model_reports[dct['name']] = {
                        'name': dct['model']._meta.module_name,
                        'verbose_name': dct['model']._meta.verbose_name,
                        'model': dct['model'],
                        'data': None,
                        'month_totals': [],
                        'year_totals': [],
                        'total': 0,
                        'date_grouping_field': 'created',
                        }
            # get date_grouping_field if other than created
            for key, model_report in model_reports.items():
                model_reports_ordered_keys.append(key)
                # get an instance of the model
                m = model_report['model']()
                # get date_grouping_field if method is defined at the model level
                try:
                    model_reports[model_report['name']]['date_grouping_field'] = m.get_date_grouping_field()
                except:
                    pass
            model_reports_ordered_keys.sort()

            start_date = form.cleaned_data['start_date']
            start_date = datetime.combine(start_date, time.min)
            end_date = form.cleaned_data['end_date']
            end_date = datetime.combine(end_date, time.max)

            # prepare ordered lists of years, months and sites
            years = range(start_date.year, end_date.year)
            if not years:
                years = [start_date.year, ]
            months = range(start_date.month, end_date.month + 1)

            # get data for each model
            for key, model_report in model_reports.items():

                # note reference to actual db_table name ...mysql dependent??
                extra_select = {'year': 'extract(year from ' + model_report['model']._meta.db_table + '.' + 
                                  model_report['date_grouping_field'] + ')',
                                  'month': 'extract(month from ' + model_report['model']._meta.db_table + '.' + 
                                  model_report['date_grouping_field'] + ')'
                                  }

                data = model_report['model'].objects.filter(
                    Q((model_report['date_grouping_field'] + '__gte', start_date)),
                    Q((model_report['date_grouping_field'] + '__lte',
                        end_date))).extra(select=extra_select).values('year', 'month', gender, site_name
                                        ).annotate(frequency=Count(model_report['date_grouping_field'])
                                    ).order_by()
                # rename gender and site_name keys for template
                new_data = []
                for d in data:
                    if gender in d:
                        d['gender'] = d[gender]
                    if site_name in d:
                        d['site_name'] = d[site_name]
                    new_data.append(d)

                model_reports[model_report['name']]['data'] = new_data
                total = 0
                for year in years:
                    year_total = 0
                    for month in months:
                        month_total = 0
                        for x in [rpt['frequency'] for rpt in model_reports[model_report['name']]['data'] if rpt['year'] == year and rpt['month'] == month]:
                            month_total += x
                        model_reports[model_report['name']]['month_totals'].append({'year': year, 'month': month, 'total': month_total})
                        year_total += month_total
                    model_reports[model_report['name']]['year_totals'].append({'year': year, 'total': year_total})
                    total += year_total
                model_reports[model_report['name']]['total'] = total

    else:
        form = DateRangeForm(request.POST)
    ordered_model_list = [{"verbose_name": model['model']._meta.verbose_name, "module_name": model['model']._meta.module_name} for model in model_list]
    ordered_model_list.sort()
    return render_to_response(template, {
        'form': form,
        'years': years,
        'months': months,
        'sites': [],
        'cumulative_frequency': 0,
        'model_list': ordered_model_list,
        'model_list_title': model_list_title,
        'model_reports': model_reports,
        'model_reports_ordered_keys': model_reports_ordered_keys,
        'section_name': section_name,
        'app_name': settings.APP_NAME,
        'report_title': report_title,
        'report': '',
        'report_name': kwargs.get('report_name')}, context_instance=RequestContext(request))
