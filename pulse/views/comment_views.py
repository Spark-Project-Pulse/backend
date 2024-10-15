from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from rest_framework import status
from ..models import Comments
from ..serializers import CommentSerializer


@api_view(["POST"])
def createComment(request: HttpRequest) -> JsonResponse:
    """Create a comment

    Returns:
        JsonResponse:
    """
    serializer = CommentSerializer(data=request.data)  # Use request.data for DRF (djang-rest-framework) compatibility
    if serializer.is_valid():
        comment = serializer.save()  # Save the new comment
        return JsonResponse(
            {"comment_id": comment.comment_id,
             "answer_id": comment.answer_id,
             "response": comment.response}, status=status.HTTP_201_CREATED
        )
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def getCommentsByAnswerId(request: HttpRequest, answer_id: str) -> JsonResponse:
    # Retrieve all comments for the given answer_id
    comments = Comments.objects.filter(answer=answer_id)
    
    # Serialize the list of comments, setting many=True to indicate multiple objects
    serializer = CommentSerializer(comments, many=True)

    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)