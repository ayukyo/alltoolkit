!! AllToolkit - Fortran String Utilities Module
!! Zero-dependency string manipulation utilities for Fortran 90/95/2003+
!!
!! Features:
!! - String trimming and padding
!! - Case conversion
!! - Substring operations
!! - String searching and replacement
!! - String validation
!! - String splitting and joining
!! - String formatting
!!
!! Author: AllToolkit Contributors
!! License: MIT

module string_utils
    implicit none
    
    ! Module constants
    character(len=*), parameter :: LOWERCASE_CHARS = 'abcdefghijklmnopqrstuvwxyz'
    character(len=*), parameter :: UPPERCASE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    character(len=*), parameter :: DIGIT_CHARS = '0123456789'
    
    ! Default string length
    integer, parameter :: MAX_STRING_LEN = 1024
    
contains

    !--------------------------------------------------------------------------
    ! Empty/Blank Checks
    !--------------------------------------------------------------------------
    
    !> Check if a string is empty (length 0)
    function is_empty(str) result(res)
        character(len=*), intent(in) :: str
        logical :: res
        res = len_trim(str) == 0
    end function is_empty
    
    !> Check if a string is blank (empty or whitespace only)
    function is_blank(str) result(res)
        character(len=*), intent(in) :: str
        res = len_trim(str) == 0
    end function is_blank
    
    !> Check if a string is not blank
    function is_not_blank(str) result(res)
        character(len=*), intent(in) :: str
        res = len_trim(str) > 0
    end function is_not_blank
    
    !--------------------------------------------------------------------------
    ! Trimming and Whitespace
    !--------------------------------------------------------------------------
    
    !> Remove leading and trailing whitespace from a string
    function str_trim(str) result(res)
        character(len=*), intent(in) :: str
        character(len=len(str)) :: res
        res = trim(adjustl(str))
    end function str_trim
    
    !> Check if a character is whitespace
    function is_whitespace(c) result(res)
        character, intent(in) :: c
        logical :: res
        res = (c == ' ' .or. c == char(9) .or. c == char(10) .or. c == char(13))
    end function is_whitespace
    
    !> Remove all whitespace from a string
    function remove_whitespace(str) result(res)
        character(len=*), intent(in) :: str
        character(len=len(str)) :: res
        integer :: i, j
        character :: c
        
        res = ''
        j = 0
        do i = 1, len(str)
            c = str(i:i)
            if (.not. is_whitespace(c)) then
                j = j + 1
                res(j:j) = c
            end if
        end do
    end function remove_whitespace
    
    !> Normalize whitespace (collapse multiple spaces to single)
    function normalize_whitespace(str) result(res)
        character(len=*), intent(in) :: str
        character(len=len(str)) :: res
        integer :: i, j
        logical :: last_was_space
        character :: c
        
        res = ''
        j = 0
        last_was_space = .true.
        
        do i = 1, len_trim(str)
            c = str(i:i)
            if (is_whitespace(c)) then
                if (.not. last_was_space) then
                    j = j + 1
                    res(j:j) = ' '
                    last_was_space = .true.
                end if
            else
                j = j + 1
                res(j:j) = c
                last_was_space = .false.
            end if
        end do
    end function normalize_whitespace
    
    !--------------------------------------------------------------------------
    ! Case Conversion
    !--------------------------------------------------------------------------
    
    !> Convert string to lowercase
    function to_lower(str) result(res)
        character(len=*), intent(in) :: str
        character(len=len(str)) :: res
        integer :: i, pos
        character :: c
        
        res = str
        do i = 1, len(str)
            c = str(i:i)
            pos = index(UPPERCASE_CHARS, c)
            if (pos > 0) res(i:i) = LOWERCASE_CHARS(pos:pos)
        end do
    end function to_lower
    
    !> Convert string to uppercase
    function to_upper(str) result(res)
        character(len=*), intent(in) :: str
        character(len=len(str)) :: res
        integer :: i, pos
        character :: c
        
        res = str
        do i = 1, len(str)
            c = str(i:i)
            pos = index(LOWERCASE_CHARS, c)
            if (pos > 0) res(i:i) = UPPERCASE_CHARS(pos:pos)
        end do
    end function to_upper
    
    !> Capitalize first letter of string
    function capitalize(str) result(res)
        character(len=*), intent(in) :: str
        character(len=len(str)) :: res
        
        if (len_trim(str) > 0) then
            res = to_lower(str)
            res(1:1) = to_upper(str(1:1))
        else
            res = str
        end if
    end function capitalize
    
    !> Swap case of string
    function swap_case(str) result(res)
        character(len=*), intent(in) :: str
        character(len=len(str)) :: res
        integer :: i, pos_lower, pos_upper
        character :: c
        
        res = str
        do i = 1, len(str)
            c = str(i:i)
            pos_lower = index(LOWERCASE_CHARS, c)
            pos_upper = index(UPPERCASE_CHARS, c)
            if (pos_lower > 0) then
                res(i:i) = UPPERCASE_CHARS(pos_lower:pos_lower)
            else if (pos_upper > 0) then
                res(i:i) = LOWERCASE_CHARS(pos_upper:pos_upper)
            end if
        end do
    end function swap_case
    
    !--------------------------------------------------------------------------
    ! Substring Operations
    !--------------------------------------------------------------------------
    
    !> Extract substring after first occurrence of separator
    function substring_after(str, separator) result(res)
        character(len=*), intent(in) :: str, separator
        character(len=len(str)) :: res
        integer :: pos, sep_len
        
        sep_len = len_trim(separator)
        pos = index(str, trim(separator))
        
        if (pos > 0) then
            res = str(pos + sep_len:)
        else
            res = ''
        end if
    end function substring_after
    
    !> Extract substring after last occurrence of separator
    function substring_after_last(str, separator) result(res)
        character(len=*), intent(in) :: str, separator
        character(len=len(str)) :: res
        integer :: pos, last_pos, sep_len
        
        sep_len = len_trim(separator)
        last_pos = 0
        pos = 1
        
        do while (pos > 0)
            pos = index(str(last_pos + 1:), trim(separator))
            if (pos > 0) last_pos = last_pos + pos
        end do
        
        if (last_pos > 0) then
            res = str(last_pos + sep_len:)
        else
            res = ''
        end if
    end function substring_after_last
    
    !> Extract substring before first occurrence of separator
    function substring_before(str, separator) result(res)
        character(len=*), intent(in) :: str, separator
        character(len=len(str)) :: res
        integer :: pos
        
        pos = index(str, trim(separator))
        
        if (pos > 1) then
            res = str(1:pos-1)
        else
            res = ''
        end if
    end function substring_before
    
    !> Extract substring before last occurrence of separator
    function substring_before_last(str, separator) result(res)
        character(len=*), intent(in) :: str, separator
        character(len=len(str)) :: res
        integer :: pos, last_pos
        
        last_pos = 0
        pos = 1
        
        do while (pos > 0)
            pos = index(str(last_pos + 1:), trim(separator))
            if (pos > 0) last_pos = last_pos + pos
        end do
        
        if (last_pos > 1) then
            res = str(1:last_pos-1)
        else
            res = ''
        end if
    end function substring_before_last
    
    !> Extract substring between two markers
    function substring_between(str, open_marker, close_marker) result(res)
        character(len=*), intent(in) :: str, open_marker, close_marker
        character(len=len(str)) :: res
        integer :: open_pos, close_pos
        
        open_pos = index(str, trim(open_marker))
        if (open_pos > 0) then
            close_pos = index(str(open_pos + len_trim(open_marker):), trim(close_marker))
            if (close_pos > 0) then
                res = str(open_pos + len_trim(open_marker):open_pos + len_trim(open_marker) + close_pos - 2)
                return
            end if
        end if
        res = ''
    end function substring_between
    
    !> Truncate string to maximum length with suffix
    function truncate(str, max_len, suffix) result(res)
        character(len=*), intent(in) :: str, suffix
        integer, intent(in) :: max_len
        character(len=len(str)) :: res
        integer :: trunc_len
        
        if (len_trim(str) <= max_len) then
            res = str
        else
            trunc_len = max_len - len_trim(suffix)
            if (trunc_len > 0) then
                res = str(1:trunc_len) // trim(suffix)
            else
                res = str(1:max_len)
            end if
        end if
    end function truncate
    
    !--------------------------------------------------------------------------
    ! Prefix/Suffix Operations
    !--------------------------------------------------------------------------
    
    !> Check if string starts with prefix (case sensitive)
    function starts_with(str, prefix) result(res)
        character(len=*), intent(in) :: str, prefix
        logical :: res
        integer :: prefix_len
        
        prefix_len = len_trim(prefix)
        if (prefix_len == 0) then
            res = .true.
        else if (len_trim(str) < prefix_len) then
            res = .false.
        else
            res = str(1:prefix_len) == prefix(1:prefix_len)
        end if
    end function starts_with
    
    !> Check if string starts with prefix (case insensitive)
    function starts_with_ignore_case(str, prefix) result(res)
        character(len=*), intent(in) :: str, prefix
        logical :: res
        res = starts_with(to_lower(str), to_lower(prefix))
    end function starts_with_ignore_case
    
    !> Check if string ends with suffix (case sensitive)
    function ends_with(str, suffix) result(res)
        character(len=*), intent(in) :: str, suffix
        logical :: res
        integer :: suffix_len, str_len
        
        suffix_len = len_trim(suffix)
        str_len = len_trim(str)
        
        if (suffix_len == 0) then
            res = .true.
        else if (str_len < suffix_len) then
            res = .false.
        else
            res = str(str_len - suffix_len + 1:str_len) == suffix(1:suffix_len)
        end if
    end function ends_with
    
    !> Check if string ends with suffix (case insensitive)
    function ends_with_ignore_case(str, suffix) result(res)
        character(len=*), intent(in) :: str, suffix
        logical :: res
        res = ends_with(to_lower(str), to_lower(suffix))
    end function ends_with_ignore_case
    
    !> Remove prefix from string if present
    function remove_prefix(str, prefix) result(res)
        character(len=*), intent(in) :: str, prefix
        character(len=len(str)) :: res
        
        if (starts_with(str, prefix)) then
            res = str(len_trim(prefix) + 1:)
        else
            res = str
        end if
    end function remove_prefix
    
    !> Remove suffix from string if present
    function remove_suffix(str, suffix) result(res)
        character(len=*), intent(in) :: str, suffix
        character(len=len(str)) :: res
        integer :: str_len, suffix_len
        
        if (ends_with(str, suffix)) then
            str_len = len_trim(str)
            suffix_len = len_trim(suffix)
            res = str(1:str_len - suffix_len)
        else
            res = str
        end if
    end function remove_suffix
    
    !--------------------------------------------------------------------------
    ! Search and Count
    !--------------------------------------------------------------------------
    
    !> Count occurrences of substring in string
    function count_substring(str, substr) result(res)
        character(len=*), intent(in) :: str, substr
        integer :: res
        integer :: pos, substr_len
        
        res = 0
        substr_len = len_trim(substr)
        if (substr_len == 0) return
        
        pos = 1
        do while (pos > 0)
            pos = index(str(pos:), trim(substr))
            if (pos > 0) then
                res = res + 1
                pos = pos + substr_len
            end if
        end do
    end function count_substring
    
    !> Check if string contains substring (case sensitive)
    function contains_substring(str, substr) result(res)
        character(len=*), intent(in) :: str, substr
        logical :: res
        res = index(str, trim(substr)) > 0
    end function contains_substring
    
    !> Check if string contains substring (case insensitive)
    function contains_substring_ignore_case(str, substr) result(res)
        character(len=*), intent(in) :: str, substr
        logical :: res
        res = contains_substring(to_lower(str), to_lower(substr))
    end function contains_substring_ignore_case
    
    !> Find position of first occurrence of substring
    function index_of(str, substr) result(res)
        character(len=*), intent(in) :: str, substr
        integer :: res
        res = index(str, trim(substr))
    end function index_of
    
    !> Find position of last occurrence of substring
    function last_index_of(str, substr) result(res)
        character(len=*), intent(in) :: str, substr
        integer :: res, pos, last_pos
        
        last_pos = 0
        pos = 1
        
        do while (pos > 0)
            pos = index(str(last_pos + 1:), trim(substr))
            if (pos > 0) last_pos = last_pos + pos
        end do
        
        res = last_pos
    end function last_index_of
    
    !--------------------------------------------------------------------------
    ! Replacement
    !--------------------------------------------------------------------------
    
    !> Replace first occurrence of old substring with new substring
    function replace_first(str, old_substr, new_substr) result(res)
        character(len=*), intent(in) :: str, old_substr, new_substr
        character(len=MAX_STRING_LEN) :: res
        integer :: pos, old_len
        
        old_len = len_trim(old_substr)
        pos = index(str, trim(old_substr))
        
        if (pos > 0) then
            res = str(1:pos-1) // trim(new_substr) // str(pos + old_len:)
        else
            res = str
        end if
    end function replace_first
    
    !> Replace all occurrences of old substring with new substring
    function replace_all(str, old_substr, new_substr) result(res)
        character(len=*), intent(in) :: str, old_substr, new_substr
        character(len=MAX_STRING_LEN) :: res, temp
        integer :: pos, old_len
        
        old_len = len_trim(old_substr)
        if (old_len == 0) then
            res = str
            return
        end if
        
        res = str
        pos = index(res, trim(old_substr))
        
        do while (pos > 0)
            temp = res(1:pos-1) // trim(new_substr) // res(pos + old_len:)
            res = temp
            pos = index(res(pos + len_trim(new_substr):), trim(old_substr))
            if (pos > 0) pos = pos + pos + len_trim(new_substr) - 1
        end do
    end function replace_all
    
    !--------------------------------------------------------------------------
    ! Padding
    !--------------------------------------------------------------------------
    
    !> Pad string on the left to reach target length
    function pad_left(str, target_len, pad_char) result(res)
        character(len=*), intent(in) :: str, pad_char
        integer, intent(in) :: target_len
        character(len=target_len) :: res
        integer :: str_len, pad_len
        
        str_len = len_trim(str)
        if (str_len >= target_len) then
            res = str(1:target_len)
        else
            pad_len = target_len - str_len
            res = repeat(trim(pad_char), pad_len) // trim(str)
        end if
    end function pad_left
    
    !> Pad string on the right to reach target length
    function pad_right(str, target_len, pad_char) result(res)
        character(len=*), intent(in) :: str, pad_char
        integer, intent(in) :: target_len
        character(len=target_len) :: res
        integer :: str_len
        
        str_len = len_trim(str)
        if (str_len >= target_len) then
            res = str(1:target_len)
        else
            res = trim(str) // repeat(trim(pad_char), target_len - str_len)
        end if
    end function pad_right
    
    !> Center string with padding on both sides
    function center(str, target_len, pad_char) result(res)
        character(len=*), intent(in) :: str, pad_char
        integer, intent(in) :: target_len
        character(len=target_len) :: res
        integer :: str_len, left_pad, right_pad
        
        str_len = len_trim(str)
        if (str_len >= target_len) then
            res = str(1:target_len)
        else
            left_pad = (target_len - str_len) / 2
            right_pad = target_len - str_len - left_pad
            res = repeat(trim(pad_char), left_pad) // trim(str) // repeat(trim(pad_char), right_pad)
        end if
    end function center
    
    !--------------------------------------------------------------------------
    ! Reversal and Repetition
    !--------------------------------------------------------------------------
    
    !> Reverse string
    function reverse_string(str) result(res)
        character(len=*), intent(in) :: str
        character(len=len(str)) :: res
        integer :: i, str_len
        
        str_len = len_trim(str)
        do i = 1, str_len
            res(i:i) = str(str_len - i + 1:str_len - i + 1)
        end do
        do i = str_len + 1, len(str)
            res(i:i) = ' '
        end do
    end function reverse_string
    
    !> Repeat string n times
    function repeat_string(str, n) result(res)
        character(len=*), intent(in) :: str
        integer, intent(in) :: n
        character(len=len(str) * max(n, 0)) :: res
        integer :: i
        
        res = ''
        do i = 1, n
            res = res // trim(str)
        end do
    end function repeat_string
    
    !--------------------------------------------------------------------------
    ! Validation
    !--------------------------------------------------------------------------
    
    !> Check if string is numeric (integer or float)
    function is_numeric(str) result(res)
        character(len=*), intent(in) :: str
        logical :: res
        integer :: i, decimal_count
        character :: c
        logical :: has_digit
        
        res = .false.
        has_digit = .false.
        decimal_count = 0
        
        do i = 1, len_trim(str)
            c = str(i:i)
            if (c >= '0' .and. c <= '9') then
                has_digit = .true.
            else if (c == '.') then
                decimal_count = decimal_count + 1
                if (decimal_count > 1) return
            else if (i == 1 .and. (c == '+' .or. c == '-')) then
                continue
            else
                return
            end if
        end do
        
        res = has_digit
    end function is_numeric
    
    !> Check if string is integer
    function is_integer_str(str) result(res)
        character(len=*), intent(in) :: str
        logical :: res
        integer :: i
        character :: c
        logical :: has_digit
        
        res = .false.
        has_digit = .false.
        
        do i = 1, len_trim(str)
            c = str(i:i)
            if (c >= '0' .and. c <= '9') then
                has_digit = .true.
            else if (i == 1 .and. (c == '+' .or. c == '-')) then
                continue
            else
                return
            end if
        end do
        
        res = has_digit
    end function is_integer_str
    
    !> Check if string contains only alphabetic characters
    function is_alpha(str) result(res)
        character(len=*), intent(in) :: str
        logical :: res
        integer :: i, pos
        character :: c
        
        res = .false.
        if (len_trim(str) == 0) return
        
        do i = 1, len_trim(str)
            c = str(i:i)
            pos = index(LOWERCASE_CHARS, c)
            if (pos == 0) pos = index(UPPERCASE_CHARS, c)
            if (pos == 0) return
        end do
        
        res = .true.
    end function is_alpha
    
    !> Check if string contains only alphanumeric characters
    function is_alphanumeric(str) result(res)
        character(len=*), intent(in) :: str
        logical :: res
        integer :: i, pos
        character :: c
        
        res = .false.
        if (len_trim(str) == 0) return
        
        do i = 1, len_trim(str)
            c = str(i:i)
            pos = index(LOWERCASE_CHARS, c)
            if (pos == 0) pos = index(UPPERCASE_CHARS, c)
            if (pos == 0) pos = index(DIGIT_CHARS, c)
            if (pos == 0) return
        end do
        
        res = .true.
    end function is_alphanumeric
    
    !> Check if string is valid email format (basic validation)
    function is_valid_email(str) result(res)
        character(len=*), intent(in) :: str
        logical :: res
        integer :: at_pos, dot_pos
        
        res = .false.
        at_pos = index(str, '@')
        if (at_pos <= 1) return
        if (at_pos == len_trim(str)) return
        
        dot_pos = index(str(at_pos:), '.')
        if (dot_pos <= 2) return
        if (at_pos + dot_pos - 1 == len_trim(str)) return
        
        res = .true.
    end function is_valid_email
    
    !--------------------------------------------------------------------------
    ! Utility Functions
    !--------------------------------------------------------------------------
    
    !> Return default value if string is blank
    function default_if_blank(str, default_val) result(res)
        character(len=*), intent(in) :: str, default_val
        character(len=len(default_val)) :: res
        
        if (is_blank(str)) then
            res = default_val
        else
            res = str(1:len(default_val))
        end if
    end function default_if_blank
    
    !> Compare two strings for equality (case sensitive)
    function str_equals(str1, str2) result(res)
        character(len=*), intent(in) :: str1, str2
        logical :: res
        res = trim(str1) == trim(str2)
    end function str_equals
    
    !> Compare two strings for equality (case insensitive)
    function str_equals_ignore_case(str1, str2) result(res)
        character(len=*), intent(in) :: str1, str2
        logical :: res
        res = str_equals(to_lower(str1), to_lower(str2))
    end function str_equals_ignore_case

end module string_utils
