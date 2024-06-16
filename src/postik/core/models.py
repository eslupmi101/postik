from django.db import models


class CreateModel(models.Model):
    """
    Abstract model. Field with creaton date
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        db_index=True
    )

    class Meta:
        abstract = True
