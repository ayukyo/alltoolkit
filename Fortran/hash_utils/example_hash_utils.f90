! example_hash_utils.f90 - Usage examples for hash_utils module
! Author: AllToolkit
! Date: 2026-05-26

program example_hash_utils
    use hash_utils
    implicit none
    
    print *, "========================================"
    print *, "  Hash Table Utils - Examples"
    print *, "========================================"
    print *, ""
    
    call example_basic_usage()
    call example_user_database()
    call example_word_counter()
    call example_config_parser()
    call example_hash_functions()
    
    print *, ""
    print *, "All examples completed!"

contains

    subroutine example_basic_usage()
        type(hash_table) :: table
        character(len=:), allocatable :: value
        integer :: status
        
        print *, "--- Example 1: Basic Usage ---"
        print *, ""
        
        ! Create and initialize
        call table%init()
        print *, "Created empty hash table"
        
        ! Insert key-value pairs
        call table%insert("name", "Alice")
        call table%insert("age", "30")
        call table%insert("city", "Tokyo")
        print *, "Inserted 3 entries"
        
        ! Get values
        call table%get("name", value, status)
        print *, "name: " // trim(value)
        
        call table%get("age", value, status)
        print *, "age: " // trim(value)
        
        call table%get("city", value, status)
        print *, "city: " // trim(value)
        
        ! Check if key exists
        print *, ""
        print *, "Contains 'name'? ", table%contains("name")
        print *, "Contains 'country'? ", table%contains("country")
        
        ! Update a value
        call table%insert("age", "31")
        call table%get("age", value, status)
        print *, ""
        print *, "Updated age: " // trim(value)
        
        ! Delete an entry
        call table%remove("city", status)
        print *, ""
        print *, "After removing 'city':"
        print *, "Size: ", table%size()
        print *, "Contains 'city'? ", table%contains("city")
        
        ! Show table as string
        print *, ""
        print *, "Table: " // table%to_string()
        
        ! Clean up
        call table%destroy()
        print *, ""
    end subroutine example_basic_usage

    subroutine example_user_database()
        type(hash_table) :: users
        character(len=:), allocatable :: value
        integer :: status
        
        print *, "--- Example 2: Simple User Database ---"
        print *, ""
        
        call users%init(32)  ! Pre-allocate for better performance
        
        ! Add users
        call users%insert("alice", "Alice Johnson|alice@example.com|Admin")
        call users%insert("bob", "Bob Smith|bob@example.com|User")
        call users%insert("charlie", "Charlie Brown|charlie@example.com|User")
        
        print *, "User Database Created"
        print *, "Number of users: ", users%size()
        print *, ""
        
        ! Look up user
        call users%get("bob", value, status)
        if (status == HASH_SUCCESS) then
            print *, "Found user 'bob':"
            print *, "  Data: " // trim(value)
        end if
        
        ! Remove user
        call users%remove("charlie", status)
        print *, ""
        print *, "After removing 'charlie':"
        print *, "Number of users: ", users%size()
        
        call users%destroy()
        print *, ""
    end subroutine example_user_database

    subroutine example_word_counter()
        type(hash_table) :: word_counts
        character(len=:), allocatable :: keys(:)
        character(len=:), allocatable :: value
        character(len=256) :: line, word
        character(len=32) :: count_str
        integer :: i, count, status, space_pos
        
        print *, "--- Example 3: Word Counter ---"
        print *, ""
        
        call word_counts%init()
        
        ! Simulate counting words from text
        line = "the quick brown fox jumps over the lazy dog the fox was quick"
        
        print *, "Input text:"
        print *, "  " // trim(line)
        print *, ""
        
        ! Simple word counting (splitting by spaces)
        do while (len_trim(line) > 0)
            ! Get next word
            space_pos = index(line, " ")
            if (space_pos == 0) then
                word = trim(line)
                line = ""
            else
                word = trim(line(1:space_pos-1))
                line = adjustl(line(space_pos+1:))
            end if
            
            if (len_trim(word) == 0) cycle
            
            ! Update count
            call word_counts%get(word, value, status)
            if (status == HASH_SUCCESS) then
                read(value, *) count
                count = count + 1
            else
                count = 1
            end if
            write(count_str, '(I0)') count
            call word_counts%insert(word, trim(count_str))
        end do
        
        ! Display results
        print *, "Word frequencies:"
        call word_counts%keys(keys)
        do i = 1, size(keys)
            call word_counts%get(keys(i), value, status)
            print *, "  " // trim(keys(i)) // ": " // trim(value)
        end do
        
        print *, ""
        print *, "Unique words: ", word_counts%size()
        
        call word_counts%destroy()
        print *, ""
    end subroutine example_word_counter

    subroutine example_config_parser()
        type(hash_table) :: config
        character(len=:), allocatable :: value
        integer :: status
        
        print *, "--- Example 4: Configuration Parser ---"
        print *, ""
        
        call config%init()
        
        ! Simulate config file parsing
        call config%insert("server.host", "localhost")
        call config%insert("server.port", "8080")
        call config%insert("database.url", "postgresql://localhost/mydb")
        call config%insert("database.pool_size", "10")
        call config%insert("logging.level", "INFO")
        call config%insert("logging.file", "/var/log/app.log")
        
        print *, "Configuration loaded:"
        print '(A,F6.2,A)', "  Load factor: ", config%load_factor(), "%"
        print *, "  Capacity: ", config%get_capacity()
        print *, ""
        
        ! Access config values
        print *, "Server configuration:"
        call config%get("server.host", value, status)
        print *, "  Host: " // trim(value)
        call config%get("server.port", value, status)
        print *, "  Port: " // trim(value)
        
        print *, ""
        print *, "Database configuration:"
        call config%get("database.url", value, status)
        print *, "  URL: " // trim(value)
        call config%get("database.pool_size", value, status)
        print *, "  Pool Size: " // trim(value)
        
        print *, ""
        print *, "Full configuration:"
        print *, "  " // config%to_string()
        
        call config%destroy()
        print *, ""
    end subroutine example_config_parser

    subroutine example_hash_functions()
        integer :: h1, h2
        
        print *, "--- Example 5: Hash Functions ---"
        print *, ""
        
        ! FNV-1a hash
        h1 = fnv1a_hash("hello world")
        print *, "FNV-1a hash of 'hello world': ", h1
        
        h2 = fnv1a_hash("hello world!")
        print *, "FNV-1a hash of 'hello world!': ", h2
        print *, "Similar strings produce very different hashes"
        print *, ""
        
        ! DJB2 hash
        h1 = djb2_hash("password123")
        print *, "DJB2 hash of 'password123': ", h1
        
        h2 = djb2_hash("password124")
        print *, "DJB2 hash of 'password124': ", h2
        print *, ""
        
        ! Combine hashes
        h1 = fnv1a_hash("user_123")
        h2 = fnv1a_hash("session_456")
        print *, "Combined hash: ", combine_hash(h1, h2)
        
        print *, ""
    end subroutine example_hash_functions

end program example_hash_utils