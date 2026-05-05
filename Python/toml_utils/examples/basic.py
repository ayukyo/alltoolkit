"""
TOML Utils - Basic Usage Examples
==================================

This example demonstrates basic TOML parsing and generation.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import parse, dumps, load, dump, get, set_value, merge


def example_parse():
    """Basic parsing example."""
    print("=" * 60)
    print("Example 1: Basic TOML Parsing")
    print("=" * 60)
    
    toml_string = '''
[package]
name = "my-project"
version = "1.0.0"
description = "A sample project"
authors = ["Alice", "Bob"]

[dependencies]
python = "^3.8"
requests = "^2.28"

[tool.pytest]
verbose = true
testpaths = ["tests"]
'''
    
    config = parse(toml_string)
    
    print(f"Package name: {config['package']['name']}")
    print(f"Version: {config['package']['version']}")
    print(f"Authors: {', '.join(config['package']['authors'])}")
    print(f"Dependencies: {list(config['dependencies'].keys())}")
    print(f"Pytest verbose: {config['tool']['pytest']['verbose']}")


def example_generate():
    """Basic generation example."""
    print("\n" + "=" * 60)
    print("Example 2: TOML Generation")
    print("=" * 60)
    
    config = {
        'project': {
            'name': 'toml-utils',
            'version': '1.0.0',
            'license': 'MIT'
        },
        'settings': {
            'debug': True,
            'max_connections': 100,
            'timeout': 30.5
        },
        'features': ['parsing', 'generation', 'validation']
    }
    
    toml_output = dumps(config)
    print("Generated TOML:")
    print(toml_output)


def example_dot_access():
    """Dot notation access example."""
    print("\n" + "=" * 60)
    print("Example 3: Dot Notation Access")
    print("=" * 60)
    
    config = {
        'database': {
            'primary': {
                'host': 'localhost',
                'port': 5432
            },
            'replica': {
                'host': 'replica.example.com',
                'port': 5433
            }
        }
    }
    
    # Get nested values using dot notation
    print(f"Primary host: {get(config, 'database.primary.host')}")
    print(f"Primary port: {get(config, 'database.primary.port')}")
    print(f"Replica host: {get(config, 'database.replica.host')}")
    
    # Get with default value
    print(f"Username: {get(config, 'database.username', 'admin')}")
    
    # Set nested values
    set_value(config, 'database.primary.ssl', True)
    print(f"SSL enabled: {get(config, 'database.primary.ssl')}")


def example_merge():
    """Configuration merge example."""
    print("\n" + "=" * 60)
    print("Example 4: Configuration Merging")
    print("=" * 60)
    
    base_config = {
        'server': {
            'host': 'localhost',
            'port': 8080
        },
        'database': {
            'host': 'localhost',
            'port': 5432
        },
        'debug': False
    }
    
    env_config = {
        'server': {
            'port': 3000  # Override port
        },
        'debug': True  # Enable debug
    }
    
    merged = merge(base_config, env_config)
    
    print("Base config:")
    print(f"  server.port: {base_config['server']['port']}")
    print(f"  debug: {base_config['debug']}")
    
    print("\nEnv config:")
    print(f"  server.port: {env_config['server']['port']}")
    print(f"  debug: {env_config['debug']}")
    
    print("\nMerged config:")
    print(f"  server.host: {merged['server']['host']}")  # From base
    print(f"  server.port: {merged['server']['port']}")  # From env (overridden)
    print(f"  database.host: {merged['database']['host']}")  # From base
    print(f"  debug: {merged['debug']}")  # From env (overridden)


if __name__ == '__main__':
    example_parse()
    example_generate()
    example_dot_access()
    example_merge()
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)