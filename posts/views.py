from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, UpdateView, CreateView, DeleteView
from core.mixins import SuperUserRequiredMixin
from posts.forms import ReplyForm, PostForm
from posts.models import Post, Reply


class AuditPostListView(LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    model = Post
    template_name = 'posts/audit_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.unpublished()
        return queryset


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.published()
        return queryset


class AuthorPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        queryset = queryset.filter(approved=True, marked_as_deleted=False)
        return queryset


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'posts/post.html'
    form_class = ReplyForm

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        reply = form.save(commit=False)
        post = self.get_object()
        reply.save()
        post.replies.add(reply)
        messages.info(self.request, message='Your reply must be approved before it can be displayed.')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/post_form.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy('posts:home')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        messages.info(self.request, message='Your post must be approved before it can be displayed.')
        return redirect(self.get_success_url())


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/post_form.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not self.request.user.is_superuser:
            if not obj.author == self.request.user:
                raise PermissionDenied
        return obj


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:author_post_list')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if not self.request.user.is_superuser:
            if not obj.author == self.request.user:
                raise PermissionDenied
        return obj

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ReplyDeleteView(LoginRequiredMixin, DeleteView):
    model = Reply

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.kwargs['post_id']})

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if not self.request.user.is_superuser:
            if not self.request.user == post.author:
                raise PermissionDenied
        return post.replies.get(pk=self.kwargs['reply_id'])

    def get(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ApprovePostView(LoginRequiredMixin, SuperUserRequiredMixin, View):

    def get_success_url(self):
        return reverse_lazy('posts:audit_posts')

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        post.approve()
        return redirect(self.get_success_url())


class ApproveReplyView(LoginRequiredMixin, View):

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.kwargs['post_id']})

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if not self.request.user.is_superuser:
            if not self.request.user == post.author:
                raise PermissionDenied
        return post.replies.get(pk=self.kwargs['reply_id'])

    def get(self, request, *args, **kwargs):
        reply = self.get_object()
        reply.approve()
        return redirect(self.get_success_url())
