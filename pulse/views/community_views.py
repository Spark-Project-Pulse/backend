from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from django.http import JsonResponse
from rest_framework import status
from ..models import Communities
from ..serializers import CommunitySerializer
from rest_framework.decorators import throttle_classes

@api_view(["POST"])
def createCommunity(request: HttpRequest) -> JsonResponse:
    """
    Create a community using the CommunitySerializer to validate
    and save the incoming data.

    Args:
        request (HttpRequest): The incoming HTTP request containing the data.

    Returns:
        JsonResponse: A response with the created community's ID if successful,
        or validation errors if the data is invalid.
    """
    serializer = CommunitySerializer(
        data=request.data
    )  # Deserialize and validate the data
    if serializer.is_valid():
        community = serializer.save()  # Save the valid data as a new Community instance
        return JsonResponse(
            {"community_id": community.community_id}, status=status.HTTP_201_CREATED
        )
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def getAllCommunities(request: HttpRequest) -> JsonResponse:
    """
    Retrieve communities from the database with pagination, optional tag filtering, and search functionality.
    """
    # Get query parameters
    # page_number = int(request.GET.get('page', 1))
    # page_size = int(request.GET.get('page_size', 20))
    # selected_tags = request.GET.getlist('tags')  # Expecting UUIDs like ?tags=uuid1&tags=uuid2
    # search_query = request.GET.get('search', '').strip()

    # Start with all communities, ordered by creation date descending
    communities = Communities.objects.all()

    # Apply search filter if search_query is provided
    # if search_query:
    #     search_vector = SearchQuery(search_query, search_type='websearch')
    #     communities = communities.annotate(
    #         rank=SearchRank('search_vector', search_vector)
    #     ).filter(search_vector=search_vector).order_by('-rank', '-created_at')
    # else:
    #     communities = communities.order_by('-created_at')

    # Filter communities by tags if any tags are provided
    # if selected_tags:
    #     # Convert tag IDs to UUID objects
    #     try:
    #         selected_tags = [UUID(tag_id) for tag_id in selected_tags]
    #     except ValueError:
    #         return JsonResponse({'error': 'Invalid tag IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
    #     num_selected_tags = len(selected_tags)

    #     # Filter communities that have all of the selected tags
    #     communities = communities.filter(tags__tag_id__in=selected_tags)
    #     communities = communities.annotate(
    #         matching_tags=Count('tags', filter=Q(tags__tag_id__in=selected_tags), distinct=True)
    #     ).filter(matching_tags=num_selected_tags)

    # Remove duplicates
    communities = communities.distinct()

    # Pagination
    # paginator = Paginator(communities, page_size)
    # try:
    #     page_obj = paginator.page(page_number)
    # except EmptyPage:
    #     page_obj = []

    # serializer = CommunitySerializer(page_obj.object_list, many=True)
    serializer = CommunitySerializer(communities, many=True)
    
    # response_data = {
    #     'communities': serializer.data,
    #     'totalCommunities': paginator.count,
    #     'totalPages': paginator.num_pages,
    #     'currentPage': page_number,
    # }
    # return JsonResponse(response_data, status=status.HTTP_200_OK)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(["GET"])
def getCommunityById(request: HttpRequest, community_id: str) -> JsonResponse:
    """
    Retrieve a single community by its ID and serialize it to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.
        community_id (str): The ID of the community to retrieve.

    Returns:
        JsonResponse: A response containing serialized data for the requested community.
    """
    community = get_object_or_404(
        Communities, community_id=community_id
    )  # Get the community or return 404
    serializer = CommunitySerializer(community)  # Serialize the single instance to JSON
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)

