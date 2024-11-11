from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from rest_framework import status
from ..supabase_utils import check_content
from ..models import Comments
from ..serializers import CommentSerializer


@api_view(["POST"])
def createComment(request: HttpRequest) -> JsonResponse:
    """
    Create a comment for the given question

    Args:
        request (HttpRequest): The incoming HTTP request containing the data.

    Returns:
        JsonResponse: A response with comment's data if successful, or invalidation errors if unsuccessful
    """
    serializer = CommentSerializer(data=request.data)  # Use request.data for DRF (djang-rest-framework) compatibility
    if serializer.is_valid():
        # Content moderation
        response_text = request.data['response']
        if check_content(response_text):
            return JsonResponse({"toxic": True}, status=status.HTTP_400_BAD_REQUEST)
        comment = serializer.save()  # Save the new comment
        serialized_comment = CommentSerializer(comment)  # Serialize the saved comment
        return JsonResponse(serialized_comment.data, status=status.HTTP_201_CREATED)  # Return the serialized data

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def getCommentsByAnswerId(request: HttpRequest, answer_id: str) -> JsonResponse:
    """
    Gets all comments for an answer

    Args:
        request (HttpRequest): The incoming HTTP request
        answer_id (str): The answer's id

    Returns:
        JsonResponse: A response with list of comments
    """
    # Retrieve all comments for the given answer_id
    comments = Comments.objects.filter(answer=answer_id)
    
    # Serialize the list of comments, setting many=True to indicate multiple objects
    serializer = CommentSerializer(comments, many=True)

    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)