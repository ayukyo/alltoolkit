!! AllToolkit - Fortran Physics Utilities Module
!! Zero-dependency physics calculation functions for Fortran 90/95/2003+
!!
!! Features:
!! - Kinematics (displacement, velocity, acceleration)
!! - Dynamics (force, momentum, kinetic energy)
!! - Energy calculations (kinetic, potential, work)
!! - Thermodynamics basics (heat, specific heat)
!! - Wave formulas (frequency, wavelength)
!! - Unit conversions (SI prefixes, angle, temperature)
!! - Circular motion (centripetal force, angular velocity)
!! - Projectile motion (range, max height, time of flight)
!! - Gravitational calculations
!! - Fluid mechanics basics (pressure, buoyancy)
!!
!! Author: AllToolkit Contributors
!! License: MIT

module physics_utils
    implicit none
    
    !==========================================================================
    ! Physical Constants (SI Units)
    !==========================================================================
    real(8), parameter :: GRAVITY = 9.80665d0         ! Acceleration due to gravity (m/s^2)
    real(8), parameter :: SPEED_OF_LIGHT = 2.99792458d8  ! Speed of light (m/s)
    real(8), parameter :: PLANCK_CONSTANT = 6.62607015d-34  ! Planck constant (J·s)
    real(8), parameter :: BOLTZMANN = 1.380649d-23    ! Boltzmann constant (J/K)
    real(8), parameter :: AVOGADRO = 6.02214076d23    ! Avogadro's number (1/mol)
    real(8), parameter :: ELECTRON_MASS = 9.1093837d-31  ! Electron mass (kg)
    real(8), parameter :: PROTON_MASS = 1.6726219d-27  ! Proton mass (kg)
    real(8), parameter :: NEUTRON_MASS = 1.6749275d-27 ! Neutron mass (kg)
    real(8), parameter :: ELECTRON_CHARGE = 1.602176634d-19  ! Elementary charge (C)
    real(8), parameter :: VACUUM_PERMITTIVITY = 8.8541878128d-12  ! ε0 (F/m)
    real(8), parameter :: VACUUM_PERMEABILITY = 1.25663706212d-6  ! μ0 (H/m)
    real(8), parameter :: GAS_CONSTANT = 8.314462618d0  ! Universal gas constant (J/(mol·K))
    real(8), parameter :: STEFAN_BOLTZMANN = 5.670374419d-8  ! Stefan-Boltzmann constant (W/(m^2·K^4))
    real(8), parameter :: ATOMIC_MASS_UNIT = 1.66053906660d-27  ! Atomic mass unit (kg)
    
    ! PI constant for calculations
    real(8), parameter :: PI = 3.14159265358979323846d0
    
