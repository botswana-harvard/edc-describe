from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..models import Related


class RelatedAdmin(BaseModelAdmin):

    list_filter = ('app_label', 'model_name')
    list_display = ('app_label', 'model_name', 'field_name', 'related_to_model', 'related_to_field_name')
admin.site.register(Related, RelatedAdmin)
