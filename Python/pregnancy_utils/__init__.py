#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Pregnancy Utilities Module
========================================
A comprehensive pregnancy and due date calculation utility module.

This module provides comprehensive pregnancy calculation and tracking utilities
with zero external dependencies.

Features:
    - Due date calculation (Naegele's rule, conception date, IVF)
    - Gestational age calculation
    - Trimester determination
    - Pregnancy milestones tracking
    - Fetal development information
    - Prenatal checkup schedule
    - Pregnancy progress tracking
    - High risk pregnancy assessment

Example usage:
    >>> from pregnancy_utils import calculate_full_pregnancy
    >>> result = calculate_full_pregnancy('2024-01-01')
    >>> print(f"Due date: {result.due_date}")
    >>> print(f"Current week: {result.current_week}w {result.current_day}d")
"""

from .mod import (
    # Enums
    Trimester,
    PregnancyStatus,
    CalculationMethod,
    
    # Data classes
    DueDateResult,
    PregnancyMilestone,
    FetalDevelopment,
    CheckupSchedule,
    
    # Core calculation functions
    calculate_due_date_from_lmp,
    calculate_due_date_from_conception,
    calculate_due_date_from_ivf,
    calculate_gestational_age,
    get_trimester,
    get_pregnancy_status,
    calculate_progress_percentage,
    
    # Full calculation functions
    calculate_full_pregnancy,
    get_milestones,
    get_next_milestone,
    get_fetal_development,
    get_checkup_schedule,
    get_upcoming_checkups,
    
    # Utility functions
    format_gestational_age,
    get_pregnancy_summary,
    estimate_lmp_from_due_date,
    estimate_conception_from_due_date,
    is_high_risk_pregnancy,
    
    # Constants
    PREGNANCY_DAYS,
    PREGNANCY_WEEKS,
    PREGNANCY_MILESTONES,
    FETAL_SIZES,
    PRENATAL_SCHEDULE,
)

__version__ = '1.0.0'
__author__ = 'AllToolkit Contributors'
__license__ = 'MIT'

__all__ = [
    # Enums
    'Trimester',
    'PregnancyStatus',
    'CalculationMethod',
    
    # Data classes
    'DueDateResult',
    'PregnancyMilestone',
    'FetalDevelopment',
    'CheckupSchedule',
    
    # Core calculation functions
    'calculate_due_date_from_lmp',
    'calculate_due_date_from_conception',
    'calculate_due_date_from_ivf',
    'calculate_gestational_age',
    'get_trimester',
    'get_pregnancy_status',
    'calculate_progress_percentage',
    
    # Full calculation functions
    'calculate_full_pregnancy',
    'get_milestones',
    'get_next_milestone',
    'get_fetal_development',
    'get_checkup_schedule',
    'get_upcoming_checkups',
    
    # Utility functions
    'format_gestational_age',
    'get_pregnancy_summary',
    'estimate_lmp_from_due_date',
    'estimate_conception_from_due_date',
    'is_high_risk_pregnancy',
    
    # Constants
    'PREGNANCY_DAYS',
    'PREGNANCY_WEEKS',
    'PREGNANCY_MILESTONES',
    'FETAL_SIZES',
    'PRENATAL_SCHEDULE',
    
    # Module info
    '__version__',
    '__author__',
    '__license__',
]