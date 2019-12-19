from django.contrib.auth import login
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import LoginForm, SignupForm


class LoginView(AuthLoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm


class LogoutView(AuthLogoutView):
    next_page = reverse_lazy('core:login')


class SignupView(FormView):
    template_name = 'core/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('posts:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        login(self.request, user)
        return redirect(self.success_url)
