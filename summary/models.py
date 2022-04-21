from typing import Iterable, Optional
from django.db import models
from django.forms import ValidationError

# Create your models here.


class Summary(models.Model):

    class Ministry_Choices(models.TextChoices):
        MINISTRY_1 = "CENTRAL MINISTRY"
        MINISTRY_2 = "STATE MINISTRY"

    text = models.CharField(max_length=10000, blank=True)
    link = models.CharField(max_length=10000, blank=True)
    heading = models.CharField(max_length=10000, blank=False, null=False)
    slug = models.SlugField(null=False)
    summary = models.CharField(max_length=10000, blank=False, null=False)
    highlights = models.CharField(max_length=10000, blank=False, null=False)
    assets = models.CharField(max_length=10000, blank=False, null=True)
    ministry = models.CharField(
        max_length=10000, choices=Ministry_Choices.choices)
