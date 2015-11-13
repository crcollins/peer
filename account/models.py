from django.db import models
from django.conf import settings

from utils import generate_key


class ActivationKey(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now=True)
    value = models.CharField(max_length=10, default=generate_key)

