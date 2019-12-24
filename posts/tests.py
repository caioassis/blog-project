import os
from xml.etree import ElementTree
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.test import TestCase
from django.urls import reverse_lazy
from .models import Post, Reply

User = get_user_model()


class PostTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='admin', email='admin@admin.com', password='admin123')
        user = User.objects.create_user(username='caio', email='caio@caio.com', password='123456')
        User.objects.create_user(username='eduardo', email='eduardo@eduardo.com', password='123456')
        # Create 5 posts for only 1 user.
        Post.objects.bulk_create(
            [
                Post(
                    title=f'Test Post {str(i)}',
                    content='Test content',
                    author=user
                ) for i in range(1, 6)
            ]
        )
        # Publish only 1 post of user.
        post = Post.objects.filter(author=user).get(title='Test Post 1')
        post.approve()
        # Create 3 replies and approve only one
        for i in range(1, 4):
            post.replies.add(
                Reply.objects.create(
                    name='Caio Eduardo Borges Assis',
                    email='caio@caio.com',
                    content=f'Post Reply {str(i)}'
                )
            )
        post.replies.get(content='Post Reply 1').approve()

    def setUp(self) -> None:
        self.client = Client()

    def test_new_post_is_unpublished(self):
        user = User.objects.get(username='caio')
        previous_published_posts_count = Post.objects.published().count()
        post = Post.objects.create(author=user, title='Post with test title', content='Post test content')
        self.assertFalse(post.approved)
        self.assertFalse(post.marked_as_deleted)
        published_posts_count = Post.objects.published().count()
        self.assertEqual(previous_published_posts_count, published_posts_count)

    def test_new_post_with_thumbnail_upload(self):
        user = User.objects.get(username='caio')
        image = SimpleUploadedFile(
            name='python.png',
            content=open(os.path.join(settings.BASE_DIR, 'python-logo.png'), 'rb').read(),
            content_type='image/png'
        )
        post = Post.objects.create(author=user, title='Post with test title', content='Post test content', thumbnail=image)
        self.assertIsNotNone(post.thumbnail.name)

    def test_user_home_view_shows_published_posts(self):
        self.client.login(username='caio', password='123456')
        response = self.client.get(reverse_lazy('posts:home'))
        self.assertEqual(response.context['posts'].count(), 1)
        posts = list(response.context['posts'].values_list('title', flat=True))
        expected_posts = ['Test Post 1']
        self.assertEqual(posts, expected_posts)

    def test_user_cannot_publish_post(self):
        self.client.login(username='caio', password='123456')
        response = self.client.get(reverse_lazy('posts:approve_post', kwargs={'pk': 5}))
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_publish_post(self):
        self.client.login(username='admin', password='admin123')
        previous_published_posts_count = Post.objects.published().count()
        response = self.client.get(reverse_lazy('posts:approve_post', kwargs={'pk': 5}))
        # If succeeded, approve post view redirects back to audit posts view
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('posts:audit_posts'))
        published_posts_count = Post.objects.published().count()
        self.assertEqual(published_posts_count, previous_published_posts_count+1)

    def test_user_cannot_access_post_audit_view(self):
        self.client.login(username='caio', password='123456')
        response = self.client.get(reverse_lazy('posts:audit_posts'))
        self.assertEqual(response.status_code, 403)

    def test_post_sorting_in_post_list_view(self):
        for post in Post.objects.unpublished():
            post.approve()
        expected_post_sorting = [
            {'title': f'Test Post {str(i)}'} for i in range(5, 0, -1)
        ]
        response = self.client.get(reverse_lazy('posts:home'))
        posts = list(response.context['posts'].values('title'))
        self.assertEqual(posts, expected_post_sorting)

    def test_post_sorting_in_rss_feed(self):
        for post in Post.objects.unpublished():
            post.approve()
        response = self.client.get(reverse_lazy('posts:post_feed'))
        content = response.content.decode()
        # Parse RSS feed and find all items
        root = ElementTree.fromstring(content)
        items = root.find('channel').findall('item')
        expected_feed_posts = [{'title': f'Test Post {str(i)}'} for i in range(5, 0, -1)]
        feed_posts = [{'title': item.find('title').text} for item in items]
        self.assertEqual(feed_posts, expected_feed_posts)

    def test_post_create_reply(self):
        post = Post.objects.get(title='Test Post 2')
        reply = Reply.objects.create(name='Caio Eduardo', email='caio@caio.com', content='Reply content')
        post.replies.add(reply)
        self.assertFalse(reply.approved)
        self.assertFalse(reply.marked_as_deleted)
        self.assertEqual(post.approved_replies.count(), 0)

    def test_user_can_delete_his_post(self):
        user = User.objects.get(username='caio')
        self.client.login(username='caio', password='123456')
        post = user.posts.first()
        response = self.client.get(reverse_lazy('posts:post_delete', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 302) # Redirect to another page after delete

    def test_user_cannot_delete_others_posts(self):
        user = User.objects.get(username='eduardo')
        new_post = Post.objects.create(title='Test', content='Test', author=user)
        self.client.login(username='caio', password='123456')
        response = self.client.get(reverse_lazy('posts:post_delete', kwargs={'pk': new_post.pk}))
        self.assertEqual(response.status_code, 403)

    def test_post_replies_verify_count(self):
        post = Post.objects.get(title='Test Post 1')
        self.assertEqual(post.approved_replies.count(), 1)

    def test_post_replies_sorting(self):
        user = User.objects.get(username='caio')
        post = user.posts.published().get(title='Test Post 1')
        new_reply = Reply.objects.create(name='New Reply', email='reply@reply.com', content='Reply Content')
        post.replies.add(new_reply)
        new_reply.approve()
        self.assertEqual(post.approved_replies.count(), 2)
        expected_replies = [{'content': new_reply.content}, {'content': 'Post Reply 1'}]
        replies = list(post.approved_replies.values('content'))
        self.assertEqual(replies, expected_replies)

    def test_superuser_can_approve_reply(self):
        self.client.login(username='admin', password='admin123')
        post = Post.objects.published().first()
        previous_approved_replies_count = post.approved_replies.count()
        reply = post.replies.unapproved().first()
        response = self.client.get(reverse_lazy('posts:reply_approve', kwargs={'post_id': post.pk, 'reply_id': reply.pk}))
        self.assertEqual(response.status_code, 302)  # Redirected if succeeded
        approved_replies_count = post.approved_replies.count()
        self.assertEqual(approved_replies_count, previous_approved_replies_count+1)

    def test_superuser_can_delete_reply(self):
        self.client.login(username='admin', password='admin123')
        post = Post.objects.published().first()
        previous_replies_count = post.replies.count()
        reply = post.replies.unapproved().first()
        response = self.client.get(reverse_lazy('posts:reply_delete', kwargs={'post_id': post.pk, 'reply_id': reply.pk}))
        self.assertEqual(response.status_code, 302)  # Redirected if succeeded
        replies_count = post.replies.count()
        self.assertEqual(replies_count, previous_replies_count-1)

    def test_user_can_approve_reply_of_his_post(self):
        self.client.login(username='caio', password='123456')
        post = Post.objects.published().first()
        previous_approved_replies_count = post.approved_replies.count()
        reply = post.replies.unapproved().first()
        response = self.client.get(reverse_lazy('posts:reply_approve', kwargs={'post_id': post.pk, 'reply_id': reply.pk}))
        self.assertEqual(response.status_code, 302)  # Redirected if succeeded
        approved_replies_count = post.approved_replies.count()
        self.assertEqual(approved_replies_count, previous_approved_replies_count + 1)

    def test_user_can_delete_reply_of_his_post(self):
        self.client.login(username='caio', password='123456')
        post = Post.objects.published().first()
        previous_replies_count = post.replies.count()
        reply = post.replies.first()
        response = self.client.get(reverse_lazy('posts:reply_delete', kwargs={'post_id': post.pk, 'reply_id': reply.pk}))
        self.assertEqual(response.status_code, 302)  # Redirected if succeeded
        replies_count = post.replies.count()
        self.assertEqual(replies_count, previous_replies_count-1)

    def test_user_cannot_approve_reply_of_others_posts(self):
        self.client.login(username='eduardo', password='123456')
        post = Post.objects.published().first()
        previous_approved_replies_count = post.approved_replies.count()
        reply = post.replies.unapproved().first()
        response = self.client.get(reverse_lazy('posts:reply_approve', kwargs={'post_id': post.pk, 'reply_id': reply.pk}))
        self.assertEqual(response.status_code, 403)
        approved_replies_count = post.approved_replies.count()
        self.assertEqual(approved_replies_count, previous_approved_replies_count)

    def test_user_cannot_delete_reply_of_others_posts(self):
        self.client.login(username='eduardo', password='123456')
        post = Post.objects.published().first()
        previous_replies_count = post.replies.count()
        reply = post.replies.first()
        response = self.client.get(reverse_lazy('posts:reply_delete', kwargs={'post_id': post.pk, 'reply_id': reply.pk}))
        self.assertEqual(response.status_code, 403)
        replies_count = post.replies.count()
        self.assertEqual(replies_count, previous_replies_count)
