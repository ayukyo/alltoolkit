"""
AllToolkit - Python Context Utilities Tests

Comprehensive test suite for context management utilities.
"""

import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor

from mod import (
    # Classes
    Scope,
    ScopedContext,
    RequestContext,
    ContextVar,
    ContextPropagator,
    # Exceptions
    ContextError,
    ContextNotFoundError,
    ScopeNotFoundError,
    InvalidScopeError,
    # Functions
    get_context,
    get_request_context,
    ctx_get,
    ctx_set,
    ctx_has,
    ctx_delete,
    ctx_scope,
    ctx_snapshot,
    ctx_restore,
    # Decorators
    with_context,
    with_scope,
    request_context,
)


class TestScope(unittest.TestCase):
    """Test Scope class."""
    
    def test_scope_creation(self):
        """Test creating a scope."""
        scope = Scope(name='test')
        self.assertEqual(scope.name, 'test')
        self.assertIsNotNone(scope.id)
        self.assertIsNone(scope.parent)
        self.assertEqual(scope.data, {})
        self.assertFalse(scope.readonly)
    
    def test_scope_get_set(self):
        """Test getting and setting values."""
        scope = Scope(name='test')
        scope.set('key1', 'value1')
        scope.set('key2', 123)
        
        self.assertEqual(scope.get('key1'), 'value1')
        self.assertEqual(scope.get('key2'), 123)
        self.assertIsNone(scope.get('nonexistent'))
        self.assertEqual(scope.get('nonexistent', 'default'), 'default')
    
    def test_scope_has(self):
        """Test checking key existence."""
        scope = Scope(name='test')
        scope.set('key1', 'value1')
        
        self.assertTrue(scope.has('key1'))
        self.assertFalse(scope.has('nonexistent'))
    
    def test_scope_delete(self):
        """Test deleting keys."""
        scope = Scope(name='test')
        scope.set('key1', 'value1')
        
        self.assertTrue(scope.delete('key1'))
        self.assertFalse(scope.has('key1'))
        self.assertFalse(scope.delete('nonexistent'))
    
    def test_scope_readonly(self):
        """Test readonly scope."""
        scope = Scope(name='test', readonly=True)
        
        with self.assertRaises(InvalidScopeError):
            scope.set('key', 'value')
        
        with self.assertRaises(InvalidScopeError):
            scope.delete('key')
        
        with self.assertRaises(InvalidScopeError):
            scope.clear()
    
    def test_scope_inheritance(self):
        """Test scope inheritance."""
        parent = Scope(name='parent')
        parent.set('inherited', 'from_parent')
        parent.set('overridden', 'parent_value')
        
        child = Scope(name='child', parent=parent)
        child.set('own_key', 'child_value')
        child.set('overridden', 'child_value')
        
        # Child has own key
        self.assertEqual(child.get('own_key'), 'child_value')
        
        # Child inherits from parent
        self.assertEqual(child.get('inherited'), 'from_parent')
        
        # Child overrides parent
        self.assertEqual(child.get('overridden'), 'child_value')
        
        # get_local only gets child's values
        self.assertEqual(child.get_local('own_key'), 'child_value')
        self.assertIsNone(child.get_local('inherited'))
    
    def test_scope_keys_items(self):
        """Test getting keys and items."""
        parent = Scope(name='parent')
        parent.set('p1', 1)
        parent.set('p2', 2)
        
        child = Scope(name='child', parent=parent)
        child.set('c1', 3)
        
        # Keys include parent keys
        keys = child.keys()
        self.assertIn('p1', keys)
        self.assertIn('p2', keys)
        self.assertIn('c1', keys)
        
        # Local keys only
        local_keys = child.keys(include_parents=False)
        self.assertEqual(len(local_keys), 1)
        self.assertIn('c1', local_keys)
        
        # Items
        items = child.items()
        self.assertEqual(items['p1'], 1)
        self.assertEqual(items['p2'], 2)
        self.assertEqual(items['c1'], 3)
    
    def test_scope_depth_path(self):
        """Test scope depth and path."""
        root = Scope(name='root')
        level1 = Scope(name='level1', parent=root)
        level2 = Scope(name='level2', parent=level1)
        
        self.assertEqual(root.depth(), 0)
        self.assertEqual(level1.depth(), 1)
        self.assertEqual(level2.depth(), 2)
        
        self.assertEqual(root.path(), ['root'])
        self.assertEqual(level1.path(), ['root', 'level1'])
        self.assertEqual(level2.path(), ['root', 'level1', 'level2'])
    
    def test_scope_age(self):
        """Test scope age."""
        scope = Scope(name='test')
        time.sleep(0.01)
        self.assertGreater(scope.age(), 0)


