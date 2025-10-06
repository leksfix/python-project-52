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
    ordering = "id"
    template_name = "statuses/status_list.html"


class StatusesCreateView(SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/status_create.html"
    success_url = reverse_lazy("statuses_index")
    success_message = _("Status successfully created")



class StatusesUpdateView(SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/status_update.html"
    success_url = reverse_lazy("statuses_index")
    success_message = _("Status successfully updated")



class StatusesDeleteView(SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses/status_confirm_delete.html"
    success_url = reverse_lazy("statuses_index")
    success_message = _("Status successfully deleted")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, _("The status cannot be deleted because it is in use"))
            return redirect(reverse_lazy("statuses_index"))
