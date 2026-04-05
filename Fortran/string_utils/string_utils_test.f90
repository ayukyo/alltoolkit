!! AllToolkit - Fortran String Utilities Test Suite
!! Comprehensive tests for string_utils module

program string_utils_test
    use string_utils
    implicit none
    
    integer :: passed, failed, total
    
    passed = 0
    failed = 0
    total = 0
    
    print *, '========================================'
    print *, 'Fortran String Utilities Test Suite'
    print *, '========================================'
    print *, ''
    
    call test_empty_blank()
    call test_trimming()
    call test_case_conversion()
    call test_substring_ops()
    call test_prefix_suffix()
    call test_search_count()
    call test_replacement()
    call test_padding()
    call test_reverse_repeat()
    call test_validation()
    call test_utility()
    
    print *, ''
    print *, '========================================'
    print *, 'Test Results:'
    print *, '  Passed: ', passed
    print *, '  Failed: ', failed
    print *, '  Total:  ', total
    print *, '========================================'
    
    if (failed > 0) stop 1
    
contains

    subroutine assert_true(condition, test_name)
        logical, intent(in) :: condition
        character(len=*), intent(in) :: test_name
        total = total + 1
        if (condition) then
            passed = passed + 1
            print *, '  [PASS] ', test_name
        else
            failed = failed + 1
            print *, '  [FAIL] ', test_name
        end if
    end subroutine assert_true
    
    subroutine assert_equals_str(expected, actual, test_name)
        character(len=*), intent(in) :: expected, actual
        character(len=*), intent(in) :: test_name
        total = total + 1
        if (trim(expected) == trim(actual)) then
            passed = passed + 1
            print *, '  [PASS] ', test_name
        else
            failed = failed + 1
            print *, '  [FAIL] ', test_name
        end if
    end subroutine assert_equals_str
    
    subroutine assert_equals_int(expected, actual, test_name)
        integer, intent(in) :: expected, actual
        character(len=*), intent(in) :: test_name
        total = total + 1
        if (expected == actual) then
            passed = passed + 1
            print *, '  [PASS] ', test_name
        else
            failed = failed + 1
            print *, '  [FAIL] ', test_name
        end if
    end subroutine assert_equals_int
    
    subroutine test_empty_blank()
        print *, ''
        print *, '--- Empty/Blank Checks ---'
        call assert_true(is_empty(''), 'is_empty empty')
        call assert_true(.not. is_empty('hello'), 'is_empty non-empty')
        call assert_true(is_blank('   '), 'is_blank whitespace')
        call assert_true(is_not_blank('hello'), 'is_not_blank')
    end subroutine test_empty_blank
    
    subroutine test_trimming()
        print *, ''
        print *, '--- Trimming ---'
        call assert_equals_str('hello', str_trim('  hello  '), 'str_trim')
        call assert_equals_str('hello', remove_whitespace('h e l l o'), 'remove_whitespace')
        call assert_equals_str('hello world', normalize_whitespace('hello   world'), 'normalize_whitespace')
    end subroutine test_trimming
    
    subroutine test_case_conversion()
        print *, ''
        print *, '--- Case Conversion ---'
        call assert_equals_str('hello', to_lower('HELLO'), 'to_lower')
        call assert_equals_str('HELLO', to_upper('hello'), 'to_upper')
        call assert_equals_str('Hello', capitalize('hello'), 'capitalize')
        call assert_equals_str('hELLO', swap_case('Hello'), 'swap_case')
    end subroutine test_case_conversion
    
    subroutine test_substring_ops()
        print *, ''
        print *, '--- Substring Operations ---'
        call assert_equals_str('world', substring_after('hello world', 'hello '), 'substring_after')
        call assert_equals_str('world', substring_after_last('hello hello world', 'hello '), 'substring_after_last')
        call assert_equals_str('hello', substring_before('hello world', ' world'), 'substring_before')
        call assert_equals_str('content', substring_between('<div>content</div>', '<div>', '</div>'), 'substring_between')
        call assert_equals_str('hello...', truncate('hello world', 8, '...'), 'truncate')
    end subroutine test_substring_ops
    
    subroutine test_prefix_suffix()
        print *, ''
        print *, '--- Prefix/Suffix ---'
        call assert_true(starts_with('hello world', 'hello'), 'starts_with')
        call assert_true(ends_with('hello world', 'world'), 'ends_with')
        call assert_true(starts_with_ignore_case('Hello', 'hello'), 'starts_with_ignore_case')
        call assert_true(ends_with_ignore_case('Hello', 'HELLO'), 'ends_with_ignore_case')
        call assert_equals_str('world', remove_prefix('hello world', 'hello '), 'remove_prefix')
        call assert_equals_str('hello', remove_suffix('hello world', ' world'), 'remove_suffix')
    end subroutine test_prefix_suffix
    
    subroutine test_search_count()
        print *, ''
        print *, '--- Search and Count ---'
        call assert_equals_int(2, count_substring('hello hello world', 'hello'), 'count_substring')
        call assert_equals_int(0, count_substring('hello world', 'xyz'), 'count_substring not found')
        call assert_true(contains_substring('hello world', 'world'), 'contains_substring')
        call assert_equals_int(7, index_of('hello world', 'world'), 'index_of')
        call assert_equals_int(7, last_index_of('hello hello world', 'hello'), 'last_index_of')
    end subroutine test_search_count
    
    subroutine test_replacement()
        print *, ''
        print *, '--- Replacement ---'
        call assert_equals_str('hello universe', replace_first('hello world', 'world', 'universe'), 'replace_first')
        call assert_equals_str('hi hi hi', replace_all('hello hello hello', 'hello', 'hi'), 'replace_all')
    end subroutine test_replacement
    
    subroutine test_padding()
        print *, ''
        print *, '--- Padding ---'
        call assert_equals_str('00042', pad_left('42', 5, '0'), 'pad_left')
        call assert_equals_str('42000', pad_right('42', 5, '0'), 'pad_right')
        call assert_equals_str('  hi  ', center('hi', 6, ' '), 'center')
    end subroutine test_padding
    
    subroutine test_reverse_repeat()
        print *, ''
        print *, '--- Reverse and Repeat ---'
        call assert_equals_str('olleh', reverse_string('hello'), 'reverse_string')
        call assert_equals_str('hihihi', repeat_string('hi', 3), 'repeat_string')
    end subroutine test_reverse_repeat
    
    subroutine test_validation()
        print *, ''
        print *, '--- Validation ---'
        call assert_true(is_numeric('123'), 'is_numeric integer')
        call assert_true(is_numeric('3.14'), 'is_numeric float')
        call assert_true(.not. is_numeric('abc'), 'is_numeric not numeric')
        call assert_true(is_integer_str('123'), 'is_integer_str')
        call assert_true(is_alpha('abc'), 'is_alpha')
        call assert_true(is_alphanumeric('abc123'), 'is_alphanumeric')
        call assert_true(is_valid_email('test@example.com'), 'is_valid_email')
        call assert_true(.not. is_valid_email('invalid'), 'is_valid_email invalid')
    end subroutine test_validation
    
    subroutine test_utility()
        print *, ''
        print *, '--- Utility ---'
        call assert_equals_str('default', default_if_blank('', 'default'), 'default_if_blank')
        call assert_equals_str('hello', default_if_blank('hello', 'default'), 'default_if_blank with value')
        call assert_true(str_equals('hello', 'hello'), 'str_equals')
        call assert_true(str_equals_ignore_case('Hello', 'HELLO'), 'str_equals_ignore_case')
    end subroutine test_utility

end program string_utils_test
