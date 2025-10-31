from django import forms
from django_filters import filters, FilterSet
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from django.utils.translation import gettext_lazy as _


class TasksFilter(FilterSet):
    label = filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all(),
        label=_("Label"),
    )
    my_tasks = filters.BooleanFilter(
        method="my_tasks_filter",
        field_name="executor_id",
        label=_("Only my tasks"),
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = [
            "status",
            "executor",
            "label",
            "my_tasks",
        ]

    def my_tasks_filter(self, queryset, name, value):
        if value:
            return queryset.filter(executor_id=self.request.user.id)
        return queryset
