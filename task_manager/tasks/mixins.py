from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin

class CheckAuthorIsMe(UserPassesTestMixin):
    author_error_message = ""
    author_error_url = ""

    def test_func(self):
        return self.get_object().author_id == self.request.user.id

    def handle_no_permission(self):
        messages.error(self.request, self.author_error_message)
        return redirect(self.author_error_url)
