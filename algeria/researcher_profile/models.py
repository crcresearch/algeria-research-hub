from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Research_Area(models.Model): ####implement fuzzy matching / standardization of names
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Collaboration_Area(models.Model): ####implement fuzzy matching / standardization of names
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Link(models.Model):
    link = models.URLField(max_length=255, null=True, blank=True)
    link_type = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, related_name='links') # foreign key for professional links

    def __str__(self):
        return self.name



class Profile(models.Model):
    name = models.CharField(max_length=255)
    image = models.URLField(max_length=255, null=True, blank=True)
    institution = models.ManyToManyField(Institution)
    department = models.ManyToManyField(Department)
    position = models.ManyToManyField(Position)
    email = models.EmailField(max_length=254)
    resume_cv_link = models.URLField(max_length=255, null=True, blank=True)
    whatsapp = models.CharField(max_length=4096)
    research_areas = models.ManyToManyField(Research_Area, related_name='primary')
    research_overview = models.TextField()
    collaboration_areas = models.ManyToManyField(Research_Area, related_name='collaboration')
    recent_publications = models.TextField()

    def __str__(self):
        return self.title
