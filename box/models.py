from django.db import models

from django.db import models

class Box(models.Model):
    title = models.CharField(max_length=255)
    color = models.CharField(max_length=20)

