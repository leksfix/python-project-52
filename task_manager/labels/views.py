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
    queryset = Label.objects.all().order_by("id")
    template_name = "labels/label_list.html"


class LabelsCreateView(SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "common/create_update.html"
    success_url = reverse_lazy("labels:index")
    success_message = _("Label successfully created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Create label")
        context["action_url"] = reverse_lazy("labels:create")
        context["submit_btn_text"] = _("Create")

        return context


class LabelsUpdateView(SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "common/create_update.html"
    success_url = reverse_lazy("labels:index")
    success_message = _("Label successfully updated")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Edit label")
        context["action_url"] = reverse_lazy(
            "labels:update", kwargs={"pk": self.object.id}
        )
        context["submit_btn_text"] = _("Update")

        return context


class LabelsDeleteView(SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("labels:index")
    success_message = _("Label successfully deleted")

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        if object.task_set.exists():
            messages.error(
                request, _("The label cannot be deleted because it is in use")
            )
            return redirect(reverse_lazy("labels:index"))

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Delete label")
        context["warning_message"] = (
            _("Are you sure you want to delete") + " " + self.object.name + "?"
        )
        context["delete_url"] = reverse_lazy(
            "labels:delete", kwargs={"pk": self.object.id}
        )
        context["delete_btn_text"] = _("Yes, delete")

        return context
