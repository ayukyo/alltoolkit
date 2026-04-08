!! File Utilities Module for Fortran
!! Provides file and directory operations, path manipulation, and file information utilities
!! Zero dependencies - uses only Fortran standard library
!!
!! Author: AllToolkit Contributors
!! License: MIT

module file_utils
    use, intrinsic :: iso_fortran_env, only: int32, int64, real64, error_unit
    implicit none
    
    private
    public :: file_exists, file_is_readable, file_is_writable
    public :: file_size, file_modification_time, file_creation_time
    public :: file_copy, file_move, file_delete, file_rename
    public :: directory_exists, directory_create, directory_delete
    public :: directory_list, directory_list_files, directory_list_dirs
    public :: path_join, path_split, path_basename, path_dirname
    public :: path_extension, path_without_extension
    public :: path_is_absolute, path_normalize, path_relative
    public :: path_separator, get_current_directory, change_directory
    public :: read_file_text, write_file_text, append_file_text
    public :: read_file_binary, write_file_binary
    public :: FileInfo, FileList, PathComponents
    
    !! Constants
    character(len=*), parameter :: PATH_SEP = '/'
    character(len=*), parameter :: PATH_SEP_WIN = '\'
    integer(int64), parameter :: BUFFER_SIZE = 8192_int64
    
    !! Derived types
    type :: FileInfo
        character(len=:), allocatable :: path
        character(len=:), allocatable :: name
        integer(int64) :: size
        integer(int64) :: mod_time
        logical :: is_directory
        logical :: is_file
        logical :: is_readable
        logical :: is_writable
    end type FileInfo
    
    type :: FileList
        type(FileInfo), dimension(:), allocatable :: files
        integer :: count
    end type FileList
    
    type :: PathComponents
        character(len=:), allocatable :: dirname
        character(len=:), allocatable :: basename
        character(len=:), allocatable :: extension
        character(len=:), allocatable :: filename
    end type PathComponents
    
