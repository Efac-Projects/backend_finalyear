from django.db import models

# Create your models here.


class textTobeAudio(models.Model):
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.text
