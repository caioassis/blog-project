from django.db.models import Manager


class PostManager(Manager):

    def get_queryset(self):
        """
        Override get_queryset method to prevent fetching deleted posts, but they still exist in database.
        :return:
        """
        return super().get_queryset().filter(marked_as_deleted=False)

    def published(self):
        return self.get_queryset().published()

    def unpublished(self):
        return self.get_queryset().unpublished()


class ReplyManager(Manager):

    def get_queryset(self):
        """
        Override get_queryset method to prevent fetching deleted replies, but they still exist in database.
        :return:
        """
        return super().get_queryset().filter(marked_as_deleted=False)


