from django.db import models
from django.conf import settings


class Paper(models.Model):
    PENDING = 0
    REJECTED = 1
    REVISION = 2
    ACCEPTED = 3
    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (REJECTED, "Rejected"),
        (REVISION, "Revision"),
        (ACCEPTED, "Accepted"),
    )
    title = models.CharField(max_length=255)
    abstract = models.TextField(max_length=1024)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    pdf_file = models.FileField(upload_to="papers")
    submitted = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(auto_now=False, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)

    def is_public(self):
        return self.status == Paper.ACCEPTED

