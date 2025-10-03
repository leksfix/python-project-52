from django.contrib import messages
from django.views.generic import TemplateView
from task_manager.forms import LoginForm
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin


class IndexView(TemplateView):
    template_name = "index.html"



class LoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = "login.html"
    authentication_form = LoginForm
    next_page = 'index'
    success_message = _("You are logged in")



class LogoutView(auth_views.LogoutView):
    next_page = 'index'

    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        messages.info(request, _("You are logged out"))
        return res
