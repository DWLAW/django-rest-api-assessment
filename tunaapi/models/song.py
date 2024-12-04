from django.db import models
from .artist import Artist

class Song(models.Model):
    title = models.CharField(max_length=55)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.CharField(max_length=55)
    length = models.IntegerField()
