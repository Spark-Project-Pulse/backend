import os

DEBUG=False

ALLOWED_HOSTS = ['pulse-backend-704608178414.us-east4.run.app']

CORS_ALLOWED_ORIGINS = [
    os.environ.get('CORS_ALLOWED_ORIGIN'),
]

print(CORS_ALLOWED_ORIGINS)