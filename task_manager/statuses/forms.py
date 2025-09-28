from django.forms import ModelForm
from task_manager.statuses.models import Status
from django.utils.translation import gettext, get_language, gettext_lazy

class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
