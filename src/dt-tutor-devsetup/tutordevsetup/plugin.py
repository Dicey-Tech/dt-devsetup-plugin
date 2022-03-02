from glob import glob
import os
import pkg_resources

from .__about__ import __version__

templates = pkg_resources.resource_filename("tutordevsetup", "templates")

config = {
    "defaults": {
        "VERSION": __version__,
        "AUTHN_MFE_APP": {
            "name": "auth",
            "port": 1999,
            "repository": "https://github.com/Dicey-Tech/frontend-app-authn",
            "version": "develop",
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
    }
}

hooks = {
    "init": ["lms"],
}


def patches():
    all_patches = {}
    patches_dir = pkg_resources.resource_filename("tutordevsetup", "patches")
    for path in glob(os.path.join(patches_dir, "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
