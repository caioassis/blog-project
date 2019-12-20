from django.db.models import QuerySet


class PostQuerySet(QuerySet):

    def published(self):
        return self.filter(approved=True)

    def unpublished(self):
        return self.filter(approved=False)


class ReplyQuerySet(QuerySet):

    def approved_only(self):
        return self.filter(approved=True)
