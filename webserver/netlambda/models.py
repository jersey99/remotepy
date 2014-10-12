from django.db import models
from djangotoolbox.fields import ListField

class Function(models.Model):
    created_on = models.DateTimeField(auto_add_now=True, null=True)
    name = models.CharField()
    body = models.TextField()
