from google.auth import exceptions as auth_exceptions
from google.cloud import secretmanager
import os

def get_secret(secret_name):
    """Fetch a secret from Google Secret Manager using a service account key file locally or the default service account in Cloud Run."""
    try:
        # Modify secret name based on environment
        is_production = bool(os.getenv('K_SERVICE'))
        
        if is_production:
            secret_name += "_PRODUCTION"
        elif os.getenv('DOCKER_LOCAL'):
            secret_name += "_LOCAL_DOCKER"
        else:
            secret_name += "_LOCAL"
        
        # Access Google Secret Manager
        client = secretmanager.SecretManagerServiceClient()
        
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        if not project_id:
            raise Exception("GOOGLE_CLOUD_PROJECT environment variable is not set.")
        
        # Build the resource name of the secret
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        
        # Access the secret version
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")
    
    except auth_exceptions.DefaultCredentialsError as e:
        raise Exception("Failed to access Google Secret Manager: ensure your credentials are set correctly.") from e
    except Exception as e:
        raise Exception(f"An error occurred while accessing the secret '{secret_name}' from Google Secret Manager: {e}") from e