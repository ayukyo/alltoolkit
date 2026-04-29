"""
Semaphore utilities for Python.

A semaphore is a synchronization primitive that limits the number of concurrent
operations. This module provides enhanced semaphore implementations with:

- Standard counting semaphores with timeout support
- Weighted semaphores for variable resource allocation
- Semaphore pools for managing multiple resources
- Async/await support
- Context manager protocol
- Zero external dependencies

Author: AllToolkit
Date: 2026-04-29
Version: 1.0.0
"""

from .semaphore_utils import (
    Semaphore,
    WeightedSemaphore,
    SemaphorePool,
    AsyncSemaphore,
    AsyncWeightedSemaphore,
    BoundedSemaphore,
    PrioritySemaphore,
    RateLimiter,
    ConcurrencyLimit,
    SemaphoreError,
    TimeoutError,
    CancelledError,
    acquire_all,
    run_with_semaphore,
    create_bounded,
    create_pool,
    create_rate_limiter,
)

__all__ = [
    'Semaphore',
    'WeightedSemaphore',
    'SemaphorePool',
    'AsyncSemaphore',
    'AsyncWeightedSemaphore',
    'BoundedSemaphore',
    'PrioritySemaphore',
    'RateLimiter',
    'ConcurrencyLimit',
    'SemaphoreError',
    'TimeoutError',
    'CancelledError',
    'acquire_all',
    'run_with_semaphore',
    'create_bounded',
    'create_pool',
    'create_rate_limiter',
]

__version__ = '1.0.0'
__author__ = 'AllToolkit'