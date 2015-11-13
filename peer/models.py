from django.db import models
from django.conf import settings


class Paper(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField(max_length=1024)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    pdf_file = models.FileField(upload_to="papers")
    submitted = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(auto_now=False, null=True)

    def is_public(self):
        return bool(self.published)


