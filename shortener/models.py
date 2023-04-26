from django.db import models

# Create your models here.

class Urls(models.Model):
    url = models.URLField(max_length=2000)
    shortened_url_id = models.IntegerField(blank=True,null=True)
    title = models.CharField(max_length=2000, blank=True)
    access_count = models.IntegerField(default=0)
    def __str__(self):
        return self.url