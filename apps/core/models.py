from django.db.models import DateTimeField, Model


class AbstractBaseModel(Model):
    """Abstract base model with created and updated timestamps."""

    created_at = DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        """Meta options."""

        abstract = True