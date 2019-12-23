from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    title = 'Latest posts from BLOG'
    link = '/posts/'
    description = 'Latest published posts on BLOG.'

    def items(self):
        return Post.objects.published().order_by('-created_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def author_name(self, item):
        return item.author.username

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse_lazy('posts:post_detail', args=[item.pk])
