from django.contrib import admin

from ..models import GroupingHint


class GroupingHintAdmin(admin.ModelAdmin):

    list_filter = ('app_label', 'model_name')
    list_display = ('app_label', 'model_name', 'field_name')

admin.site.register(GroupingHint, GroupingHintAdmin)
