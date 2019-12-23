import uuid
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils import timezone
from .managers import PostManager, ReplyManager
from .querysets import PostQuerySet, ReplyQuerySet

User = get_user_model()


class Reply(models.Model):
    name = models.CharField(verbose_name='Name', max_length=40)
    email = models.EmailField(verbose_name='Email', unique=False)
    content = models.CharField(verbose_name='Content', max_length=250)
    created_at = models.DateTimeField(verbose_name='Creation Date', auto_now_add=True)
    approved = models.BooleanField(verbose_name='Approved', default=False)
    marked_as_deleted = models.BooleanField(verbose_name='Marked as deleted', default=False)

    objects = ReplyManager.from_queryset(ReplyQuerySet)()

    def approve(self):
        self.approved = True
        self.save()

    def delete(self):
        self.marked_as_deleted = True
        self.save()
        return

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'
        ordering = ['-created_at', '-approved']


def post_thumbnails_dir_path(instance, filename):
    """
    Function that creates a unique file name for each post thumbnail and returns the upload path.
    :param instance:
    :param filename:
    :return:
    """
    today = timezone.now()
    return f'thumbnails/{instance.author}/{today.strftime("%Y/%m/%d")}/{uuid.uuid4()}-{filename}'


class Post(models.Model):
    thumbnail = models.FileField(verbose_name='Thumbnail', upload_to=post_thumbnails_dir_path, blank=True, null=True)
    title = models.CharField(verbose_name='Title', max_length=50)
    author = models.ForeignKey(verbose_name='Author', to=User, related_name='posts', on_delete=models.CASCADE, null=True)
    content = models.TextField(verbose_name='Content')
    replies = models.ManyToManyField(verbose_name='Replies', to=Reply, blank=True)
    created_at = models.DateTimeField(verbose_name='Creation Date', auto_now_add=True, blank=True)
    approved = models.BooleanField(default=False)
    marked_as_deleted = models.BooleanField(verbose_name='Deleted', default=False)

    @property
    def approved_replies(self):
        """
        Get approved replies.
        :return:
        """
        return self.replies.filter(approved=True, marked_as_deleted=False)

    objects = PostManager.from_queryset(PostQuerySet)()

    def __str__(self):
        return self.title

    def approve(self):
        self.approved = True
        self.save()

    def delete(self):
        # Ensure post deletion occurs inside a transaction, which means it has to delete both post and its replies or
        # don't delete any at all.
        with transaction.atomic():
            self.marked_as_deleted = True
            self.save()
            self.replies.delete()
        return

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at', '-approved']
        indexes = [
            models.Index(fields=['title'], name='idx_post_title'),
            models.Index(fields=['author'], name='idx_post_author'),
            models.Index(fields=['created_at'], name='idx_post_created_at'),
        ]
