!! File Utils Test Suite for Fortran
!! Comprehensive tests for file_utils module

program file_utils_test
    use file_utils
    use, intrinsic :: iso_fortran_env, only: int32, int64, output_unit, error_unit
    implicit none
    
    integer :: total_tests, passed_tests, failed_tests
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    print *, '========================================'
    print *, 'File Utils Test Suite'
    print *, '========================================'
    print *
    
    ! Run all test categories
    call test_file_existence()
    call test_path_operations()
    call test_file_io()
    call test_file_operations()
    call test_directory_operations()
    
    ! Summary
    print *
    print *, '========================================'
    print *, 'Test Summary'
    print *, '========================================'
    print *, 'Total tests:  ', total_tests
    print *, 'Passed:       ', passed_tests
    print *, 'Failed:       ', failed_tests
    print *, '========================================'
    
    if (failed_tests == 0) then
        print *, 'All tests passed!'
        stop 0
    else
        print *, 'Some tests failed!'
        stop 1
    end if
    
contains
    
    ! Helper to run a single test
    subroutine run_test(test_name, condition)
        character(len=*), intent(in) :: test_name
        logical, intent(in) :: condition
        
        total_tests = total_tests + 1
        
        if (condition) then
            passed_tests = passed_tests + 1
            print *, '[PASS] ', test_name
        else
            failed_tests = failed_tests + 1
            print *, '[FAIL] ', test_name
        end if
    end subroutine run_test
    
    !==========================================================================
    ! Test File Existence
    !==========================================================================
    subroutine test_file_existence()
        logical :: exists, readable, writable
        integer :: unit_num, iostat
        character(len=256) :: test_file
        
        print *, '----------------------------------------'
        print *, 'Testing File Existence and Permissions'
        print *, '----------------------------------------'
        
        ! Create a test file
        test_file = 'test_file_utils_temp.txt'
        open(newunit=unit_num, file=test_file, status='replace', action='write', iostat=iostat)
        if (iostat == 0) then
            write(unit_num, *) 'Test content'
            close(unit_num)
        end if
        
        ! Test file_exists
        exists = file_exists(test_file)
        call run_test('file_exists returns true for existing file', exists)
        
        exists = file_exists('nonexistent_file_xyz.txt')
        call run_test('file_exists returns false for nonexistent file', .not. exists)
        
        ! Test file_is_readable
        readable = file_is_readable(test_file)
        call run_test('file_is_readable returns true for readable file', readable)
        
        readable = file_is_readable('nonexistent_file_xyz.txt')
        call run_test('file_is_readable returns false for nonexistent file', .not. readable)
        
        ! Test file_is_writable
        writable = file_is_writable(test_file)
        call run_test('file_is_writable returns true for writable file', writable)
        
        ! Clean up
        call file_delete(test_file)
        
        print *
    end subroutine test_file_existence
    
    !==========================================================================
    ! Test Path Operations
    !==========================================================================
    subroutine test_path_operations()
        character(len=:), allocatable :: joined, basename, dirname, ext, no_ext
        type(PathComponents) :: components
        logical :: is_abs
        
        print *, '----------------------------------------'
        print *, 'Testing Path Operations'
        print *, '----------------------------------------'
        
        ! Test path_join
        joined = path_join('/home', 'user')
        call run_test('path_join combines paths', joined == '/home/user' .or. joined == '/home\user')
        
        joined = path_join('/home/', 'user')
        call run_test('path_join handles trailing separator', joined == '/home/user' .or. joined == '/home/\user')
        
        ! Test path_basename
        basename = path_basename('/home/user/file.txt')
        call run_test('path_basename extracts filename', basename == 'file.txt')
        
        basename = path_basename('file.txt')
        call run_test('path_basename handles simple filename', basename == 'file.txt')
        
        ! Test path_dirname
        dirname = path_dirname('/home/user/file.txt')
        call run_test('path_dirname extracts directory', dirname == '/home/user')
        
        dirname = path_dirname('file.txt')
        call run_test('path_dirname handles simple filename', dirname == '.')
        
        ! Test path_extension
        ext = path_extension('/home/user/file.txt')
        call run_test('path_extension extracts extension', ext == 'txt')
        
        ext = path_extension('file')
        call run_test('path_extension handles no extension', ext == '')
        
        ! Test path_without_extension
        no_ext = path_without_extension('/home/user/file.txt')
        call run_test('path_without_extension removes extension', no_ext == 'file')
        
        ! Test path_split
        components = path_split('/home/user/file.txt')
        call run_test('path_split extracts dirname', components%dirname == '/home/user')
        call run_test('path_split extracts basename', components%basename == 'file.txt')
        call run_test('path_split extracts filename', components%filename == 'file')
        call run_test('path_split extracts extension', components%extension == 'txt')
        
        ! Test path_is_absolute
        is_abs = path_is_absolute('/home/user')
        call run_test('path_is_absolute recognizes Unix absolute path', is_abs)
        
        is_abs = path_is_absolute('relative/path')
        call run_test('path_is_absolute recognizes relative path', .not. is_abs)
        
        is_abs = path_is_absolute('C:\Windows')
        call run_test('path_is_absolute recognizes Windows absolute path', is_abs)
        
        ! Test path_separator
        call run_test('path_separator returns non-empty', len(path_separator()) >= 1)
        
        print *
    end subroutine test_path_operations
    
    !==========================================================================
    ! Test File I/O
    !==========================================================================
    subroutine test_file_io()
        character(len=:), allocatable :: content
        logical :: success
        integer(int64) :: fsize
        character(len=256) :: test_file
        
        print *, '----------------------------------------'
        print *, 'Testing File I/O Operations'
        print *, '----------------------------------------'
        
        test_file = 'test_io_temp.txt'
        
        ! Test write_file_text
        success = write_file_text(test_file, 'Hello, World!')
        call run_test('write_file_text creates file', success)
        call run_test('write_file_text file exists', file_exists(test_file))
        
        ! Test read_file_text
        success = read_file_text(test_file, content)
        call run_test('read_file_text reads file', success)
        call run_test('read_file_text content matches', content == 'Hello, World!')
        
        ! Test file_size
        fsize = file_size(test_file)
        call run_test('file_size returns positive for existing file', fsize > 0)
        
        fsize = file_size('nonexistent_file_xyz.txt')
        call run_test('file_size returns -1 for nonexistent file', fsize == -1)
        
        ! Test append_file_text
        success = append_file_text(test_file, ' Appended text.')
        call run_test('append_file_text appends to file', success)
        
        success = read_file_text(test_file, content)
        call run_test('read_file_text reads appended content', success)
        
        ! Clean up
        call file_delete(test_file)
        
        print *
    end subroutine test_file_io
    
    !==========================================================================
    ! Test File Operations
    !==========================================================================
    subroutine test_file_operations()
        logical :: success
        character(len=256) :: src_file, dst_file
        
        print *, '----------------------------------------'
        print *, 'Testing File Operations'
        print *, '----------------------------------------'
        
        src_file = 'test_copy_src.txt'
        dst_file = 'test_copy_dst.txt'
        
        ! Create source file
        success = write_file_text(src_file, 'Copy test content')
        call run_test('Created source file for copy test', success)
        
        ! Test file_copy
        success = file_copy(src_file, dst_file)
        call run_test('file_copy copies file', success)
        call run_test('file_copy destination exists', file_exists(dst_file))
        
        ! Test file_delete
        success = file_delete(dst_file)
        call run_test('file_delete deletes file', success)
        call run_test('file_delete file no longer exists', .not. file_exists(dst_file))
        
        ! Test file_rename
        dst_file = 'test_renamed.txt'
        success = file_rename(src_file, dst_file)
        call run_test('file_rename renames file', success)
        call run_test('file_rename source no longer exists', .not. file_exists(src_file))
        call run_test('file_rename destination exists', file_exists(dst_file))
        
        ! Test file_move (alias for rename)
        src_file = 'test_moved.txt'
        success = file_move(dst_file, src_file)
        call run_test('file_move moves file', success)
        
        ! Clean up
        call file_delete(src_file)
        
        print *
    end subroutine test_file_operations
    
    !==========================================================================
    ! Test Directory Operations
    !==========================================================================
    subroutine test_directory_operations()
        logical :: exists, success
        character(len=256) :: test_dir
        
        print *, '----------------------------------------'
        print *, 'Testing Directory Operations'
        print *, '----------------------------------------'
        
        test_dir = 'test_dir_temp'
        
        ! Test directory_exists (before creation)
        exists = directory_exists(test_dir)
        call run_test('directory_exists returns false for nonexistent dir', .not. exists)
        
        ! Test directory_create
        success = directory_create(test_dir)
        call run_test('directory_create creates directory', success)
        call run_test('directory_exists returns true after creation', directory_exists(test_dir))
        
        ! Test directory_delete
        success = directory_delete(test_dir)
        call run_test('directory_delete deletes directory', success)
        call run_test('directory_exists returns false after deletion', .not. directory_exists(test_dir))
        
        ! Test get_current_directory
        call run_test('get_current_directory returns non-empty', len(get_current_directory()) >= 1)
        
        print *
    end subroutine test_directory_operations
    
end program file_utils_test
