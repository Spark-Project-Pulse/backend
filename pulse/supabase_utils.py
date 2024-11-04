# NOTE: commenting out this file (for now), as we are using the Django ORM instead (can bring this back if needed)
# NOTE: bringing this back since it is needed to access supabase's storage system

from django.conf import settings
from supabase import create_client, Client

def get_supabase_client() -> Client:
  url: str = settings.SUPABASE_URL
  key: str = settings.SUPABASE_ANON_KEY
  return create_client(url, key)