from django.db import models
from edc_base.model.models import BaseUuidModel


class Related (BaseUuidModel):

    """A model to refer to when the 'option' or 'choice' field name (related_to_field_name) of the foreignkey is not obvious, e.g. not = 'name'.  """

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

    related_to_model = models.CharField(
        max_length=50,
        )

    related_to_field_name = models.CharField(
        max_length=50,
        )

    objects = models.Manager()

    def __unicode__(self):
        return '%s__%s' % (self.model_name, self.field_name)

    class Meta:
        app_label = "model_describer"
        db_table = "bhp_describer_related"
        unique_together = ['app_label', 'model_name', 'field_name']
