from ..devstack import *

{% include "dt_learninghub/apps/settings/partials/common.py" %}

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ DT_LEARNINGHUB_OAUTH2_KEY_DEV }}"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "{{ DT_LEARNINGHUB_OAUTH2_SECRET }}"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://lms:8000/oauth2"

SOCIAL_AUTH_EDX_OAUTH2_KEY = "{{ DT_LEARNINGHUB_OAUTH2_KEY_SSO_DEV }}"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "{{ DT_LEARNINGHUB_OAUTH2_SECRET_SSO }}"
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "http://{{ LMS_HOST }}:8000"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = SOCIAL_AUTH_EDX_OAUTH2_ISSUER
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = SOCIAL_AUTH_EDX_OAUTH2_ISSUER + "/logout"

DISCOVERY_SERVICE_API_URL = "http://{{ DISCOVERY_HOST }}:8381/api/v1/"

CORS_ORIGIN_WHITELIST.append("http://{{ MFE_HOST }}:{{ DT_LEARNINGHUB_MFE_APP['port'] }}")
CORS_ORIGIN_WHITELIST.append("http://{{ MFE_HOST }}:{{ DT_LEARNINGHUB_DASHBOARD_MFE_APP['port'] }}")
CORS_ORIGIN_WHITELIST.append("http://{{ MFE_HOST }}:1999")

CSRF_TRUSTED_ORIGINS.append("{{ MFE_HOST }}:{{ DT_LEARNINGHUB_MFE_APP['port'] }}")
CSRF_TRUSTED_ORIGINS.append("{{ MFE_HOST }}:{{ DT_LEARNINGHUB_DASHBOARD_MFE_APP['port'] }}")
CSRF_TRUSTED_ORIGINS.append("{{ MFE_HOST }}:1999")

# TODO Remove
AUTO_AUTH = True

SWAGGER_SETTINGS = {
    'DOC_EXPANSION': 'list',
    "USE_SESSION_AUTH": True,
    "SECURITY_DEFINITIONS": {
        "Classroom API - Swagger": {
            "type": "oauth2",
            "authorizationUrl": SOCIAL_AUTH_EDX_OAUTH2_ISSUER + "/oauth2/authorize",
            "tokenUrl": SOCIAL_AUTH_EDX_OAUTH2_ISSUER + "/oauth2/access_token",
            "flow": "authorizationCode",
            "scopes": "user_id",
        }
    },
    "OAUTH2_REDIRECT_URL": "http://{{ DT_LEARNINGHUB_HOST }}:8180/static/drf-yasg/swagger-ui-dist/oauth2-redirect.html",
    "OAUTH2_CONFIG": {
        "clientId": "swagger_classroom",
        "clientSecret": "swagger",
        "appName": "swagger"

    },
}

{{ patch("dt-learninghub-development-settings") }}