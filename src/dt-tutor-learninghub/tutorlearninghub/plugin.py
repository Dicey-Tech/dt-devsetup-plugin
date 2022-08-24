from glob import glob
import os
import pkg_resources

from tutor import hooks

from .__about__ import __version__

config = {
    "unique": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 24|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
    },
    "defaults": {
        "PORT": "8180",
        # Fix for Dicey-Tech/dt-tutor-plugins#3 - Override this config value in production
        "CLASSROOM_MFE_URL": "{{ 'https' if ENABLE_HTTPS else 'http' }}://apps.{{ LMS_HOST }}/{{ DT_LEARNINGHUB_MFE_APP['name'] }}",
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}diceytech/dt_learninghub:{{ DT_LEARNINGHUB_VERSION }}",
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
            "repository": "https://github.com/Dicey-Tech/frontend-app-dashboard",
            "port": 8081,
            "version": "master",
            "env": {
                "production": {
                    "CLASSROOM_BASE_URL": "{{ 'https' if ENABLE_HTTPS else 'http' }}://{{ DT_LEARNINGHUB_HOST }}",
                    "CLASSROOM_MFE_URL": "{{ DT_LEARNINGHUB_CLASSROOM_MFE_URL }}",
                    "EXPLORE_COURSES_URL": "https://diceytech.co.uk/projects/",
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
    "overrides": {
        "MFE_GRADEBOOK_MFE_APP": None,
    },
}

hooks.Filters.COMMANDS_INIT.add_item(
    (
        "mysql",
        ("dt_learninghub", "tasks", "mysql", "init"),
    )
)

hooks.Filters.COMMANDS_INIT.add_item(
    (
        "lms",
        ("dt_learninghub", "tasks", "lms", "init"),
    )
)

hooks.Filters.COMMANDS_INIT.add_item(
    (
        "dt_learninghub",
        ("dt_learninghub", "tasks", "dt_learninghub", "init"),
    )
)

hooks.Filters.IMAGES_BUILD.add_item(
    (
        "dt_learninghub",
        ("plugins", "dt_learninghub", "build", "dt_learninghub"),
        "{{ DT_LEARNINGHUB_DOCKER_IMAGE }}",
        (),
    )
)

####### Boilerplate code
# Add the "templates" folder as a template root
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorlearninghub", "templates")
)

# Render the "build" and "apps" folders
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("dt_learninghub/build", "plugins"),
        ("dt_learninghub/apps", "plugins"),
    ],
)

# Load patches from files
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorlearninghub", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

# Add configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"DT_LEARNINGHUB_{key}", value)
        for key, value in config.get("defaults", {}).items()
    ]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (f"DT_LEARNINGHUB_{key}", value)
        for key, value in config.get("unique", {}).items()
    ]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config.get("overrides", {}).items()))
