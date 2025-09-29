from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from task_manager.users.forms import UserCreateForm, UserUpdateForm
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy
from task_manager.utils.mixins import FormMessagesMixin

class UsersIndexView(ListView):
    model = User
    ordering = "id"
    template_name = "users/user_list.html"


class UsersCreateView(FormMessagesMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "users/user_create.html"
    success_url = reverse_lazy("users_index")
    success_message = gettext_lazy("User successfully created")



class UsersUpdateView(FormMessagesMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/user_update.html"
    success_url = reverse_lazy("users_index")
    success_message = gettext_lazy("User successfully updated")



class UsersDeleteView(FormMessagesMixin, DeleteView):
    model = User
    template_name = "users/user_delete.html"
    success_url = reverse_lazy("users_index")
    success_message = gettext_lazy("User successfully deleted")
