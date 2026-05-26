! hash_utils.f90 - Hash Table (Dictionary) Implementation in Fortran
! A zero-dependency hash table module for storing key-value pairs
! 
! Features:
! - String keys with string values
! - Automatic resizing
! - Linear probing collision resolution
! - FNV-1a hash function
! - CRUD operations (Create, Read, Update, Delete)
! - Iteration support
!
! Author: AllToolkit
! Date: 2026-05-26

module hash_utils
    implicit none
    private

    ! Constants
    integer, parameter, public :: HASH_SUCCESS = 0
    integer, parameter, public :: HASH_KEY_NOT_FOUND = -1
    integer, parameter, public :: HASH_TABLE_FULL = -2
    integer, parameter, public :: HASH_INVALID_INPUT = -3
    
    ! Default parameters
    integer, parameter :: DEFAULT_CAPACITY = 16
    integer, parameter :: MAX_LOAD_FACTOR_PERCENT = 70  ! Resize at 70% load
    real, parameter :: RESIZE_FACTOR = 2.0

    ! Hash entry states
    integer, parameter :: ENTRY_EMPTY = 0
    integer, parameter :: ENTRY_OCCUPIED = 1
    integer, parameter :: ENTRY_DELETED = 2

    ! Hash entry type
    type :: hash_entry
        character(len=:), allocatable :: key
        character(len=:), allocatable :: value
        integer :: state = ENTRY_EMPTY
    end type hash_entry

    ! Hash table type
    type, public :: hash_table
        private
        type(hash_entry), allocatable :: entries(:)
        integer :: count = 0
        integer :: deleted_count = 0
        integer :: capacity = 0
    contains
        procedure :: init => hash_table_init
        procedure :: destroy => hash_table_destroy
        procedure :: insert => hash_table_insert
        procedure :: get => hash_table_get
        procedure :: contains => hash_table_contains
        procedure :: remove => hash_table_remove
        procedure :: size => hash_table_size
        procedure :: is_empty => hash_table_is_empty
        procedure :: clear => hash_table_clear
        procedure :: keys => hash_table_keys
        procedure :: values => hash_table_values
        procedure :: load_factor => hash_table_load_factor
        procedure :: rehash => hash_table_rehash
        procedure :: get_capacity => hash_table_capacity
        procedure :: get_all_entries => hash_table_get_entries
        procedure :: to_string => hash_table_to_string
        procedure :: from_pairs => hash_table_from_pairs
        ! Private helper procedures
        procedure, private :: find_slot
        procedure, private :: should_resize
    end type hash_table

    ! Public procedures
    public :: fnv1a_hash
    public :: djb2_hash
    public :: combine_hash

