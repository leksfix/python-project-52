from django.db import models
from django.utils.translation import gettext, gettext_lazy

class Status(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=gettext_lazy("Name")
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = gettext_lazy("Status")
        verbose_name_plural = gettext_lazy("Statuses")