from glob import glob
import os
import pkg_resources

from .__about__ import __version__

templates = pkg_resources.resource_filename("classroom_plugin", "templates")

config = {
    "add": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 24|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}diceytech/dt-classroom:{{ DT_CLASSROOM_VERSION }}",
        "HOST": "classroom.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "classroom",
        "MYSQL_USERNAME": "classroom",
        "OAUTH2_KEY": "classroom",
        "OAUTH2_KEY_DEV": "classroom-dev",
        "OAUTH2_KEY_SSO": "classroom-sso",
        "OAUTH2_KEY_SSO_DEV": "classroom-sso-dev",
        "CACHE_REDIS_DB": "{{ OPENEDX_CACHE_REDIS_DB }}",
        "MFE_APP": {
            "name": "classroom",
            "repository": "https://github.com/Dicey-Tech/frontend-app-classroom",
            "port": 8080,
            "version": "main",
        },
        "DASHBOARD_MFE_APP": {
            "name": "dasbhoard",
            "repository": "https://github.com/Dicey-Tech/frontend-app-teacher-dashboard",
            "port": 8081,
            "version": "develop",
            "env": {
                "production": {
                    "CLASSROOM_BASE_URL": "{{ DT_CLASSROOM_HOST }}",
                    "CLASSROOM_MFE_URL": "apps.{{ LMS_HOST }}/{{ DT_CLASSROOM_MFE_APP['name'] }}",
                },
                "development": {
                    "CLASSROOM_BASE_URL": "{{ DT_CLASSROOM_HOST }}:8180",
                    "CLASSROOM_MFE_URL": "apps.{{ LMS_HOST }}:{{ DT_CLASSROOM_MFE_APP['port'] }}/{{ DT_CLASSROOM_MFE_APP['name'] }}",
                },
            },
        },
    },
}

hooks = {
    "build-image": {"dt_classroom": "{{ DT_CLASSROOM_DOCKER_IMAGE }}"},
    "init": ["mysql", "dt_classroom", "lms"],
}


def patches():
    all_patches = {}
    patches_dir = pkg_resources.resource_filename("classroom_plugin", "patches")
    for path in glob(os.path.join(patches_dir, "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
