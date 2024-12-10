from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist, Genre

class SongView(ViewSet):
  
  def retrieve(self, request, pk):
    """Handle GET requests for single song
          
        Returns:
            Response -- JSON serialized song
        """
    
    song = Song.objects.get(pk=pk)
    serializer = SingleSongSerializer(song)
    return Response(serializer.data)
  
  def list(self, request):
        """Handle GET requests to get all songs 

        Returns:
            Response -- JSON serialized list of songs
        """
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
      
  def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized song instance
        """
        artist_id = Artist.objects.get(pk=request.data["artist_id"])
        
        song = Song.objects.create(
            title=request.data["title"],
            artist_id=artist_id,
            album=request.data["album"],
            length=request.data["length"]
        )
        serializer = SongSerializer(song)
        return Response(serializer.data)

  def update(self, request, pk):
    """Handle PUT requests for an song

    Returns:
        Response -- Empty body with 204 status code
    """
    artist_id = Artist.objects.get(pk=request.data["artist_id"])

    song = Song.objects.get(pk=pk)
    song.title = request.data["title"]
    song.artist_id = artist_id
    song.album = request.data["album"]
    song.length = request.data["length"]
    song.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  
  def destroy(self, request, pk):
    song = song.objects.get(pk=pk)
    song.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  
  
class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for song 
    """
    class Meta:
        model = Song
        fields = ('id', 'artist_id', 'title', 'album', 'length')

class SingleSongSerializer(serializers.ModelSerializer):
    """JSON serializer for song types
    """
    class Meta:
        model = Song
        fields = ('id', 'artist_id', 'title', 'album', 'length', 'genres')
        depth = 2
