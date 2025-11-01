from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext_lazy as _


class CheckSameUserMixin(UserPassesTestMixin):
    same_user_error_message = _(
        "You do not have permission to modify another user"
    )
    same_user_error_url = ""

    def test_func(self):
        return self.kwargs["pk"] == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, self.same_user_error_message)
        return redirect(self.same_user_error_url)
