from django.db import models

# Create your models here.
class Resource(models.Model):
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=255)
    presenters = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    presentation_type = models.CharField(max_length=255, null=True, blank=True)
    technical_topics = models.CharField(max_length=255, null=True, blank=True)
    presentation_date = models.DateTimeField(null=True, blank=True)
    publication_status = models.CharField(max_length=255, null=True, blank=True)
    presentation_slides = models.URLField(max_length=255, null=True, blank=True)
    documents = models.URLField(max_length=255, null=True, blank=True)
    captions = models.URLField(max_length=255, null=True, blank=True)
    presentation_video = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

