from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect


class TasksIndexView(LoginRequiredMixin, ListView):
    queryset = Task.objects.order_by("id")
    template_name = "tasks/task_list.html"
    login_url = reverse_lazy("login")


class TasksDetailView(LoginRequiredMixin, DetailView):
    model = Task
    #queryset = Task.objects.get(pk=self.request.id)
    template_name = "tasks/task_detail.html"
    login_url = reverse_lazy("login")


class TasksCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_create.html"
    success_url = reverse_lazy("tasks_index")
    success_message = _("Task successfully created")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        
        return super().form_valid(form)



class TasksUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_update.html"
    success_url = reverse_lazy("tasks_index")
    success_message = _("Task successfully updated")
    login_url = reverse_lazy("login")



class TasksDeleteView(UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks_index")
    success_message = _("Task successfully deleted")
    login_url = reverse_lazy("login")
    del_error_message = _("A task can only be deleted by its author")

    def test_func(self):
        self.get_object().author_id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, self.del_error_message)
        return redirect(reverse_lazy("tasks_index"))

