!! AllToolkit - Fortran String Utilities Example
!! Demonstrates usage of string_utils module

program string_utils_example
    use string_utils
    implicit none
    
    character(len=100) :: str, result_str
    integer :: count_val, pos
    
    print *, '========================================'
    print *, 'Fortran String Utilities Examples'
    print *, '========================================'
    print *, ''
    
    ! Example 1: Empty/Blank Checks
    print *, '--- Example 1: Empty/Blank Checks ---'
    str = '  '
    print *, 'String: "', trim(str), '"'
    print *, 'is_blank: ', is_blank(str)
    print *, 'is_empty: ', is_empty(str)
    str = 'hello'
    print *, 'String: "', trim(str), '"'
    print *, 'is_not_blank: ', is_not_blank(str)
    print *, ''
    
    ! Example 2: Trimming and Whitespace
    print *, '--- Example 2: Trimming and Whitespace ---'
    str = '  hello world  '
    print *, 'Original: "', trim(str), '"'
    print *, 'str_trim: "', trim(str_trim(str)), '"'
    str = 'h e l l o'
    print *, 'Original: "', trim(str), '"'
    print *, 'remove_whitespace: "', trim(remove_whitespace(str)), '"'
    str = 'hello   world'
    print *, 'Original: "', trim(str), '"'
    print *, 'normalize_whitespace: "', trim(normalize_whitespace(str)), '"'
    print *, ''
    
    ! Example 3: Case Conversion
    print *, '--- Example 3: Case Conversion ---'
    str = 'Hello World'
    print *, 'Original: "', trim(str), '"'
    print *, 'to_lower: "', trim(to_lower(str)), '"'
    print *, 'to_upper: "', trim(to_upper(str)), '"'
    print *, 'capitalize: "', trim(capitalize('hello')), '"'
    print *, 'swap_case: "', trim(swap_case(str)), '"'
    print *, ''
    
    ! Example 4: Substring Operations
    print *, '--- Example 4: Substring Operations ---'
    str = 'hello world'
    print *, 'String: "', trim(str), '"'
    print *, 'substring_after "hello ": "', trim(substring_after(str, 'hello ')), '"'
    print *, 'substring_before " world": "', trim(substring_before(str, ' world')), '"'
    str = 'hello hello world'
    print *, 'String: "', trim(str), '"'
    print *, 'substring_after_last "hello ": "', trim(substring_after_last(str, 'hello ')), '"'
    str = '<div>content</div>'
    print *, 'String: "', trim(str), '"'
    print *, 'substring_between: "', trim(substring_between(str, '<div>', '</div>')), '"'
    str = 'hello world'
    print *, 'truncate to 8 with "...": "', trim(truncate(str, 8, '...')), '"'
    print *, ''
    
    ! Example 5: Prefix/Suffix Operations
    print *, '--- Example 5: Prefix/Suffix Operations ---'
    str = 'hello world'
    print *, 'String: "', trim(str), '"'
    print *, 'starts_with "hello": ', starts_with(str, 'hello')
    print *, 'ends_with "world": ', ends_with(str, 'world')
    print *, 'starts_with_ignore_case "HELLO": ', starts_with_ignore_case(str, 'HELLO')
    print *, 'remove_prefix "hello ": "', trim(remove_prefix(str, 'hello ')), '"'
    print *, 'remove_suffix " world": "', trim(remove_suffix(str, ' world')), '"'
    print *, ''
    
    ! Example 6: Search and Count
    print *, '--- Example 6: Search and Count ---'
    str = 'hello hello world'
    print *, 'String: "', trim(str), '"'
    count_val = count_substring(str, 'hello')
    print *, 'count_substring "hello": ', count_val
    print *, 'contains_substring "world": ', contains_substring(str, 'world')
    pos = index_of(str, 'world')
    print *, 'index_of "world": ', pos
    pos = last_index_of(str, 'hello')
    print *, 'last_index_of "hello": ', pos
    print *, ''
    
    ! Example 7: Replacement
    print *, '--- Example 7: Replacement ---'
    str = 'hello world'
    print *, 'Original: "', trim(str), '"'
    print *, 'replace_first "world" -> "universe": "', &
             trim(replace_first(str, 'world', 'universe')), '"'
    str = 'hello hello hello'
    print *, 'Original: "', trim(str), '"'
    print *, 'replace_all "hello" -> "hi": "', &
             trim(replace_all(str, 'hello', 'hi')), '"'
    print *, ''
    
    ! Example 8: Padding
    print *, '--- Example 8: Padding ---'
    str = '42'
    print *, 'Original: "', trim(str), '"'
    print *, 'pad_left to 5 with "0": "', trim(pad_left(str, 5, '0')), '"'
    print *, 'pad_right to 5 with "0": "', trim(pad_right(str, 5, '0')), '"'
    print *, 'center in 6 with spaces: "', trim(center('hi', 6, ' ')), '"'
    print *, ''
    
    ! Example 9: Reversal and Repetition
    print *, '--- Example 9: Reversal and Repetition ---'
    str = 'hello'
    print *, 'Original: "', trim(str), '"'
    print *, 'reverse_string: "', trim(reverse_string(str)), '"'
    print *, 'repeat_string 3 times: "', trim(repeat_string('hi', 3)), '"'
    print *, ''
    
    ! Example 10: Validation
    print *, '--- Example 10: Validation ---'
    print *, 'is_numeric "123": ', is_numeric('123')
    print *, 'is_numeric "3.14": ', is_numeric('3.14')
    print *, 'is_numeric "abc": ', is_numeric('abc')
    print *, 'is_integer_str "123": ', is_integer_str('123')
    print *, 'is_alpha "abc": ', is_alpha('abc')
    print *, 'is_alphanumeric "abc123": ', is_alphanumeric('abc123')
    print *, 'is_valid_email "test@example.com": ', is_valid_email('test@example.com')
    print *, 'is_valid_email "invalid": ', is_valid_email('invalid')
    print *, ''
    
    ! Example 11: Utility Functions
    print *, '--- Example 11: Utility Functions ---'
    str = ''
    print *, 'default_if_blank for empty: "', &
             trim(default_if_blank(str, 'default')), '"'
    str = 'hello'
    print *, 'default_if_blank for "hello": "', &
             trim(default_if_blank(str, 'default')), '"'
    print *, 'str_equals "hello" == "hello": ', str_equals('hello', 'hello')
    print *, 'str_equals_ignore_case "Hello" == "HELLO": ', &
             str_equals_ignore_case('Hello', 'HELLO')
    print *, ''
    
    print *, '========================================'
    print *, 'Examples completed!'
    print *, '========================================'

end program string_utils_example
