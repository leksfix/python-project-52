from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from task_manager.tasks.filters import TasksFilter
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_filters.views import FilterView
from task_manager.tasks.mixins import CheckAuthorIsMe



class TasksIndexView(LoginRequiredMixin, FilterView):
    filterset_class = TasksFilter
    template_name = "tasks/task_filter.html"



class TasksDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"


class TasksCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "common/create_update.html"
    success_url = reverse_lazy("tasks:index")
    success_message = _("Task successfully created")

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['page_title'] = _("Create task")
        context['action_url'] = reverse_lazy('tasks:create')
        context['submit_btn_text'] = _("Create")

        return context




class TasksUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "common/create_update.html"
    success_url = reverse_lazy("tasks:index")
    success_message = _("Task successfully updated")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['page_title'] = _("Edit task")
        context['action_url'] = reverse_lazy('tasks:update', kwargs={'pk': self.object.id})
        context['submit_btn_text'] = _("Update")

        return context




class TasksDeleteView(CheckAuthorIsMe, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("tasks:index")
    success_message = _("Task successfully deleted")
    author_error_message = _("A task can only be deleted by its author")
    author_error_url = reverse_lazy("tasks:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['page_title'] = _("Delete task")
        context['warning_message'] = _("Are you sure you want to delete") + ' ' + self.object.name + '?'
        context['delete_url'] = reverse_lazy('tasks:delete', kwargs={'pk': self.object.id})
        context['delete_btn_text'] = _("Yes, delete")

        return context