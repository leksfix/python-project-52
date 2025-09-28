from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm
from django.urls import reverse_lazy
from django.utils.translation import gettext

class StatusesIndexView(ListView):
    model = Status
    ordering = "id"
    template_name = "statuses/status_list.html"


class StatusesCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/status_create.html"
    success_url = reverse_lazy("statuses_index")

    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        messages.success(request, gettext("Status successfully created"))
        return res



class StatusesUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/status_update.html"
    success_url = reverse_lazy("statuses_index")

    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        messages.success(request, gettext("Status successfully updated"))
        return res



class StatusesDeleteView(DeleteView):
    model = Status
    template_name = "statuses/status_delete.html"
    success_url = reverse_lazy("statuses_index")

    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        messages.success(request, gettext("Status successfully deleted"))
        return res

