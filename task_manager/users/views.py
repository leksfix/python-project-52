from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from task_manager.users.models import User
from task_manager.users.forms import UserCreateForm, UserUpdateForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from task_manager.users.mixins import CheckSameUserMixin


class UsersIndexView(ListView):
    model = User
    queryset = User.objects.all().order_by("id")
    template_name = "users/user_list.html"


class UsersCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "common/create_update.html"
    success_url = reverse_lazy("login")
    success_message = _("User successfully created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Registration")
        context["action_url"] = reverse_lazy("users:create")
        context["submit_btn_text"] = _("Register")

        return context


class UsersUpdateView(CheckSameUserMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "common/create_update.html"
    success_url = reverse_lazy("users:index")
    success_message = _("User successfully updated")
    same_user_error_url = reverse_lazy("users:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Update user")
        context["action_url"] = reverse_lazy(
            "users:update",
            kwargs={"pk": self.object.id}
        )
        context["submit_btn_text"] = _("Update")

        return context


class UsersDeleteView(CheckSameUserMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("users:index")
    success_message = _("User successfully deleted")
    same_user_error_url = reverse_lazy("users:index")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                self.request, _("The user cannot be deleted because it is in use")
            )
            return redirect(reverse_lazy("users:index"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = _("Delete user")
        context["warning_message"] = (
            _("Are you sure you want to delete") + " " + self.object.get_full_name() + "?"
        )
        context["delete_url"] = reverse_lazy(
            "users:delete", kwargs={"pk": self.object.id}
        )
        context["delete_btn_text"] = _("Yes, delete")

        return context
