from django.conf import settings
from supabase import create_client, Client


def get_supabase_client() -> Client:
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_ANON_KEY
    return create_client(url, key)


def create_bucket_if_not_exists(bucket_name):
    """
    Checks if the specified bucket exists and creates it if it doesn't.
    """
    supabase = get_supabase_client()

    # Check if the bucket exists
    buckets = supabase.storage.list_buckets()

    # Check if the response is successful and get the list of buckets
    if isinstance(buckets, list):

        # Get all bucket names
        bucket_names = [bucket.name for bucket in buckets]

        # Check if the specified bucket already exists
        if bucket_name in bucket_names:
            print(f"Bucket '{bucket_name}' already exists.")
        else:
            # Create the bucket since it doesn't exist
            try:
                response = supabase.storage.create_bucket(bucket_name)
                if "error" in response:
                    print(f"Error creating bucket: {response['error']}")
                    return False
                else:
                    print(f"Bucket '{bucket_name}' created successfully.")
                return True
            except Exception as e:
                print("Error creating bucket: ", e)
                return False
    else:
        print(f"Unexpected response format: {buckets}")

    return True