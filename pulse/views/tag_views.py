from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..models import Tags
from rest_framework import status
from ..serializers import TagSerializer

@api_view(["GET"])
def get_all_tags(request):
    """Retrieve all available tags."""
    tags = Tags.objects.all()
    serializer = TagSerializer(tags, many=True)
    return JsonResponse(serializer.data, safe=False)
