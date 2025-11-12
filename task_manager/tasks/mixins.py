from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class CheckAuthorIsMe(UserPassesTestMixin):
    author_error_message = _("A task can only be deleted by its author")
    author_error_url = reverse_lazy("tasks:index")

    def test_func(self):
        return self.get_object().author_id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, self.author_error_message)
        return redirect(self.author_error_url)
