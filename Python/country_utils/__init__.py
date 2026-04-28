#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Country Utilities Module

ISO 3166 country codes and utilities with zero external dependencies.
"""

from .mod import (
    Country,
    get_country,
    get_by_alpha2,
    get_by_alpha3,
    get_by_numeric,
    get_by_name,
    search_countries,
    get_all_countries,
    get_countries_by_continent,
    get_countries_by_region,
    validate_alpha2,
    validate_alpha3,
    validate_numeric,
    alpha2_to_alpha3,
    alpha3_to_alpha2,
    alpha2_to_numeric,
    numeric_to_alpha2,
    get_flag_emoji,
    get_calling_code,
    get_currency,
    get_continents,
    get_regions,
    find,
    all_countries,
    __all__,
)

__version__ = "1.0.0"
__author__ = "AllToolkit"