from xml.parsers.expat import model
from django.db import models

# Create your models here.


class audios(models.Model):
    location = models.CharField(max_length=600)

    def __str__(self):
        return self.firstName
