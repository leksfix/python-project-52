from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from task_manager.users.forms import UserCreateForm, UserUpdateForm
from django.urls import reverse_lazy
from django.utils.translation import gettext

class UsersIndexView(ListView):
    model = User
    ordering = "id"
    template_name = "users/user_list.html"


class UsersCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "users/user_create.html"
    success_url = reverse_lazy("users_index")
    
    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        messages.success(request, gettext("User successfully created"))
        return res



class UsersUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/user_update.html"
    success_url = reverse_lazy("users_index")

    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        messages.success(request, gettext("User successfully updated"))
        return res



class UsersDeleteView(DeleteView):
    model = User
    template_name = "users/user_delete.html"
    success_url = reverse_lazy("users_index")

    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        messages.success(request, gettext("User successfully deleted"))
        return res
