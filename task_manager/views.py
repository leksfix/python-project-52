from django.contrib import messages
from django.views.generic import TemplateView
from task_manager.forms import LoginForm
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext, gettext_lazy
from task_manager.utils.mixins import FormMessagesMixin


class IndexView(TemplateView):
    template_name = "index.html"



class LoginView(FormMessagesMixin, auth_views.LoginView):
    template_name = "login.html"
    authentication_form = LoginForm
    next_page = 'index'
    success_message = gettext_lazy("You are logged in")



class LogoutView(auth_views.LogoutView):
    next_page = 'index'

    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        messages.info(request, gettext_lazy("You are logged out"))
        return res
