"""
Feature Flag Utils - A comprehensive feature flag (feature toggle) management library.

This module provides a zero-dependency implementation of feature flags for managing
software releases, A/B testing, and enabling/disabling functionality without code changes.

Features:
- Simple boolean flags
- Percentage-based rollout
- User-specific targeting
- Time-based activation
- Environment-based flags
- Flag inheritance and dependencies
- Audit logging
- Thread-safe operations
- JSON serialization for persistence
"""

import json
import time
import threading
import hashlib
import random
from datetime import datetime, timedelta
from typing import (
    Any, Dict, List, Optional, Set, Callable, Union,
    Iterator, Tuple, TypeVar, Generic
)
from dataclasses import dataclass, field, asdict
from enum import Enum
from functools import wraps


def _parse_iso_datetime(iso_str: str) -> datetime:
    """Parse ISO format datetime string (compatible with Python 3.6)."""
    if not iso_str:
        return None
    # Handle various ISO formats
    try:
        # Try strptime for common formats
        if '.' in iso_str:
            # Has microseconds
            if '+' in iso_str or iso_str.endswith('Z'):
                # Has timezone
                iso_str = iso_str.replace('Z', '+00:00')
                fmt = "%Y-%m-%dT%H:%M:%S.%f%z"
            else:
                fmt = "%Y-%m-%dT%H:%M:%S.%f"
        else:
            # No microseconds
            if '+' in iso_str or iso_str.endswith('Z'):
                iso_str = iso_str.replace('Z', '+00:00')
                fmt = "%Y-%m-%dT%H:%M:%S%z"
            else:
                fmt = "%Y-%m-%dT%H:%M:%S"
        return datetime.strptime(iso_str, fmt)
    except ValueError:
        # Fallback: try simpler formats
        try:
            return datetime.strptime(iso_str.split('+')[0].split('Z')[0].split('.')[0],
                                     "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return datetime.strptime(iso_str[:19], "%Y-%m-%dT%H:%M:%S")


class FlagState(Enum):
    """Enumeration of possible flag states."""
    ON = "on"
    OFF = "off"
    PERCENTAGE = "percentage"
    CONDITIONAL = "conditional"


class FlagType(Enum):
    """Types of feature flags."""
    BOOLEAN = "boolean"
    VARIANT = "variant"
    PERCENTAGE = "percentage"
    SCHEDULED = "scheduled"


@dataclass
class FlagCondition:
    """Represents a condition for conditional flag evaluation."""
    attribute: str
    operator: str  # eq, ne, in, not_in, gt, lt, gte, lte, contains, regex
    value: Any
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate this condition against a context."""
        attr_value = context.get(self.attribute)
        
        if attr_value is None:
            return False
        
        if self.operator == "eq":
            return attr_value == self.value
        elif self.operator == "ne":
            return attr_value != self.value
        elif self.operator == "in":
            return attr_value in self.value
        elif self.operator == "not_in":
            return attr_value not in self.value
        elif self.operator == "gt":
            return attr_value > self.value
        elif self.operator == "lt":
            return attr_value < self.value
        elif self.operator == "gte":
            return attr_value >= self.value
        elif self.operator == "lte":
            return attr_value <= self.value
        elif self.operator == "contains":
            return self.value in attr_value
        elif self.operator == "regex":
            import re
            return bool(re.match(self.value, str(attr_value)))
        
        return False


@dataclass
class FlagRule:
    """A rule for flag evaluation with conditions and result."""
    name: str
    conditions: List[FlagCondition]
    result: Any
    priority: int = 0  # Higher priority rules are evaluated first
    
    def matches(self, context: Dict[str, Any]) -> bool:
        """Check if all conditions match the context."""
        return all(cond.evaluate(context) for cond in self.conditions)


@dataclass
class FeatureFlag:
    """
    Represents a feature flag with all its configuration options.
    """
    key: str
    name: str
    description: str = ""
    flag_type: FlagType = FlagType.BOOLEAN
    state: FlagState = FlagState.OFF
    enabled: bool = False
    
    # Percentage rollout (0-100)
    rollout_percentage: float = 0.0
    
    # Variant configuration for A/B testing
    variants: Dict[str, Any] = field(default_factory=dict)
    default_variant: str = ""
    
    # User targeting
    targeted_users: Set[str] = field(default_factory=set)
    excluded_users: Set[str] = field(default_factory=set)
    
    # Time-based activation
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    # Environment targeting
    environments: Set[str] = field(default_factory=set)
    
    # Conditional rules
    rules: List[FlagRule] = field(default_factory=list)
    
    # Dependencies on other flags
    dependencies: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: str = ""
    tags: Set[str] = field(default_factory=set)
    
    # Variant weights for percentage distribution
    variant_weights: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert flag to dictionary for serialization."""
        return {
            "key": self.key,
            "name": self.name,
            "description": self.description,
            "flag_type": self.flag_type.value,
            "state": self.state.value,
            "enabled": self.enabled,
            "rollout_percentage": self.rollout_percentage,
            "variants": self.variants,
            "default_variant": self.default_variant,
            "targeted_users": list(self.targeted_users),
            "excluded_users": list(self.excluded_users),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "environments": list(self.environments),
            "rules": [
                {
                    "name": r.name,
                    "conditions": [
                        {"attribute": c.attribute, "operator": c.operator, "value": c.value}
                        for c in r.conditions
                    ],
                    "result": r.result,
                    "priority": r.priority
                }
                for r in self.rules
            ],
            "dependencies": self.dependencies,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "created_by": self.created_by,
            "tags": list(self.tags),
            "variant_weights": self.variant_weights
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FeatureFlag":
        """Create a flag from dictionary."""
        rules = []
        for r in data.get("rules", []):
            conditions = [
                FlagCondition(
                    attribute=c["attribute"],
                    operator=c["operator"],
                    value=c["value"]
                )
                for c in r.get("conditions", [])
            ]
            rules.append(FlagRule(
                name=r["name"],
                conditions=conditions,
                result=r["result"],
                priority=r.get("priority", 0)
            ))
        
        return cls(
            key=data["key"],
            name=data["name"],
            description=data.get("description", ""),
            flag_type=FlagType(data.get("flag_type", "boolean")),
            state=FlagState(data.get("state", "off")),
            enabled=data.get("enabled", False),
            rollout_percentage=data.get("rollout_percentage", 0.0),
            variants=data.get("variants", {}),
            default_variant=data.get("default_variant", ""),
            targeted_users=set(data.get("targeted_users", [])),
            excluded_users=set(data.get("excluded_users", [])),
            start_time=_parse_iso_datetime(data.get("start_time")) if data.get("start_time") else None,
            end_time=_parse_iso_datetime(data.get("end_time")) if data.get("end_time") else None,
            environments=set(data.get("environments", [])),
            rules=rules,
            dependencies=data.get("dependencies", []),
            created_at=_parse_iso_datetime(data.get("created_at")) if data.get("created_at") else datetime.now(),
            updated_at=_parse_iso_datetime(data.get("updated_at")) if data.get("updated_at") else datetime.now(),
            created_by=data.get("created_by", ""),
            tags=set(data.get("tags", [])),
            variant_weights=data.get("variant_weights", {})
        )


@dataclass
class AuditEntry:
    """Represents an audit log entry for flag changes."""
    timestamp: datetime
    flag_key: str
    action: str  # created, updated, deleted, evaluated
    old_value: Any = None
    new_value: Any = None
    user: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "flag_key": self.flag_key,
            "action": self.action,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "user": self.user,
            "context": self.context
        }


class FeatureFlagManager:
    """
    Central manager for feature flags with thread-safe operations,
    persistence support, and comprehensive evaluation logic.
    """
    
    def __init__(self, environment: str = "default"):
        self._flags: Dict[str, FeatureFlag] = {}
        self._environment = environment
        self._audit_log: List[AuditEntry] = []
        self._lock = threading.RLock()
        self._change_callbacks: List[Callable[[str, str, Any], None]] = []
    
    @property
    def environment(self) -> str:
        """Get current environment."""
        return self._environment
    
    @environment.setter
    def environment(self, value: str):
        """Set current environment."""
        with self._lock:
            self._environment = value
    
    def create_flag(
        self,
        key: str,
        name: str,
        description: str = "",
        enabled: bool = False,
        flag_type: FlagType = FlagType.BOOLEAN,
        **kwargs
    ) -> FeatureFlag:
        """
        Create a new feature flag.
        
        Args:
            key: Unique identifier for the flag
            name: Human-readable name
            description: Description of what the flag controls
            enabled: Initial enabled state
            flag_type: Type of the flag
            **kwargs: Additional flag configuration options
            
        Returns:
            The created FeatureFlag instance
        """
        with self._lock:
            if key in self._flags:
                raise ValueError(f"Flag '{key}' already exists")
            
            flag = FeatureFlag(
                key=key,
                name=name,
                description=description,
                enabled=enabled,
                flag_type=flag_type,
                **kwargs
            )
            
            self._flags[key] = flag
            self._log_audit(key, "created", new_value=flag.to_dict())
            self._notify_change(key, "created", flag.to_dict())
            
            return flag
    
    def get_flag(self, key: str) -> Optional[FeatureFlag]:
        """Get a flag by its key."""
        return self._flags.get(key)
    
    def update_flag(self, key: str, **kwargs) -> FeatureFlag:
        """
        Update a flag's properties.
        
        Args:
            key: Flag key
            **kwargs: Properties to update
            
        Returns:
            The updated FeatureFlag instance
        """
        with self._lock:
            flag = self._flags.get(key)
            if not flag:
                raise KeyError(f"Flag '{key}' not found")
            
            old_value = flag.to_dict()
            
            for attr, value in kwargs.items():
                if hasattr(flag, attr):
                    if attr in ("targeted_users", "excluded_users", "environments", "tags"):
                        value = set(value) if not isinstance(value, set) else value
                    setattr(flag, attr, value)
            
            flag.updated_at = datetime.now()
            
            self._log_audit(key, "updated", old_value=old_value, new_value=flag.to_dict())
            self._notify_change(key, "updated", flag.to_dict())
            
            return flag
    
    def delete_flag(self, key: str) -> bool:
        """Delete a flag by its key."""
        with self._lock:
            if key not in self._flags:
                return False
            
            old_value = self._flags[key].to_dict()
            del self._flags[key]
            
            self._log_audit(key, "deleted", old_value=old_value)
            self._notify_change(key, "deleted", old_value)
            
            return True
    
    def enable(self, key: str) -> FeatureFlag:
        """Enable a flag."""
        return self.update_flag(key, enabled=True, state=FlagState.ON)
    
    def disable(self, key: str) -> FeatureFlag:
        """Disable a flag."""
        return self.update_flag(key, enabled=False, state=FlagState.OFF)
    
    def toggle(self, key: str) -> FeatureFlag:
        """Toggle a flag's enabled state."""
        flag = self._flags.get(key)
        if not flag:
            raise KeyError(f"Flag '{key}' not found")
        return self.update_flag(key, enabled=not flag.enabled)
    
    def is_enabled(
        self,
        key: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Check if a flag is enabled for the given context.
        
        This method implements the full evaluation chain:
        1. Check if flag exists
        2. Check dependencies
        3. Check environment targeting
        4. Check time-based activation
        5. Check user exclusion
        6. Check user targeting
        7. Check conditional rules
        8. Check percentage rollout
        9. Fall back to default state
        
        Args:
            key: Flag key
            user_id: Optional user identifier for targeting
            context: Additional context for rule evaluation
            
        Returns:
            Boolean indicating if the flag is enabled
        """
        with self._lock:
            flag = self._flags.get(key)
            if not flag:
                return False
            
            # Default context
            ctx = context or {}
            if user_id:
                ctx["user_id"] = user_id
            
            # Check dependencies
            for dep_key in flag.dependencies:
                if not self.is_enabled(dep_key, user_id, ctx):
                    return False
            
            # Check environment targeting
            if flag.environments and self._environment not in flag.environments:
                return False
            
            # Check time-based activation
            now = datetime.now()
            if flag.start_time and now < flag.start_time:
                return False
            if flag.end_time and now > flag.end_time:
                return False
            
            # Check user exclusion
            if user_id and user_id in flag.excluded_users:
                return False
            
            # Check user targeting
            if user_id and user_id in flag.targeted_users:
                self._log_audit(key, "evaluated", context=ctx, new_value=True)
                return True
            
            # Check conditional rules (sorted by priority, highest first)
            sorted_rules = sorted(flag.rules, key=lambda r: -r.priority)
            for rule in sorted_rules:
                if rule.matches(ctx):
                    self._log_audit(key, "evaluated", context=ctx, new_value=rule.result)
                    return bool(rule.result)
            
            # Check percentage rollout
            if flag.state == FlagState.PERCENTAGE or flag.rollout_percentage > 0:
                if user_id:
                    # Deterministic hash-based percentage
                    hash_value = self._hash_percentage(key, user_id)
                    result = hash_value < flag.rollout_percentage
                    self._log_audit(key, "evaluated", context=ctx, new_value=result)
                    return result
                else:
                    # Random percentage (for anonymous users)
                    result = random.random() * 100 < flag.rollout_percentage
                    self._log_audit(key, "evaluated", context=ctx, new_value=result)
                    return result
            
            # Fall back to enabled state
            self._log_audit(key, "evaluated", context=ctx, new_value=flag.enabled)
            return flag.enabled
    
    def get_variant(
        self,
        key: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Get the variant value for a flag (for A/B testing).
        
        Args:
            key: Flag key
            user_id: User identifier for consistent variant assignment
            context: Additional context
            
        Returns:
            The variant value for the user
        """
        with self._lock:
            flag = self._flags.get(key)
            if not flag or not flag.variants:
                return None
            
            if not self.is_enabled(key, user_id, context):
                return flag.variants.get(flag.default_variant)
            
            # Use variant weights if defined
            if flag.variant_weights:
                if user_id:
                    # Deterministic assignment based on user_id
                    hash_value = self._hash_percentage(key + "_variant", user_id)
                    cumulative = 0.0
                    for variant_name, weight in flag.variant_weights.items():
                        cumulative += weight
                        if hash_value < cumulative:
                            return flag.variants.get(variant_name)
                else:
                    # Random assignment
                    r = random.random() * 100
                    cumulative = 0.0
                    for variant_name, weight in flag.variant_weights.items():
                        cumulative += weight
                        if r < cumulative:
                            return flag.variants.get(variant_name)
            
            # Fall back to default variant
            return flag.variants.get(flag.default_variant)
    
    def _hash_percentage(self, key: str, user_id: str) -> float:
        """Generate a deterministic percentage (0-100) from key+user_id."""
        combined = f"{key}:{user_id}"
        hash_bytes = hashlib.md5(combined.encode()).hexdigest()
        # Take first 8 hex characters and convert to int
        hash_int = int(hash_bytes[:8], 16)
        # Map to 0-100 range
        return (hash_int % 10000) / 100.0
    
    def set_rollout_percentage(self, key: str, percentage: float) -> FeatureFlag:
        """
        Set the rollout percentage for a flag.
        
        Args:
            key: Flag key
            percentage: Percentage of users (0-100) to enable for
            
        Returns:
            The updated FeatureFlag
        """
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        return self.update_flag(key, rollout_percentage=percentage, state=FlagState.PERCENTAGE)
    
    def add_targeted_users(self, key: str, *user_ids: str) -> FeatureFlag:
        """Add users to the targeted list."""
        with self._lock:
            flag = self._flags.get(key)
            if not flag:
                raise KeyError(f"Flag '{key}' not found")
            flag.targeted_users.update(user_ids)
            flag.updated_at = datetime.now()
            return flag
    
    def remove_targeted_users(self, key: str, *user_ids: str) -> FeatureFlag:
        """Remove users from the targeted list."""
        with self._lock:
            flag = self._flags.get(key)
            if not flag:
                raise KeyError(f"Flag '{key}' not found")
            flag.targeted_users.difference_update(user_ids)
            flag.updated_at = datetime.now()
            return flag
    
    def add_rule(
        self,
        key: str,
        name: str,
        conditions: List[Dict[str, Any]],
        result: Any,
        priority: int = 0
    ) -> FeatureFlag:
        """
        Add a conditional rule to a flag.
        
        Args:
            key: Flag key
            name: Rule name
            conditions: List of condition dictionaries
            result: Result if rule matches
            priority: Rule priority (higher = evaluated first)
            
        Returns:
            The updated FeatureFlag
        """
        with self._lock:
            flag = self._flags.get(key)
            if not flag:
                raise KeyError(f"Flag '{key}' not found")
            
            rule_conditions = [
                FlagCondition(
                    attribute=c["attribute"],
                    operator=c["operator"],
                    value=c["value"]
                )
                for c in conditions
            ]
            
            rule = FlagRule(name=name, conditions=rule_conditions, result=result, priority=priority)
            flag.rules.append(rule)
            flag.updated_at = datetime.now()
            
            return flag
    
    def set_schedule(
        self,
        key: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> FeatureFlag:
        """Set activation schedule for a flag."""
        return self.update_flag(key, start_time=start_time, end_time=end_time)
    
    def set_environments(self, key: str, *environments: str) -> FeatureFlag:
        """Set target environments for a flag."""
        return self.update_flag(key, environments=set(environments))
    
    def add_dependency(self, key: str, depends_on: str) -> FeatureFlag:
        """Add a dependency on another flag."""
        with self._lock:
            if depends_on not in self._flags:
                raise KeyError(f"Dependency flag '{depends_on}' not found")
            flag = self._flags.get(key)
            if not flag:
                raise KeyError(f"Flag '{key}' not found")
            if depends_on not in flag.dependencies:
                flag.dependencies.append(depends_on)
            flag.updated_at = datetime.now()
            return flag
    
    def set_variants(
        self,
        key: str,
        variants: Dict[str, Any],
        default: str,
        weights: Optional[Dict[str, float]] = None
    ) -> FeatureFlag:
        """
        Set variants for A/B testing.
        
        Args:
            key: Flag key
            variants: Dictionary of variant name -> value
            default: Default variant name
            weights: Optional dictionary of variant weights (should sum to 100)
            
        Returns:
            The updated FeatureFlag
        """
        return self.update_flag(
            key,
            variants=variants,
            default_variant=default,
            variant_weights=weights or {},
            flag_type=FlagType.VARIANT
        )
    
    def list_flags(self, enabled_only: bool = False, tags: Optional[Set[str]] = None) -> List[FeatureFlag]:
        """
        List all flags with optional filtering.
        
        Args:
            enabled_only: Only return enabled flags
            tags: Only return flags with any of these tags
            
        Returns:
            List of matching FeatureFlag instances
        """
        with self._lock:
            flags = list(self._flags.values())
            
            if enabled_only:
                flags = [f for f in flags if f.enabled]
            
            if tags:
                flags = [f for f in flags if f.tags & tags]
            
            return flags
    
    def search_flags(self, query: str) -> List[FeatureFlag]:
        """Search flags by key, name, or description."""
        query_lower = query.lower()
        with self._lock:
            return [
                f for f in self._flags.values()
                if query_lower in f.key.lower()
                or query_lower in f.name.lower()
                or query_lower in f.description.lower()
            ]
    
    def get_audit_log(
        self,
        flag_key: Optional[str] = None,
        action: Optional[str] = None,
        limit: int = 100
    ) -> List[AuditEntry]:
        """
        Get audit log entries.
        
        Args:
            flag_key: Filter by flag key
            action: Filter by action type
            limit: Maximum entries to return
            
        Returns:
            List of AuditEntry instances
        """
        with self._lock:
            entries = list(self._audit_log)
            
            if flag_key:
                entries = [e for e in entries if e.flag_key == flag_key]
            
            if action:
                entries = [e for e in entries if e.action == action]
            
            return entries[-limit:]
    
    def _log_audit(
        self,
        flag_key: str,
        action: str,
        old_value: Any = None,
        new_value: Any = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Log an audit entry."""
        entry = AuditEntry(
            timestamp=datetime.now(),
            flag_key=flag_key,
            action=action,
            old_value=old_value,
            new_value=new_value,
            context=context or {}
        )
        self._audit_log.append(entry)
    
    def on_change(self, callback: Callable[[str, str, Any], None]):
        """
        Register a callback for flag changes.
        
        Args:
            callback: Function called with (flag_key, action, value)
        """
        self._change_callbacks.append(callback)
    
    def _notify_change(self, flag_key: str, action: str, value: Any):
        """Notify registered callbacks of a change."""
        for callback in self._change_callbacks:
            try:
                callback(flag_key, action, value)
            except Exception:
                pass  # Don't let callback errors propagate
    
    def export_json(self) -> str:
        """Export all flags to JSON string."""
        with self._lock:
            data = {
                "environment": self._environment,
                "flags": [f.to_dict() for f in self._flags.values()],
                "exported_at": datetime.now().isoformat()
            }
            return json.dumps(data, indent=2)
    
    def import_json(self, json_str: str, merge: bool = True) -> int:
        """
        Import flags from JSON string.
        
        Args:
            json_str: JSON string to import
            merge: If True, merge with existing flags; if False, replace
            
        Returns:
            Number of flags imported
        """
        with self._lock:
            data = json.loads(json_str)
            
            if not merge:
                self._flags.clear()
            
            count = 0
            for flag_data in data.get("flags", []):
                flag = FeatureFlag.from_dict(flag_data)
                self._flags[flag.key] = flag
                count += 1
            
            return count
    
    def export_to_file(self, filepath: str):
        """Export flags to a JSON file."""
        with open(filepath, "w") as f:
            f.write(self.export_json())
    
    def import_from_file(self, filepath: str, merge: bool = True) -> int:
        """Import flags from a JSON file."""
        with open(filepath, "r") as f:
            return self.import_json(f.read(), merge)
    
    def clear(self):
        """Remove all flags."""
        with self._lock:
            self._flags.clear()
            self._audit_log.clear()
    
    def __len__(self) -> int:
        return len(self._flags)
    
    def __contains__(self, key: str) -> bool:
        return key in self._flags
    
    def __iter__(self) -> Iterator[FeatureFlag]:
        return iter(self._flags.values())


def flag_enabled(
    manager: FeatureFlagManager,
    key: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None
):
    """
    Decorator to conditionally execute a function based on a feature flag.
    
    Usage:
        @flag_enabled(manager, "new_feature")
        def my_function():
            # This only executes if the flag is enabled
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if manager.is_enabled(key, user_id, context):
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator


def flag_variant(
    manager: FeatureFlagManager,
    key: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None
):
    """
    Decorator to select function variant based on feature flag variant.
    
    Usage:
        @flag_variant(manager, "ab_test", "user123")
        def my_function(variant):
            # variant will be the flag variant value
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            variant = manager.get_variant(key, user_id, context)
            return func(variant, *args, **kwargs)
        return wrapper
    return decorator


class FlagContext:
    """
    Context manager for temporarily modifying flag state.
    Useful for testing.
    """
    
    def __init__(
        self,
        manager: FeatureFlagManager,
        key: str,
        enabled: bool,
        user_id: Optional[str] = None
    ):
        self.manager = manager
        self.key = key
        self.enabled = enabled
        self.user_id = user_id
        self._original_enabled = None
        self._original_state = None
    
    def __enter__(self):
        flag = self.manager.get_flag(self.key)
        if flag:
            self._original_enabled = flag.enabled
            self._original_state = flag.state
            if self.enabled:
                self.manager.enable(self.key)
            else:
                self.manager.disable(self.key)
        else:
            self.manager.create_flag(self.key, self.key, enabled=self.enabled)
        return self
    
    def __exit__(self, *args):
        if self._original_enabled is not None:
            self.manager.update_flag(
                self.key,
                enabled=self._original_enabled,
                state=self._original_state
            )


# Convenience functions for quick flag operations
_global_manager: Optional[FeatureFlagManager] = None


def get_global_manager() -> FeatureFlagManager:
    """Get or create the global flag manager."""
    global _global_manager
    if _global_manager is None:
        _global_manager = FeatureFlagManager()
    return _global_manager


def set_global_manager(manager: FeatureFlagManager):
    """Set the global flag manager."""
    global _global_manager
    _global_manager = manager


def is_enabled(key: str, user_id: Optional[str] = None, context: Optional[Dict[str, Any]] = None) -> bool:
    """Check if a flag is enabled using the global manager."""
    return get_global_manager().is_enabled(key, user_id, context)


def create_flag(key: str, name: str, **kwargs) -> FeatureFlag:
    """Create a flag using the global manager."""
    return get_global_manager().create_flag(key, name, **kwargs)


def enable_flag(key: str) -> FeatureFlag:
    """Enable a flag using the global manager."""
    return get_global_manager().enable(key)


def disable_flag(key: str) -> FeatureFlag:
    """Disable a flag using the global manager."""
    return get_global_manager().disable(key)


if __name__ == "__main__":
    # Demo usage
    manager = FeatureFlagManager(environment="production")
    
    # Create a simple boolean flag
    flag1 = manager.create_flag(
        key="new_ui",
        name="New UI Design",
        description="Enable the redesigned user interface",
        enabled=False
    )
    print(f"Created flag: {flag1.key} - {flag1.name}")
    
    # Create a percentage rollout flag
    flag2 = manager.create_flag(
        key="new_checkout",
        name="New Checkout Flow",
        description="Enable the new checkout experience",
        enabled=False
    )
    manager.set_rollout_percentage("new_checkout", 25)
    print(f"Created percentage flag: {flag2.key} - {flag2.rollout_percentage}%")
    
    # Create a targeted flag
    flag3 = manager.create_flag(
        key="beta_feature",
        name="Beta Feature",
        description="Beta testing feature",
        enabled=False
    )
    manager.add_targeted_users("beta_feature", "user1", "user2", "user3")
    print(f"Created targeted flag: {flag3.key} - targeting {len(flag3.targeted_users)} users")
    
    # Test evaluations
    print("\nFlag evaluations:")
    print(f"new_ui for user1: {manager.is_enabled('new_ui', 'user1')}")
    print(f"beta_feature for user1: {manager.is_enabled('beta_feature', 'user1')}")
    print(f"beta_feature for user99: {manager.is_enabled('beta_feature', 'user99')}")
    
    # Enable new_ui
    manager.enable("new_ui")
    print(f"\nAfter enabling new_ui: {manager.is_enabled('new_ui', 'user1')}")
    
    # Export to JSON
    print("\nExported JSON:")
    print(manager.export_json())