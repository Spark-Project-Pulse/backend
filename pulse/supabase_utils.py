# NOTE: commenting out this file (for now), as we are using the Django ORM instead (can bring this back if needed)

# import os
# from supabase import create_client, Client

# def get_supabase_client() -> Client:
#     url: str = os.environ.get("SUPABASE_URL")
#     key: str = os.environ.get("SUPABASE_KEY")
#     return create_client(url, key)