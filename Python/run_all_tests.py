#!/usr/bin/env python
"""Run all module tests and collect results."""

import os
import subprocess
import glob
import re
import sys

python_dir = '/home/admin/.openclaw/workspace/AllToolkit/Python'
results = {'passed': [], 'failed': [], 'error': []}

test_files = sorted(glob.glob(f'{python_dir}/*/*_test.py'))

print(f"Found {len(test_files)} test files")
print("Running tests...\n")

for test_file in test_files:
    module_dir = os.path.dirname(test_file)
    module_name = os.path.basename(module_dir)
    test_name = os.path.basename(test_file)
    
    # Run test from module directory
    try:
        proc = subprocess.Popen(
            ['python', test_name],
            cwd=module_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate()
        output = stdout.decode('utf-8', errors='replace') + stderr.decode('utf-8', errors='replace')
        returncode = proc.returncode
    except Exception as e:
        output = str(e)
        returncode = -1
    
    # Count tests from output
    count = 0
    m = re.search(r'Tests?:\s*(\d+)', output)
    if m:
        count = int(m.group(1))
    else:
        m = re.search(r'Tests run:\s*(\d+)', output)
        if m:
            count = int(m.group(1))
    
    if returncode == 0 and ('OK' in output or 'All tests passed' in output or 'passed' in output):
        results['passed'].append((module_name, count, output))
    elif returncode != 0:
        results['failed'].append((module_name, count, output))
    else:
        results['error'].append((module_name, count, output))

# Print summary
print("=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print(f"\nPassed modules: {len(results['passed'])}")
for m, c, o in sorted(results['passed']):
    print(f"  {m}: {c} tests")

print(f"\nFailed modules: {len(results['failed'])}")
for m, c, o in sorted(results['failed']):
    # Extract error type
    lines = o.split('\n') if o else []
    err_line = lines[-5] if len(lines) > 5 else (lines[-1] if lines else 'no output')
    print(f"  {m}: {err_line[:80]}")

print(f"\nError modules: {len(results['error'])}")
for m, c, o in sorted(results['error']):
    print(f"  {m}")

print(f"\nTotal: {len(results['passed'])} passed, {len(results['failed'])} failed, {len(results['error'])} errors")
print(f"Total tests: {sum(c for m,c,o in results['passed'])}")

# Return success if all passed
sys.exit(0 if len(results['failed']) == 0 and len(results['error']) == 0 else 1)