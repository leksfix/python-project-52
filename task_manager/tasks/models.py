from django.db import models
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User

class Task(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_("Name")
    )
    description = models.TextField(
        verbose_name=_("Description")
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_("Status")
    )
    author = models.ForeignKey(
        User,
        related_name="tasks",
        on_delete=models.PROTECT,
        verbose_name=_("Author")
    )
    assignee = models.ForeignKey(
        User,
        related_name="assigned_tasks",
        on_delete=models.PROTECT,
        verbose_name=_("Assignee")
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        verbose_name=_("Labels")
        )

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")