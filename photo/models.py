from django.db import models
from datetime import datetime

class Photo(models.Model):
    name = models.URLField(max_length=400,verbose_name="URL")
    dateadded = models.DateTimeField(auto_now_add=datetime.now())
