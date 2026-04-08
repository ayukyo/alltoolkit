!! File Utils Example for Fortran
!! Demonstrates usage of file_utils module

program file_utils_example
    use file_utils
    use, intrinsic :: iso_fortran_env, only: int32, int64, output_unit
    implicit none
    
    character(len=:), allocatable :: content, joined, basename, dirname, ext
    type(PathComponents) :: components
    logical :: success, exists
    integer(int64) :: fsize
    character(len=256) :: test_file, test_file2, test_dir
    integer(int32), dimension(:), allocatable :: binary_data
    integer :: i
    
    print *, '========================================'
    print *, 'File Utils Example'
    print *, 'Fortran File Operations Demonstration'
    print *, '========================================'
    print *
    
    !==========================================================================
    ! Example 1: File Existence and Information
    !==========================================================================
    print *, '----------------------------------------'
    print *, 'Example 1: File Existence and Information'
    print *, '----------------------------------------'
    
    test_file = 'example_test.txt'
    
    ! Create a test file
    success = write_file_text(test_file, 'This is example content.')
    print *, 'Created test file: ', success
    
    ! Check if file exists
    exists = file_exists(test_file)
    print *, 'File exists: ', exists
    
    ! Check file size
    fsize = file_size(test_file)
    print *, 'File size: ', fsize, ' bytes'
    
    ! Check if readable/writable
    print *, 'Is readable: ', file_is_readable(test_file)
    print *, 'Is writable: ', file_is_writable(test_file)
    
    print *
    
    !==========================================================================
    ! Example 2: Path Manipulation
    !==========================================================================
    print *, '----------------------------------------'
    print *, 'Example 2: Path Manipulation'
    print *, '----------------------------------------'
    
    ! Join paths
    joined = path_join('/home', 'user')
    print *, 'path_join("/home", "user") = ', joined
    
    joined = path_join('/home/', 'documents/file.txt')
    print *, 'path_join("/home/", "documents/file.txt") = ', joined
    
    ! Get basename
    basename = path_basename('/home/user/document.txt')
    print *, 'path_basename("/home/user/document.txt") = ', basename
    
    ! Get dirname
    dirname = path_dirname('/home/user/document.txt')
    print *, 'path_dirname("/home/user/document.txt") = ', dirname
    
    ! Get extension
    ext = path_extension('/home/user/document.txt')
    print *, 'path_extension("/home/user/document.txt") = ', ext
    
    ! Get filename without extension
    basename = path_without_extension('/home/user/document.txt')
    print *, 'path_without_extension("/home/user/document.txt") = ', basename
    
    ! Split path into components
    components = path_split('/home/user/document.txt')
    print *, 'Path components:'
    print *, '  dirname:    ', components%dirname
    print *, '  basename:   ', components%basename
    print *, '  filename:   ', components%filename
    print *, '  extension:  ', components%extension
    
    ! Check if path is absolute
    print *, 'path_is_absolute("/home/user") = ', path_is_absolute('/home/user')
    print *, 'path_is_absolute("relative/path") = ', path_is_absolute('relative/path')
    
    ! Get path separator
    print *, 'Path separator: "', path_separator(), '"'
    
    print *
    
    !==========================================================================
    ! Example 3: Reading and Writing Text Files
    !==========================================================================
    print *, '----------------------------------------'
    print *, 'Example 3: Reading and Writing Text Files'
    print *, '----------------------------------------'
    
    ! Write text to file
    test_file = 'example_write.txt'
    success = write_file_text(test_file, 'Hello, Fortran World!')
    print *, 'write_file_text: ', success
    
    ! Read text from file
    success = read_file_text(test_file, content)
    print *, 'read_file_text: ', success
    print *, 'Content: ', content
    
    ! Append to file
    success = append_file_text(test_file, ' This is appended text.')
    print *, 'append_file_text: ', success
    
    ! Read again
    success = read_file_text(test_file, content)
    print *, 'Updated content: ', content
    
    print *
    
    !==========================================================================
    ! Example 4: File Copy and Move Operations
    !==========================================================================
    print *, '----------------------------------------'
    print *, 'Example 4: File Copy and Move Operations'
    print *, '----------------------------------------'
    
    test_file = 'example_source.txt'
    test_file2 = 'example_copied.txt'
    
    ! Create source file
    success = write_file_text(test_file, 'Source file content for copy test.')
    print *, 'Created source file: ', success
    
    ! Copy file
    success = file_copy(test_file, test_file2)
    print *, 'file_copy: ', success
    print *, 'Destination exists: ', file_exists(test_file2)
    
    ! Verify content
    success = read_file_text(test_file2, content)
    print *, 'Copied content: ', content
    
    ! Move/Rename file
    test_file2 = 'example_renamed.txt'
    success = file_rename('example_copied.txt', test_file2)
    print *, 'file_rename: ', success
    print *, 'Original exists: ', file_exists('example_copied.txt')
    print *, 'Renamed exists: ', file_exists(test_file2)
    
    print *
    
    !==========================================================================
    ! Example 5: Binary File Operations
    !==========================================================================
    print *, '----------------------------------------'
    print *, 'Example 5: Binary File Operations'
    print *, '----------------------------------------'
    
    test_file = 'example_binary.bin'
    
    ! Create binary data
    allocate(binary_data(10))
    do i = 1, 10
        binary_data(i) = i * 10
    end do
    
    ! Write binary data
    success = write_file_binary(test_file, binary_data)
    print *, 'write_file_binary: ', success
    print *, 'Binary file size: ', file_size(test_file), ' bytes'
    
    ! Read binary data
    if (allocated(binary_data)) deallocate(binary_data)
    success = read_file_binary(test_file, binary_data)
    print *, 'read_file_binary: ', success
    print *, 'Binary data read: ', binary_data
    
    print *
    
    !==========================================================================
    ! Example 6: Directory Operations
    !==========================================================================
    print *, '----------------------------------------'
    print *, 'Example 6: Directory Operations'
    print *, '----------------------------------------'
    
    test_dir = 'example_test_directory'
    
    ! Check if directory exists
    exists = directory_exists(test_dir)
    print *, 'directory_exists (before): ', exists
    
    ! Create directory
    success = directory_create(test_dir)
    print *, 'directory_create: ', success
    print *, 'directory_exists (after): ', directory_exists(test_dir)
    
    ! Get current directory
    print *, 'Current directory: ', get_current_directory()
    
    ! Delete directory
    success = directory_delete(test_dir)
    print *, 'directory_delete: ', success
    print *, 'directory_exists (after delete): ', directory_exists(test_dir)
    
    print *
    
    !==========================================================================
    ! Cleanup
    !==========================================================================
    print *, '----------------------------------------'
    print *, 'Cleanup: Removing test files'
    print *, '----------------------------------------'
    
    call file_delete('example_test.txt')
    call file_delete('example_write.txt')
    call file_delete('example_source.txt')
    call file_delete('example_renamed.txt')
    call file_delete('example_binary.bin')
    
    print *, 'Test files cleaned up.'
    print *
    print *, '========================================'
    print *, 'Example completed!'
    print *, '========================================'
    
end program file_utils_example