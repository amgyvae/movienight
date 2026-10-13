from django.db import models

class TimeSampedModel(models.Model):
    """  An abstract base class model that provides self-updating 'created' and 'modified' fields. """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        abstract = True