contains

    !==========================================================================
    ! Kinematics (Motion in One Dimension)
    !==========================================================================
    
    !> Calculate displacement using equation: s = v0*t + 0.5*a*t^2
    !! @param v0 Initial velocity (m/s)
    !! @param t Time (s)
    !! @param a Acceleration (m/s^2)
    !! @return Displacement (m)
    function kinematic_displacement(v0, t, a) result(s)
        real(8), intent(in) :: v0, t, a
        real(8) :: s
        s = v0 * t + 0.5d0 * a * t * t
    end function kinematic_displacement
    
    !> Calculate final velocity: v = v0 + a*t
    !! @param v0 Initial velocity (m/s)
    !! @param a Acceleration (m/s^2)
    !! @param t Time (s)
    !! @return Final velocity (m/s)
    function kinematic_velocity(v0, a, t) result(v)
        real(8), intent(in) :: v0, a, t
        real(8) :: v
        v = v0 + a * t
    end function kinematic_velocity
    
    !> Calculate velocity from displacement: v^2 = v0^2 + 2*a*s
    !! @param v0 Initial velocity (m/s)
    !! @param a Acceleration (m/s^2)
    !! @param s Displacement (m)
    !! @return Final velocity (m/s)
    function kinematic_velocity_squared(v0, a, s) result(v)
        real(8), intent(in) :: v0, a, s
        real(8) :: v
        real(8) :: v_squared
        v_squared = v0 * v0 + 2.0d0 * a * s
        if (v_squared >= 0.0d0) then
            v = sqrt(v_squared)
        else
            v = 0.0d0  ! Invalid case: imaginary velocity
        end if
    end function kinematic_velocity_squared
    
    !> Calculate average velocity
    !! @param s Displacement (m)
    !! @param t Time (s)
    !! @return Average velocity (m/s)
    function average_velocity(s, t) result(v_avg)
        real(8), intent(in) :: s, t
        real(8) :: v_avg
        if (t > 0.0d0) then
            v_avg = s / t
        else
            v_avg = 0.0d0
        end if
    end function average_velocity
    
    !> Calculate average speed (total distance over time)
    !! @param total_distance Total distance traveled (m)
    !! @param t Time (s)
    !! @return Average speed (m/s)
    function average_speed(total_distance, t) result(speed)
        real(8), intent(in) :: total_distance, t
        real(8) :: speed
        if (t > 0.0d0) then
            speed = total_distance / t
        else
            speed = 0.0d0
        end if
    end function average_speed
    
    !==========================================================================
    ! Dynamics (Forces and Motion)
    !==========================================================================
    
    !> Calculate force from Newton's second law: F = m*a
    !! @param m Mass (kg)
    !! @param a Acceleration (m/s^2)
    !! @return Force (N)
    function force_newton(m, a) result(f)
        real(8), intent(in) :: m, a
        real(8) :: f
        f = m * a
    end function force_newton
    
    !> Calculate weight (gravitational force): W = m*g
    !! @param m Mass (kg)
    !! @param g Gravitational acceleration (m/s^2), default is 9.80665
    !! @return Weight (N)
    function weight(m, g) result(w)
        real(8), intent(in) :: m
        real(8), intent(in), optional :: g
        real(8) :: w, g_val
        g_val = GRAVITY
        if (present(g)) g_val = g
        w = m * g_val
    end function weight
    
    !> Calculate momentum: p = m*v
    !! @param m Mass (kg)
    !! @param v Velocity (m/s)
    !! @return Momentum (kg·m/s)
    function momentum(m, v) result(p)
        real(8), intent(in) :: m, v
        real(8) :: p
        p = m * v
    end function momentum
    
    !> Calculate impulse: J = F*t = Δp
    !! @param force Force (N)
    !! @param time Time interval (s)
    !! @return Impulse (N·s or kg·m/s)
    function impulse(force, time) result(j)
        real(8), intent(in) :: force, time
        real(8) :: j
        j = force * time
    end function impulse
    
    !> Calculate friction force: F = μ*N
    !! @param mu Coefficient of friction
    !! @param normal_force Normal force (N)
    !! @return Friction force (N)
    function friction_force(mu, normal_force) result(f)
        real(8), intent(in) :: mu, normal_force
        real(8) :: f
        f = mu * normal_force
    end function friction_force
    
    !> Calculate normal force on inclined plane: N = m*g*cos(θ)
    !! @param m Mass (kg)
    !! @param angle_degrees Angle in degrees
    !! @param g Gravitational acceleration (m/s^2), optional
    !! @return Normal force (N)
    function normal_force_inclined(m, angle_degrees, g) result(n)
        real(8), intent(in) :: m, angle_degrees
        real(8), intent(in), optional :: g
        real(8) :: n, g_val, angle_rad
        g_val = GRAVITY
        if (present(g)) g_val = g
        angle_rad = angle_degrees * PI / 180.0d0
        n = m * g_val * cos(angle_rad)
    end function normal_force_inclined
    
    !==========================================================================
    ! Work, Energy, and Power
    !==========================================================================
    
    !> Calculate kinetic energy: KE = 0.5*m*v^2
    !! @param m Mass (kg)
    !! @param v Velocity (m/s)
    !! @return Kinetic energy (J)
    function kinetic_energy(m, v) result(ke)
        real(8), intent(in) :: m, v
        real(8) :: ke
        ke = 0.5d0 * m * v * v
    end function kinetic_energy
    
    !> Calculate gravitational potential energy: PE = m*g*h
    !! @param m Mass (kg)
    !! @param h Height (m)
    !! @param g Gravitational acceleration (m/s^2), optional
    !! @return Potential energy (J)
    function potential_energy(m, h, g) result(pe)
        real(8), intent(in) :: m, h
        real(8), intent(in), optional :: g
        real(8) :: pe, g_val
        g_val = GRAVITY
        if (present(g)) g_val = g
        pe = m * g_val * h
    end function potential_energy
    
    !> Calculate elastic potential energy: PE = 0.5*k*x^2
    !! @param k Spring constant (N/m)
    !! @param x Displacement from equilibrium (m)
    !! @return Elastic potential energy (J)
    function elastic_potential_energy(k, x) result(pe)
        real(8), intent(in) :: k, x
        real(8) :: pe
        pe = 0.5d0 * k * x * x
    end function elastic_potential_energy
    
    !> Calculate work: W = F*d*cos(θ)
    !! @param force Force (N)
    !! @param displacement Displacement (m)
    !! @param angle_degrees Angle between force and displacement (degrees), optional
    !! @return Work (J)
    function work(force, displacement, angle_degrees) result(w)
        real(8), intent(in) :: force, displacement
        real(8), intent(in), optional :: angle_degrees
        real(8) :: w, angle_rad, cos_angle
        cos_angle = 1.0d0
        if (present(angle_degrees)) then
            angle_rad = angle_degrees * PI / 180.0d0
            cos_angle = cos(angle_rad)
        end if
        w = force * displacement * cos_angle
    end function work
    
    !> Calculate power from work and time: P = W/t
    !! @param work_done Work (J)
    !! @param time Time (s)
    !! @return Power (W)
    function power_work(work_done, time) result(p)
        real(8), intent(in) :: work_done, time
        real(8) :: p
        if (time > 0.0d0) then
            p = work_done / time
        else
            p = 0.0d0
        end if
    end function power_work
    
    !> Calculate power from force and velocity: P = F*v
    !! @param force Force (N)
    !! @param velocity Velocity (m/s)
    !! @return Power (W)
    function power_force_velocity(force, velocity) result(p)
        real(8), intent(in) :: force, velocity
        real(8) :: p
        p = force * velocity
    end function power_force_velocity
    
    !> Calculate mechanical energy (KE + PE)
    !! @param m Mass (kg)
    !! @param v Velocity (m/s)
    !! @param h Height (m)
    !! @param g Gravitational acceleration (m/s^2), optional
    !! @return Total mechanical energy (J)
    function mechanical_energy(m, v, h, g) result(e)
        real(8), intent(in) :: m, v, h
        real(8), intent(in), optional :: g
        real(8) :: e
        e = kinetic_energy(m, v) + potential_energy(m, h, g)
    end function mechanical_energy
    
    !==========================================================================
    ! Circular Motion
    !==========================================================================
    
    !> Calculate centripetal acceleration: a = v^2/r
    !! @param v Velocity (m/s)
    !! @param r Radius (m)
    !! @return Centripetal acceleration (m/s^2)
    function centripetal_acceleration(v, r) result(a)
        real(8), intent(in) :: v, r
        real(8) :: a
        if (r > 0.0d0) then
            a = v * v / r
        else
            a = 0.0d0
        end if
    end function centripetal_acceleration
    
    !> Calculate centripetal force: F = m*v^2/r
    !! @param m Mass (kg)
    !! @param v Velocity (m/s)
    !! @param r Radius (m)
    !! @return Centripetal force (N)
    function centripetal_force(m, v, r) result(f)
        real(8), intent(in) :: m, v, r
        real(8) :: f
        if (r > 0.0d0) then
            f = m * v * v / r
        else
            f = 0.0d0
        end if
    end function centripetal_force
    
    !> Calculate angular velocity from linear velocity: ω = v/r
    !! @param v Linear velocity (m/s)
    !! @param r Radius (m)
    !! @return Angular velocity (rad/s)
    function angular_velocity_from_linear(v, r) result(omega)
        real(8), intent(in) :: v, r
        real(8) :: omega
        if (r > 0.0d0) then
            omega = v / r
        else
            omega = 0.0d0
        end if
    end function angular_velocity_from_linear
    
    !> Calculate linear velocity from angular velocity: v = ω*r
    !! @param omega Angular velocity (rad/s)
    !! @param r Radius (m)
    !! @return Linear velocity (m/s)
    function linear_velocity_from_angular(omega, r) result(v)
        real(8), intent(in) :: omega, r
        real(8) :: v
        v = omega * r
    end function linear_velocity_from_angular
    
    !> Calculate angular velocity from frequency: ω = 2*π*f
    !! @param frequency Frequency (Hz)
    !! @return Angular velocity (rad/s)
    function angular_velocity_from_frequency(frequency) result(omega)
        real(8), intent(in) :: frequency
        real(8) :: omega
        omega = 2.0d0 * PI * frequency
    end function angular_velocity_from_frequency
    
    !> Calculate period from frequency: T = 1/f
    !! @param frequency Frequency (Hz)
    !! @return Period (s)
    function period_from_frequency(frequency) result(t)
        real(8), intent(in) :: frequency
        real(8) :: t
        if (frequency > 0.0d0) then
            t = 1.0d0 / frequency
        else
            t = 0.0d0
        end if
    end function period_from_frequency
    
    !> Calculate frequency from period: f = 1/T
    !! @param period Period (s)
    !! @return Frequency (Hz)
    function frequency_from_period(period) result(f)
        real(8), intent(in) :: period
        real(8) :: f
        if (period > 0.0d0) then
            f = 1.0d0 / period
        else
            f = 0.0d0
        end if
    end function frequency_from_period
    
    !==========================================================================
    ! Projectile Motion
    !==========================================================================
    
    !> Calculate horizontal range of projectile: R = v0^2*sin(2θ)/g
    !! @param v0 Initial velocity (m/s)
    !! @param angle_degrees Launch angle (degrees)
    !! @param g Gravitational acceleration (m/s^2), optional
    !! @return Horizontal range (m)
    function projectile_range(v0, angle_degrees, g) result(r)
        real(8), intent(in) :: v0, angle_degrees
        real(8), intent(in), optional :: g
        real(8) :: r, g_val, angle_rad
        g_val = GRAVITY
        if (present(g)) g_val = g
        angle_rad = angle_degrees * PI / 180.0d0
        r = v0 * v0 * sin(2.0d0 * angle_rad) / g_val
    end function projectile_range
    
    !> Calculate maximum height of projectile: H = v0^2*sin^2(θ)/(2g)
    !! @param v0 Initial velocity (m/s)
    !! @param angle_degrees Launch angle (degrees)
    !! @param g Gravitational acceleration (m/s^2), optional
    !! @return Maximum height (m)
    function projectile_max_height(v0, angle_degrees, g) result(h)
        real(8), intent(in) :: v0, angle_degrees
        real(8), intent(in), optional :: g
        real(8) :: h, g_val, angle_rad
        g_val = GRAVITY
        if (present(g)) g_val = g
        angle_rad = angle_degrees * PI / 180.0d0
        h = v0 * v0 * sin(angle_rad) ** 2 / (2.0d0 * g_val)
    end function projectile_max_height
    
    !> Calculate time of flight for projectile: T = 2*v0*sin(θ)/g
    !! @param v0 Initial velocity (m/s)
    !! @param angle_degrees Launch angle (degrees)
    !! @param g Gravitational acceleration (m/s^2), optional
    !! @return Time of flight (s)
    function projectile_time_of_flight(v0, angle_degrees, g) result(t)
        real(8), intent(in) :: v0, angle_degrees
        real(8), intent(in), optional :: g
        real(8) :: t, g_val, angle_rad
        g_val = GRAVITY
        if (present(g)) g_val = g
        angle_rad = angle_degrees * PI / 180.0d0
        t = 2.0d0 * v0 * sin(angle_rad) / g_val
    end function projectile_time_of_flight
    
    !> Calculate horizontal velocity component
    !! @param v0 Initial velocity (m/s)
    !! @param angle_degrees Launch angle (degrees)
    !! @return Horizontal velocity (m/s)
    function projectile_horizontal_velocity(v0, angle_degrees) result(vx)
        real(8), intent(in) :: v0, angle_degrees
        real(8) :: vx, angle_rad
        angle_rad = angle_degrees * PI / 180.0d0
        vx = v0 * cos(angle_rad)
    end function projectile_horizontal_velocity
    
    !> Calculate vertical velocity component
    !! @param v0 Initial velocity (m/s)
    !! @param angle_degrees Launch angle (degrees)
    !! @return Vertical velocity (m/s)
    function projectile_vertical_velocity(v0, angle_degrees) result(vy)
        real(8), intent(in) :: v0, angle_degrees
        real(8) :: vy, angle_rad
        angle_rad = angle_degrees * PI / 180.0d0
        vy = v0 * sin(angle_rad)
    end function projectile_vertical_velocity
    
    !==========================================================================
    ! Gravitational Physics
    !==========================================================================
    
    !> Calculate gravitational force between two masses: F = G*m1*m2/r^2
    !! @param m1 First mass (kg)
    !! @param m2 Second mass (kg)
    !! @param r Distance between centers (m)
    !! @return Gravitational force (N)
    function gravitational_force(m1, m2, r) result(f)
        real(8), intent(in) :: m1, m2, r
        real(8) :: f
        real(8), parameter :: G = 6.67430d-11  ! Gravitational constant
        if (r > 0.0d0) then
            f = G * m1 * m2 / (r * r)
        else
            f = 0.0d0
        end if
    end function gravitational_force
    
    !> Calculate gravitational potential energy: PE = -G*m1*m2/r
    !! @param m1 First mass (kg)
    !! @param m2 Second mass (kg)
    !! @param r Distance between centers (m)
    !! @return Gravitational potential energy (J), negative
    function gravitational_potential_energy(m1, m2, r) result(pe)
        real(8), intent(in) :: m1, m2, r
        real(8) :: pe
        real(8), parameter :: G = 6.67430d-11
        if (r > 0.0d0) then
            pe = -G * m1 * m2 / r
        else
            pe = 0.0d0
        end if
    end function gravitational_potential_energy
    
    !> Calculate escape velocity: v = sqrt(2*G*M/r)
    !! @param m Mass of planet/body (kg)
    !! @param r Radius from center (m)
    !! @return Escape velocity (m/s)
    function escape_velocity(m, r) result(v)
        real(8), intent(in) :: m, r
        real(8) :: v
        real(8), parameter :: G = 6.67430d-11
        if (r > 0.0d0) then
            v = sqrt(2.0d0 * G * m / r)
        else
            v = 0.0d0
        end if
    end function escape_velocity
    
    !> Calculate orbital velocity: v = sqrt(G*M/r)
    !! @param m Mass of central body (kg)
    !! @param r Orbital radius (m)
    !! @return Orbital velocity (m/s)
    function orbital_velocity(m, r) result(v)
        real(8), intent(in) :: m, r
        real(8) :: v
        real(8), parameter :: G = 6.67430d-11
        if (r > 0.0d0) then
            v = sqrt(G * m / r)
        else
            v = 0.0d0
        end if
    end function orbital_velocity
    
    !==========================================================================
    ! Waves
    !==========================================================================
    
    !> Calculate wave velocity: v = f*λ
    !! @param frequency Frequency (Hz)
    !! @param wavelength Wavelength (m)
    !! @return Wave velocity (m/s)
    function wave_velocity(frequency, wavelength) result(v)
        real(8), intent(in) :: frequency, wavelength
        real(8) :: v
        v = frequency * wavelength
    end function wave_velocity
    
    !> Calculate wavelength: λ = v/f
    !! @param velocity Wave velocity (m/s)
    !! @param frequency Frequency (Hz)
    !! @return Wavelength (m)
    function wavelength(velocity, frequency) result(lambda)
        real(8), intent(in) :: velocity, frequency
        real(8) :: lambda
        if (frequency > 0.0d0) then
            lambda = velocity / frequency
        else
            lambda = 0.0d0
        end if
    end function wavelength
    
    !> Calculate frequency from wavelength: f = v/λ
    !! @param velocity Wave velocity (m/s)
    !! @param wavelength Wavelength (m)
    !! @return Frequency (Hz)
    function wave_frequency(velocity, wavelength) result(f)
        real(8), intent(in) :: velocity, wavelength
        real(8) :: f
        if (wavelength > 0.0d0) then
            f = velocity / wavelength
        else
            f = 0.0d0
        end if
    end function wave_frequency
    
    !> Calculate photon energy: E = h*f
    !! @param frequency Frequency (Hz)
    !! @return Energy (J)
    function photon_energy(frequency) result(e)
        real(8), intent(in) :: frequency
        real(8) :: e
        e = PLANCK_CONSTANT * frequency
    end function photon_energy
    
    !> Calculate photon energy in eV
    !! @param frequency Frequency (Hz)
    !! @return Energy (eV)
    function photon_energy_ev(frequency) result(e)
        real(8), intent(in) :: frequency
        real(8) :: e
        e = PLANCK_CONSTANT * frequency / ELECTRON_CHARGE
    end function photon_energy_ev
    
    !==========================================================================
    ! Thermodynamics Basics
    !==========================================================================
    
    !> Calculate heat transfer: Q = m*c*ΔT
    !! @param m Mass (kg)
    !! @param specific_heat Specific heat capacity (J/(kg·K))
    !! @param delta_t Temperature change (K or °C)
    !! @return Heat (J)
    function heat_transfer(m, specific_heat, delta_t) result(q)
        real(8), intent(in) :: m, specific_heat, delta_t
        real(8) :: q
        q = m * specific_heat * delta_t
    end function heat_transfer
    
    !> Calculate temperature change: ΔT = Q/(m*c)
    !! @param q Heat (J)
    !! @param m Mass (kg)
    !! @param specific_heat Specific heat capacity (J/(kg·K))
    !! @return Temperature change (K)
    function temperature_change(q, m, specific_heat) result(delta_t)
        real(8), intent(in) :: q, m, specific_heat
        real(8) :: delta_t
        if (m > 0.0d0 .and. specific_heat > 0.0d0) then
            delta_t = q / (m * specific_heat)
        else
            delta_t = 0.0d0
        end if
    end function temperature_change
    
    !> Calculate thermal expansion: ΔL = α*L0*ΔT
    !! @param l0 Original length (m)
    !! @param alpha Coefficient of linear expansion (1/K)
    !! @param delta_t Temperature change (K)
    !! @return Length change (m)
    function linear_expansion(l0, alpha, delta_t) result(delta_l)
        real(8), intent(in) :: l0, alpha, delta_t
        real(8) :: delta_l
        delta_l = alpha * l0 * delta_t
    end function linear_expansion
    
    !> Calculate ideal gas pressure: P = n*R*T/V
    !! @param n Number of moles
    !! @param t Temperature (K)
    !! @param v Volume (m^3)
    !! @return Pressure (Pa)
    function ideal_gas_pressure(n, t, v) result(p)
        real(8), intent(in) :: n, t, v
        real(8) :: p
        if (v > 0.0d0) then
            p = n * GAS_CONSTANT * t / v
        else
            p = 0.0d0
        end if
    end function ideal_gas_pressure
    
    !> Calculate ideal gas volume: V = n*R*T/P
    !! @param n Number of moles
    !! @param t Temperature (K)
    !! @param p Pressure (Pa)
    !! @return Volume (m^3)
    function ideal_gas_volume(n, t, p) result(v)
        real(8), intent(in) :: n, t, p
        real(8) :: v
        if (p > 0.0d0) then
            v = n * GAS_CONSTANT * t / p
        else
            v = 0.0d0
        end if
    end function ideal_gas_volume
    
    !==========================================================================
    ! Fluid Mechanics Basics
    !==========================================================================
    
    !> Calculate pressure: P = F/A
    !! @param force Force (N)
    !! @param area Area (m^2)
    !! @return Pressure (Pa)
    function pressure(force, area) result(p)
        real(8), intent(in) :: force, area
        real(8) :: p
        if (area > 0.0d0) then
            p = force / area
        else
            p = 0.0d0
        end if
    end function pressure
    
    !> Calculate hydrostatic pressure: P = ρ*g*h
    !! @param density Fluid density (kg/m^3)
    !! @param h Depth (m)
    !! @param g Gravitational acceleration (m/s^2), optional
    !! @return Pressure (Pa)
    function hydrostatic_pressure(density, h, g) result(p)
        real(8), intent(in) :: density, h
        real(8), intent(in), optional :: g
        real(8) :: p, g_val
        g_val = GRAVITY
        if (present(g)) g_val = g
        p = density * g_val * h
    end function hydrostatic_pressure
    
    !> Calculate buoyant force: Fb = ρ_fluid*V*g
    !! @param fluid_density Fluid density (kg/m^3)
    !! @param volume Displaced volume (m^3)
    !! @param g Gravitational acceleration (m/s^2), optional
    !! @return Buoyant force (N)
    function buoyant_force(fluid_density, volume, g) result(fb)
        real(8), intent(in) :: fluid_density, volume
        real(8), intent(in), optional :: g
        real(8) :: fb, g_val
        g_val = GRAVITY
        if (present(g)) g_val = g
        fb = fluid_density * volume * g_val
    end function buoyant_force
    
    !> Calculate flow rate: Q = A*v
    !! @param area Cross-sectional area (m^2)
    !! @param velocity Flow velocity (m/s)
    !! @return Volumetric flow rate (m^3/s)
    function flow_rate(area, velocity) result(q)
        real(8), intent(in) :: area, velocity
        real(8) :: q
        q = area * velocity
    end function flow_rate
    
    !> Bernoulli's equation (simplified): P1 + 0.5*ρ*v1^2 = P2 + 0.5*ρ*v2^2
    !! @param p1 Pressure at point 1 (Pa)
    !! @param v1 Velocity at point 1 (m/s)
    !! @param v2 Velocity at point 2 (m/s)
    !! @param density Fluid density (kg/m^3)
    !! @return Pressure at point 2 (Pa)
    function bernoulli_pressure(p1, v1, v2, density) result(p2)
        real(8), intent(in) :: p1, v1, v2, density
        real(8) :: p2
        p2 = p1 + 0.5d0 * density * (v1 * v1 - v2 * v2)
    end function bernoulli_pressure
    
    !==========================================================================
    ! Simple Harmonic Motion
    !==========================================================================
    
    !> Calculate angular frequency of spring: ω = sqrt(k/m)
    !! @param k Spring constant (N/m)
    !! @param m Mass (kg)
    !! @return Angular frequency (rad/s)
    function spring_angular_frequency(k, m) result(omega)
        real(8), intent(in) :: k, m
        real(8) :: omega
        if (m > 0.0d0 .and. k > 0.0d0) then
            omega = sqrt(k / m)
        else
            omega = 0.0d0
        end if
    end function spring_angular_frequency
    
    !> Calculate period of spring: T = 2*π*sqrt(m/k)
    !! @param m Mass (kg)
    !! @param k Spring constant (N/m)
    !! @return Period (s)
    function spring_period(m, k) result(t)
        real(8), intent(in) :: m, k
        real(8) :: t
        if (m > 0.0d0 .and. k > 0.0d0) then
            t = 2.0d0 * PI * sqrt(m / k)
        else
            t = 0.0d0
        end if
    end function spring_period
    
    !> Calculate frequency of spring: f = (1/2π)*sqrt(k/m)
    !! @param k Spring constant (N/m)
    !! @param m Mass (kg)
    !! @return Frequency (Hz)
    function spring_frequency(k, m) result(f)
        real(8), intent(in) :: k, m
        real(8) :: f
        if (m > 0.0d0 .and. k > 0.0d0) then
            f = sqrt(k / m) / (2.0d0 * PI)
        else
            f = 0.0d0
        end if
    end function spring_frequency
    
    !> Calculate pendulum period: T = 2*π*sqrt(L/g)
    !! @param length Pendulum length (m)
    !! @param g Gravitational acceleration (m/s^2), optional
    !! @return Period (s)
    function pendulum_period(length, g) result(t)
        real(8), intent(in) :: length
        real(8), intent(in), optional :: g
        real(8) :: t, g_val
        g_val = GRAVITY
        if (present(g)) g_val = g
        if (length > 0.0d0 .and. g_val > 0.0d0) then
            t = 2.0d0 * PI * sqrt(length / g_val)
        else
            t = 0.0d0
        end if
    end function pendulum_period
    
    !==========================================================================
    ! Unit Conversions
    !==========================================================================
    
    !> Convert Celsius to Kelvin
    !! @param celsius Temperature in Celsius
    !! @return Temperature in Kelvin
    function celsius_to_kelvin(celsius) result(kelvin)
        real(8), intent(in) :: celsius
        real(8) :: kelvin
        kelvin = celsius + 273.15d0
    end function celsius_to_kelvin
    
    !> Convert Kelvin to Celsius
    !! @param kelvin Temperature in Kelvin
    !! @return Temperature in Celsius
    function kelvin_to_celsius(kelvin) result(celsius)
        real(8), intent(in) :: kelvin
        real(8) :: celsius
        celsius = kelvin - 273.15d0
    end function kelvin_to_celsius
    
    !> Convert Fahrenheit to Celsius
    !! @param fahrenheit Temperature in Fahrenheit
    !! @return Temperature in Celsius
    function fahrenheit_to_celsius(fahrenheit) result(celsius)
        real(8), intent(in) :: fahrenheit
        real(8) :: celsius
        celsius = (fahrenheit - 32.0d0) * 5.0d0 / 9.0d0
    end function fahrenheit_to_celsius
    
    !> Convert Celsius to Fahrenheit
    !! @param celsius Temperature in Celsius
    !! @return Temperature in Fahrenheit
    function celsius_to_fahrenheit(celsius) result(fahrenheit)
        real(8), intent(in) :: celsius
        real(8) :: fahrenheit
        fahrenheit = celsius * 9.0d0 / 5.0d0 + 32.0d0
    end function celsius_to_fahrenheit
    
    !> Convert degrees to radians
    !! @param degrees Angle in degrees
    !! @return Angle in radians
    function degrees_to_radians(degrees) result(radians)
        real(8), intent(in) :: degrees
        real(8) :: radians
        radians = degrees * PI / 180.0d0
    end function degrees_to_radians
    
    !> Convert radians to degrees
    !! @param radians Angle in radians
    !! @return Angle in degrees
    function radians_to_degrees(radians) result(degrees)
        real(8), intent(in) :: radians
        real(8) :: degrees
        degrees = radians * 180.0d0 / PI
    end function radians_to_degrees
    
    !> Convert meters per second to kilometers per hour
    !! @param ms Velocity in m/s
    !! @return Velocity in km/h
    function ms_to_kmh(ms) result(kmh)
        real(8), intent(in) :: ms
        real(8) :: kmh
        kmh = ms * 3.6d0
    end function ms_to_kmh
    
    !> Convert kilometers per hour to meters per second
    !! @param kmh Velocity in km/h
    !! @return Velocity in m/s
    function kmh_to_ms(kmh) result(ms)
        real(8), intent(in) :: kmh
        real(8) :: ms
        ms = kmh / 3.6d0
    end function kmh_to_ms
    
    !> Convert Joules to electron volts
    !! @param j Energy in Joules
    !! @return Energy in eV
    function joules_to_ev(j) result(ev)
        real(8), intent(in) :: j
        real(8) :: ev
        ev = j / ELECTRON_CHARGE
    end function joules_to_ev
    
    !> Convert electron volts to Joules
    !! @param ev Energy in eV
    !! @return Energy in Joules
    function ev_to_joules(ev) result(j)
        real(8), intent(in) :: ev
        real(8) :: j
        j = ev * ELECTRON_CHARGE
    end function ev_to_joules
    
    !> Apply SI prefix multiplier
    !! @param value Base value
    !! @param prefix Prefix name ('kilo', 'mega', 'giga', 'milli', 'micro', 'nano', etc.)
    !! @return Scaled value
    function apply_si_prefix(value, prefix) result(scaled)
        real(8), intent(in) :: value
        character(len=*), intent(in) :: prefix
        real(8) :: scaled
        
        select case (trim(adjustl(prefix)))
            case ('yocto'); scaled = value * 1.0d24
            case ('zepto'); scaled = value * 1.0d21
            case ('atto');  scaled = value * 1.0d18
            case ('femto'); scaled = value * 1.0d15
            case ('pico');  scaled = value * 1.0d12
            case ('nano');  scaled = value * 1.0d9
            case ('micro'); scaled = value * 1.0d6
            case ('milli'); scaled = value * 1.0d3
            case ('centi'); scaled = value * 1.0d2
            case ('deci');  scaled = value * 1.0d1
            case ('deca');  scaled = value * 1.0d-1
            case ('hecto'); scaled = value * 1.0d-2
            case ('kilo');  scaled = value * 1.0d-3
            case ('mega');  scaled = value * 1.0d-6
            case ('giga');  scaled = value * 1.0d-9
            case ('tera');  scaled = value * 1.0d-12
            case ('peta');  scaled = value * 1.0d-15
            case ('exa');   scaled = value * 1.0d-18
            case ('zetta'); scaled = value * 1.0d-21
            case ('yotta'); scaled = value * 1.0d-24
            case default;   scaled = value
        end select
    end function apply_si_prefix
    
    !==========================================================================
    ! Rotational Motion
    !==========================================================================
    
    !> Calculate rotational kinetic energy: KE = 0.5*I*ω^2
    !! @param moment_of_inertia Moment of inertia (kg·m^2)
    !! @param omega Angular velocity (rad/s)
    !! @return Rotational kinetic energy (J)
    function rotational_kinetic_energy(moment_of_inertia, omega) result(ke)
        real(8), intent(in) :: moment_of_inertia, omega
        real(8) :: ke
        ke = 0.5d0 * moment_of_inertia * omega * omega
    end function rotational_kinetic_energy
    
    !> Calculate angular momentum: L = I*ω
    !! @param moment_of_inertia Moment of inertia (kg·m^2)
    !! @param omega Angular velocity (rad/s)
    !! @return Angular momentum (kg·m^2/s)
    function angular_momentum(moment_of_inertia, omega) result(l)
        real(8), intent(in) :: moment_of_inertia, omega
        real(8) :: l
        l = moment_of_inertia * omega
    end function angular_momentum
    
    !> Calculate torque: τ = r*F*sin(θ)
    !! @param r Lever arm distance (m)
    !! @param force Force (N)
    !! @param angle_degrees Angle between r and F (degrees), optional
    !! @return Torque (N·m)
    function torque(r, force, angle_degrees) result(tau)
        real(8), intent(in) :: r, force
        real(8), intent(in), optional :: angle_degrees
        real(8) :: tau, angle_rad, sin_angle
        sin_angle = 1.0d0
        if (present(angle_degrees)) then
            angle_rad = angle_degrees * PI / 180.0d0
            sin_angle = sin(angle_rad)
        end if
        tau = r * force * sin_angle
    end function torque
    
    !> Calculate moment of inertia for solid cylinder: I = 0.5*m*r^2
    !! @param m Mass (kg)
    !! @param r Radius (m)
    !! @return Moment of inertia (kg·m^2)
    function moment_of_inertia_cylinder(m, r) result(i)
        real(8), intent(in) :: m, r
        real(8) :: i
        i = 0.5d0 * m * r * r
    end function moment_of_inertia_cylinder
    
    !> Calculate moment of inertia for solid sphere: I = (2/5)*m*r^2
    !! @param m Mass (kg)
    !! @param r Radius (m)
    !! @return Moment of inertia (kg·m^2)
    function moment_of_inertia_sphere(m, r) result(i)
        real(8), intent(in) :: m, r
        real(8) :: i
        i = 0.4d0 * m * r * r
    end function moment_of_inertia_sphere
    
    !> Calculate moment of inertia for thin rod about center: I = (1/12)*m*l^2
    !! @param m Mass (kg)
    !! @param l Length (m)
    !! @return Moment of inertia (kg·m^2)
    function moment_of_inertia_rod_center(m, l) result(i)
        real(8), intent(in) :: m, l
        real(8) :: i
        i = m * l * l / 12.0d0
    end function moment_of_inertia_rod_center
    
    !> Calculate moment of inertia for thin rod about end: I = (1/3)*m*l^2
    !! @param m Mass (kg)
    !! @param l Length (m)
    !! @return Moment of inertia (kg·m^2)
    function moment_of_inertia_rod_end(m, l) result(i)
        real(8), intent(in) :: m, l
        real(8) :: i
        i = m * l * l / 3.0d0
    end function moment_of_inertia_rod_end

end module physics_utils