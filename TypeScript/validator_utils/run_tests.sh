#!/bin/bash
# Validator Utils - Test Runner
# 运行所有测试

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== AllToolkit Validator Utils - Test Runner ==="
echo ""

# Check for available runtimes
if command -v deno &> /dev/null; then
    echo "Running tests with Deno..."
    deno test validator_utils_test.ts
elif command -v bun &> /dev/null; then
    echo "Running tests with Bun..."
    bun test validator_utils_test.ts
elif command -v node &> /dev/null; then
    echo "Running tests with Node.js..."
    npx tsx validator_utils_test.ts
else
    echo "Error: No compatible runtime found (Deno, Bun, or Node.js required)"
    exit 1
fi

echo ""
echo "=== Tests Complete ==="
