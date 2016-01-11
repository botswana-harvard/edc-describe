from django.db import models
from edc_base.model.models import BaseUuidModel


class GroupingHint (BaseUuidModel):

    """A model to list a field_name that should be grouped on but has no choices tuple.

    Fields with choices tuples do not need to be listed here as they are automatically
    grouped on by the describer object.
    """

    app_label = models.CharField(
        max_length=50,
        db_index=True
        )
    model_name = models.CharField(
        max_length=50,
        db_index=True
        )

    field_name = models.CharField(
        max_length=50,
        db_index=True
        )

    objects = models.Manager()

    def __unicode__(self):
        return '%s__%s' % (self.model_name, self.field_name)

    class Meta:
        app_label = "model_describer"
        db_table = "bhp_describer_groupinghint"
        unique_together = ['app_label', 'model_name', 'field_name']
