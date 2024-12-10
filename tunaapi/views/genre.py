from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre

class GenreView(ViewSet):
  
  def retrieve(self, request, pk):
    """Handle GET requests for single genre
          
        Returns:
            Response -- JSON serialized genre
        """
    
    genre = Genre.objects.get(pk=pk)
    serializer = SingleGenreSerializer(genre)
    return Response(serializer.data)
  
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
        return Response(serializer.data)

  def update(self, request, pk):
    """Handle PUT requests for an genre

    Returns:
        Response -- Empty body with 204 status code
    """

    genre = Genre.objects.get(pk=pk)
    genre.description = request.data["description"]
    genre.save()

    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  
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
class SingleGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for artist types
    """
    class Meta:
        model = Genre
        fields = ('id', 'description', 'songs')
        depth = 1
        db_table = 'songs'
