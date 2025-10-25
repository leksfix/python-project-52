from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError


class StatusesIndexView(ListView):
    model = Status
    queryset = Status.objects.all().order_by("id")
    template_name = "statuses/status_list.html"


class StatusesCreateView(SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "common/create_update.html"
    success_url = reverse_lazy("statuses:index")
    success_message = _("Status successfully created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Create status")
        context["action_url"] = reverse_lazy("statuses:create")
        context["submit_btn_text"] = _("Create")

        return context


class StatusesUpdateView(SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "common/create_update.html"
    success_url = reverse_lazy("statuses:index")
    success_message = _("Status successfully updated")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Edit status")
        context["action_url"] = reverse_lazy(
            "statuses:update", kwargs={"pk": self.object.id}
        )
        context["submit_btn_text"] = _("Update")

        return context


class StatusesDeleteView(SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("statuses:index")
    success_message = _("Status successfully deleted")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                self.request, _("The status cannot be deleted because it is in use")
            )
            return redirect(reverse_lazy("statuses:index"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Delete status")
        context["warning_message"] = (
            _("Are you sure you want to delete") + " " + self.object.name + "?"
        )
        context["delete_url"] = reverse_lazy(
            "statuses:delete", kwargs={"pk": self.object.id}
        )
        context["delete_btn_text"] = _("Yes, delete")

        return context
