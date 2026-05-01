# Feature Flag Utils

A comprehensive, zero-dependency feature flag (feature toggle) management library for Python.

## Features

- **Simple Boolean Flags** - Basic on/off switches
- **Percentage Rollout** - Gradually enable features for a percentage of users
- **User Targeting** - Enable features for specific users
- **User Exclusion** - Block specific users from features
- **Conditional Rules** - Complex rule-based evaluation with multiple conditions
- **Time-Based Activation** - Schedule feature activation/deactivation
- **Environment Targeting** - Enable features per environment (dev, staging, prod)
- **Flag Dependencies** - Chain flags together
- **A/B Testing Variants** - Multiple variants with weighted distribution
- **Audit Logging** - Track all flag changes and evaluations
- **Thread-Safe Operations** - Safe for multi-threaded applications
- **JSON Serialization** - Easy persistence and loading

## Installation

No external dependencies required. Simply copy the `mod.py` file to your project.

## Quick Start

```python
from feature_flag_utils.mod import FeatureFlagManager

# Create a manager
manager = FeatureFlagManager(environment="production")

# Create a simple flag
manager.create_flag(
    key="new_ui",
    name="New UI Design",
    description="Enable the redesigned user interface",
    enabled=False
)

# Check if flag is enabled
if manager.is_enabled("new_ui"):
    # Show new UI
    pass
else:
    # Show old UI
    pass

# Enable the flag
manager.enable("new_ui")
assert manager.is_enabled("new_ui") is True
```

## Usage Examples

### Basic Boolean Flag

```python
manager = FeatureFlagManager()

# Create and enable a flag
manager.create_flag("dark_mode", "Dark Mode", enabled=True)

if manager.is_enabled("dark_mode"):
    print("Dark mode is enabled!")
```

### User Targeting

```python
manager = FeatureFlagManager()

# Create a flag for beta testers
manager.create_flag("beta_feature", "Beta Feature")
manager.add_targeted_users("beta_feature", "user1", "user2", "user3")

# Check for specific users
manager.is_enabled("beta_feature", "user1")  # True
manager.is_enabled("beta_feature", "user99")  # False
```

### Percentage Rollout

```python
manager = FeatureFlagManager()

# Gradually roll out to 25% of users
manager.create_flag("new_checkout", "New Checkout Flow")
manager.set_rollout_percentage("new_checkout", 25)

# Same user always gets same result (deterministic)
manager.is_enabled("new_checkout", "user123")  # Consistent result
```

### Conditional Rules

```python
manager = FeatureFlagManager()

manager.create_flag("premium_feature", "Premium Feature")
manager.add_rule(
    "premium_feature",
    name="premium_users",
    conditions=[
        {"attribute": "tier", "operator": "eq", "value": "premium"}
    ],
    result=True
)

# Evaluate with context
context = {"tier": "premium", "user_id": "123"}
manager.is_enabled("premium_feature", context=context)  # True
```

### Supported Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equal | `{"attribute": "country", "operator": "eq", "value": "US"}` |
| `ne` | Not equal | `{"attribute": "status", "operator": "ne", "value": "banned"}` |
| `in` | In list | `{"attribute": "role", "operator": "in", "value": ["admin", "mod"]}` |
| `not_in` | Not in list | `{"attribute": "level", "operator": "not_in", "value": [1, 2]}` |
| `gt` | Greater than | `{"attribute": "age", "operator": "gt", "value": 18}` |
| `lt` | Less than | `{"attribute": "score", "operator": "lt", "value": 100}` |
| `gte` | Greater than or equal | `{"attribute": "level", "operator": "gte", "value": 10}` |
| `lte` | Less than or equal | `{"attribute": "attempts", "operator": "lte", "value": 3}` |
| `contains` | String contains | `{"attribute": "email", "operator": "contains", "@admin"}` |
| `regex` | Regex match | `{"attribute": "phone", "operator": "regex", "value": r"^\d{3}-\d{4}$"}` |

### Time-Based Activation

```python
from datetime import datetime, timedelta

manager = FeatureFlagManager()

manager.create_flag("holiday_sale", "Holiday Sale", enabled=True)
manager.set_schedule(
    "holiday_sale",
    start_time=datetime.now() + timedelta(days=7),
    end_time=datetime.now() + timedelta(days=14)
)

# Won't be enabled until start_time
manager.is_enabled("holiday_sale")  # False (before start)
```

### Environment Targeting

```python
manager = FeatureFlagManager(environment="production")

manager.create_flag("new_api", "New API", enabled=True)
manager.set_environments("new_api", "staging", "production")

# Flag is enabled in production
manager.is_enabled("new_api")  # True

# Switch environment
manager.environment = "development"
manager.is_enabled("new_api")  # False
```

### Flag Dependencies

```python
manager = FeatureFlagManager()

# Parent feature must be enabled first
manager.create_flag("core_feature", "Core Feature", enabled=True)

# Child feature depends on parent
manager.create_flag("advanced_feature", "Advanced Feature", enabled=True)
manager.add_dependency("advanced_feature", "core_feature")

# Child is enabled only when parent is enabled
manager.is_enabled("advanced_feature")  # True (parent is on)

manager.disable("core_feature")
manager.is_enabled("advanced_feature")  # False (parent is off)
```

### A/B Testing Variants

```python
manager = FeatureFlagManager()

manager.create_flag("button_color", "Button Color Test", enabled=True)
manager.set_variants(
    "button_color",
    variants={
        "control": "blue",
        "treatment_a": "green",
        "treatment_b": "red"
    },
    default="control",
    weights={"control": 33, "treatment_a": 33, "treatment_b": 34}
)

# Get variant for user (consistent per user)
color = manager.get_variant("button_color", "user123")
print(f"Button color: {color}")
```

