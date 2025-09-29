from django.contrib import messages

class FormMessagesMixin():
    success_message = "OK"

    def form_valid(self, form):
        res = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return res
