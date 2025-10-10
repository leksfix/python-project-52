from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.labels.models import Label
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect, render
import django_filters
import django.forms


class TasksFilter(django_filters.FilterSet):
    label = django_filters.filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all(),
        label=_("Label"),
    )
    my_tasks = django_filters.filters.BooleanFilter(
        method='my_tasks_filter',
        field_name="assignee_id",
        label=_("Only my tasks"),
        widget=django.forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = [
            "status",
            "assignee",
        ]
    
    def my_tasks_filter(self, queryset, name, value):
        if value:
            return queryset.filter(assignee_id=self.request.user.id)
        return queryset


def tasks_index(request):
    filter = TasksFilter(
        request.GET,
        queryset=Task.objects.all(),
        request=request
    )
    return render(request, 'tasks/task_filter.html', {'filter': filter})


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

