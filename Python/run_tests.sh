#!/bin/bash
passed=0
failed=0
total=0
failed_list=""
passed_list=""
test_count_total=0

cd /home/admin/.openclaw/workspace/AllToolkit/Python

for dir in */; do
  test_file="${dir}*_test.py"
  if ls $test_file 2>/dev/null | head -1 | read actual_file; then
    cd "$dir"
    result=$(python *_test.py 2>&1)
    cd ..
    
    # Parse test count
    count=$(echo "$result" | grep -oE 'Tests?: [0-9]+' | grep -oE '[0-9]+' || echo "0")
    if [ "$count" = "0" ]; then
      count=$(echo "$result" | grep -oE 'Tests run: [0-9]+' | grep -oE '[0-9]+' || echo "0")
    fi
    
    # Check if passed
    if echo "$result" | grep -qE "(OK|All tests passed|passed.*0 failed)"; then
      passed=$((passed + 1))
      test_count_total=$((test_count_total + count))
      passed_list="$passed_list$dir: $count tests\n"
    else
      failed=$((failed + 1))
      failed_list="$failed_list$dir\n"
    fi
    total=$((total + 1))
  fi
done

echo "=== TEST RESULTS ==="
echo "Passed: $passed modules ($test_count_total tests)"
echo "Failed: $failed modules"
echo ""
if [ -n "$failed_list" ]; then
  echo "Failed modules:"
  echo "$failed_list"
fi