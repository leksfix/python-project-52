from django.contrib import messages
from django.views.generic import TemplateView
from task_manager.forms import LoginForm
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext


class IndexView(TemplateView):
    template_name = "index.html"



class LoginView(auth_views.LoginView):
    template_name = "login.html"
    authentication_form = LoginForm
    next_page = 'index'

    def dispatch(self, request, *args, **kwargs):
        res = super().dispatch(request, *args, **kwargs)
        if request.user.is_authenticated:
            messages.success(request, gettext("You are logged in"))
        return res



class LogoutView(auth_views.LogoutView):
    next_page = 'index'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, gettext("You are logged out"))
        return super().dispatch(request, *args, **kwargs)
