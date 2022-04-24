from xml.parsers.expat import model
from django.db import models

# Create your models here.


class approvals(models.Model):
    firstName = models.CharField(max_length=15)

    def __str__(self):
        return self.firstName
