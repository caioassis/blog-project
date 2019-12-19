import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Reply(models.Model):
    name = models.CharField(verbose_name='Name', max_length=40)
    email = models.EmailField(verbose_name='Email', unique=False)
    content = models.CharField(verbose_name='Content', max_length=250)
    marked_as_deleted = models.BooleanField(verbose_name='Marked as deleted', default=False)

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'


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
    author = models.ForeignKey(verbose_name='Author', to=User, related_name='posts', on_delete=models.SET_NULL, null=True)
    content = models.TextField(verbose_name='Content')
    replies = models.ManyToManyField(verbose_name='Replies', to=Reply, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Creation Date', auto_now_add=True, blank=True)
    published = models.BooleanField(default=False)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def publish(self):
        self.published = True
        self.save()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-published', '-deleted', '-created_at']
        indexes = [
            models.Index(fields=['title'], name='idx_post_title'),
            models.Index(fields=['author'], name='idx_post_author'),
            models.Index(fields=['created_at'], name='idx_post_created_at'),
        ]