contains

    !---------------------------------------------------------------------------
    ! FNV-1a hash function (Fowler–Noll–Vo)
    ! Returns a 32-bit hash value
    !---------------------------------------------------------------------------
    function fnv1a_hash(str) result(hash)
        character(len=*), intent(in) :: str
        integer :: hash
        integer :: i
        integer, parameter :: FNV_PRIME = int(Z'01000193')
        integer, parameter :: FNV_OFFSET = int(Z'811c9dc5')
        
        hash = FNV_OFFSET
        do i = 1, len_trim(str)
            hash = ieor(hash, iachar(str(i:i)))
            hash = iand(hash * FNV_PRIME, int(Z'FFFFFFFF'))
        end do
    end function fnv1a_hash

    !---------------------------------------------------------------------------
    ! DJB2 hash function by Dan Bernstein
    !---------------------------------------------------------------------------
    function djb2_hash(str) result(hash)
        character(len=*), intent(in) :: str
        integer :: hash
        integer :: i
        
        hash = 5381
        do i = 1, len_trim(str)
            hash = iand(hash * 33 + iachar(str(i:i)), int(Z'FFFFFFFF'))
        end do
    end function djb2_hash

    !---------------------------------------------------------------------------
    ! Combine two hash values
    !---------------------------------------------------------------------------
    function combine_hash(h1, h2) result(combined)
        integer, intent(in) :: h1, h2
        integer :: combined
        
        combined = ieor(ieor(h1, h2) * 31 + h1, h2)
        combined = iand(combined, int(Z'FFFFFFFF'))
    end function combine_hash

    !---------------------------------------------------------------------------
    ! Initialize hash table
    !---------------------------------------------------------------------------
    subroutine hash_table_init(this, initial_capacity)
        class(hash_table), intent(inout) :: this
        integer, intent(in), optional :: initial_capacity
        integer :: cap
        
        call this%destroy()
        
        cap = DEFAULT_CAPACITY
        if (present(initial_capacity)) then
            if (initial_capacity > 0) then
                cap = initial_capacity
            end if
        end if
        
        ! Round up to nearest power of 2
        cap = next_power_of_2(cap)
        
        allocate(this%entries(cap))
        this%capacity = cap
        this%count = 0
        this%deleted_count = 0
    end subroutine hash_table_init

    !---------------------------------------------------------------------------
    ! Destroy hash table and free memory
    !---------------------------------------------------------------------------
    subroutine hash_table_destroy(this)
        class(hash_table), intent(inout) :: this
        integer :: i
        
        if (allocated(this%entries)) then
            do i = 1, size(this%entries)
                if (allocated(this%entries(i)%key)) deallocate(this%entries(i)%key)
                if (allocated(this%entries(i)%value)) deallocate(this%entries(i)%value)
                this%entries(i)%state = ENTRY_EMPTY
            end do
            deallocate(this%entries)
        end if
        
        this%count = 0
        this%deleted_count = 0
        this%capacity = 0
    end subroutine hash_table_destroy

    !---------------------------------------------------------------------------
    ! Insert key-value pair
    !---------------------------------------------------------------------------
    subroutine hash_table_insert(this, key, value, status)
        class(hash_table), intent(inout) :: this
        character(len=*), intent(in) :: key
        character(len=*), intent(in) :: value
        integer, intent(out), optional :: status
        integer :: idx, stat
        
        stat = HASH_INVALID_INPUT
        if (len_trim(key) == 0) then
            if (present(status)) status = stat
            return
        end if
        
        ! Initialize if not done
        if (.not. allocated(this%entries)) then
            call this%init()
        end if
        
        ! Check if we need to resize
        if (this%should_resize()) then
            call this%rehash(this%capacity * 2)
        end if
        
        ! Find slot
        idx = this%find_slot(key)
        
        if (this%entries(idx)%state == ENTRY_OCCUPIED) then
            ! Update existing
            this%entries(idx)%value = trim(value)
        else
            ! Insert new
            this%entries(idx)%key = trim(key)
            this%entries(idx)%value = trim(value)
            this%entries(idx)%state = ENTRY_OCCUPIED
            this%count = this%count + 1
        end if
        
        stat = HASH_SUCCESS
        if (present(status)) status = stat
    end subroutine hash_table_insert

    !---------------------------------------------------------------------------
    ! Get value by key
    !---------------------------------------------------------------------------
    subroutine hash_table_get(this, key, value, status)
        class(hash_table), intent(inout) :: this
        character(len=*), intent(in) :: key
        character(len=:), allocatable, intent(out) :: value
        integer, intent(out), optional :: status
        integer :: idx, stat
        
        stat = HASH_KEY_NOT_FOUND
        value = ""
        
        if (len_trim(key) == 0) then
            stat = HASH_INVALID_INPUT
            if (present(status)) status = stat
            return
        end if
        
        if (.not. allocated(this%entries)) then
            if (present(status)) status = stat
            return
        end if
        
        idx = this%find_slot(key)
        
        if (this%entries(idx)%state == ENTRY_OCCUPIED .and. &
            this%entries(idx)%key == trim(key)) then
            value = this%entries(idx)%value
            stat = HASH_SUCCESS
        end if
        
        if (present(status)) status = stat
    end subroutine hash_table_get

    !---------------------------------------------------------------------------
    ! Check if key exists
    !---------------------------------------------------------------------------
    function hash_table_contains(this, key) result(found)
        class(hash_table), intent(inout) :: this
        character(len=*), intent(in) :: key
        logical :: found
        integer :: idx
        
        found = .false.
        if (len_trim(key) == 0) return
        if (.not. allocated(this%entries)) return
        
        idx = this%find_slot(key)
        found = (this%entries(idx)%state == ENTRY_OCCUPIED .and. &
                 this%entries(idx)%key == trim(key))
    end function hash_table_contains

    !---------------------------------------------------------------------------
    ! Remove key-value pair
    !---------------------------------------------------------------------------
    subroutine hash_table_remove(this, key, status)
        class(hash_table), intent(inout) :: this
        character(len=*), intent(in) :: key
        integer, intent(out), optional :: status
        integer :: idx, stat
        
        stat = HASH_KEY_NOT_FOUND
        
        if (len_trim(key) == 0) then
            stat = HASH_INVALID_INPUT
            if (present(status)) status = stat
            return
        end if
        
        if (.not. allocated(this%entries)) then
            if (present(status)) status = stat
            return
        end if
        
        idx = this%find_slot(key)
        
        if (this%entries(idx)%state == ENTRY_OCCUPIED .and. &
            this%entries(idx)%key == trim(key)) then
            this%entries(idx)%state = ENTRY_DELETED
            this%count = this%count - 1
            this%deleted_count = this%deleted_count + 1
            stat = HASH_SUCCESS
            
            ! Rehash if too many deleted entries
            if (this%deleted_count > this%capacity / 4) then
                call this%rehash(this%capacity)
            end if
        end if
        
        if (present(status)) status = stat
    end subroutine hash_table_remove

    !---------------------------------------------------------------------------
    ! Get number of entries
    !---------------------------------------------------------------------------
    function hash_table_size(this) result(n)
        class(hash_table), intent(in) :: this
        integer :: n
        n = this%count
    end function hash_table_size

    !---------------------------------------------------------------------------
    ! Check if table is empty
    !---------------------------------------------------------------------------
    function hash_table_is_empty(this) result(empty)
        class(hash_table), intent(in) :: this
        logical :: empty
        empty = (this%count == 0)
    end function hash_table_is_empty

    !---------------------------------------------------------------------------
    ! Clear all entries
    !---------------------------------------------------------------------------
    subroutine hash_table_clear(this)
        class(hash_table), intent(inout) :: this
        integer :: i
        
        if (allocated(this%entries)) then
            do i = 1, size(this%entries)
                if (allocated(this%entries(i)%key)) deallocate(this%entries(i)%key)
                if (allocated(this%entries(i)%value)) deallocate(this%entries(i)%value)
                this%entries(i)%state = ENTRY_EMPTY
            end do
        end if
        
        this%count = 0
        this%deleted_count = 0
    end subroutine hash_table_clear

    !---------------------------------------------------------------------------
    ! Get all keys
    !---------------------------------------------------------------------------
    subroutine hash_table_keys(this, keys_array)
        class(hash_table), intent(in) :: this
        character(len=:), allocatable, intent(out) :: keys_array(:)
        integer :: i, j
        
        allocate(character(len=256) :: keys_array(this%count))
        j = 0
        
        if (allocated(this%entries)) then
            do i = 1, size(this%entries)
                if (this%entries(i)%state == ENTRY_OCCUPIED) then
                    j = j + 1
                    keys_array(j) = this%entries(i)%key
                end if
            end do
        end if
    end subroutine hash_table_keys

    !---------------------------------------------------------------------------
    ! Get all values
    !---------------------------------------------------------------------------
    subroutine hash_table_values(this, values_array)
        class(hash_table), intent(in) :: this
        character(len=:), allocatable, intent(out) :: values_array(:)
        integer :: i, j
        
        allocate(character(len=256) :: values_array(this%count))
        j = 0
        
        if (allocated(this%entries)) then
            do i = 1, size(this%entries)
                if (this%entries(i)%state == ENTRY_OCCUPIED) then
                    j = j + 1
                    values_array(j) = this%entries(i)%value
                end if
            end do
        end if
    end subroutine hash_table_values

    !---------------------------------------------------------------------------
    ! Get load factor (0-100%)
    !---------------------------------------------------------------------------
    function hash_table_load_factor(this) result(lf)
        class(hash_table), intent(in) :: this
        real :: lf
        
        if (this%capacity == 0) then
            lf = 0.0
        else
            lf = real(this%count + this%deleted_count) / real(this%capacity) * 100.0
        end if
    end function hash_table_load_factor

    !---------------------------------------------------------------------------
    ! Rehash with new capacity
    !---------------------------------------------------------------------------
    subroutine hash_table_rehash(this, new_capacity)
        class(hash_table), intent(inout) :: this
        integer, intent(in) :: new_capacity
        type(hash_entry), allocatable :: old_entries(:)
        integer :: i, old_size
        
        if (.not. allocated(this%entries)) then
            call this%init(new_capacity)
            return
        end if
        
        ! Save old entries
        call move_alloc(this%entries, old_entries)
        old_size = size(old_entries)
        
        ! Allocate new table
        allocate(this%entries(new_capacity))
        this%capacity = new_capacity
        this%count = 0
        this%deleted_count = 0
        
        ! Re-insert old entries
        do i = 1, old_size
            if (old_entries(i)%state == ENTRY_OCCUPIED) then
                call this%insert(old_entries(i)%key, old_entries(i)%value)
            end if
        end do
        
        ! Clean up old entries
        do i = 1, old_size
            if (allocated(old_entries(i)%key)) deallocate(old_entries(i)%key)
            if (allocated(old_entries(i)%value)) deallocate(old_entries(i)%value)
        end do
        deallocate(old_entries)
    end subroutine hash_table_rehash

    !---------------------------------------------------------------------------
    ! Get capacity
    !---------------------------------------------------------------------------
    function hash_table_capacity(this) result(cap)
        class(hash_table), intent(in) :: this
        integer :: cap
        cap = this%capacity
    end function hash_table_capacity

    !---------------------------------------------------------------------------
    ! Get all entries as formatted string
    !---------------------------------------------------------------------------
    subroutine hash_table_get_entries(this, entries_str)
        class(hash_table), intent(in) :: this
        character(len=:), allocatable, intent(out) :: entries_str(:)
        integer :: i, j
        
        allocate(character(len=512) :: entries_str(this%count))
        j = 0
        
        if (allocated(this%entries)) then
            do i = 1, size(this%entries)
                if (this%entries(i)%state == ENTRY_OCCUPIED) then
                    j = j + 1
                    entries_str(j) = trim(this%entries(i)%key) // " => " // &
                                     trim(this%entries(i)%value)
                end if
            end do
        end if
    end subroutine hash_table_get_entries

    !---------------------------------------------------------------------------
    ! Convert to string representation
    !---------------------------------------------------------------------------
    function hash_table_to_string(this) result(str)
        class(hash_table), intent(in) :: this
        character(len=:), allocatable :: str
        character(len=:), allocatable :: entries(:)
        character(len=4096) :: buffer
        integer :: i
        
        buffer = "{"
        
        if (this%count > 0) then
            call this%get_all_entries(entries)
            do i = 1, size(entries)
                if (i > 1) buffer = trim(buffer) // ", "
                buffer = trim(buffer) // trim(entries(i))
            end do
        end if
        
        buffer = trim(buffer) // "}"
        str = trim(buffer)
    end function hash_table_to_string

    !---------------------------------------------------------------------------
    ! Create hash table from key-value pairs
    !---------------------------------------------------------------------------
    subroutine hash_table_from_pairs(this, keys, values, n)
        class(hash_table), intent(inout) :: this
        character(len=*), intent(in) :: keys(:)
        character(len=*), intent(in) :: values(:)
        integer, intent(in) :: n
        integer :: i
        
        call this%init(n * 2)  ! Double size to reduce collisions
        
        do i = 1, n
            call this%insert(keys(i), values(i))
        end do
    end subroutine hash_table_from_pairs

    !---------------------------------------------------------------------------
    ! Helper: Find slot for a key (PRIVATE)
    !---------------------------------------------------------------------------
    function find_slot(this, key) result(idx)
        class(hash_table), intent(inout) :: this
        character(len=*), intent(in) :: key
        integer :: idx
        integer :: hash_val, i
        
        hash_val = fnv1a_hash(key)
        idx = iand(hash_val, this%capacity - 1) + 1  ! Fortran is 1-indexed
        
        ! Linear probing
        do i = 1, this%capacity
            if (this%entries(idx)%state == ENTRY_EMPTY) exit
            if (this%entries(idx)%state == ENTRY_OCCUPIED .and. &
                this%entries(idx)%key == trim(key)) exit
            
            idx = mod(idx, this%capacity) + 1
        end do
    end function find_slot

    !---------------------------------------------------------------------------
    ! Helper: Check if resize is needed (PRIVATE)
    !---------------------------------------------------------------------------
    function should_resize(this) result(needed)
        class(hash_table), intent(in) :: this
        logical :: needed
        
        needed = (this%load_factor() > real(MAX_LOAD_FACTOR_PERCENT))
    end function should_resize

    !---------------------------------------------------------------------------
    ! Helper: Get next power of 2
    !---------------------------------------------------------------------------
    function next_power_of_2(n) result(power)
        integer, intent(in) :: n
        integer :: power
        integer :: temp
        
        power = 1
        temp = n - 1
        do while (temp > 0)
            temp = ishft(temp, -1)
            power = ishft(power, 1)
        end do
        
        power = max(power, DEFAULT_CAPACITY)
    end function next_power_of_2

end module hash_utils