! AllToolkit - Fortran Queue Utilities Module
! Zero-dependency queue data structure utilities for Fortran 90/95/2003+
!
! Features:
! - Integer queue with dynamic resizing
! - String queue with dynamic resizing  
! - Double precision queue
! - Basic queue operations (enqueue, dequeue, peek, etc.)
!
! Author: AllToolkit Contributors
! License: MIT

module queue_utils
    implicit none
    
    ! Constants
    integer, parameter :: QUEUE_INITIAL_CAPACITY = 16
    integer, parameter :: QUEUE_MAX_STRING_LEN = 256
    
    ! Integer Queue Type
    type :: int_queue_t
        integer, dimension(:), allocatable :: data
        integer :: count = 0
        integer :: capacity = 0
    end type int_queue_t
    
    ! String Queue Type
    type :: str_queue_t
        character(len=QUEUE_MAX_STRING_LEN), dimension(:), allocatable :: data
        integer :: count = 0
        integer :: capacity = 0
    end type str_queue_t
    
    ! Double Precision Queue Type
    type :: double_queue_t
        double precision, dimension(:), allocatable :: data
        integer :: count = 0
        integer :: capacity = 0
    end type double_queue_t

contains

    !==========================================================================
    ! Integer Queue Functions
    !==========================================================================
    
    !> Initialize an integer queue
    subroutine int_queue_init(q, initial_capacity)
        type(int_queue_t), intent(out) :: q
        integer, intent(in), optional :: initial_capacity
        integer :: cap
        
        if (present(initial_capacity)) then
            cap = max(1, initial_capacity)
        else
            cap = QUEUE_INITIAL_CAPACITY
        end if
        
        allocate(q%data(cap))
        q%count = 0
        q%capacity = cap
    end subroutine int_queue_init
    
    !> Destroy an integer queue and free memory
    subroutine int_queue_destroy(q)
        type(int_queue_t), intent(inout) :: q
        
        if (allocated(q%data)) deallocate(q%data)
        q%count = 0
        q%capacity = 0
    end subroutine int_queue_destroy
    
    !> Add element to the rear of the queue
    subroutine int_queue_enqueue(q, value)
        type(int_queue_t), intent(inout) :: q
        integer, intent(in) :: value
        integer, dimension(:), allocatable :: temp
        integer :: new_cap, i
        
        ! Resize if needed
        if (q%count >= q%capacity) then
            new_cap = q%capacity * 2
            allocate(temp(new_cap))
            do i = 1, q%count
                temp(i) = q%data(i)
            end do
            deallocate(q%data)
            allocate(q%data(new_cap))
            do i = 1, q%count
                q%data(i) = temp(i)
            end do
            deallocate(temp)
            q%capacity = new_cap
        end if
        
        q%count = q%count + 1
        q%data(q%count) = value
    end subroutine int_queue_enqueue
    
    !> Remove and return element from the front of the queue
    function int_queue_dequeue(q, value) result(success)
        type(int_queue_t), intent(inout) :: q
        integer, intent(out) :: value
        logical :: success
        integer :: i
        
        if (q%count == 0) then
            success = .false.
            value = 0
            return
        end if
        
        value = q%data(1)
        
        ! Shift elements forward
        do i = 2, q%count
            q%data(i-1) = q%data(i)
        end do
        
        q%count = q%count - 1
        success = .true.
    end function int_queue_dequeue
    
    !> Peek at the front element without removing it
    function int_queue_peek(q, value) result(success)
        type(int_queue_t), intent(in) :: q
        integer, intent(out) :: value
        logical :: success
        
        if (q%count == 0) then
            success = .false.
            value = 0
            return
        end if
        
        value = q%data(1)
        success = .true.
    end function int_queue_peek
    
    !> Peek at the rear element without removing it
    function int_queue_peek_back(q, value) result(success)
        type(int_queue_t), intent(in) :: q
        integer, intent(out) :: value
        logical :: success
        
        if (q%count == 0) then
            success = .false.
            value = 0
            return
        end if
        
        value = q%data(q%count)
        success = .true.
    end function int_queue_peek_back
    
    !> Check if queue is empty
    function int_queue_is_empty(q) result(res)
        type(int_queue_t), intent(in) :: q
        logical :: res
        res = q%count == 0
    end function int_queue_is_empty
    
    !> Get number of elements in queue
    function int_queue_size(q) result(res)
        type(int_queue_t), intent(in) :: q
        integer :: res
        res = q%count
    end function int_queue_size
    
    !> Clear all elements from queue
    subroutine int_queue_clear(q)
        type(int_queue_t), intent(inout) :: q
        q%count = 0
    end subroutine int_queue_clear
    
    !> Check if queue contains a value
    function int_queue_contains(q, value) result(res)
        type(int_queue_t), intent(in) :: q
        integer, intent(in) :: value
        logical :: res
        integer :: i
        
        res = .false.
        do i = 1, q%count
            if (q%data(i) == value) then
                res = .true.
                return
            end if
        end do
    end function int_queue_contains
    
    !> Reverse the order of elements in queue
    subroutine int_queue_reverse(q)
        type(int_queue_t), intent(inout) :: q
        integer :: i, j, temp
        
        j = q%count
        do i = 1, q%count / 2
            temp = q%data(i)
            q%data(i) = q%data(j)
            q%data(j) = temp
            j = j - 1
        end do
    end subroutine int_queue_reverse
    
    !> Remove first occurrence of a value from queue
    function int_queue_remove(q, value) result(removed)
        type(int_queue_t), intent(inout) :: q
        integer, intent(in) :: value
        logical :: removed
        integer :: i, j
        
        removed = .false.
        
        do i = 1, q%count
            if (q%data(i) == value .and. .not. removed) then
                removed = .true.
                do j = i + 1, q%count
                    q%data(j-1) = q%data(j)
                end do
                q%count = q%count - 1
                return
            end if
        end do
    end function int_queue_remove
    
    !==========================================================================
    ! String Queue Functions
    !==========================================================================
    
    !> Initialize a string queue
    subroutine str_queue_init(q, initial_capacity)
        type(str_queue_t), intent(out) :: q
        integer, intent(in), optional :: initial_capacity
        integer :: cap
        
        if (present(initial_capacity)) then
            cap = max(1, initial_capacity)
        else
            cap = QUEUE_INITIAL_CAPACITY
        end if
        
        allocate(q%data(cap))
        q%count = 0
        q%capacity = cap
    end subroutine str_queue_init
    
    !> Destroy a string queue
    subroutine str_queue_destroy(q)
        type(str_queue_t), intent(inout) :: q
        
        if (allocated(q%data)) deallocate(q%data)
        q%count = 0
        q%capacity = 0
    end subroutine str_queue_destroy
    
    !> Add string to the rear of the queue
    subroutine str_queue_enqueue(q, value)
        type(str_queue_t), intent(inout) :: q
        character(len=*), intent(in) :: value
        character(len=QUEUE_MAX_STRING_LEN), dimension(:), allocatable :: temp
        integer :: new_cap, i
        
        if (q%count >= q%capacity) then
            new_cap = q%capacity * 2
            allocate(temp(new_cap))
            do i = 1, q%count
                temp(i) = q%data(i)
            end do
            deallocate(q%data)
            allocate(q%data(new_cap))
            do i = 1, q%count
                q%data(i) = temp(i)
            end do
            deallocate(temp)
            q%capacity = new_cap
        end if
        
        q%count = q%count + 1
        q%data(q%count) = value
    end subroutine str_queue_enqueue
    
    !> Remove and return string from the front of the queue
    function str_queue_dequeue(q, value) result(success)
        type(str_queue_t), intent(inout) :: q
        character(len=*), intent(out) :: value
        logical :: success
        integer :: i
        
        if (q%count == 0) then
            success = .false.
            value = ''
            return
        end if
        
        value = q%data(1)
        
        do i = 2, q%count
            q%data(i-1) = q%data(i)
        end do
        
        q%count = q%count - 1
        success = .true.
    end function str_queue_dequeue
    
    !> Peek at the front string
    function str_queue_peek(q, value) result(success)
        type(str_queue_t), intent(in) :: q
        character(len=*), intent(out) :: value
        logical :: success
        
        if (q%count == 0) then
            success = .false.
            value = ''
            return
        end if
        
        value = q%data(1)
        success = .true.
    end function str_queue_peek
    
    !> Peek at the rear string
    function str_queue_peek_back(q, value) result(success)
        type(str_queue_t), intent(in) :: q
        character(len=*), intent(out) :: value
        logical :: success
        
        if (q%count == 0) then
            success = .false.
            value = ''
            return
        end if
        
        value = q%data(q%count)
        success = .true.
    end function str_queue_peek_back
    
    !> Check if string queue is empty
    function str_queue_is_empty(q) result(res)
        type(str_queue_t), intent(in) :: q
        logical :: res
        res = q%count == 0
    end function str_queue_is_empty
    
    !> Get string queue size
    function str_queue_size(q) result(res)
        type(str_queue_t), intent(in) :: q
        integer :: res
        res = q%count
    end function str_queue_size
    
    !> Clear string queue
    subroutine str_queue_clear(q)
        type(str_queue_t), intent(inout) :: q
        q%count = 0
    end subroutine str_queue_clear
    
    !> Check if string queue contains a value
    function str_queue_contains(q, value) result(res)
        type(str_queue_t), intent(in) :: q
        character(len=*), intent(in) :: value
        logical :: res
        integer :: i
        
        res = .false.
        do i = 1, q%count
            if (trim(q%data(i)) == trim(value)) then
                res = .true.
                return
            end if
        end do
    end function str_queue_contains
    
    !> Reverse string queue
    subroutine str_queue_reverse(q)
        type(str_queue_t), intent(inout) :: q
        integer :: i, j
        character(len=QUEUE_MAX_STRING_LEN) :: temp
        
        j = q%count
        do i = 1, q%count / 2
            temp = q%data(i)
            q%data(i) = q%data(j)
            q%data(j) = temp
            j = j - 1
        end do
    end subroutine str_queue_reverse
    
    !> Remove first occurrence of a string
    function str_queue_remove(q, value) result(removed)
        type(str_queue_t), intent(inout) :: q
        character(len=*), intent(in) :: value
        logical :: removed
        integer :: i, j
        
        removed = .false.
        
        do i = 1, q%count
            if (trim(q%data(i)) == trim(value) .and. .not. removed) then
                removed = .true.
                do j = i + 1, q%count
                    q%data(j-1) = q%data(j)
                end do
                q%count = q%count - 1
                return
            end if
        end do
    end function str_queue_remove
    
    !==========================================================================
    ! Double Precision Queue Functions
    !==========================================================================
    
    !> Initialize a double precision queue
    subroutine double_queue_init(q, initial_capacity)
        type(double_queue_t), intent(out) :: q
        integer, intent(in), optional :: initial_capacity
        integer :: cap
        
        if (present(initial_capacity)) then
            cap = max(1, initial_capacity)
        else
            cap = QUEUE_INITIAL_CAPACITY
        end if
        
        allocate(q%data(cap))
        q%count = 0
        q%capacity = cap
    end subroutine double_queue_init
    
    !> Destroy a double queue
    subroutine double_queue_destroy(q)
        type(double_queue_t), intent(inout) :: q
        
        if (allocated(q%data)) deallocate(q%data)
        q%count = 0
        q%capacity = 0
    end subroutine double_queue_destroy
    
    !> Add double to the rear of the queue
    subroutine double_queue_enqueue(q, value)
        type(double_queue_t), intent(inout) :: q
        double precision, intent(in) :: value
        double precision, dimension(:), allocatable :: temp
        integer :: new_cap, i
        
        if (q%count >= q%capacity) then
            new_cap = q%capacity * 2
            allocate(temp(new_cap))
            do i = 1, q%count
                temp(i) = q%data(i)
            end do
            deallocate(q%data)
            allocate(q%data(new_cap))
            do i = 1, q%count
                q%data(i) = temp(i)
            end do
            deallocate(temp)
            q%capacity = new_cap
        end if
        
        q%count = q%count + 1
        q%data(q%count) = value
    end subroutine double_queue_enqueue
    
    !> Remove and return double from the front
    function double_queue_dequeue(q, value) result(success)
        type(double_queue_t), intent(inout) :: q
        double precision, intent(out) :: value
        logical :: success
        integer :: i
        
        if (q%count == 0) then
            success = .false.
            value = 0.0d0
            return
        end if
        
        value = q%data(1)
        
        do i = 2, q%count
            q%data(i-1) = q%data(i)
        end do
        
        q%count = q%count - 1
        success = .true.
    end function double_queue_dequeue
    
    !> Peek at front element
    function double_queue_peek(q, value) result(success)
        type(double_queue_t), intent(in) :: q
        double precision, intent(out) :: value
        logical :: success
        
        if (q%count == 0) then
            success = .false.
            value = 0.0d0
            return
        end if
        
        value = q%data(1)
        success = .true.
    end function double_queue_peek
    
    !> Peek at rear element
    function double_queue_peek_back(q, value) result(success)
        type(double_queue_t), intent(in) :: q
        double precision, intent(out) :: value
        logical :: success
        
        if (q%count == 0) then
            success = .false.
            value = 0.0d0
            return
        end if
        
        value = q%data(q%count)
        success = .true.
    end function double_queue_peek_back
    
    !> Check if queue is empty
    function double_queue_is_empty(q) result(res)
        type(double_queue_t), intent(in) :: q
        logical :: res
        res = q%count == 0
    end function double_queue_is_empty
    
    !> Get queue size
    function double_queue_size(q) result(res)
        type(double_queue_t), intent(in) :: q
        integer :: res
        res = q%count
    end function double_queue_size
    
    !> Clear queue
    subroutine double_queue_clear(q)
        type(double_queue_t), intent(inout) :: q
        q%count = 0
    end subroutine double_queue_clear
    
    !> Check if queue contains a value
    function double_queue_contains(q, value) result(res)
        type(double_queue_t), intent(in) :: q
        double precision, intent(in) :: value
        logical :: res
        integer :: i
        
        res = .false.
        do i = 1, q%count
            if (q%data(i) == value) then
                res = .true.
                return
            end if
        end do
    end function double_queue_contains
    
    !> Reverse queue order
    subroutine double_queue_reverse(q)
        type(double_queue_t), intent(inout) :: q
        integer :: i, j
        double precision :: temp
        
        j = q%count
        do i = 1, q%count / 2
            temp = q%data(i)
            q%data(i) = q%data(j)
            q%data(j) = temp
            j = j - 1
        end do
    end subroutine double_queue_reverse
    
    !> Remove first occurrence of value
    function double_queue_remove(q, value) result(removed)
        type(double_queue_t), intent(inout) :: q
        double precision, intent(in) :: value
        logical :: removed
        integer :: i, j
        
        removed = .false.
        
        do i = 1, q%count
            if (q%data(i) == value .and. .not. removed) then
                removed = .true.
                do j = i + 1, q%count
                    q%data(j-1) = q%data(j)
                end do
                q%count = q%count - 1
                return
            end if
        end do
    end function double_queue_remove

end module queue_utils