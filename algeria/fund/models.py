from django.db import models

# Create your models here.
class Fund(models.Model):
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    posted_date = models.DateTimeField()
    closed_date = models.DateTimeField()
    link = models.URLField(max_length=255)

    def __str__(self):
        return self.title