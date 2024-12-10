from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, Song

class GenreView(ViewSet):
  
  def retrieve(self, request, pk):
    """Handle GET requests for single genre
          
        Returns:
            Response -- JSON serialized genre
        """
    try:
            genre = Genre.objects.get(pk=pk)
            songs = Song.objects.filter(genresforsongs__genre_id=genre)
            genre.songs = songs.all()
            serializer = SingleGenreSerializer(genre)
            return Response(serializer.data)
    except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
  def list(self, request):
        """Handle GET requests to get all genres 

        Returns:
            Response -- JSON serialized list of genres
        """
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
      
  def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized genre instance
        """
        genre = Genre.objects.create(
            description=request.data["description"],
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

  def update(self, request, pk):
    """Handle PUT requests for an genre

    Returns:
        Response -- Empty body with 204 status code
    """

    genre = Genre.objects.get(pk=pk)
    genre.description = request.data["description"]
    genre.save()

    serializer = GenreSerializer(genre)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  
  def destroy(self, request, pk):
    genre = Genre.objects.get(pk=pk)
    genre.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  
  
class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for genre 
    """
    class Meta:
        model = Genre
        fields = ('id', 'description')
        
class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for song 
    """
    class Meta:
        model = Song
        fields = ('id', 'artist_id', 'title', 'album', 'length')
class SingleGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for artist types
    """
    songs = SongSerializer(read_only=True, many=True)
    class Meta:
        model = Genre
        fields = ('id', 'description', 'songs')
        depth = 1
