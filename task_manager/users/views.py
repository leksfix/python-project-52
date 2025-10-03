from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from task_manager.users.forms import UserCreateForm, UserUpdateForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.db.utils import IntegrityError

class CheckSameUserMixin():
    same_user_error_message = _("You do not have permission to modify another user")
    same_user_error_url = ""

    def get(self, request, *args, **kwargs):
        res = super().get(request, *args, **kwargs)
        if not self.object.id == self.request.user.id:
            messages.error(request, self.same_user_error_message)
            return redirect(self.same_user_error_url)

        return res

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if not user.id == self.request.user.id:
            messages.error(request, self.same_user_error_message)
            return redirect(self.same_user_error_url)

        return super().post(request, *args, **kwargs)



class UsersIndexView(ListView):
    model = User
    ordering = "id"
    template_name = "users/user_list.html"


class UsersCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "users/user_create.html"
    success_url = reverse_lazy("users_index")
    success_message = _("User successfully created")



class UsersUpdateView(CheckSameUserMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/user_update.html"
    success_url = reverse_lazy("users_index")
    success_message = _("User successfully updated")
    same_user_error_url = reverse_lazy("users_index")



class UsersDeleteView(CheckSameUserMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users_index")
    success_message = _("User successfully deleted")
    same_user_error_url = reverse_lazy("users_index")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.error(self.request, _("The user cannot be deleted because it is in use"))
            return redirect(reverse_lazy("users_index"))
