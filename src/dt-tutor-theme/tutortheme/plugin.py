from glob import glob
import os
import pkg_resources

from tutor import hooks

from .__about__ import __version__


################# Configuration
config = {
    # Add here your new settings
    "defaults": {
        "VERSION": __version__,
    },
    # Add here settings that don't have a reasonable default for all users. For
    # instance: passwords, secret keys, etc.
    "unique": {},
    "overrides": {},
}

# Plugin templates
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutortheme", "templates")
)
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("dt_theme", "build/openedx/themes"),
    ],
)

# Force the rendering of scss files, even though they are included in a "partials" directory
hooks.Filters.ENV_PATTERNS_INCLUDE.add_item(
    r"dt_theme/lms/static/sass/partials/lms/theme/"
)

# Load all configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"DT_THEME_{key}", value) for key, value in config["defaults"].items()]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"DT_THEME_{key}", value) for key, value in config["unique"].items()]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))
