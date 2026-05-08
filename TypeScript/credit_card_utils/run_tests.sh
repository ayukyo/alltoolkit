#!/bin/bash
# Credit Card Utilities Test Runner
# Run all tests for the credit card utilities module

echo "Running Credit Card Utilities Tests..."
echo "========================================"

# Check if ts-node is available
if command -v npx &> /dev/null; then
    npx ts-node credit_card_utils_test.ts
else
    echo "Error: ts-node not found. Please install it with:"
    echo "npm install -g ts-node typescript"
    exit 1
fi

echo "========================================"
echo "Tests completed!"