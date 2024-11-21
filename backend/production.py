DEBUG = False


ALLOWED_HOSTS = ['*']

# TODO: we really need to properly configure allowed hosts (for some reason the following does not work)

# ALLOWED_HOSTS = [
#     "pulse-frontend-704608178414.us-east4.run.app",
#     "codehive.buzz",
# ]

CORS_ALLOWED_ORIGINS = [
    "https://pulse-frontend-704608178414.us-east4.run.app",
    "https://codehive.buzz",
]

DATABASE_OPTIONS_SSLMODE = "require"
