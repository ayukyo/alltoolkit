"""
AllToolkit - Context Utilities Usage Examples

Demonstrates practical use cases for context management utilities.
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor

# Import from parent directory
import sys
sys.path.insert(0, '..')
from mod import (
    ScopedContext,
    RequestContext,
    ContextVar,
    ContextPropagator,
    ctx_get,
    ctx_set,
    ctx_scope,
    ctx_snapshot,
    ctx_restore,
    with_context,
    with_scope,
    request_context,
    get_context,
    get_request_context,
)


def example_1_basic_scoped_context():
    """
    Example 1: Basic ScopedContext Usage
    
    Shows how to create and use a scoped context for storing
    and retrieving values across nested scopes.
    """
    print("=" * 60)
    print("Example 1: Basic ScopedContext Usage")
    print("=" * 60)
    
    ctx = ScopedContext(name='application')
    
    # Set root-level values
    ctx.set('app_name', 'MyApp')
    ctx.set('version', '1.0.0')
    
    print(f"App: {ctx.get('app_name')}, Version: {ctx.get('version')}")
    print(f"Scope depth: {ctx.scope_depth}")
    
    # Create nested scopes
    with ctx.scope('request'):
        ctx.set('request_id', 'req-001')
        ctx.set('user_id', 123)
        
        print(f"\nIn request scope:")
        print(f"  Scope depth: {ctx.scope_depth}")
        print(f"  Request ID: {ctx.get('request_id')}")
        print(f"  User ID: {ctx.get('user_id')}")
        print(f"  App name (inherited): {ctx.get('app_name')}")
        
        # Further nested scope
        with ctx.scope('transaction'):
            ctx.set('transaction_id', 'tx-abc')
            
            print(f"\nIn transaction scope:")
            print(f"  Scope depth: {ctx.scope_depth}")
            print(f"  Transaction ID: {ctx.get('transaction_id')}")
            print(f"  Request ID (inherited): {ctx.get('request_id')}")
            print(f"  App name (inherited): {ctx.get('app_name')}")
    
    # Back to root
    print(f"\nBack to root scope:")
    print(f"  Scope depth: {ctx.scope_depth}")
    print(f"  Request ID exists: {ctx.has('request_id')}")  # False
    
    print("\n")


def example_2_context_override():
    """
    Example 2: Context Override
    
    Shows how to temporarily override context values
    for specific operations.
    """
    print("=" * 60)
    print("Example 2: Context Override")
    print("=" * 60)
    
    ctx = ScopedContext(name='override_demo')
    
    # Set default values
    ctx.set('user', 'default_user')
    ctx.set('role', 'guest')
    ctx.set('permissions', ['read'])
    
    print(f"Default: user={ctx.get('user')}, role={ctx.get('role')}")
    
    # Override for admin operation
    with ctx.override(user='admin', role='superuser', permissions=['read', 'write', 'delete']):
        print(f"Override: user={ctx.get('user')}, role={ctx.get('role')}")
        print(f"Permissions: {ctx.get('permissions')}")
    
    print(f"After: user={ctx.get('user')}, role={ctx.get('role')}")
    
    # Original permissions preserved
    print(f"Original permissions preserved: {ctx.get('permissions')}")
    
    print("\n")


def example_3_request_context():
    """
    Example 3: Request Context
    
    Shows how to use request context for web-style
    request handling with automatic cleanup.
    """
    print("=" * 60)
    print("Example 3: Request Context")
    print("=" * 60)
    
    req = RequestContext()
    
    # Simulate handling a request
    with req:
        # Set request-specific data
        req.request_id = 'req-12345'
        req.user_id = 42
        req.session_id = 'sess-abc'
        req.ip_address = '192.168.1.1'
        
        print(f"Request context active: {req.active}")
        print(f"Request ID: {req.request_id}")
        print(f"Elapsed time: {req.elapsed:.6f}s")
        
        # Access via attribute or get
        print(f"User ID (attribute): {req.user_id}")
        print(f"IP address (get): {req.get('ip_address')}")
        
        time.sleep(0.1)
        print(f"After 100ms: elapsed={req.elapsed:.3f}s")
    
    print(f"After request: active={req.active}")
    
    # Using as decorator
    @req
    def handle_api_request():
        req.endpoint = '/api/users'
        req.method = 'GET'
        return f"Handling {req.method} {req.endpoint}"
    
    result = handle_api_request()
    print(f"\nDecorator result: {result}")
    
    print("\n")


def example_4_context_var():
    """
    Example 4: Context Variables
    
    Shows how to use typed context variables with
    default values and change callbacks.
    """
    print("=" * 60)
    print("Example 4: Context Variables")
    print("=" * 60)
    
    # Create context variables
    user_id = ContextVar('user_id', default=None)
    trace_id = ContextVar('trace_id', default='no-trace')
    
    # Track changes
    changes = []
    
    def on_trace_change(old, new):
        changes.append(f"trace_id: {old} -> {new}")
    
    trace_with_callback = ContextVar('trace_with_callback', default='none', on_change=on_trace_change)
    
    print(f"user_id (default): {user_id.get()}")
    print(f"trace_id (default): {trace_id.get()}")
    
    # Set values
    user_id.set(12345)
    trace_with_callback.set('trace-001')
    
    print(f"user_id (set): {user_id.get()}")
    print(f"trace_with_callback: {trace_with_callback.get()}")
    
    # Use 'using' for temporary values
    with trace_id.using('temp-trace'):
        print(f"trace_id (using): {trace_id.get()}")
    
    print(f"trace_id (after): {trace_id.get()}")
    
    # Multiple nested values
    trace_with_callback.set('trace-002')
    trace_with_callback.set('trace-003')
    trace_with_callback.reset()
    
    print(f"\nChange history:")
    for change in changes:
        print(f"  {change}")
    
    print("\n")


def example_5_snapshot_restore():
    """
    Example 5: Snapshot and Restore
    
    Shows how to capture and restore context state.
    """
    print("=" * 60)
    print("Example 5: Snapshot and Restore")
    print("=" * 60)
    
    ctx = ScopedContext(name='snapshot_demo')
    
    # Initial state
    ctx.set('config_a', 100)
    ctx.set('config_b', 'production')
    ctx.set('flag', True)
    
    print("Initial state:")
    print(f"  config_a={ctx.get('config_a')}")
    print(f"  config_b={ctx.get('config_b')}")
    print(f"  flag={ctx.get('flag')}")
    
    # Take snapshot
    snapshot = ctx.snapshot()
    print(f"\nSnapshot taken with {len(snapshot)} keys")
    
    # Modify context
    ctx.set('config_a', 999)
    ctx.set('config_b', 'testing')
    ctx.delete('flag')
    ctx.set('new_key', 'added')
    
    print("\nModified state:")
    print(f"  config_a={ctx.get('config_a')}")
    print(f"  config_b={ctx.get('config_b')}")
    print(f"  flag={ctx.get('flag', 'NOT_FOUND')}")
    print(f"  new_key={ctx.get('new_key')}")
    
    # Restore snapshot
    ctx.restore(snapshot)
    
    print("\nRestored state:")
    print(f"  config_a={ctx.get('config_a')}")
    print(f"  config_b={ctx.get('config_b')}")
    print(f"  flag={ctx.get('flag')}")
    print(f"  new_key={ctx.get('new_key', 'NOT_FOUND')}")
    
    print("\n")


def example_6_context_propagation():
    """
    Example 6: Context Propagation
    
    Shows how to propagate context across threads.
    """
    print("=" * 60)
    print("Example 6: Context Propagation")
    print("=" * 60)
    
    ctx = ScopedContext(name='propagation_demo')
    
    # Set values in main thread
    ctx.set('session_id', 'sess-main')
    ctx.set('user', 'main_user')
    
    propagator = ContextPropagator(ctx)
    propagator.capture(['session_id', 'user'])
    
    print(f"Captured: {propagator.captured_items}")
    
    # Propagate to worker thread
    def worker():
        with ctx.scope('worker'):
            propagator.apply()
            print(f"\nWorker thread context:")
            print(f"  session_id={ctx.get('session_id')}")
            print(f"  user={ctx.get('user')}")
    
    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()
    
    print(f"\nMain thread still has context:")
    print(f"  session_id={ctx.get('session_id')}")
    
    print("\n")


def example_7_decorators():
    """
    Example 7: Decorators
    
    Shows how to use decorators for context management.
    """
    print("=" * 60)
    print("Example 7: Decorators")
    print("=" * 60)
    
    # with_context decorator
    @with_context(user='admin', role='superuser')
    def admin_operation():
        print(f"In admin_operation:")
        print(f"  user={ctx_get('user')}")
        print(f"  role={ctx_get('role')}")
        return True
    
    admin_operation()
    print(f"After admin_operation: user={ctx_get('user', 'NONE')}")
    
    # with_scope decorator
    @with_scope('database_transaction')
    def database_operation():
        ctx_set('tx_id', 'tx-001')
        ctx_set('query_count', 5)
        print(f"\nIn database_operation:")
        print(f"  tx_id={ctx_get('tx_id')}")
        print(f"  query_count={ctx_get('query_count')}")
        return ctx_snapshot()
    
    snapshot = database_operation()
    print(f"After database_operation: tx_id={ctx_get('tx_id', 'NONE')}")
    
    # request_context decorator
    req = RequestContext()
    
    @req
    def api_handler():
        req.endpoint = '/api/data'
        req.method = 'POST'
        print(f"\nIn api_handler:")
        print(f"  Request ID: {req.request_id}")
        print(f"  Endpoint: {req.endpoint}")
        print(f"  Method: {req.method}")
    
    api_handler()
    
    print("\n")


def example_8_web_request_simulation():
    """
    Example 8: Web Request Simulation
    
    Simulates a web application request handling workflow
    using scoped contexts.
    """
    print("=" * 60)
    print("Example 8: Web Request Simulation")
    print("=" * 60)
    
    ctx = ScopedContext(name='web_app')
    
    # Application-level config (root scope)
    ctx.set('db_host', 'localhost')
    ctx.set('db_port', 5432)
    ctx.set('cache_enabled', True)
    
    print("Application config set")
    
    def handle_request(request_id, user_id):
        """Simulate handling a web request."""
        with ctx.scope(f'request_{request_id}'):
            # Request-specific data
            ctx.set('request_id', request_id)
            ctx.set('user_id', user_id)
            ctx.set('start_time', time.time())
            
            print(f"\n[Request {request_id}] Starting for user {user_id}")
            print(f"  DB host (inherited): {ctx.get('db_host')}")
            
            # Authentication scope
            with ctx.scope('auth'):
                ctx.set('auth_token', f'token-{user_id}')
                ctx.set('auth_method', 'jwt')
                
                print(f"  [Auth] Token: {ctx.get('auth_token')}")
                
                # Business logic scope
                with ctx.scope('business'):
                    ctx.set('operation', 'fetch_data')
                    
                    # Access all inherited values
                    result = {
                        'request_id': ctx.get('request_id'),
                        'user_id': ctx.get('user_id'),
                        'db_host': ctx.get('db_host'),
                        'auth_token': ctx.get('auth_token'),
                        'operation': ctx.get('operation'),
                    }
                    
                    print(f"  [Business] All context items: {result}")
                    
                    return result
    
    # Handle multiple requests concurrently
    requests = [('req-001', 123), ('req-002', 456), ('req-003', 789)]
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(handle_request, req_id, uid) for req_id, uid in requests]
        for f in futures:
            result = f.result()
            print(f"  [Result] {result['request_id']} completed")
    
    print("\n")


def example_9_readonly_scope():
    """
    Example 9: Readonly Scope
    
    Shows how to use readonly scopes for immutable configuration.
    """
    print("=" * 60)
    print("Example 9: Readonly Scope")
    print("=" * 60)
    
    ctx = ScopedContext(name='config_demo')
    
    # Set mutable configuration
    ctx.set('mutable_config', 'can_change')
    
    with ctx.scope('immutable_config', readonly=True) as scope:
        # Cannot set in readonly scope
        print(f"In readonly scope '{scope.name}'")
        
        # Reading from parent works
        print(f"  mutable_config (from parent): {ctx.get('mutable_config')}")
        
        # Trying to set would raise InvalidScopeError
        try:
            ctx.set('new_value', 'test')
            print("  ERROR: Should have raised exception!")
        except Exception as e:
            print(f"  Cannot set in readonly scope: {e}")
    
    print("\n")


def example_10_context_path_tracking():
    """
    Example 10: Context Path Tracking
    
    Shows how to track the path through nested scopes.
    """
    print("=" * 60)
    print("Example 10: Context Path Tracking")
    print("=" * 60)
    
    ctx = ScopedContext(name='path_tracking')
    
    print(f"Current path: {ctx.scope_path()}")
    
    with ctx.scope('layer_1'):
        print(f"Path: {ctx.scope_path()}")
        
        with ctx.scope('layer_2'):
            print(f"Path: {ctx.scope_path()}")
            
            with ctx.scope('layer_3'):
                print(f"Path: {ctx.scope_path()}")
                print(f"Depth: {ctx.scope_depth}")
        
        print(f"Back to: {ctx.scope_path()}")
    
    print(f"Final path: {ctx.scope_path()}")
    
    print("\n")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AllToolkit - Context Utilities Examples")
    print("=" * 60 + "\n")
    
    example_1_basic_scoped_context()
    example_2_context_override()
    example_3_request_context()
    example_4_context_var()
    example_5_snapshot_restore()
    example_6_context_propagation()
    example_7_decorators()
    example_8_web_request_simulation()
    example_9_readonly_scope()
    example_10_context_path_tracking()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()