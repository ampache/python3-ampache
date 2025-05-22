# Copyright 2023 Ampache.org

"""
ampache metadata

- Versioning should follow SemVer (https://semver.org)
- DEBUG flag is a global setting for debug information that should be False at
  distribution time.

  >>> from ._meta import DEBUG
  >>> if DEBUG:
  ...     print("Debugging")

"""

__author__ = "Lachlan de Waard (lachlan-00)"
__version__ = "6.7.0"

DEBUG = False
