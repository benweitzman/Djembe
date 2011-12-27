from django.db import models
from datetime import datetime

class Photo(models.Model):
    name = models.CharField(max_length=400)
    dateadded = models.DateTimeField(auto_now_add=datetime.now())
