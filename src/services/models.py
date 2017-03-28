from __future__ import unicode_literals
from django.db import models
from redactor.fields import RedactorField

class Option(models.Model):
    name = models.SlugField(max_length=20, help_text="Unique name for this option.")
    value = models.CharField(max_length=100, help_text="Value for this option.")

    def __unicode__(self):
        return self.name
