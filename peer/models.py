from django.db import models
from django.conf import settings


PENDING = 0
REJECTED = 1
REVISION = 2
ACCEPTED = 3

DECISION_CHOICES = (
    (REJECTED, "Rejected"),
    (REVISION, "Revision"),
    (ACCEPTED, "Accepted"),
)
STATUS_CHOICES = ((PENDING, "Pending"), ) + DECISION_CHOICES


class Paper(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField(max_length=1024)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    pdf_file = models.FileField(upload_to="papers")
    submitted = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(auto_now=False, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)

    def is_public(self):
        return self.status == ACCEPTED

