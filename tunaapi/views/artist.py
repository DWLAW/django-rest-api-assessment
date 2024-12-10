from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Count
from tunaapi.models import Artist

class ArtistView(ViewSet):
  
  def retrieve(self, request, pk):
    """Handle GET requests for single artist
          
        Returns:
            Response -- JSON serialized artist
        """
    artist = Artist.objects.get(pk=pk)
    serializer = SingleArtistSerializer(artist)
    return Response(serializer.data)
  
  def list(self, request):
        """Handle GET requests to get all artists 

        Returns:
            Response -- JSON serialized list of artists
        """
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)
      
  def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized artist instance
        """
        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"],
        )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

  def update(self, request, pk):
    """Handle PUT requests for an artist

    Returns:
        Response -- Empty body with 204 status code
    """

    artist = Artist.objects.get(pk=pk)
    artist.name = request.data["name"]
    artist.age = request.data["age"]
    artist.bio = request.data["bio"]
    artist.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  
  def destroy(self, request, pk):
    artist = Artist.objects.get(pk=pk)
    artist.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  
  
class ArtistSerializer(serializers.ModelSerializer):
    song_count = serializers.IntegerField(default=None)
    """JSON serializer for artist 
    """
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count',)
class SingleArtistSerializer(serializers.ModelSerializer):
    song_count = serializers.IntegerField(default=None)
    """JSON serializer for artist types
    """
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')
        depth = 1
        db_table = 'songs'
