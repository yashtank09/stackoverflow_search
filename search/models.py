from django.db import models

# Create your models here.
class SearchResults(models.Model):
    question_id = models.IntegerField(primary_key=True)
    ques_link  = models.CharField(max_length=512, null=False)
    question_title = models.CharField(max_length=256, null=False)