class TestScopedContext(unittest.TestCase):
    """Test ScopedContext class."""
    
    def setUp(self):
        """Set up test context."""
        self.ctx = ScopedContext(name='test_root')
    
    def test_basic_operations(self):
        """Test basic get/set/has/delete operations."""
        self.ctx.set('key1', 'value1')
        self.assertEqual(self.ctx.get('key1'), 'value1')
        self.assertTrue(self.ctx.has('key1'))
        
        self.assertTrue(self.ctx.delete('key1'))
        self.assertFalse(self.ctx.has('key1'))
    
    def test_bracket_notation(self):
        """Test bracket notation for access."""
        self.ctx['key'] = 'value'
        self.assertEqual(self.ctx['key'], 'value')
        self.assertTrue('key' in self.ctx)
        
        with self.assertRaises(ContextNotFoundError):
            _ = self.ctx['nonexistent']
    
    def test_nested_scopes(self):
        """Test nested scope creation."""
        self.ctx.set('root_key', 'root_value')
        
        with self.ctx.scope('level1') as scope1:
            self.assertEqual(scope1.name, 'level1')
            self.assertEqual(self.ctx.get('root_key'), 'root_value')
            
            self.ctx.set('level1_key', 'level1_value')
            self.assertEqual(self.ctx.get('level1_key'), 'level1_value')
            
            with self.ctx.scope('level2') as scope2:
                self.assertEqual(scope2.name, 'level2')
                self.assertEqual(self.ctx.get('root_key'), 'root_value')
                self.assertEqual(self.ctx.get('level1_key'), 'level1_value')
            
            # Back to level1
            self.assertTrue(self.ctx.has('level1_key'))
        
        # Back to root - level1_key is gone
        self.assertFalse(self.ctx.has('level1_key'))
        self.assertTrue(self.ctx.has('root_key'))
    
    def test_scope_depth(self):
        """Test scope depth tracking."""
        self.assertEqual(self.ctx.scope_depth, 0)
        
        with self.ctx.scope('a'):
            self.assertEqual(self.ctx.scope_depth, 1)
            
            with self.ctx.scope('b'):
                self.assertEqual(self.ctx.scope_depth, 2)
            
            self.assertEqual(self.ctx.scope_depth, 1)
        
        self.assertEqual(self.ctx.scope_depth, 0)
    
    def test_override(self):
        """Test context override."""
        self.ctx.set('key', 'original')
        
        with self.ctx.override(key='overridden'):
            self.assertEqual(self.ctx.get('key'), 'overridden')
        
        self.assertEqual(self.ctx.get('key'), 'original')
    
    def test_override_multiple_keys(self):
        """Test overriding multiple keys."""
        self.ctx.set('a', 1)
        self.ctx.set('b', 2)
        
        with self.ctx.override(a=10, c=30):
            self.assertEqual(self.ctx.get('a'), 10)
            self.assertEqual(self.ctx.get('b'), 2)  # Unchanged
            self.assertEqual(self.ctx.get('c'), 30)
        
        self.assertEqual(self.ctx.get('a'), 1)
        self.assertEqual(self.ctx.get('b'), 2)
        self.assertFalse(self.ctx.has('c'))
    
    def test_override_nonexistent_key(self):
        """Test overriding a key that doesn't exist."""
        self.assertFalse(self.ctx.has('new_key'))
        
        with self.ctx.override(new_key='temp'):
            self.assertEqual(self.ctx.get('new_key'), 'temp')
        
        # Key is removed after override
        self.assertFalse(self.ctx.has('new_key'))
    
    def test_snapshot_restore(self):
        """Test snapshot and restore."""
        self.ctx.set('a', 1)
        self.ctx.set('b', 2)
        
        snapshot = self.ctx.snapshot()
        
        self.ctx.set('a', 100)
        self.ctx.set('c', 3)
        self.ctx.delete('b')
        
        self.ctx.restore(snapshot)
        
        self.assertEqual(self.ctx.get('a'), 1)
        self.assertEqual(self.ctx.get('b'), 2)
        self.assertFalse(self.ctx.has('c'))
    
    def test_scope_path(self):
        """Test scope path tracking."""
        self.assertEqual(self.ctx.scope_path(), ['test_root'])
        
        with self.ctx.scope('first'):
            self.assertEqual(self.ctx.scope_path(), ['test_root', 'first'])
            
            with self.ctx.scope('second'):
                self.assertEqual(self.ctx.scope_path(), ['test_root', 'first', 'second'])
    
    def test_get_scope_by_name(self):
        """Test finding scope by name."""
        with self.ctx.scope('target') as target_scope:
            found = self.ctx.get_scope_by_name('target')
            self.assertEqual(found, target_scope)
        
        # Not found after scope ends
        self.assertIsNone(self.ctx.get_scope_by_name('target'))
    
    def test_thread_safety(self):
        """Test thread-safe operations."""
        results = {}
        
        def thread_func(thread_id):
            with self.ctx.scope(f'thread_{thread_id}'):
                self.ctx.set('thread_data', thread_id)
                time.sleep(0.01)  # Allow interleaving
                results[thread_id] = self.ctx.get('thread_data')
        
        threads = [threading.Thread(target=thread_func, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Each thread should have its own value
        for i in range(10):
            self.assertEqual(results[i], i)


class TestRequestContext(unittest.TestCase):
    """Test RequestContext class."""
    
    def setUp(self):
        """Set up test request context."""
        # Create a fresh instance for testing
        self.req = RequestContext()
        self.req._initialized = False
        self.req.__init__()
    
    def test_context_manager(self):
        """Test using as context manager."""
        self.assertFalse(self.req.active)
        
        with self.req:
            self.assertTrue(self.req.active)
            self.assertIsNotNone(self.req.request_id)
            self.req.set('user', 'test_user')
            self.assertEqual(self.req.get('user'), 'test_user')
        
        self.assertFalse(self.req.active)
    
    def test_attribute_access(self):
        """Test attribute-style access."""
        with self.req:
            self.req.user_id = 123
            self.req.username = 'test'
            
            self.assertEqual(self.req.user_id, 123)
            self.assertEqual(self.req.username, 'test')
            
            del self.req.username
            self.assertFalse(self.req.has('username'))
    
    def test_decorator(self):
        """Test using as decorator."""
        @self.req
        def my_func():
            self.assertTrue(self.req.active)
            self.req.value = 42
            return self.req.value
        
        result = my_func()
        self.assertEqual(result, 42)
        self.assertFalse(self.req.active)
    
    def test_elapsed_time(self):
        """Test elapsed time tracking."""
        with self.req:
            self.assertIsNotNone(self.req.elapsed)
            time.sleep(0.01)
            self.assertGreater(self.req.elapsed, 0)
    
    def test_thread_safety(self):
        """Test thread-safe request contexts."""
        results = {}
        
        def thread_func(thread_id):
            with self.req:
                self.req.thread_data = thread_id
                time.sleep(0.01)
                results[thread_id] = self.req.thread_data
        
        threads = [threading.Thread(target=thread_func, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        for i in range(5):
            self.assertEqual(results[i], i)


class TestContextVar(unittest.TestCase):
    """Test ContextVar class."""
    
    def test_basic_operations(self):
        """Test basic get/set operations."""
        var = ContextVar('test_var')
        
        self.assertFalse(var.is_set())
        var.set('value')
        self.assertTrue(var.is_set())
        self.assertEqual(var.get(), 'value')
    
    def test_default_value(self):
        """Test default value."""
        var = ContextVar('test_var', default='default_value')
        
        self.assertEqual(var.get(), 'default_value')
        var.set('new_value')
        self.assertEqual(var.get(), 'new_value')
    
    def test_get_with_default(self):
        """Test get with default parameter."""
        var = ContextVar('test_var')
        
        self.assertEqual(var.get('override_default'), 'override_default')
    
    def test_reset(self):
        """Test resetting values."""
        var = ContextVar('test_var', default='default')
        
        var.set('first')
        var.set('second')
        
        self.assertTrue(var.reset())
        self.assertEqual(var.get(), 'first')
        
        self.assertTrue(var.reset())
        self.assertEqual(var.get(), 'default')
        
        self.assertFalse(var.reset())  # Nothing to reset
    
    def test_using_context_manager(self):
        """Test using() context manager."""
        var = ContextVar('test_var', default='default')
        
        var.set('original')
        
        with var.using('temporary'):
            self.assertEqual(var.get(), 'temporary')
        
        self.assertEqual(var.get(), 'original')
    
    def test_on_change_callback(self):
        """Test on_change callback."""
        changes = []
        
        def on_change(old, new):
            changes.append((old, new))
        
        var = ContextVar('test_var', on_change=on_change)
        
        var.set('first')
        var.set('second')
        var.reset()
        
        self.assertEqual(len(changes), 3)
        # Note: old is ... on first set
        self.assertEqual(changes[1], ('first', 'second'))


class TestContextPropagator(unittest.TestCase):
    """Test ContextPropagator class."""
    
    def setUp(self):
        """Set up test context."""
        self.ctx = ScopedContext(name='test')
    
    def test_capture_apply(self):
        """Test capture and apply."""
        self.ctx.set('key1', 'value1')
        self.ctx.set('key2', 'value2')
        
        propagator = ContextPropagator(self.ctx)
        propagator.capture()
        
        # Clear context
        self.ctx.clear()
        self.assertFalse(self.ctx.has('key1'))
        
        # Apply captured
        propagator.apply()
        
        self.assertEqual(self.ctx.get('key1'), 'value1')
        self.assertEqual(self.ctx.get('key2'), 'value2')
    
    def test_capture_specific_keys(self):
        """Test capturing specific keys."""
        self.ctx.set('key1', 'value1')
        self.ctx.set('key2', 'value2')
        
        propagator = ContextPropagator(self.ctx)
        propagator.capture(['key1'])
        
        self.ctx.clear()
        propagator.apply()
        
        self.assertTrue(self.ctx.has('key1'))
        self.assertFalse(self.ctx.has('key2'))
    
    def test_propagate_context_manager(self):
        """Test propagate context manager."""
        self.ctx.set('key', 'original')
        
        propagator = ContextPropagator(self.ctx)
        
        with propagator.propagate():
            self.ctx.set('key', 'modified')
            self.assertEqual(self.ctx.get('key'), 'modified')
        
        # Should be restored
        self.assertEqual(self.ctx.get('key'), 'original')
    
    def test_age(self):
        """Test captured context age."""
        propagator = ContextPropagator(self.ctx)
        
        self.assertIsNone(propagator.age)  # Before capture
        propagator.capture()
        time.sleep(0.01)
        self.assertGreater(propagator.age, 0)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_global_context_operations(self):
        """Test global context convenience functions."""
        ctx_set('test_key', 'test_value')
        self.assertEqual(ctx_get('test_key'), 'test_value')
        self.assertTrue(ctx_has('test_key'))
        self.assertTrue(ctx_delete('test_key'))
        self.assertFalse(ctx_has('test_key'))
    
    def test_ctx_scope(self):
        """Test ctx_scope function."""
        with ctx_scope('test_scope'):
            ctx_set('scoped_key', 'scoped_value')
            self.assertTrue(ctx_has('scoped_key'))
        
        self.assertFalse(ctx_has('scoped_key'))
    
    def test_snapshot_restore(self):
        """Test ctx_snapshot and ctx_restore."""
        ctx_set('a', 1)
        ctx_set('b', 2)
        
        snapshot = ctx_snapshot()
        
        ctx_set('a', 100)
        ctx_delete('b')
        
        ctx_restore(snapshot)
        
        self.assertEqual(ctx_get('a'), 1)
        self.assertEqual(ctx_get('b'), 2)


class TestDecorators(unittest.TestCase):
    """Test decorators."""
    
    def test_with_context(self):
        """Test with_context decorator."""
        @with_context(user='admin', role='superuser')
        def my_func():
            return ctx_get('user'), ctx_get('role')
        
        user, role = my_func()
        self.assertEqual(user, 'admin')
        self.assertEqual(role, 'superuser')
        
        # Values are gone after function
        self.assertFalse(ctx_has('user'))
    
    def test_with_scope(self):
        """Test with_scope decorator."""
        @with_scope('transaction')
        def transaction_func():
            ctx_set('tx_id', 'abc123')
            return ctx_has('tx_id')
        
        self.assertTrue(transaction_func())
        self.assertFalse(ctx_has('tx_id'))
    
    def test_request_context_decorator(self):
        """Test request_context decorator."""
        @request_context
        def request_func():
            return get_request_context().active
        
        self.assertTrue(request_func())


class TestConcurrency(unittest.TestCase):
    """Test concurrent operations."""
    
    def test_concurrent_scopes(self):
        """Test concurrent scope operations."""
        ctx = ScopedContext(name='concurrent_test')
        results = []
        errors = []
        
        def worker(worker_id):
            try:
                with ctx.scope(f'worker_{worker_id}'):
                    ctx.set('worker_data', worker_id)
                    time.sleep(0.01)  # Allow interleaving
                    value = ctx.get('worker_data')
                    if value == worker_id:
                        results.append(worker_id)
            except Exception as e:
                errors.append((worker_id, str(e)))
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(worker, i) for i in range(20)]
            for f in futures:
                f.result()
        
        self.assertEqual(len(results), 20)
        self.assertEqual(len(errors), 0)
    
    def test_concurrent_context_vars(self):
        """Test concurrent context variable operations."""
        var = ContextVar('concurrent_var')
        results = []
        errors = []
        
        def worker(worker_id):
            try:
                with var.using(worker_id):
                    time.sleep(0.01)
                    value = var.get()
                    if value == worker_id:
                        results.append(worker_id)
            except Exception as e:
                errors.append((worker_id, str(e)))
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(worker, i) for i in range(20)]
            for f in futures:
                f.result()
        
        self.assertEqual(len(results), 20)
        self.assertEqual(len(errors), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)