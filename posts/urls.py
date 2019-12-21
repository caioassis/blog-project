from django.urls import path
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, AuthorPostListView,
                    AuditPostListView, PostDeleteView, ApprovePostView, ReplyDeleteView, ApproveReplyView)

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('my_posts/', AuthorPostListView.as_view(), name='author_post_list'),
    path('audit_posts/', AuditPostListView.as_view(), name='audit_posts'),
    path('<int:pk>/approve/', ApprovePostView.as_view(), name='approve_post'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/replies/<int:reply_id>/approve/', ApproveReplyView.as_view(), name='reply_approve'),
    path('<int:post_id>/replies/<int:reply_id>/delete/', ReplyDeleteView.as_view(), name='reply_delete'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