### Decorators

```python
from feature_flag_utils.mod import FeatureFlagManager, flag_enabled, flag_variant

manager = FeatureFlagManager()
manager.create_flag("new_algorithm", "New Algorithm", enabled=True)

# Only execute if flag is enabled
@flag_enabled(manager, "new_algorithm")
def run_new_algorithm():
    return "New algorithm result!"

result = run_new_algorithm()  # Only runs if flag is enabled

# Get variant in function
manager.set_variants("new_algorithm", {"a": 1, "b": 2}, default="a")

@flag_variant(manager, "new_algorithm")
def run_with_variant(variant):
    return f"Using variant: {variant}"
```

### Testing with FlagContext

```python
from feature_flag_utils.mod import FeatureFlagManager, FlagContext

manager = FeatureFlagManager()
manager.create_flag("test_feature", "Test Feature", enabled=False)

def test_with_feature():
    # Temporarily enable for testing
    with FlagContext(manager, "test_feature", True):
        assert manager.is_enabled("test_feature") is True
        # Run test code here
    
    # Flag is back to original state
    assert manager.is_enabled("test_feature") is False
```

### Persistence

```python
manager = FeatureFlagManager()

# Create some flags
manager.create_flag("feature1", "Feature 1", enabled=True)
manager.create_flag("feature2", "Feature 2", enabled=False)

# Export to JSON
json_str = manager.export_json()

# Save to file
manager.export_to_file("flags.json")

# Load from file
new_manager = FeatureFlagManager()
new_manager.import_from_file("flags.json")

# Or import from JSON string
new_manager.import_json(json_str)
```

### Audit Logging

```python
manager = FeatureFlagManager()
manager.create_flag("feature", "Feature")

# Enable the feature
manager.enable("feature")

# Check with user
manager.is_enabled("feature", "user123")

# Get audit log
log = manager.get_audit_log()
for entry in log:
    print(f"{entry.timestamp}: {entry.action} on {entry.flag_key}")

# Filter by flag or action
flag_log = manager.get_audit_log(flag_key="feature")
create_log = manager.get_audit_log(action="created")
```

### Change Notifications

```python
manager = FeatureFlagManager()

def on_flag_change(flag_key, action, value):
    print(f"Flag {flag_key} was {action}")
    # Send to webhook, update cache, etc.

manager.on_change(on_flag_change)

manager.create_flag("feature", "Feature")  # Triggers callback
```

### Global Manager

```python
from feature_flag_utils.mod import (
    get_global_manager, is_enabled, create_flag, enable_flag, disable_flag
)

# Use global convenience functions
create_flag("feature", "Feature")
enable_flag("feature")

if is_enabled("feature"):
    print("Feature is enabled!")

disable_flag("feature")
```

## API Reference

### FeatureFlagManager

| Method | Description |
|--------|-------------|
| `create_flag(key, name, ...)` | Create a new feature flag |
| `get_flag(key)` | Get flag by key |
| `update_flag(key, **kwargs)` | Update flag properties |
| `delete_flag(key)` | Delete a flag |
| `enable(key)` | Enable a flag |
| `disable(key)` | Disable a flag |
| `toggle(key)` | Toggle flag state |
| `is_enabled(key, user_id, context)` | Check if flag is enabled |
| `get_variant(key, user_id, context)` | Get variant value for A/B tests |
| `set_rollout_percentage(key, percentage)` | Set percentage rollout |
| `add_targeted_users(key, *user_ids)` | Add users to targeting |
| `remove_targeted_users(key, *user_ids)` | Remove users from targeting |
| `add_rule(key, name, conditions, result)` | Add conditional rule |
| `set_schedule(key, start_time, end_time)` | Set activation schedule |
| `set_environments(key, *envs)` | Set target environments |
| `add_dependency(key, depends_on)` | Add flag dependency |
| `set_variants(key, variants, default, weights)` | Set A/B test variants |
| `list_flags(enabled_only, tags)` | List all flags |
| `search_flags(query)` | Search flags by text |
| `get_audit_log(flag_key, action, limit)` | Get audit entries |
| `on_change(callback)` | Register change callback |
| `export_json()` | Export to JSON string |
| `import_json(json_str, merge)` | Import from JSON string |
| `export_to_file(filepath)` | Export to JSON file |
| `import_from_file(filepath, merge)` | Import from JSON file |

### FeatureFlag Properties

| Property | Type | Description |
|----------|------|-------------|
| `key` | str | Unique identifier |
| `name` | str | Human-readable name |
| `description` | str | Description |
| `enabled` | bool | Whether flag is enabled |
| `state` | FlagState | ON, OFF, PERCENTAGE, CONDITIONAL |
| `flag_type` | FlagType | BOOLEAN, VARIANT, PERCENTAGE, SCHEDULED |
| `rollout_percentage` | float | Percentage rollout (0-100) |
| `variants` | dict | Variant values for A/B testing |
| `default_variant` | str | Default variant name |
| `targeted_users` | set | Users with explicit access |
| `excluded_users` | set | Users explicitly blocked |
| `start_time` | datetime | Activation start time |
| `end_time` | datetime | Activation end time |
| `environments` | set | Target environments |
| `rules` | list | Conditional rules |
| `dependencies` | list | Required flag keys |
| `tags` | set | Tags for categorization |

## License

MIT License - Feel free to use in any project.