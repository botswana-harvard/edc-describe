from django.contrib import admin

from ..models import Related


class RelatedAdmin(admin.ModelAdmin):

    list_filter = ('app_label', 'model_name')
    list_display = ('app_label', 'model_name', 'field_name', 'related_to_model', 'related_to_field_name')

admin.site.register(Related, RelatedAdmin)
