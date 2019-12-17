from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from posts.forms import ReplyForm
from posts.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published=True)
        return queryset


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'posts/post.html'
    form_class = ReplyForm
