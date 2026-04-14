#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ID Generator Utilities - Distributed System Example

This example shows how to use Snowflake ID in a distributed system.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import threading
import time
from collections import defaultdict
from mod import SnowflakeGenerator


class OrderService:
    """Simulated order service using Snowflake IDs."""
    
    def __init__(self, worker_id: int, datacenter_id: int):
        self.id_gen = SnowflakeGenerator(
            worker_id=worker_id,
            datacenter_id=datacenter_id
        )
        self.orders = {}
    
    def create_order(self, customer_id: str, items: list) -> dict:
        """Create a new order with Snowflake ID."""
        order_id = self.id_gen.generate()
        
        order = {
            'id': order_id,
            'customer_id': customer_id,
            'items': items,
            'created_at': time.time(),
            'status': 'pending'
        }
        
        self.orders[order_id] = order
        return order
    
    def get_order(self, order_id: int) -> dict:
        """Get order by ID."""
        return self.orders.get(order_id)


def simulate_datacenter():
    """Simulate a datacenter with multiple workers."""
    print("Simulating distributed order system...")
    print()
    
    # Create services for different workers
    services = {
        'dc1_worker0': OrderService(worker_id=0, datacenter_id=1),
        'dc1_worker1': OrderService(worker_id=1, datacenter_id=1),
        'dc2_worker0': OrderService(worker_id=0, datacenter_id=2),
        'dc2_worker1': OrderService(worker_id=1, datacenter_id=2),
    }
    
    # Collect all IDs for uniqueness check
    all_ids = []
    all_ids_lock = threading.Lock()
    
    def process_orders(service_name: str, service: OrderService, count: int):
        """Process orders for a service."""
        for i in range(count):
            order = service.create_order(
                customer_id=f"CUST_{i:04d}",
                items=[f"ITEM_{j}" for j in range(3)]
            )
            
            with all_ids_lock:
                all_ids.append(order['id'])
            
            # Parse the ID to show its components
            parsed = SnowflakeGenerator.parse(order['id'])
            print(f"  [{service_name}] Order {order['id']}")
            print(f"    DC: {parsed['datacenter_id']}, Worker: {parsed['worker_id']}, Seq: {parsed['sequence']}")
    
    print("Creating orders from multiple workers...")
    print("-" * 60)
    
    threads = []
    for name, service in services.items():
        t = threading.Thread(target=process_orders, args=(name, service, 3))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print()
    print("-" * 60)
    print(f"Total orders created: {len(all_ids)}")
    print(f"Unique IDs: {len(set(all_ids))}")
    print(f"Duplicates: {len(all_ids) - len(set(all_ids))}")
    
    # Verify ordering
    sorted_ids = sorted(all_ids)
    print(f"IDs are monotonically increasing: {all_ids == sorted_ids}")
    
    # Group by datacenter
    by_dc = defaultdict(int)
    for id in all_ids:
        parsed = SnowflakeGenerator.parse(id)
        by_dc[parsed['datacenter_id']] += 1
    
    print()
    print("Orders by datacenter:")
    for dc, count in sorted(by_dc.items()):
        print(f"  Datacenter {dc}: {count} orders")
    
    print()
    print("✓ Distributed system simulation completed!")


if __name__ == '__main__':
    simulate_datacenter()