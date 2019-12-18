from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.urls import reverse_lazy
from .forms import LoginForm


class LoginView(AuthLoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm


class LogoutView(AuthLogoutView):
    next_page = reverse_lazy('core:login')
