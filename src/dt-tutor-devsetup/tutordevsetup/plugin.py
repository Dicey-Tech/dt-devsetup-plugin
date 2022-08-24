from glob import glob
import os
import pkg_resources

from tutor import hooks

from .__about__ import __version__

config = {
    "defaults": {
        "VERSION": __version__,
        "ENTERPRISE_USER": "enterprise_worker",
        "AUTHN_MFE_APP": {
            "name": "auth",
            "port": 1999,
            "repository": "https://github.com/Dicey-Tech/frontend-app-authn",
            "version": "master",
            "env": {
                "production": {
                    "DISABLE_ENTERPRISE_LOGIN": "true",
                    "ENABLE_PROGRESSIVE_PROFILING": "true",
                    "TOS_AND_HONOR_CODE": "https://diceytech.co.uk/terms-and-conditions/",
                    "PRIVACY_POLICY": "https://diceytech.co.uk/privacy-policy/",
                    "INFO_EMAIL": "contact@diceytech.co.uk",
                },
            },
        },
    },
    "unique": {},
    "overrides": {
        "OPENEDX_CMS_UWSGI_WORKERS": 1,
        "OPENEDX_LMS_UWSGI_WORKERS": 2,
    },
}

hooks.Filters.COMMANDS_INIT.add_item(
    (
        "lms",
        ("dt_devsetup", "tasks", "lms", "init"),
    )
)

####### Boilerplate code
# Add the "templates" folder as a template root
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutordevsetup", "templates")
)

# Render the "build" and "apps" folders
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("dt_devsetup/build", "plugins"),
        ("dt_devsetup/apps", "plugins"),
    ],
)

# Load patches from files
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutordevsetup", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

# Add configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"DT_DEVSETUP_{key}", value) for key, value in config.get("defaults", {}).items()]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"DT_DEVSETUP_{key}", value) for key, value in config.get("unique", {}).items()]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config.get("overrides", {}).items()))
