from django.http import JsonResponse
from .supabase_utils import get_supabase_client

# Example: Fetch data from a table called 'test_table'
def test_supabase_get(request):
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("test_table").select("*").execute()

        return JsonResponse({"status": "success", "data": response.data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

# Example: Put data into a table called 'test-table'
def test_supabase_set(request):
    supabase = get_supabase_client()
    
    try:
        data = { "id": 3, "name": "testing"}
        
        response = supabase.table("test_table").insert(data).execute()
        return JsonResponse({"status": "success", "data": response.data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)