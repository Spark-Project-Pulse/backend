from rest_framework.decorators import api_view, parser_classes
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import JsonResponse, HttpRequest
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings
from ..models import Hives, HiveMembers, Users, UserRoles
from ..serializers import HiveSerializer, HiveMemberSerializer
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count, Q
from uuid import UUID
from services.notification_service import NotificationService
from rest_framework.parsers import MultiPartParser
from ..supabase_utils import get_supabase_client, create_bucket_if_not_exists
from services.ai_model_service import check_img_content, check_content
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import throttle_classes
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Count, Q, F
from django.db.models.functions import Greatest
from django.contrib.postgres.aggregates import StringAgg
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.views.decorators.http import require_GET

'''POST Requests'''

@api_view(["POST"])
@parser_classes([MultiPartParser])  # To handle file uploads
def createHiveRequest(request: HttpRequest) -> JsonResponse:
    """
    Create a hive request using the HiveSerializer to validate
    and save the incoming data.

    Args:
        request (HttpRequest): The incoming HTTP request containing the data.

    Returns:
        JsonResponse: A response with the requested hive ID if successful,
        or validation errors if the data is invalid.
    """
    # Deserialize and validate the data
    serializer = HiveSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Text Content moderation
    title = request.data['title']
    description = request.data['description']
    if check_content(title + description):
        return JsonResponse({"error": "Toxic content detected in your hive."}, status=status.HTTP_200_OK)
    
    # Save the valid data as a new Hive instance
    hive = serializer.save()
    
    # Handle the optional image upload
    avatar_file = request.FILES.get('avatar')
    if avatar_file:
        # Image Content moderation
        image_content = avatar_file.read()
        if check_img_content(image_content):
            return JsonResponse({"error": "Innapropriate content detected in your image."}, status=status.HTTP_200_OK)
        # Get Supabase client
        supabase = get_supabase_client()

        # Create bucket if it does not exist
        if not create_bucket_if_not_exists('hive-avatars'):
            return JsonResponse({'error': 'Could not ensure bucket exists.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Set the upload path in Supabase Storage
        upload_path = f"{hive.hive_id}/avatar"

        # Upload the image file to Supabase Storage
        response = supabase.storage.from_("hive-avatars").upload(
            path=upload_path,
            file=image_content,
            file_options={"content-type": avatar_file.content_type, "upsert": "true"}
        )

        if response.path:
            # Store the image URL in the hive's data
            hive.avatar_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/hive-avatars/{upload_path}"
            hive.save()
        else:
            return JsonResponse({"error": "Failed to upload hive avatar"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse(
        {"hive_id": hive.hive_id, "title": hive.title},
        status=status.HTTP_201_CREATED
    )

@api_view(["POST"])
def approveHiveRequest(request: HttpRequest) -> JsonResponse:
    """
    Approve a hive request by setting approved=True. 
    Adds the owner as a hive member if approval is successful.

    Args:
        request (HttpRequest): The incoming HTTP request containing hive_id and user_id.

    Returns:
        JsonResponse: A success message or an error message.
    """
    # Extract hive_id and role from the request body
    hive_id = request.data.get('hive_id')
    user_id = request.data.get('user_id')
    
    # Get the hive or return 404 if not found
    hive = get_object_or_404(Hives, hive_id=hive_id, approved=False)
    user_role = get_object_or_404(UserRoles, role=user_id).role_type
    
    # Check if the user has admin privileges
    if user_role != 'admin':
        return JsonResponse({"error": "Unauthorized: Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)

    # Approve the hive request
    hive.approved = True
    hive.save()

    # Add the owner to HiveMembers if there is an owner
    if hive.owner:
        HiveMembers.objects.create(hive=hive, user=hive.owner)
        hive.member_count += 1  # Increment member count by 1
        NotificationService.handle_hive_accepted(hive) # Handle notifications
        hive.save()
        
    return JsonResponse({"message": "Hive request approved successfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def rejectHiveRequest(request: HttpRequest) -> JsonResponse:
    """
    Reject a hive request by deleting the hive from the database.

    Args:
        request (HttpRequest): The incoming HTTP request containing hive_id and user_id.

    Returns:
        JsonResponse: A success message or an error message.
    """
    # Extract hive_id and role from the request body
    hive_id = request.data.get('hive_id')
    user_id = request.data.get('user_id')
    
    # Get the hive or return 404 if not found
    hive = get_object_or_404(Hives, hive_id=hive_id, approved=False)
    user_role = get_object_or_404(UserRoles, role=user_id).role_type
    
    # Check if the user has admin privileges
    if user_role != 'admin':
        return JsonResponse({"error": "Unauthorized: Admin privileges required"}, status=status.HTTP_403_FORBIDDEN)
    
    # Get the hive or return 404 if not found
    hive = get_object_or_404(Hives, hive_id=hive_id, approved=False)
    NotificationService.handle_hive_rejected(hive.owner, hive.title) # Handle notifications

    # Delete the hive request
    hive.delete()
    
    return JsonResponse({"message": "Hive request rejected successfully"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def addHiveMember(request: HttpRequest) -> JsonResponse:
    """
    Add a member, increasing its member count by 1
    and add them to the HiveMembers table.

    Args:
        request (HttpRequest): The incoming HTTP request containing hive_id and user_id.

    Returns:
        JsonResponse: Success message or error message.
    """
    hive_id = request.data.get('hive_id')
    user_id = request.data.get('user_id')

    hive = get_object_or_404(Hives, pk=hive_id)
    user = get_object_or_404(Users, pk=user_id)

    # Added the user to the hive
    HiveMembers.objects.create(hive=hive, user=user)
    hive.member_count += 1  # Increment member count by 1
    hive.save()

    return JsonResponse({"message": "Join successful"}, status=status.HTTP_200_OK)

@api_view(["POST"])
def removeHiveMember(request: HttpRequest) -> JsonResponse:
    """
    Remove a member, decreasing its member count by 1
    and remove them from the HiveMembers table.

    Args:
        request (HttpRequest): The incoming HTTP request containing hive_id and user_id.

    Returns:
        JsonResponse: Success message or error message.
    """
    hive_id = request.data.get('hive_id')
    user_id = request.data.get('user_id')

    hive = get_object_or_404(Hives, pk=hive_id)
    user = get_object_or_404(Users, pk=user_id)
    
    existing_member = HiveMembers.objects.filter(hive=hive, user=user).first()

    # Remove the user from the hive
    existing_member.delete()
    hive.member_count -= 1  # Decrement member count by 1
    hive.save()

    return JsonResponse({"message": "Remove successful"}, status=status.HTTP_200_OK)

'''GET Requests'''

@api_view(["GET"])
def getAllHives(request: HttpRequest) -> JsonResponse:
    """
    Retrieve hives from the database with pagination, optional tag filtering, and search functionality.
    """
    # Get query parameters
    page_number = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    selected_tags = request.GET.getlist('tags')  # Expecting UUIDs like ?tags=uuid1&tags=uuid2
    search_query = request.GET.get('search', '').strip()

    # Start with all approved hives, ordered by creation date descending
    hives = Hives.objects.filter(approved=True)

    # Apply search filter if search_query is provided
    if search_query:
        search_vector = SearchQuery(search_query, search_type='websearch')
        hives = hives.annotate(
            rank=SearchRank('search_vector', search_vector)
        ).filter(search_vector=search_vector).order_by('-rank', '-member_count')
    else:
        hives = hives.order_by('-member_count')

    # Filter hives by tags if any tags are provided
    if selected_tags:
        # Convert tag IDs to UUID objects
        try:
            selected_tags = [UUID(tag_id) for tag_id in selected_tags]
        except ValueError:
            return JsonResponse({'error': 'Invalid tag IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
        num_selected_tags = len(selected_tags)

        # Filter hives that have all of the selected tags
        hives = hives.filter(tags__tag_id__in=selected_tags)
        hives = hives.annotate(
            matching_tags=Count('tags', filter=Q(tags__tag_id__in=selected_tags), distinct=True)
        ).filter(matching_tags=num_selected_tags)

    # Remove duplicates
    hives = hives.distinct()

    # Pagination
    paginator = Paginator(hives, page_size)
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = []

    serializer = HiveSerializer(page_obj.object_list, many=True)
    
    response_data = {
        'hives': serializer.data,
        'totalHives': paginator.count,
        'totalPages': paginator.num_pages,
        'currentPage': page_number,
    }
    return JsonResponse(response_data, status=status.HTTP_200_OK)

@api_view(["GET"])
def getAllHiveOptions(request: HttpRequest) -> JsonResponse:
    """
    Retrieve all approved hives from the database and serialize them
    to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        Json
    """
    hives = Hives.objects.filter(approved=True)
    serializer = HiveSerializer(hives, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(["GET"])
def getAllHiveMembers(request: HttpRequest, hive_id: str) -> JsonResponse:
    """
    Get all hive members by hive ID.

    Args:
        request (HttpRequest): The incoming HTTP request.
        hive_id (str): The ID of the hive.

    Returns:
        JsonResponse: A response indicating whether the user is part of the hive.
    """
    # Validate hive
    hive = get_object_or_404(Hives, hive_id=hive_id)

    # Get the users that are part of the hive
    members = HiveMembers.objects.filter(hive=hive).order_by('-hive_reputation')
    
    # Serialize the list of members, setting many=True to indicate multiple objects
    serializer = HiveMemberSerializer(members, many=True)

    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(["GET"])
def getHiveById(request: HttpRequest, hive_id: str) -> JsonResponse:
    """
    Retrieve a single hive by its ID and serialize it to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.
        hive_id (str): The ID of the hive to retrieve.

    Returns:
        JsonResponse: A response containing serialized data for the requested hive.
    """
    hive = get_object_or_404(Hives, hive_id=hive_id, approved=True)  # Get the hive or return 404
    serializer = HiveSerializer(hive)  # Serialize the single instance to JSON
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def getHiveByTitle(request: HttpRequest, title: str) -> JsonResponse:
    """
    Retrieve a single hive by its title and serialize it to JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.
        title (str): The title of the hive to retrieve.

    Returns:
        JsonResponse: A response containing serialized data for the requested hive.
    """
    hive = get_object_or_404(Hives, title=title, approved=True)  # Get the hive or return 404
    serializer = HiveSerializer(hive)  # Serialize the single instance to JSON
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def getUserHivesById(request: HttpRequest, user_id: str) -> JsonResponse:
    """
    Retrieve all hives associated with a user's ID and return them in JSON format.

    Args:
        request (HttpRequest): The incoming HTTP request.
        user_id (str): The ID of the user whose hives are to be retrieved.

    Returns:
        JsonResponse: A response containing serialized data for the user's hives.
    """
    hives = get_list_or_404(HiveMembers, user=user_id)
    serializer = HiveMemberSerializer(hives, many=True)  # Serialize multiple instances
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(["GET"])
def getAllHiveRequests(request: HttpRequest) -> JsonResponse:
    """
    Retrieve all hive requests that are not yet approved, ordered by the oldest first.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A response with a list of hive requests.
    """
    # Filter for hives where approved is False and order by created_at (oldest first)
    hive_requests = Hives.objects.filter(approved=False).order_by('created_at')
    serializer = HiveSerializer(hive_requests, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(["GET"])
def userIsPartOfHive(request: HttpRequest, title: str, user_id: str) -> JsonResponse:
    """
    Check if a user is part of a hive by hive title and user ID.

    Args:
        request (HttpRequest): The incoming HTTP request.
        title (str): The title of the hive.
        user_id (str): The ID of the user.

    Returns:
        JsonResponse: A response indicating whether the user is part of the hive.
    """
    # Validate hive and user
    hive = get_object_or_404(Hives, title=title)
    user = get_object_or_404(Users, pk=user_id)

    # Check if the user is part of the hive
    is_member = HiveMembers.objects.filter(hive=hive, user=user).exists()

    return JsonResponse({"is_member": is_member}, status=status.HTTP_200_OK)

class BurstUserRateThrottle(UserRateThrottle):
    rate = '10/min'

class BurstAnonRateThrottle(AnonRateThrottle):
    rate = '5/min'

@require_GET
@csrf_exempt
@throttle_classes([BurstUserRateThrottle, BurstAnonRateThrottle])
def searchHives(request):
    # Get query parameters
    query = request.GET.get('q', '').strip()
    tags = request.GET.getlist('tags')  # Expecting tag IDs as strings
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 20)  # Default page size

    if not query and not tags:
        return JsonResponse(
            {"error": "No search query or tags provided."},
            status=status.HTTP_400_BAD_REQUEST
        )

    hives = Hives.objects.all()

    # Initialize combined_filters as Q() for AND logic
    combined_filters = Q()

    # Handle search query
    if query:
        # Define the search vector with weights
        search_vector = (
            SearchVector('title', weight='A') +
            SearchVector('description', weight='B') +
            SearchVector('tags__name', weight='C')
        )
        search_query = SearchQuery(query, search_type="websearch")
        
        # Annotate with full-text search rank and trigram similarities
        hives = hives.annotate(
            rank=SearchRank(search_vector, search_query),
            similarity_title=TrigramSimilarity('title', query),
            similarity_description=TrigramSimilarity('description', query),
        ).annotate(
            tag_names=StringAgg('tags__name', delimiter=' ', distinct=True)
        ).annotate(
            similarity_tags=TrigramSimilarity('tag_names', query)
        ).annotate(
            total_similarity=Greatest(
                F('similarity_title'),
                F('similarity_description'),
                F('similarity_tags')
            )
        )

        # Combine search filters using OR logic within search criteria
        search_filter = Q(search_vector=search_query) | Q(total_similarity__gt=0.05)

        combined_filters &= search_filter

    # Handle tag filters
    if tags:
        try:
            # Convert tag IDs to UUID objects
            tag_uuids = [UUID(tag_id) for tag_id in tags]
        except ValueError:
            return JsonResponse({'error': 'Invalid tag IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        tag_filters = Q()
        for tag_uuid in tag_uuids:
            tag_filters &= Q(tags__tag_id=tag_uuid)
        
        combined_filters &= tag_filters

    # Apply the combined AND filters
    hives = hives.filter(combined_filters).distinct().order_by('-rank', '-total_similarity', '-created_at')

    # Implement Pagination
    try:
        page_number = int(page_number)
        page_size = int(page_size)
        if page_number < 1 or page_size < 1:
            raise ValueError
    except ValueError:
        return JsonResponse({'error': 'Invalid page or page_size parameter'}, status=status.HTTP_400_BAD_REQUEST)

    paginator = Paginator(hives, page_size)
    try:
        paginated_hives = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_hives = paginator.page(1)
    except EmptyPage:
        paginated_hives = paginator.page(paginator.num_pages)

    serializer = HiveSerializer(paginated_hives.object_list, many=True)
    return JsonResponse({
        'hives': serializer.data,
        'totalHives': paginator.count,
        'totalPages': paginator.num_pages,
        'currentPage': page_number,
    }, status=status.HTTP_200_OK)