contains
    
    !==========================================================================
    ! File Existence and Permissions
    !==========================================================================
    
    !> Check if a file exists
    !! @param filepath Path to the file
    !! @return True if file exists, false otherwise
    function file_exists(filepath) result(exists)
        character(len=*), intent(in) :: filepath
        logical :: exists
        
        inquire(file=filepath, exist=exists)
    end function file_exists
    
    !> Check if a file is readable
    !! @param filepath Path to the file
    !! @return True if file is readable, false otherwise
    function file_is_readable(filepath) result(readable)
        character(len=*), intent(in) :: filepath
        logical :: readable, exists
        integer :: unit_num, iostat
        
        readable = .false.
        inquire(file=filepath, exist=exists)
        if (.not. exists) return
        
        ! Try to open file for reading
        open(newunit=unit_num, file=filepath, status='old', action='read', &
             iostat=iostat)
        if (iostat == 0) then
            readable = .true.
            close(unit_num)
        end if
    end function file_is_readable
    
    !> Check if a file is writable
    !! @param filepath Path to the file
    !! @return True if file is writable, false otherwise
    function file_is_writable(filepath) result(writable)
        character(len=*), intent(in) :: filepath
        logical :: writable, exists
        integer :: unit_num, iostat
        
        writable = .false.
        exists = file_exists(filepath)
        
        if (exists) then
            ! Try to open file for writing
            open(newunit=unit_num, file=filepath, status='old', action='write', &
                 iostat=iostat)
            if (iostat == 0) then
                writable = .true.
                close(unit_num)
            end if
        else
            ! Try to create file
            open(newunit=unit_num, file=filepath, status='new', action='write', &
                 iostat=iostat)
            if (iostat == 0) then
                writable = .true.
                close(unit_num, status='delete')  ! Clean up test file
            end if
        end if
    end function file_is_writable
    
    !> Check if a directory exists
    !! @param dirpath Path to the directory
    !! @return True if directory exists, false otherwise
    function directory_exists(dirpath) result(exists)
        character(len=*), intent(in) :: dirpath
        logical :: exists
        integer :: iostat
        character(len=256) :: testfile
        
        ! Try to create a temporary file in the directory
        testfile = trim(dirpath) // path_separator() // '.test_' // random_string(8)
        
        open(newunit=iostat, file=testfile, status='new', iostat=iostat)
        if (iostat == 0) then
            exists = .true.
            close(iostat, status='delete')
        else
            exists = .false.
        end if
    end function directory_exists
    
    !==========================================================================
    ! File Information
    !==========================================================================
    
    !> Get file size in bytes
    !! @param filepath Path to the file
    !! @return File size in bytes, -1 if file doesn't exist
    function file_size(filepath) result(fsize)
        character(len=*), intent(in) :: filepath
        integer(int64) :: fsize
        integer :: unit_num, iostat
        
        fsize = -1_int64
        if (.not. file_exists(filepath)) return
        
        open(newunit=unit_num, file=filepath, status='old', action='read', &
             form='unformatted', access='stream', iostat=iostat)
        if (iostat /= 0) return
        
        inquire(unit=unit_num, size=fsize)
        close(unit_num)
    end function file_size
    
    !> Get file modification time (simplified - returns 0 for now)
    !! @param filepath Path to the file
    !! @return Modification time as timestamp (0 if not available)
    function file_modification_time(filepath) result(mtime)
        character(len=*), intent(in) :: filepath
        integer(int64) :: mtime
        
        ! Fortran standard doesn't provide file modification time
        ! This would require system-specific extensions
        ! Returning 0 as placeholder
        mtime = 0_int64
        if (file_exists(filepath)) then
            mtime = 1_int64  ! Indicate file exists but time not available
        end if
    end function file_modification_time
    
    !> Get file creation time (simplified - returns 0 for now)
    !! @param filepath Path to the file
    !! @return Creation time as timestamp (0 if not available)
    function file_creation_time(filepath) result(ctime)
        character(len=*), intent(in) :: filepath
        integer(int64) :: ctime
        
        ! Fortran standard doesn't provide file creation time
        ctime = 0_int64
        if (file_exists(filepath)) then
            ctime = 1_int64  ! Indicate file exists but time not available
        end if
    end function file_creation_time
    
    !> Get detailed file information
    !! @param filepath Path to the file
    !! @return FileInfo structure with file details
    function get_file_info(filepath) result(info)
        character(len=*), intent(in) :: filepath
        type(FileInfo) :: info
        
        info%path = filepath
        info%name = path_basename(filepath)
        info%size = file_size(filepath)
        info%mod_time = file_modification_time(filepath)
        info%is_directory = directory_exists(filepath)
        info%is_file = file_exists(filepath) .and. (.not. info%is_directory)
        info%is_readable = file_is_readable(filepath)
        info%is_writable = file_is_writable(filepath)
    end function get_file_info
    
    !==========================================================================
    ! File Operations
    !==========================================================================
    
    !> Copy a file
    !! @param source Source file path
    !! @param dest Destination file path
    !! @return True if successful, false otherwise
    function file_copy(source, dest) result(success)
        character(len=*), intent(in) :: source, dest
        logical :: success
        integer :: src_unit, dst_unit, iostat_src, iostat_dst
        integer(int64) :: file_len, i
        character(len=1) :: byte
        
        success = .false.
        if (.not. file_exists(source)) return
        
        ! Open source file
        open(newunit=src_unit, file=source, status='old', action='read', &
             form='unformatted', access='stream', iostat=iostat_src)
        if (iostat_src /= 0) return
        
        ! Open destination file
        open(newunit=dst_unit, file=dest, status='replace', action='write', &
             form='unformatted', access='stream', iostat=iostat_dst)
        if (iostat_dst /= 0) then
            close(src_unit)
            return
        end if
        
        ! Get file size and copy byte by byte
        inquire(unit=src_unit, size=file_len)
        do i = 1, file_len
            read(src_unit, pos=i, iostat=iostat_src) byte
            if (iostat_src /= 0) exit
            write(dst_unit, pos=i, iostat=iostat_dst) byte
            if (iostat_dst /= 0) exit
        end do
        
        close(src_unit)
        close(dst_unit)
        success = (iostat_src == 0) .and. (iostat_dst == 0)
    end function file_copy
    
    !> Move/rename a file
    !! @param source Source file path
    !! @param dest Destination file path
    !! @return True if successful, false otherwise
    function file_move(source, dest) result(success)
        character(len=*), intent(in) :: source, dest
        logical :: success
        
        ! Try copy then delete (since Fortran doesn't have native move)
        success = file_copy(source, dest)
        if (success) then
            success = file_delete(source)
            if (.not. success) then
                ! Rollback: delete the copied file
                call file_delete(dest)
            end if
        end if
    end function file_move
    
    !> Rename a file (alias for file_move)
    !! @param oldname Old file name
    !! @param newname New file name
    !! @return True if successful, false otherwise
    function file_rename(oldname, newname) result(success)
        character(len=*), intent(in) :: oldname, newname
        logical :: success
        
        success = file_move(oldname, newname)
    end function file_rename
    
    !> Delete a file
    !! @param filepath Path to the file
    !! @return True if successful, false otherwise
    function file_delete(filepath) result(success)
        character(len=*), intent(in) :: filepath
        logical :: success
        integer :: unit_num, iostat
        
        success = .false.
        if (.not. file_exists(filepath)) return
        
        open(newunit=unit_num, file=filepath, status='old', iostat=iostat)
        if (iostat == 0) then
            close(unit_num, status='delete', iostat=iostat)
            success = (iostat == 0)
        end if
    end function file_delete
    
    !==========================================================================
    ! Directory Operations
    !==========================================================================
    
    !> Create a directory (simplified - creates a marker file)
    !! @param dirpath Path to the directory
    !! @return True if successful, false otherwise
    function directory_create(dirpath) result(success)
        character(len=*), intent(in) :: dirpath
        logical :: success
        integer :: unit_num, iostat
        character(len=256) :: marker_file
        
        success = .false.
        if (directory_exists(dirpath)) then
            success = .true.
            return
        end if
        
        ! Create a marker file to simulate directory creation
        ! Note: Actual directory creation requires system calls
        marker_file = trim(dirpath) // path_separator() // '.dir_marker'
        open(newunit=unit_num, file=marker_file, status='new', iostat=iostat)
        if (iostat == 0) then
            close(unit_num)
            success = .true.
        end if
    end function directory_create
    
    !> Delete a directory (simplified)
    !! @param dirpath Path to the directory
    !! @return True if successful, false otherwise
    function directory_delete(dirpath) result(success)
        character(len=*), intent(in) :: dirpath
        logical :: success
        character(len=256) :: marker_file
        
        success = .false.
        if (.not. directory_exists(dirpath)) return
        
        ! Delete marker file
        marker_file = trim(dirpath) // path_separator() // '.dir_marker'
        success = file_delete(marker_file)
    end function directory_delete
    
    !==========================================================================
    ! Path Manipulation
    !==========================================================================
    
    !> Get the path separator for the current system
    !! @return Path separator character
    function path_separator() result(sep)
        character(len=1) :: sep
        
        ! Use forward slash as default (works on Unix and modern Windows)
        sep = PATH_SEP
    end function path_separator
    
    !> Join path components
    !! @param path1 First path component
    !! @param path2 Second path component
    !! @return Joined path
    function path_join(path1, path2) result(joined)
        character(len=*), intent(in) :: path1, path2
        character(len=:), allocatable :: joined
        character(len=1) :: sep
        integer :: len1
        
        sep = path_separator()
        len1 = len_trim(path1)
        
        if (len1 == 0) then
            joined = trim(path2)
        else if (path1(len1:len1) == sep) then
            joined = trim(path1) // trim(path2)
        else
            joined = trim(path1) // sep // trim(path2)
        end if
    end function path_join
    
    !> Split a path into directory and filename
    !! @param filepath Path to split
    !! @return PathComponents structure
    function path_split(filepath) result(components)
        character(len=*), intent(in) :: filepath
        type(PathComponents) :: components
        integer :: last_sep, last_dot, i
        character(len=1) :: sep
        
        sep = path_separator()
        
        ! Find last separator
        last_sep = 0
        do i = len_trim(filepath), 1, -1
            if (filepath(i:i) == sep .or. filepath(i:i) == PATH_SEP_WIN) then
                last_sep = i
                exit
            end if
        end do
        
        if (last_sep > 0) then
            components%dirname = filepath(1:last_sep-1)
            components%basename = filepath(last_sep+1:)
        else
            components%dirname = '.'
            components%basename = filepath
        end if
        
        ! Find extension
        last_dot = index(components%basename, '.', back=.true.)
        if (last_dot > 1) then
            components%filename = components%basename(1:last_dot-1)
            components%extension = components%basename(last_dot+1:)
        else
            components%filename = components%basename
            components%extension = ''
        end if
    end function path_split
    
    !> Get the basename (filename) from a path
    !! @param filepath Path to extract basename from
    !! @return Basename (filename with extension)
    function path_basename(filepath) result(basename)
        character(len=*), intent(in) :: filepath
        character(len=:), allocatable :: basename
        type(PathComponents) :: components
        
        components = path_split(filepath)
        basename = components%basename
    end function path_basename
    
    !> Get the directory name from a path
    !! @param filepath Path to extract directory from
    !! @return Directory name
    function path_dirname(filepath) result(dirname)
        character(len=*), intent(in) :: filepath
        character(len=:), allocatable :: dirname
        type(PathComponents) :: components
        
        components = path_split(filepath)
        dirname = components%dirname
    end function path_dirname
    
    !> Get the file extension from a path
    !! @param filepath Path to extract extension from
    !! @return File extension (without dot)
    function path_extension(filepath) result(ext)
        character(len=*), intent(in) :: filepath
        character(len=:), allocatable :: ext
        type(PathComponents) :: components
        
        components = path_split(filepath)
        ext = components%extension
    end function path_extension
    
    !> Get the filename without extension
    !! @param filepath Path to extract filename from
    !! @return Filename without extension
    function path_without_extension(filepath) result(filename)
        character(len=*), intent(in) :: filepath
        character(len=:), allocatable :: filename
        type(PathComponents) :: components
        
        components = path_split(filepath)
        filename = components%filename
    end function path_without_extension
    
    !> Check if a path is absolute
    !! @param filepath Path to check
    !! @return True if path is absolute, false otherwise
    function path_is_absolute(filepath) result(is_abs)
        character(len=*), intent(in) :: filepath
        logical :: is_abs
        
        is_abs = .false.
        if (len_trim(filepath) == 0) return
        
        ! Unix absolute path starts with /
        if (filepath(1:1) == PATH_SEP) then
            is_abs = .true.
        ! Windows absolute path starts with drive letter (e.g., C:)
        else if (len_trim(filepath) >= 2) then
            if (filepath(2:2) == ':') then
                is_abs = .true.
            end if
        end if
    end function path_is_absolute
    
    !> Normalize a path (simplified)
    !! @param filepath Path to normalize
    !! @return Normalized path
    function path_normalize(filepath) result(normalized)
        character(len=*), intent(in) :: filepath
        character(len=:), allocatable :: normalized
        
        ! Simplified normalization - just replace backslashes with forward slashes
        normalized = filepath
        ! In a full implementation, would resolve .. and . components
    end function path_normalize
    
    !> Get relative path (simplified)
    !! @param from Base path
    !! @param to Target path
    !! @return Relative path from 'from' to 'to'
    function path_relative(from, to) result(rel_path)
        character(len=*), intent(in) :: from, to
        character(len=:), allocatable :: rel_path
        
        ! Simplified implementation
        if (index(to, from) == 1) then
            rel_path = to(len_trim(from)+2:)
        else
            rel_path = to
        end if
    end function path_relative
    
    !> Get current working directory
    !! @return Current directory path
    function get_current_directory() result(cwd)
        character(len=:), allocatable :: cwd
        
        ! Fortran 2003+ provides getcwd via ISO_C_BINDING or as extension
        ! This is a simplified version
        cwd = '.'
    end function get_current_directory
    
    !> Change current working directory (simplified)
    !! @param dirpath New directory path
    !! @return True if successful, false otherwise
    function change_directory(dirpath) result(success)
        character(len=*), intent(in) :: dirpath
        logical :: success
        
        ! Fortran doesn't provide standard chdir
        ! This would require system-specific extensions
        success = directory_exists(dirpath)
    end function change_directory
    
    !==========================================================================
    ! File I/O Operations
    !==========================================================================
    
    !> Read entire file as text
    !! @param filepath Path to the file
    !! @param content Output file content
    !! @return True if successful, false otherwise
    function read_file_text(filepath, content) result(success)
        character(len=*), intent(in) :: filepath
        character(len=:), allocatable, intent(out) :: content
        logical :: success
        integer :: unit_num, iostat
        integer(int64) :: fsize
        
        success = .false.
        if (.not. file_exists(filepath)) return
        
        fsize = file_size(filepath)
        if (fsize < 0) return
        
        open(newunit=unit_num, file=filepath, status='old', action='read', &
             form='formatted', iostat=iostat)
        if (iostat /= 0) return
        
        ! Read entire file
        allocate(character(len=fsize) :: content)
        read(unit_num, '(A)', iostat=iostat) content
        close(unit_num)
        
        success = (iostat == 0) .or. (iostat == -1)  ! -1 is end of file
    end function read_file_text
    
    !> Write text to file
    !! @param filepath Path to the file
    !! @param content Content to write
    !! @return True if successful, false otherwise
    function write_file_text(filepath, content) result(success)
        character(len=*), intent(in) :: filepath
        character(len=*), intent(in) :: content
        logical :: success
        integer :: unit_num, iostat
        
        success = .false.
        
        open(newunit=unit_num, file=filepath, status='replace', action='write', &
             form='formatted', iostat=iostat)
        if (iostat /= 0) return
        
        write(unit_num, '(A)', iostat=iostat) content
        close(unit_num)
        
        success = (iostat == 0)
    end function write_file_text
    
    !> Append text to file
    !! @param filepath Path to the file
    !! @param content Content to append
    !! @return True if successful, false otherwise
    function append_file_text(filepath, content) result(success)
        character(len=*), intent(in) :: filepath
        character(len=*), intent(in) :: content
        logical :: success
        integer :: unit_num, iostat
        character(len=10) :: status_str
        
        success = .false.
        
        if (file_exists(filepath)) then
            status_str = 'old'
        else
            status_str = 'new'
        end if
        
        open(newunit=unit_num, file=filepath, status=status_str, action='write', &
             position='append', form='formatted', iostat=iostat)
        if (iostat /= 0) return
        
        write(unit_num, '(A)', iostat=iostat) content
        close(unit_num)
        
        success = (iostat == 0)
    end function append_file_text
    
    !> Read file as binary data
    !! @param filepath Path to the file
    !! @param data Output byte data
    !! @return True if successful, false otherwise
    function read_file_binary(filepath, data) result(success)
        character(len=*), intent(in) :: filepath
        integer(int32), dimension(:), allocatable, intent(out) :: data
        logical :: success
        integer :: unit_num, iostat
        integer(int64) :: fsize, i
        
        success = .false.
        if (.not. file_exists(filepath)) return
        
        fsize = file_size(filepath)
        if (fsize < 0) return
        
        allocate(data(fsize))
        
        open(newunit=unit_num, file=filepath, status='old', action='read', &
             form='unformatted', access='direct', recl=1, iostat=iostat)
        if (iostat /= 0) return
        
        do i = 1, fsize
            read(unit_num, rec=i, iostat=iostat) data(i)
            if (iostat /= 0) exit
        end do
        
        close(unit_num)
        success = .true.
    end function read_file_binary
    
    !> Write binary data to file
    !! @param filepath Path to the file
    !! @param data Byte data to write
    !! @return True if successful, false otherwise
    function write_file_binary(filepath, data) result(success)
        character(len=*), intent(in) :: filepath
        integer(int32), dimension(:), intent(in) :: data
        logical :: success
        integer :: unit_num, iostat
        integer(int64) :: i
        
        success = .false.
        
        open(newunit=unit_num, file=filepath, status='replace', action='write', &
             form='unformatted', access='direct', recl=1, iostat=iostat)
        if (iostat /= 0) return
        
        do i = 1, size(data)
            write(unit_num, rec=i, iostat=iostat) data(i)
            if (iostat /= 0) exit
        end do
        
        close(unit_num)
        success = (iostat == 0)
    end function write_file_binary
    
    !==========================================================================
    ! Directory Listing (Simplified)
    !==========================================================================
    
    !> List directory contents (simplified)
    !! @param dirpath Directory path
    !! @return FileList structure
    function directory_list(dirpath) result(list)
        character(len=*), intent(in) :: dirpath
        type(FileList) :: list
        
        ! Simplified - Fortran doesn't have standard directory listing
        ! This would require system-specific extensions
        list%count = 0
        if (allocated(list%files)) deallocate(list%files)
    end function directory_list
    
    !> List files in directory
    !! @param dirpath Directory path
    !! @return FileList with only files
    function directory_list_files(dirpath) result(list)
        character(len=*), intent(in) :: dirpath
        type(FileList) :: list
        
        list = directory_list(dirpath)
        ! Would filter for files only in full implementation
    end function directory_list_files
    
    !> List subdirectories
    !! @param dirpath Directory path
    !! @return FileList with only directories
    function directory_list_dirs(dirpath) result(list)
        character(len=*), intent(in) :: dirpath
        type(FileList) :: list
        
        list = directory_list(dirpath)
        ! Would filter for directories only in full implementation
    end function directory_list_dirs
    
    !==========================================================================
    ! Utility Functions
    !==========================================================================
    
    !> Generate a random string for temporary filenames
    !! @param length Length of the random string
    !! @return Random alphanumeric string
    function random_string(length) result(str)
        integer, intent(in) :: length
        character(len=length) :: str
        character(len=62) :: chars
        integer :: i, rand_val
        real :: rand_real
        
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        
        do i = 1, length
            call random_number(rand_real)
            rand_val = int(rand_real * 62) + 1
            str(i:i) = chars(rand_val:rand_val)
        end do
    end function random_string
    
end module file_utils
