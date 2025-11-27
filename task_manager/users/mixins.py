from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class CheckSameUserMixin(UserPassesTestMixin):
    same_user_error_message = _(
        "You do not have permission to modify another user"
    )
    same_user_error_url = reverse_lazy("users:index")

    def test_func(self):
        return (
            not self.request.user.is_authenticated or
            self.kwargs["pk"] == self.request.user.id
        )

    def handle_no_permission(self):
        messages.error(self.request, self.same_user_error_message)
        return redirect(self.same_user_error_url)
