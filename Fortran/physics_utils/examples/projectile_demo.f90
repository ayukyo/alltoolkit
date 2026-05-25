!! Projectile Motion Demo
!! Demonstrates projectile motion calculations

program projectile_demo
    use physics_utils
    implicit none
    
    real(8) :: v0, angle, vx, vy, h, t, r
    integer :: i
    
    print *, "=========================================="
    print *, "   Projectile Motion Analysis Demo"
    print *, "=========================================="
    print *, ""
    
    ! Sample projectile
    v0 = 50.0d0  ! Initial velocity: 50 m/s
    angle = 45.0d0  ! Launch angle: 45 degrees
    
    print '(A, F6.1, A)', " Initial velocity: ", v0, " m/s"
    print '(A, F5.1, A)', " Launch angle: ", angle, " degrees"
    print *, ""
    
    ! Calculate components
    vx = projectile_horizontal_velocity(v0, angle)
    vy = projectile_vertical_velocity(v0, angle)
    
    print '(A, F6.2, A)', " Horizontal component: ", vx, " m/s"
    print '(A, F6.2, A)', " Vertical component: ", vy, " m/s"
    print *, ""
    
    ! Calculate trajectory parameters
    h = projectile_max_height(v0, angle)
    t = projectile_time_of_flight(v0, angle)
    r = projectile_range(v0, angle)
    
    print '(A, F7.2, A)', " Maximum height: ", h, " m"
    print '(A, F6.2, A)', " Time of flight: ", t, " s"
    print '(A, F8.2, A)', " Horizontal range: ", r, " m"
    print *, ""
    
    ! Compare different angles
    print *, "--- Range vs Launch Angle ---"
    print *, ""
    do i = 15, 75, 15
        r = projectile_range(v0, real(i, 8))
        print '(A, I3, A, F8.2, A)', " Angle ", i, "°: Range = ", r, " m"
    end do
    print *, ""
    print *, "Note: Maximum range achieved at 45 degrees (for flat ground)"
    print *, ""

end program projectile_demo