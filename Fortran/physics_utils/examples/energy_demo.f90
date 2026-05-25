!! Energy Conservation Demo
!! Demonstrates mechanical energy calculations

program energy_demo
    use physics_utils
    implicit none
    
    real(8) :: m, h0, v, ke, pe, total_e
    real(8) :: h1, v1, ke1, pe1, total_e1
    
    print *, "=========================================="
    print *, "   Energy Conservation Demo"
    print *, "=========================================="
    print *, ""
    
    ! Object falling from height
    m = 10.0d0   ! Mass: 10 kg
    h0 = 100.0d0  ! Initial height: 100 m
    v = 0.0d0    ! Initial velocity: 0 (starts from rest)
    
    print '(A, F5.1, A)', " Mass: ", m, " kg"
    print '(A, F6.1, A)', " Initial height: ", h0, " m"
    print '(A, F5.1, A)', " Initial velocity: ", v, " m/s"
    print *, ""
    
    ! Initial energy
    ke = kinetic_energy(m, v)
    pe = potential_energy(m, h0)
    total_e = mechanical_energy(m, v, h0)
    
    print *, "--- Initial Energy ---"
    print '(A, F10.2, A)', " Kinetic Energy: ", ke, " J"
    print '(A, F10.2, A)', " Potential Energy: ", pe, " J"
    print '(A, F10.2, A)', " Total Energy: ", total_e, " J"
    print *, ""
    
    ! After falling 50 meters
    h1 = 50.0d0
    v1 = kinematic_velocity_squared(0.0d0, GRAVITY, h0 - h1)
    
    ke1 = kinetic_energy(m, v1)
    pe1 = potential_energy(m, h1)
    total_e1 = mechanical_energy(m, v1, h1)
    
    print '(A, F6.1, A)', " After falling to height: ", h1, " m"
    print '(A, F6.2, A)', " Velocity: ", v1, " m/s"
    print *, ""
    
    print *, "--- Energy at 50m height ---"
    print '(A, F10.2, A)', " Kinetic Energy: ", ke1, " J"
    print '(A, F10.2, A)', " Potential Energy: ", pe1, " J"
    print '(A, F10.2, A)', " Total Energy: ", total_e1, " J"
    print *, ""
    
    print *, "Note: Total energy is conserved (ignoring air resistance)"
    print *, ""

end program energy_demo