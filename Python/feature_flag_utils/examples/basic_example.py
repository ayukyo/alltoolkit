"""
Feature Flag Utils - Basic Usage Example

This example demonstrates the core functionality of the feature flag library.
"""

import sys
import os

# Add the parent directory to path for importing mod.py directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import directly from mod.py
from mod import (
    FeatureFlagManager, FlagState, FlagType,
    flag_enabled, FlagContext
)
from datetime import datetime, timedelta


def main():
    print("=" * 60)
    print("Feature Flag Utils - Basic Example")
    print("=" * 60)
    
    # Create a manager for the 'production' environment
    manager = FeatureFlagManager(environment="production")
    
    # 1. Simple Boolean Flag
    print("\n1. Simple Boolean Flag")
    print("-" * 40)
    
    manager.create_flag(
        key="new_ui",
        name="New UI Design",
        description="Enable the redesigned user interface",
        enabled=False
    )
    
    print(f"Flag 'new_ui' created: enabled={manager.is_enabled('new_ui')}")
    
    # Enable the flag
    manager.enable("new_ui")
    print(f"After enabling: enabled={manager.is_enabled('new_ui')}")
    
    # 2. Percentage Rollout
    print("\n2. Percentage Rollout")
    print("-" * 40)
    
    manager.create_flag(
        key="new_checkout",
        name="New Checkout Flow",
        description="Enable the new checkout experience for 25% of users",
        enabled=False
    )
    
    manager.set_rollout_percentage("new_checkout", 25)
    
    # Test percentage distribution
    enabled_count = 0
    for i in range(100):
        if manager.is_enabled("new_checkout", f"user{i}"):
            enabled_count += 1
    
    print(f"Rollout percentage: 25%")
    print(f"Actual distribution: {enabled_count}/100 users ({enabled_count}%)")
    
    # Same user always gets same result
    u1_result = manager.is_enabled("new_checkout", "alice")
    u2_result = manager.is_enabled("new_checkout", "alice")
    print(f"Consistent for same user: alice={u1_result}, alice again={u2_result}")
    
    # 3. User Targeting
    print("\n3. User Targeting")
    print("-" * 40)
    
    manager.create_flag(
        key="beta_feature",
        name="Beta Feature",
        description="Feature only for beta testers",
        enabled=False
    )
    
    # Add beta testers
    manager.add_targeted_users("beta_feature", "alice", "bob", "charlie")
    
    print(f"Beta testers: alice, bob, charlie")
    print(f"alice enabled: {manager.is_enabled('beta_feature', 'alice')}")
    print(f"bob enabled: {manager.is_enabled('beta_feature', 'bob')}")
    print(f"dave enabled: {manager.is_enabled('beta_feature', 'dave')} (not a tester)")
    
    # 4. Conditional Rules
    print("\n4. Conditional Rules")
    print("-" * 40)
    
    manager.create_flag(
        key="premium_feature",
        name="Premium Feature",
        description="Feature for premium tier users",
        enabled=False
    )
    
    # Add rule: enable for premium users in US
    manager.add_rule(
        "premium_feature",
        name="premium_us_rule",
        conditions=[
            {"attribute": "tier", "operator": "eq", "value": "premium"},
            {"attribute": "country", "operator": "eq", "value": "US"}
        ],
        result=True,
        priority=10
    )
    
    # Test rule evaluation
    premium_us = {"tier": "premium", "country": "US"}
    premium_uk = {"tier": "premium", "country": "UK"}
    free_us = {"tier": "free", "country": "US"}
    
    print(f"premium + US: {manager.is_enabled('premium_feature', context=premium_us)}")
    print(f"premium + UK: {manager.is_enabled('premium_feature', context=premium_uk)}")
    print(f"free + US: {manager.is_enabled('premium_feature', context=free_us)}")
    
    # 5. A/B Testing Variants
    print("\n5. A/B Testing Variants")
    print("-" * 40)
    
    manager.create_flag(
        key="button_color_test",
        name="Button Color A/B Test",
        description="Testing different button colors",
        enabled=True
    )
    
    manager.set_variants(
        "button_color_test",
        variants={
            "control": "blue",
            "treatment_a": "green",
            "treatment_b": "red"
        },
        default="control",
        weights={"control": 33, "treatment_a": 34, "treatment_b": 33}
    )
    
    # Get variants for different users
    colors = {}
    for user in ["alice", "bob", "charlie", "dave", "eve"]:
        color = manager.get_variant("button_color_test", user)
        colors[user] = color
    
    print("Button colors assigned:")
    for user, color in colors.items():
        print(f"  {user}: {color}")
    
    # 6. Environment Targeting
    print("\n6. Environment Targeting")
    print("-" * 40)
    
    manager.create_flag(
        key="dev_only_feature",
        name="Dev Only Feature",
        description="Feature only for development environment",
        enabled=True
    )
    
    manager.set_environments("dev_only_feature", "development", "staging")
    
    print(f"Target environments: development, staging")
    print(f"In production: {manager.is_enabled('dev_only_feature')} (disabled)")
    
    manager.environment = "development"
    print(f"In development: {manager.is_enabled('dev_only_feature')} (enabled)")
    
    manager.environment = "production"  # Reset
    
    # 7. Flag Dependencies
    print("\n7. Flag Dependencies")
    print("-" * 40)
    
    manager.create_flag(
        key="core_feature",
        name="Core Feature",
        description="Core feature must be enabled first",
        enabled=True
    )
    
    manager.create_flag(
        key="advanced_feature",
        name="Advanced Feature",
        description="Advanced feature depends on core",
        enabled=True
    )
    
    manager.add_dependency("advanced_feature", "core_feature")
    
    print(f"Core enabled: {manager.is_enabled('core_feature')}")
    print(f"Advanced enabled: {manager.is_enabled('advanced_feature')} (depends on core)")
    
    manager.disable("core_feature")
    print(f"After disabling core:")
    print(f"  Core: {manager.is_enabled('core_feature')}")
    print(f"  Advanced: {manager.is_enabled('advanced_feature')} (also disabled)")
    
    manager.enable("core_feature")  # Reset
    
    # 8. Using Decorators
    print("\n8. Using Decorators")
    print("-" * 40)
    
    manager.create_flag(
        key="decorator_test",
        name="Decorator Test",
        description="Test flag for decorator example",
        enabled=True
    )
    
    @flag_enabled(manager, "decorator_test")
    def special_function():
        return "Special function executed!"
    
    result = special_function()
    print(f"Decorator result (flag enabled): {result}")
    
    manager.disable("decorator_test")
    result = special_function()
    print(f"Decorator result (flag disabled): {result}")
    
    # 9. Audit Log
    print("\n9. Audit Log")
    print("-" * 40)
    
    log = manager.get_audit_log(limit=10)
    print(f"Recent audit entries ({len(log)}):")
    for entry in log[-5:]:
        print(f"  {entry.timestamp.strftime('%H:%M:%S')}: {entry.action} on '{entry.flag_key}'")
    
    # 10. Export/Import
    print("\n10. Export/Import")
    print("-" * 40)
    
    json_export = manager.export_json()
    print(f"Exported JSON length: {len(json_export)} characters")
    
    # Create new manager and import
    new_manager = FeatureFlagManager()
    count = new_manager.import_json(json_export)
    print(f"Imported {count} flags into new manager")
    
    # Verify import
    print(f"Flag 'new_ui' in new manager: {new_manager.is_enabled('new_ui')}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Total flags: {len(manager)}")
    print(f"Enabled flags: {len(manager.list_flags(enabled_only=True))}")
    print("=" * 60)


if __name__ == "__main__":
    main()