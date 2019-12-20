from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, UpdateView, CreateView
from django.contrib import messages
from posts.forms import ReplyForm, PostForm
from posts.models import Post, Reply


class PostListView(ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published=True, deleted=False)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class AuthorPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        queryset = queryset.filter(published=True, deleted=False)
        return queryset


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'posts/post.html'
    form_class = ReplyForm


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


class ReplyCreateView(CreateView):
    model = Reply
    form_class = ReplyForm

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.kwargs['post_id']})

    def form_valid(self, form):
        reply = form.save(commit=False)
        post = Post.objects.get(pk=self.kwargs['post_id'])
        reply.save()
        post.replies.add(reply)
        messages.info(self.request, message='Your reply must be approved before it can be displayed.')
        return redirect(self.get_success_url())
