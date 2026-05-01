#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - CRDT Utilities Usage Examples
===========================================
Practical examples demonstrating CRDT usage for distributed systems.

CRDTs (Conflict-free Replicated Data Types) enable coordination-free
replication, perfect for:
- Distributed databases
- Collaborative editing
- Offline-first applications
- Multi-device sync
"""

import sys
import os
import time

# Add the Python directory to path
python_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, python_dir)

# Import the module directly using exec
mod_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mod.py")

# Read and execute the module
with open(mod_path, 'r') as f:
    mod_code = f.read()

# Create a namespace for the module
crdt_mod = {}
exec(mod_code, crdt_mod)

# Get the classes and functions
VectorClock = crdt_mod['VectorClock']
GCounter = crdt_mod['GCounter']
PNCounter = crdt_mod['PNCounter']
GSet = crdt_mod['GSet']
TwoPSet = crdt_mod['TwoPSet']
LWWRegister = crdt_mod['LWWRegister']
ORSet = crdt_mod['ORSet']
LWWElementSet = crdt_mod['LWWElementSet']
CRDTMap = crdt_mod['CRDTMap']
JSONCRDT = crdt_mod['JSONCRDT']
generate_node_id = crdt_mod['generate_node_id']
crdt_hash = crdt_mod['crdt_hash']
merge_all = crdt_mod['merge_all']


# ============================================================================
# Example 1: Distributed Counter
# ============================================================================

def example_distributed_counter():
    """
    Example: Distributed page view counter.
    
    Multiple nodes track page views independently.
    Counters eventually converge to the correct total.
    """
    print("\n" + "=" * 60)
    print("Example 1: Distributed Page View Counter")
    print("=" * 60)
    
    # Three servers tracking page views
    server_a = GCounter(node_id='server_a')
    server_b = GCounter(node_id='server_b')
    server_c = GCounter(node_id='server_c')
    
    # Server A gets 5 page views
    server_a = server_a.increment(5)
    print(f"Server A: {server_a.value} page views")
    
    # Server B gets 3 page views
    server_b = server_b.increment(3)
    print(f"Server B: {server_b.value} page views")
    
    # Server C gets 7 page views
    server_c = server_c.increment(7)
    print(f"Server C: {server_c.value} page views")
    
    # Servers sync by merging counters
    print("\n--- Syncing servers ---")
    
    # Server A receives updates from B and C
    server_a_synced = merge_all([server_a, server_b, server_c])
    print(f"Server A (synced): {server_a_synced.value} total views")
    
    # Server B receives updates from A and C
    server_b_synced = merge_all([server_b, server_a, server_c])
    print(f"Server B (synced): {server_b_synced.value} total views")
    
    # All servers now have the same total
    print(f"\n✓ All servers converged to {server_a_synced.value} views")


# ============================================================================
# Example 2: Shopping Cart
# ============================================================================

def example_shopping_cart():
    """
    Example: Distributed shopping cart.
    
    Users can add/remove items across multiple devices.
    Cart converges even with offline operations.
    """
    print("\n" + "=" * 60)
    print("Example 2: Distributed Shopping Cart")
    print("=" * 60)
    
    # OR-Set allows items to be re-added after removal
    phone_cart = ORSet[str](node_id='phone')
    tablet_cart = ORSet[str](node_id='tablet')
    
    # User adds items on phone
    phone_cart = phone_cart.add('laptop')
    phone_cart = phone_cart.add('mouse')
    print(f"Phone cart: {phone_cart.value}")
    
    # User adds different items on tablet (offline)
    tablet_cart = tablet_cart.add('keyboard')
    tablet_cart = tablet_cart.add('laptop')  # Same item, different tag
    print(f"Tablet cart: {tablet_cart.value}")
    
    # User removes mouse on phone
    phone_cart = phone_cart.remove('mouse')
    print(f"Phone cart (removed mouse): {phone_cart.value}")
    
    # Sync carts
    print("\n--- Syncing carts ---")
    synced_cart = phone_cart.merge(tablet_cart)
    print(f"Synced cart: {synced_cart.value}")
    
    # Items: laptop (present on both), keyboard (tablet only)
    # mouse was removed on phone, still removed
    print(f"\n✓ Cart synced: {len(synced_cart)} items")


# ============================================================================
# Example 3: Collaborative Document
# ============================================================================

def example_collaborative_document():
    """
    Example: Collaborative document editing.
    
    Multiple users editing a document simultaneously.
    LWW-Register resolves conflicts using timestamps.
    """
    print("\n" + "=" * 60)
    print("Example 3: Collaborative Document Editing")
    print("=" * 60)
    
    # Title register - last writer wins
    title_user1 = LWWRegister[str](node_id='user1')
    title_user2 = LWWRegister[str](node_id='user2')
    
    # User 1 sets title at t=100
    title_user1 = title_user1.set('My Document', timestamp=100.0)
    print(f"User 1 title: {title_user1.value}")
    
    # User 2 sets different title at t=150 (later)
    title_user2 = title_user2.set('Final Report', timestamp=150.0)
    print(f"User 2 title: {title_user2.value}")
    
    # Sync titles - later timestamp wins
    print("\n--- Syncing document ---")
    synced_title = title_user1.merge(title_user2)
    print(f"Synced title: {synced_title.value}")
    print(f"✓ User 2's edit wins (later timestamp)")


# ============================================================================
# Example 4: Vector Clock Ordering
# ============================================================================

def example_vector_clock():
    """
    Example: Event ordering with vector clocks.
    
    Track causality in distributed system events.
    """
    print("\n" + "=" * 60)
    print("Example 4: Event Ordering with Vector Clocks")
    print("=" * 60)
    
    # Initial clocks for 3 processes
    process_a = VectorClock()
    process_b = VectorClock()
    process_c = VectorClock()
    
    # Events happen
    # Event 1: A sends message
    process_a = process_a.increment('A')
    print(f"Event 1: A sends message. Clock: {process_a}")
    
    # Event 2: B receives from A
    process_b = process_b.merge(process_a)  # Receive A's clock
    process_b = process_b.increment('B')    # Local event
    print(f"Event 2: B receives message. Clock: {process_b}")
    
    # Event 3: C does independent work
    process_c = process_c.increment('C')
    print(f"Event 3: C independent work. Clock: {process_c}")
    
    # Compare clocks
    print("\n--- Comparing clocks ---")
    print(f"A vs B: {process_a.compare(process_b)} (A happened before B)")
    print(f"A vs C: {process_a.compare(process_c)} (concurrent)")
    print(f"B vs C: {process_b.compare(process_c)} (concurrent)")
    
    # B and C are concurrent - no causal relationship
    print(f"\n✓ B and C are concurrent (no ordering between them)")


# ============================================================================
# Example 5: User Profile Sync
# ============================================================================

def example_user_profile():
    """
    Example: User profile synchronization.
    
    JSON CRDT for complex nested data structures.
    """
    print("\n" + "=" * 60)
    print("Example 5: User Profile Sync")
    print("=" * 60)
    
    # Phone updates
    phone_profile = JSONCRDT(node_id='phone')
    phone_profile = phone_profile.set_path(['profile', 'name'], 'Alice')
    phone_profile = phone_profile.set_path(['profile', 'phone'], '123-456')
    
    print(f"Phone profile: {phone_profile.value}")
    
    # Web updates (different fields)
    web_profile = JSONCRDT(node_id='web')
    web_profile = web_profile.set_path(['profile', 'name'], 'Alice Smith')
    web_profile = web_profile.set_path(['profile', 'email'], 'alice@example.com')
    
    print(f"Web profile: {web_profile.value}")
    
    # Sync profiles
    print("\n--- Syncing profiles ---")
    synced_profile = phone_profile.merge(web_profile)
    print(f"Synced profile: {synced_profile.value}")
    
    # All fields merged (later timestamps win for conflicts)
    print(f"\n✓ Profile fields merged successfully")


# ============================================================================
# Example 6: Inventory Management
# ============================================================================

def example_inventory():
    """
    Example: Inventory management with PN-Counter.
    
    Track stock levels with increment (add) and decrement (sell).
    """
    print("\n" + "=" * 60)
    print("Example 6: Inventory Management")
    print("=" * 60)
    
    # Two warehouses tracking stock
    warehouse_ny = PNCounter(node_id='warehouse_ny')
    warehouse_sf = PNCounter(node_id='warehouse_sf')
    
    # NY receives shipment of 100 items
    warehouse_ny = warehouse_ny.increment(100)
    print(f"NY warehouse: received 100, stock = {warehouse_ny.value}")
    
    # NY sells 15 items
    warehouse_ny = warehouse_ny.decrement(15)
    print(f"NY warehouse: sold 15, stock = {warehouse_ny.value}")
    
    # SF receives shipment of 50 items
    warehouse_sf = warehouse_sf.increment(50)
    print(f"SF warehouse: received 50, stock = {warehouse_sf.value}")
    
    # SF sells 10 items
    warehouse_sf = warehouse_sf.decrement(10)
    print(f"SF warehouse: sold 10, stock = {warehouse_sf.value}")
    
    # Sync inventory
    print("\n--- Syncing inventory ---")
    synced = merge_all([warehouse_ny, warehouse_sf])
    print(f"Total inventory: {synced.value} items")
    
    # 100 + 50 - 15 - 10 = 125
    print(f"\n✓ Total stock across warehouses: {synced.value} items")


# ============================================================================
# Example 7: Todo List with 2P-Set
# ============================================================================

def example_todo_list():
    """
    Example: Todo list using 2P-Set.
    
    Tasks can be added and completed (removed).
    Completed tasks cannot be accidentally re-added.
    """
    print("\n" + "=" * 60)
    print("Example 7: Todo List with 2P-Set")
    print("=" * 60)
    
    todo_list = TwoPSet[str]()
    
    # Add tasks
    todo_list = todo_list.add('Buy groceries')
    todo_list = todo_list.add('Walk the dog')
    todo_list = todo_list.add('Clean room')
    
    print(f"Todo list: {todo_list.value}")
    print(f"Tasks to do: {len(todo_list)}")
    
    # Complete some tasks
    todo_list = todo_list.remove('Buy groceries')
    todo_list = todo_list.remove('Walk the dog')
    
    print(f"Completed 2 tasks")
    print(f"Remaining: {todo_list.value}")
    
    # Try to re-add a completed task (won't work!)
    todo_list = todo_list.add('Buy groceries')
    print(f"Tried to re-add 'Buy groceries': {todo_list.value}")
    
    print(f"\n✓ Completed tasks stay completed (no accidental re-adds)")


# ============================================================================
# Example 8: Multi-Device Counter Sync
# ============================================================================

def example_multi_device_counter():
    """
    Example: Counter synced across multiple devices.
    
    GCounter with CRDTMap for named counters.
    """
    print("\n" + "=" * 60)
    print("Example 8: Multi-Device Counter Sync")
    print("=" * 60)
    
    # Each device has its own counter map
    device_phone = CRDTMap[str, GCounter](node_id='phone')
    device_tablet = CRDTMap[str, GCounter](node_id='tablet')
    
    # Phone increments counters
    counter_views = GCounter('phone').increment(10)
    counter_clicks = GCounter('phone').increment(3)
    
    device_phone = device_phone.set('views', counter_views)
    device_phone = device_phone.set('clicks', counter_clicks)
    
    print(f"Phone counters:")
    print(f"  - views: {device_phone.get('views').value}")
    print(f"  - clicks: {device_phone.get('clicks').value}")
    
    # Tablet increments independently
    counter_views2 = GCounter('tablet').increment(5)
    counter_clicks2 = GCounter('tablet').increment(7)
    
    device_tablet = device_tablet.set('views', counter_views2)
    device_tablet = device_tablet.set('clicks', counter_clicks2)
    
    print(f"Tablet counters:")
    print(f"  - views: {device_tablet.get('views').value}")
    print(f"  - clicks: {device_tablet.get('clicks').value}")
    
    # Sync all counters
    print("\n--- Syncing counters ---")
    synced = device_phone.merge(device_tablet)
    
    print(f"Synced counters:")
    print(f"  - views: {synced.get('views').value}")
    print(f"  - clicks: {synced.get('clicks').value}")
    
    # Views: 10 + 5 = 15
    # Clicks: 3 + 7 = 10
    print(f"\n✓ All counters converged correctly")


# ============================================================================
# Main
# ============================================================================

def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("CRDT Utilities - Usage Examples")
    print("Conflict-free Replicated Data Types for Distributed Systems")
    print("=" * 60)
    
    example_distributed_counter()
    example_shopping_cart()
    example_collaborative_document()
    example_vector_clock()
    example_user_profile()
    example_inventory()
    example_todo_list()
    example_multi_device_counter()
    
    print("\n" + "=" * 60)
    print("✓ All examples completed successfully!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("  - CRDTs enable coordination-free replication")
    print("  - Merge operations are commutative, associative, idempotent")
    print("  - All replicas eventually converge to the same state")
    print("  - Perfect for offline-first and distributed applications")


if __name__ == '__main__':
    main()