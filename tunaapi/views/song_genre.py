from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import SongGenre, Genre , Song

class SongGenreView(ViewSet):
  
  def retrieve(self, request, pk):
    """Handle GET requests for single song genre
          
        Returns:
            Response -- JSON serialized song genre
        """
    
    song_genre = SongGenre.objects.get(pk=pk)
    serializer = SongGenreSerializer(song_genre)
    return Response(serializer.data)
  
  def list(self, request):
        """Handle GET requests to get all genres 

        Returns:
            Response -- JSON serialized list of genres
        """
        song_genres = SongGenre.objects.all()
        serializer = SongGenreSerializer(song_genres, many=True)
        return Response(serializer.data)
      
  def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized genre instance
        """
        songId = Song.objects.get(pk=request.data["song_id"])
        genreId = Genre.objects.get(pk=request.data["genre_id"])

        songGenre = SongGenre.objects.create(
            song_id=songId,
            genre_id=genreId,
        )
        serializer = SongGenreSerializer(songGenre)
        return Response(serializer.data)

  def update(self, request, pk):
        """Handle PUT requests for a songGenre

        Returns:
            Response -- Empty body with 204 status code
        """
        songId = Song.objects.get(pk=request.data["song_id"])
        genreId = Genre.objects.get(pk=request.data["genre_id"])
        
        songGenre = SongGenre.objects.get(pk=pk)
        songGenre.song_id = songId
        songGenre.genre_id = genreId

        songGenre.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
        song_genre = SongGenre.objects.get(pk=pk)
        song_genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
  
class SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for genre 
    """
    class Meta:
        model = SongGenre
        fields = ('id', 'song_id', 'genre_id' )
        depth = 1
