!! Test program for physics_utils module
!! Tests all physics calculation functions

program physics_utils_test
    use physics_utils
    implicit none
    
    logical :: all_passed
    integer :: test_count, pass_count
    real(8) :: tolerance
    
    tolerance = 1.0d-6
    all_passed = .true.
    test_count = 0
    pass_count = 0
    
    print *, "=========================================="
    print *, "  Physics Utilities Test Suite"
    print *, "=========================================="
    print *, ""
    
    ! Test Kinematics
    call test_kinematics()
    
    ! Test Dynamics
    call test_dynamics()
    
    ! Test Energy
    call test_energy()
    
    ! Test Circular Motion
    call test_circular_motion()
    
    ! Test Projectile Motion
    call test_projectile_motion()
    
    ! Test Waves
    call test_waves()
    
    ! Test Thermodynamics
    call test_thermodynamics()
    
    ! Test Fluid Mechanics
    call test_fluid_mechanics()
    
    ! Test Unit Conversions
    call test_unit_conversions()
    
    ! Test Simple Harmonic Motion
    call test_shm()
    
    ! Test Rotational Motion
    call test_rotational_motion()
    
    ! Test Gravitational Physics
    call test_gravitational()
    
    print *, ""
    print *, "=========================================="
    print *, "  Test Summary"
    print *, "=========================================="
    print *, ""
    print '(A, I0, A, I0, A)', " Tests run: ", test_count, ", Passed: ", pass_count, ""
    if (all_passed) then
        print *, " ALL TESTS PASSED!"
    else
        print *, " SOME TESTS FAILED!"
    end if
    print *, ""

