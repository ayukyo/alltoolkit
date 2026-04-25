! AllToolkit - Queue Utilities Example
! Demonstrates practical usage of queue data structures in Fortran

program queue_utils_example
    use queue_utils
    implicit none
    
    print *, "========================================"
    print *, "  Queue Utilities Examples"
    print *, "========================================"
    print *, ""
    
    call example_int_queue()
    call example_str_queue()
    call example_double_queue()
    call example_task_scheduler()
    
contains

    subroutine example_int_queue()
        type(int_queue_t) :: q
        integer :: val, i
        logical :: success
        
        print *, "Example 1: Integer Queue (Basic FIFO)"
        print *, "----------------------------------------"
        
        call int_queue_init(q)
        print *, "Created empty integer queue"
        
        print *, "Enqueuing values: 10, 20, 30, 40, 50"
        do i = 10, 50, 10
            call int_queue_enqueue(q, i)
        end do
        
        print *, "Queue size: ", int_queue_size(q)
        
        print *, "Dequeuing values (FIFO order):"
        do while (.not. int_queue_is_empty(q))
            success = int_queue_dequeue(q, val)
            if (success) print *, "  Dequeued: ", val
        end do
        
        call int_queue_destroy(q)
        print *, ""
    end subroutine example_int_queue
    
    subroutine example_str_queue()
        type(str_queue_t) :: q
        character(len=256) :: val
        logical :: success
        
        print *, "Example 2: String Queue (Message Buffer)"
        print *, "----------------------------------------"
        
        call str_queue_init(q)
        
        print *, "Adding messages to queue:"
        call str_queue_enqueue(q, "System initialized")
        call str_queue_enqueue(q, "User logged in")
        call str_queue_enqueue(q, "File uploaded successfully")
        call str_queue_enqueue(q, "Session ended")
        
        print *, "Messages in queue: ", str_queue_size(q)
        
        print *, "Processing messages:"
        do while (.not. str_queue_is_empty(q))
            success = str_queue_dequeue(q, val)
            if (success) print *, "  Processing: ", trim(val)
        end do
        
        call str_queue_destroy(q)
        print *, ""
    end subroutine example_str_queue
    
    subroutine example_double_queue()
        type(double_queue_t) :: q
        double precision :: val
        logical :: success
        double precision :: sum
        
        print *, "Example 3: Double Queue (Temperature Data)"
        print *, "----------------------------------------"
        
        call double_queue_init(q)
        
        print *, "Temperature readings (C):"
        call double_queue_enqueue(q, 23.5d0)
        call double_queue_enqueue(q, 24.1d0)
        call double_queue_enqueue(q, 25.8d0)
        call double_queue_enqueue(q, 26.3d0)
        call double_queue_enqueue(q, 24.9d0)
        
        sum = 0.0d0
        do while (.not. double_queue_is_empty(q))
            success = double_queue_dequeue(q, val)
            if (success) then
                print *, "  Reading: ", val
                sum = sum + val
            end if
        end do
        
        print *, "Average temperature: ", sum / 5.0d0
        
        call double_queue_destroy(q)
        print *, ""
    end subroutine example_double_queue
    
    subroutine example_task_scheduler()
        type(int_queue_t) :: task_ids
        type(str_queue_t) :: task_names
        integer :: task_id
        character(len=256) :: task_name
        logical :: success
        
        print *, "Example 4: Task Scheduler Simulation"
        print *, "----------------------------------------"
        
        call int_queue_init(task_ids)
        call str_queue_init(task_names)
        
        print *, "Adding tasks to scheduler:"
        
        call int_queue_enqueue(task_ids, 1)
        call str_queue_enqueue(task_names, "Initialize database")
        
        call int_queue_enqueue(task_ids, 2)
        call str_queue_enqueue(task_names, "Load configuration")
        
        call int_queue_enqueue(task_ids, 3)
        call str_queue_enqueue(task_names, "Start services")
        
        call int_queue_enqueue(task_ids, 4)
        call str_queue_enqueue(task_names, "Run diagnostics")
        
        call int_queue_enqueue(task_ids, 5)
        call str_queue_enqueue(task_names, "Complete startup")
        
        print *, "Tasks queued: ", int_queue_size(task_ids)
        
        print *, "Executing tasks:"
        do while (.not. int_queue_is_empty(task_ids))
            success = int_queue_dequeue(task_ids, task_id)
            success = str_queue_dequeue(task_names, task_name)
            if (success) then
                print *, task_id, ". ", trim(task_name)
            end if
        end do
        
        print *, "All tasks completed!"
        
        call int_queue_destroy(task_ids)
        call str_queue_destroy(task_names)
        print *, ""
    end subroutine example_task_scheduler

end program queue_utils_example