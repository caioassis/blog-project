from django.urls import path
from .views import PostListView, PostDetailView, PostUpdateView, ReplyCreateView, AuthorPostListView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('my_posts/', AuthorPostListView.as_view(), name='author_post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:post_id>/replies/create/', ReplyCreateView.as_view(), name='reply_create')
]
