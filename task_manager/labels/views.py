from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

class LabelsIndexView(ListView):
    model = Label
    ordering = "id"
    template_name = "labels/label_list.html"


class LabelsCreateView(SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/label_create.html"
    success_url = reverse_lazy("labels_index")
    success_message = _("Label successfully created")



class LabelsUpdateView(SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/label_update.html"
    success_url = reverse_lazy("labels_index")
    success_message = _("Label successfully updated")



class LabelsDeleteView(SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "labels/label_confirm_delete.html"
    success_url = reverse_lazy("labels_index")
    success_message = _("Label successfully deleted")

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        if object.task_set.exists():
            messages.error(request, _("The label cannot be deleted because it is in use"))
            return redirect(reverse_lazy("labels_index"))

        return super().post(request, *args, **kwargs)
