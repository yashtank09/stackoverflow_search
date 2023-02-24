from django.db import models
# Create your models here.
class SearchResults(models.Model):
    query = models.CharField(max_length=255, unique=True)
    results = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)