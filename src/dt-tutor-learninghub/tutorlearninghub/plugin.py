from glob import glob
import os
import pkg_resources

from .__about__ import __version__

templates = pkg_resources.resource_filename("tutorlearninghub", "templates")

config = {
    "add": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 24|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
    },
    "defaults": {
        "PORT": "8180",
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}diceytech/dt-learninghub:{{ DT_LEARNINGHUB_VERSION }}",
        "HOST": "learninghub.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "classroom",
        "MYSQL_USERNAME": "classroom",
        "OAUTH2_KEY": "learninghub",
        "OAUTH2_KEY_DEV": "learninghub-dev",
        "OAUTH2_KEY_SSO": "learninghub-sso",
        "OAUTH2_KEY_SSO_DEV": "learninghub-sso-dev",
        "CACHE_REDIS_DB": "{{ OPENEDX_CACHE_REDIS_DB }}",
        "MFE_APP": {
            "name": "classroom",
            "repository": "https://github.com/Dicey-Tech/frontend-app-classroom",
            "port": 8080,
            "version": "develop",
            "env": {
                "production": {
                    "CLASSROOM_BASE_URL": "{{ 'https' if ENABLE_HTTPS else 'http' }}://{{ DT_LEARNINGHUB_HOST }}",
                },
                "development": {
                    "CLASSROOM_BASE_URL": "{{ 'https' if ENABLE_HTTPS else 'http' }}://{{ DT_LEARNINGHUB_HOST }}:{{ DT_LEARNINGHUB_PORT}}",
                },
            },
        },
        "DASHBOARD_MFE_APP": {
            "name": "dashboard",
            "repository": "https://github.com/Dicey-Tech/frontend-app-teacher-dashboard",
            "port": 8081,
            "version": "develop",
            "env": {
                "production": {
                    "CLASSROOM_BASE_URL": "{{ 'https' if ENABLE_HTTPS else 'http' }}://{{ DT_LEARNINGHUB_HOST }}",
                    "CLASSROOM_MFE_URL": "{{ 'https' if ENABLE_HTTPS else 'http' }}://apps.{{ LMS_HOST }}/{{ DT_LEARNINGHUB_MFE_APP['name'] }}",
                },
                "development": {
                    "CLASSROOM_BASE_URL": "http://{{ DT_LEARNINGHUB_HOST }}:{{DT_LEARNINGHUB_PORT}}",
                    "CLASSROOM_MFE_URL": "http://apps.{{ LMS_HOST }}:{{ DT_LEARNINGHUB_MFE_APP['port'] }}/{{ DT_LEARNINGHUB_MFE_APP['name'] }}",
                },
            },
        },
        "GRADEBOOK_MFE_APP": {
            "name": "gradebook",
            "port": 1994,
            "repository": "http://github.com/Dicey-Tech/frontend-app-gradebook",
            "version": "develop",
        },
    },
}

hooks = {
    "build-image": {"dt_learninghub": "{{ DT_LEARNINGHUB_DOCKER_IMAGE }}"},
    "init": ["mysql", "dt_learninghub", "lms"],
}


def patches():
    all_patches = {}
    patches_dir = pkg_resources.resource_filename("tutorlearninghub", "patches")
    for path in glob(os.path.join(patches_dir, "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