contains

    subroutine assert_equal(actual, expected, test_name)
        real(8), intent(in) :: actual, expected
        character(len=*), intent(in) :: test_name
        test_count = test_count + 1
        if (abs(actual - expected) < tolerance) then
            pass_count = pass_count + 1
            print '(A, A)', " [PASS] ", test_name
        else
            all_passed = .false.
            print '(A, A)', " [FAIL] ", test_name
            print '(A, ES12.4, A, ES12.4)', "   Expected: ", expected, " Actual: ", actual
        end if
    end subroutine assert_equal
    
    subroutine assert_approx(actual, expected, test_name, tol)
        real(8), intent(in) :: actual, expected, tol
        character(len=*), intent(in) :: test_name
        test_count = test_count + 1
        if (abs(actual - expected) < tol) then
            pass_count = pass_count + 1
            print '(A, A)', " [PASS] ", test_name
        else
            all_passed = .false.
            print '(A, A)', " [FAIL] ", test_name
            print '(A, ES12.4, A, ES12.4)', "   Expected: ", expected, " Actual: ", actual
        end if
    end subroutine assert_approx

    subroutine test_kinematics()
        print *, "--- Kinematics Tests ---"
        
        ! Test displacement: s = v0*t + 0.5*a*t^2
        call assert_equal(kinematic_displacement(10.0d0, 5.0d0, 2.0d0), &
            10.0d0*5.0d0 + 0.5d0*2.0d0*25.0d0, "displacement calculation")
        
        ! Test velocity: v = v0 + a*t
        call assert_equal(kinematic_velocity(10.0d0, 2.0d0, 5.0d0), 20.0d0, "velocity from acceleration")
        
        ! Test velocity squared: v^2 = v0^2 + 2*a*s
        call assert_equal(kinematic_velocity_squared(10.0d0, 2.0d0, 75.0d0), 20.0d0, "velocity squared equation")
        
        ! Test average velocity
        call assert_equal(average_velocity(100.0d0, 10.0d0), 10.0d0, "average velocity")
        
        ! Test average speed
        call assert_equal(average_speed(100.0d0, 10.0d0), 10.0d0, "average speed")
    end subroutine test_kinematics
    
    subroutine test_dynamics()
        print *, "--- Dynamics Tests ---"
        
        ! Test Newton's second law: F = m*a
        call assert_equal(force_newton(10.0d0, 5.0d0), 50.0d0, "Newton's second law")
        
        ! Test weight: W = m*g
        call assert_equal(weight(10.0d0), 98.0665d0, "weight calculation")
        
        ! Test momentum: p = m*v
        call assert_equal(momentum(10.0d0, 5.0d0), 50.0d0, "momentum")
        
        ! Test impulse: J = F*t
        call assert_equal(impulse(10.0d0, 5.0d0), 50.0d0, "impulse")
        
        ! Test friction: F = μ*N
        call assert_equal(friction_force(0.5d0, 100.0d0), 50.0d0, "friction force")
        
        ! Test normal force on inclined plane
        call assert_approx(normal_force_inclined(10.0d0, 60.0d0), &
            10.0d0 * GRAVITY * 0.5d0, "normal force on inclined plane", 0.01d0)
    end subroutine test_dynamics
    
    subroutine test_energy()
        print *, "--- Energy Tests ---"
        
        ! Test kinetic energy: KE = 0.5*m*v^2
        call assert_equal(kinetic_energy(10.0d0, 5.0d0), 125.0d0, "kinetic energy")
        
        ! Test potential energy: PE = m*g*h
        call assert_equal(potential_energy(10.0d0, 5.0d0), 490.3325d0, "potential energy")
        
        ! Test elastic potential energy: PE = 0.5*k*x^2
        call assert_equal(elastic_potential_energy(100.0d0, 0.5d0), 12.5d0, "elastic potential energy")
        
        ! Test work: W = F*d
        call assert_equal(work(10.0d0, 5.0d0), 50.0d0, "work calculation")
        
        ! Test work with angle
        call assert_approx(work(10.0d0, 5.0d0, 60.0d0), 25.0d0, "work with 60 degree angle", 0.01d0)
        
        ! Test power: P = W/t
        call assert_equal(power_work(100.0d0, 10.0d0), 10.0d0, "power from work")
        
        ! Test power: P = F*v
        call assert_equal(power_force_velocity(10.0d0, 5.0d0), 50.0d0, "power from force velocity")
        
        ! Test mechanical energy
        call assert_equal(mechanical_energy(10.0d0, 5.0d0, 5.0d0), &
            kinetic_energy(10.0d0, 5.0d0) + potential_energy(10.0d0, 5.0d0), "mechanical energy")
    end subroutine test_energy
    
    subroutine test_circular_motion()
        print *, "--- Circular Motion Tests ---"
        
        ! Test centripetal acceleration: a = v^2/r
        call assert_equal(centripetal_acceleration(10.0d0, 5.0d0), 20.0d0, "centripetal acceleration")
        
        ! Test centripetal force: F = m*v^2/r
        call assert_equal(centripetal_force(10.0d0, 10.0d0, 5.0d0), 200.0d0, "centripetal force")
        
        ! Test angular velocity from linear
        call assert_equal(angular_velocity_from_linear(10.0d0, 5.0d0), 2.0d0, "angular velocity from linear")
        
        ! Test linear velocity from angular
        call assert_equal(linear_velocity_from_angular(2.0d0, 5.0d0), 10.0d0, "linear velocity from angular")
        
        ! Test angular velocity from frequency
        call assert_approx(angular_velocity_from_frequency(1.0d0), 2.0d0*PI, "angular velocity from frequency", 0.01d0)
        
        ! Test period from frequency
        call assert_equal(period_from_frequency(2.0d0), 0.5d0, "period from frequency")
        
        ! Test frequency from period
        call assert_equal(frequency_from_period(2.0d0), 0.5d0, "frequency from period")
    end subroutine test_circular_motion
    
    subroutine test_projectile_motion()
        print *, "--- Projectile Motion Tests ---"
        
        ! Test horizontal velocity component
        call assert_approx(projectile_horizontal_velocity(100.0d0, 45.0d0), &
            100.0d0 * 0.7071067811865d0, "horizontal velocity", 0.1d0)
        
        ! Test vertical velocity component
        call assert_approx(projectile_vertical_velocity(100.0d0, 45.0d0), &
            100.0d0 * 0.7071067811865d0, "vertical velocity", 0.1d0)
        
        ! Test maximum height at 90 degrees (pure vertical)
        call assert_equal(projectile_max_height(10.0d0, 90.0d0), &
            100.0d0 / (2.0d0 * GRAVITY), "max height at 90 degrees")
        
        ! Test time of flight at 90 degrees
        call assert_equal(projectile_time_of_flight(10.0d0, 90.0d0), &
            20.0d0 / GRAVITY, "time of flight at 90 degrees")
    end subroutine test_projectile_motion
    
    subroutine test_waves()
        print *, "--- Wave Tests ---"
        
        ! Test wave velocity: v = f*λ
        call assert_equal(wave_velocity(10.0d0, 2.0d0), 20.0d0, "wave velocity")
        
        ! Test wavelength: λ = v/f
        call assert_equal(wavelength(20.0d0, 10.0d0), 2.0d0, "wavelength")
        
        ! Test frequency from wavelength
        call assert_equal(wave_frequency(20.0d0, 2.0d0), 10.0d0, "wave frequency")
        
        ! Test photon energy (using visible light ~500nm)
        call assert_approx(photon_energy(6.0d14), PLANCK_CONSTANT * 6.0d14, "photon energy", 1.0d-20)
    end subroutine test_waves
    
    subroutine test_thermodynamics()
        print *, "--- Thermodynamics Tests ---"
        
        ! Test heat transfer: Q = m*c*ΔT
        call assert_equal(heat_transfer(1.0d0, 4186.0d0, 10.0d0), 41860.0d0, "heat transfer (water)")
        
        ! Test temperature change
        call assert_equal(temperature_change(41860.0d0, 1.0d0, 4186.0d0), 10.0d0, "temperature change")
        
        ! Test linear expansion
        call assert_equal(linear_expansion(1.0d0, 1.2d-5, 100.0d0), 1.2d-3, "linear expansion")
        
        ! Test ideal gas pressure
        call assert_approx(ideal_gas_pressure(1.0d0, 273.15d0, 0.0224d0), &
            101325.0d0, "ideal gas pressure", 100.0d0)
        
        ! Test Celsius to Kelvin
        call assert_equal(celsius_to_kelvin(0.0d0), 273.15d0, "Celsius to Kelvin")
        
        ! Test Kelvin to Celsius
        call assert_equal(kelvin_to_celsius(273.15d0), 0.0d0, "Kelvin to Celsius")
        
        ! Test Fahrenheit to Celsius
        call assert_equal(fahrenheit_to_celsius(32.0d0), 0.0d0, "Fahrenheit to Celsius")
        
        ! Test Celsius to Fahrenheit
        call assert_equal(celsius_to_fahrenheit(0.0d0), 32.0d0, "Celsius to Fahrenheit")
    end subroutine test_thermodynamics
    
    subroutine test_fluid_mechanics()
        print *, "--- Fluid Mechanics Tests ---"
        
        ! Test pressure: P = F/A
        call assert_equal(pressure(100.0d0, 10.0d0), 10.0d0, "pressure calculation")
        
        ! Test hydrostatic pressure: P = ρ*g*h
        call assert_equal(hydrostatic_pressure(1000.0d0, 10.0d0), &
            1000.0d0 * GRAVITY * 10.0d0, "hydrostatic pressure")
        
        ! Test buoyant force
        call assert_equal(buoyant_force(1000.0d0, 0.5d0), &
            1000.0d0 * 0.5d0 * GRAVITY, "buoyant force")
        
        ! Test flow rate: Q = A*v
        call assert_equal(flow_rate(10.0d0, 5.0d0), 50.0d0, "flow rate")
    end subroutine test_fluid_mechanics
    
    subroutine test_unit_conversions()
        print *, "--- Unit Conversion Tests ---"
        
        ! Test degrees to radians
        call assert_approx(degrees_to_radians(180.0d0), PI, "degrees to radians", 0.01d0)
        
        ! Test radians to degrees
        call assert_approx(radians_to_degrees(PI), 180.0d0, "radians to degrees", 0.01d0)
        
        ! Test m/s to km/h
        call assert_equal(ms_to_kmh(10.0d0), 36.0d0, "m/s to km/h")
        
        ! Test km/h to m/s
        call assert_equal(kmh_to_ms(36.0d0), 10.0d0, "km/h to m/s")
        
        ! Test Joules to eV
        call assert_approx(joules_to_ev(ELECTRON_CHARGE), 1.0d0, "Joules to eV", 0.001d0)
        
        ! Test eV to Joules
        call assert_approx(ev_to_joules(1.0d0), ELECTRON_CHARGE, "eV to Joules", 1.0d-25)
        
        ! Test SI prefix
        call assert_equal(apply_si_prefix(1000.0d0, "kilo"), 1.0d0, "SI prefix kilo")
        call assert_equal(apply_si_prefix(1.0d0, "mega"), 1.0d-6, "SI prefix mega")
    end subroutine test_unit_conversions
    
    subroutine test_shm()
        print *, "--- Simple Harmonic Motion Tests ---"
        
        ! Test spring angular frequency
        call assert_approx(spring_angular_frequency(100.0d0, 1.0d0), 10.0d0, &
            "spring angular frequency", 0.01d0)
        
        ! Test spring period
        call assert_approx(spring_period(1.0d0, 100.0d0), 2.0d0*PI/10.0d0, &
            "spring period", 0.01d0)
        
        ! Test pendulum period
        call assert_approx(pendulum_period(1.0d0), 2.0d0*PI/sqrt(GRAVITY), &
            "pendulum period", 0.01d0)
    end subroutine test_shm
    
    subroutine test_rotational_motion()
        print *, "--- Rotational Motion Tests ---"
        
        ! Test rotational kinetic energy
        call assert_equal(rotational_kinetic_energy(10.0d0, 5.0d0), 125.0d0, &
            "rotational kinetic energy")
        
        ! Test angular momentum
        call assert_equal(angular_momentum(10.0d0, 5.0d0), 50.0d0, "angular momentum")
        
        ! Test torque (perpendicular)
        call assert_equal(torque(5.0d0, 10.0d0), 50.0d0, "torque perpendicular")
        
        ! Test moment of inertia cylinder
        call assert_equal(moment_of_inertia_cylinder(10.0d0, 2.0d0), 20.0d0, &
            "moment of inertia cylinder")
        
        ! Test moment of inertia sphere
        call assert_equal(moment_of_inertia_sphere(10.0d0, 2.0d0), 16.0d0, &
            "moment of inertia sphere")
        
        ! Test moment of inertia rod center
        call assert_equal(moment_of_inertia_rod_center(12.0d0, 6.0d0), 36.0d0, &
            "moment of inertia rod center")
        
        ! Test moment of inertia rod end
        call assert_equal(moment_of_inertia_rod_end(12.0d0, 6.0d0), 144.0d0, &
            "moment of inertia rod end")
    end subroutine test_rotational_motion
    
    subroutine test_gravitational()
        real(8), parameter :: G_const = 6.67430d-11
        real(8), parameter :: EARTH_MASS = 5.972d24
        real(8), parameter :: EARTH_RADIUS = 6.371d6
        
        print *, "--- Gravitational Tests ---"
        
        ! Test gravitational force
        call assert_approx(gravitational_force(1000.0d0, 1000.0d0, 1.0d0), &
            G_const * 1.0d6, "gravitational force", 1.0d-7)
        
        ! Test escape velocity (Earth)
        call assert_approx(escape_velocity(EARTH_MASS, EARTH_RADIUS), &
            11186.0d0, "Earth escape velocity", 100.0d0)
        
        ! Test orbital velocity
        call assert_approx(orbital_velocity(EARTH_MASS, EARTH_RADIUS), &
            7909.0d0, "Earth orbital velocity", 100.0d0)
    end subroutine test_gravitational

end program physics_utils_test