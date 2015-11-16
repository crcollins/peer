import datetime

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
    hash_value = models.CharField(max_length=64, null=True)

    def is_public(self):
        return self.status == ACCEPTED

    def is_reviewed(self):
        return self.status != PENDING

    def needs_revision(self):
        return self.status == REVISION

    def update_status(self, status):
        self.status = status
        if self.status == ACCEPTED:
            self.published = datetime.datetime.now()
        self.save()


class Revision(models.Model):
    comments = models.TextField(max_length=1024*1024)
    pdf_file = models.FileField(upload_to="papers")
    submitted = models.DateTimeField(auto_now=True)
    paper = models.ForeignKey(Paper, related_name="revisions")
    hash_value = models.CharField(max_length=64, null=True)

    class Meta:
        get_latest_by = "submitted"


class Review(models.Model):
    paper = models.ForeignKey(Paper, related_name="reviews")
    editor = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews")
    comments = models.TextField(max_length=1024*1024)
    decision = models.IntegerField(choices=DECISION_CHOICES)
    submitted = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        get_latest_by = "submitted"
