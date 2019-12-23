from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, ListView, UpdateView
from .forms import LoginForm, SignupForm, AuthorForm
from .mixins import SuperUserRequiredMixin

User = get_user_model()


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


class AuthorListView(LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    model = User
    queryset = User.objects.all().order_by('-is_active', 'username')
    template_name = 'core/author_list.html'
    context_object_name = 'authors'


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'core/author_form.html'
    form_class = AuthorForm
    success_url = reverse_lazy('core:author_list')

    def get_object(self, queryset=None):
        """
        Check if the request.user has permission to update the user object.
        :param queryset:
        :return:
        """
        user = super().get_object()
        if not self.request.user.is_superuser:
            if not user == self.request.user:
                # User from request is trying to update a different user, so deny the request.
                raise PermissionDenied
        return user

    def form_valid(self, form):
        user = form.save(commit=False)
        if not user.is_active:
            user.posts.delete()
        user.save()
        return redirect(self.success_url)


class AuthorDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, View):

    def get_success_url(self):
        return reverse_lazy('core:author_list')

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        for post in user.posts.all():
            post.delete()
        user.save()
        return redirect(self.get_success_url())
