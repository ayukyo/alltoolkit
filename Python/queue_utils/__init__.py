#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Queue Utilities
=============================
Comprehensive queue data structure implementations.

Author: AllToolkit
License: MIT
"""

from mod import (
    Queue, ThreadSafeQueue, PriorityQueue, MaxPriorityQueue,
    Deque, CircularQueue, PriorityDeque,
    QueueEmptyError, QueueFullError,
    create_queue, create_circular_queue, create_priority_queue
)

__all__ = [
    'Queue', 'ThreadSafeQueue', 'PriorityQueue', 'MaxPriorityQueue',
    'Deque', 'CircularQueue', 'PriorityDeque',
    'QueueEmptyError', 'QueueFullError',
    'create_queue', 'create_circular_queue', 'create_priority_queue'
]