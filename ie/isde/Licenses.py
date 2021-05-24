"""
This file enumerates the Licenses in use in the Irish Spatial Data Exchange
"""

from enum import Enum


class Licenses(Enum):
    CCBY = dict(name="Creative Commons Attribution 4.0 International", spdx_url="https://spdx.org/licenses/CC-BY-4.0",
                url="https://creativecommons.org/licenses/by/4.0/legalcode")

    CCBYNC = dict(name="Creative Commons Attribution Non Commercial 4.0 International",
                  spdx_url="https://spdx.org/licenses/CC-BY-NC-4.0",
                  url="https://creativecommons.org/licenses/by-nc/4.0/legalcode")