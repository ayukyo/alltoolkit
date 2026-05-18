!! AllToolkit - Fortran Geometry Utilities Test Suite
!! Comprehensive tests for all geometry utility functions
!!
!! Author: AllToolkit Contributors
!! License: MIT

program geometry_utils_test
    use geometry_utils
    implicit none
    
    integer :: test_count, pass_count
    
    test_count = 0
    pass_count = 0
    
    print *, "========================================"
    print *, "Fortran Geometry Utilities Test Suite"
    print *, "========================================"
    print *, ""
    
    ! Test Point 2D Operations
    call test_point2d_operations()
    
    ! Test Point 3D Operations
    call test_point3d_operations()
    
    ! Test Line 2D Operations
    call test_line2d_operations()
    
    ! Test Triangle 2D Operations
    call test_triangle2d_operations()
    
    ! Test Circle 2D Operations
    call test_circle2d_operations()
    
    ! Test Rectangle 2D Operations
    call test_rectangle2d_operations()
    
    ! Test Polygon 2D Operations
    call test_polygon2d_operations()
    
    ! Test Plane 3D Operations
    call test_plane3d_operations()
    
    ! Test Sphere 3D Operations
    call test_sphere3d_operations()
    
    ! Test AABB 3D Operations
    call test_aabb3d_operations()
    
    ! Test Utility Functions
    call test_utility_functions()
    
    print *, ""
    print *, "========================================"
    print *, "Test Results:"
    print *, "========================================"
    write(*, '(A, I0, A, I0, A)') "  Passed: ", pass_count, "/", test_count, " tests"
    
    if (pass_count == test_count) then
        print *, "  Status: ALL TESTS PASSED!"
    else
        print *, "  Status: SOME TESTS FAILED!"
    end if
    print *, "========================================"
    
contains

    !==========================================================================
    ! Test Point 2D Operations
    !==========================================================================
    subroutine test_point2d_operations()
        type(point2d) :: p1, p2, mid, trans, rot, scaled
        real(8) :: dist
        
        print *, "Testing Point 2D Operations..."
        
        ! Test distance
        p1 = make_point2d(0.0d0, 0.0d0)
        p2 = make_point2d(3.0d0, 4.0d0)
        dist = distance(p1, p2)
        call assert_approx(dist, 5.0d0, "distance between (0,0) and (3,4)")
        
        ! Test midpoint
        mid = midpoint(p1, p2)
        call assert_approx(mid%x, 1.5d0, "midpoint x")
        call assert_approx(mid%y, 2.0d0, "midpoint y")
        
        ! Test translate
        trans = translate_point2d(p1, 5.0d0, -3.0d0)
        call assert_approx(trans%x, 5.0d0, "translate x")
        call assert_approx(trans%y, -3.0d0, "translate y")
        
        ! Test rotate (90 degrees counterclockwise)
        p1 = make_point2d(1.0d0, 0.0d0)
        rot = rotate_point2d(p1, PI / 2.0d0)
        call assert_approx(rot%x, 0.0d0, "rotate 90deg x")
        call assert_approx(rot%y, 1.0d0, "rotate 90deg y")
        
        ! Test scale
        scaled = scale_point2d(p2, 2.0d0)
        call assert_approx(scaled%x, 6.0d0, "scale x")
        call assert_approx(scaled%y, 8.0d0, "scale y")
        
        print *, "  Point 2D tests completed."
        print *, ""
    end subroutine test_point2d_operations
    
    !==========================================================================
    ! Test Point 3D Operations
    !==========================================================================
    subroutine test_point3d_operations()
        type(point3d) :: p1, p2, mid, v1, v2, cross, norm
        real(8) :: dist, dot
        
        print *, "Testing Point 3D Operations..."
        
        ! Test distance
        p1 = make_point3d(0.0d0, 0.0d0, 0.0d0)
        p2 = make_point3d(1.0d0, 2.0d0, 2.0d0)
        dist = distance(p1, p2)
        call assert_approx(dist, 3.0d0, "distance 3D")
        
        ! Test midpoint
        mid = midpoint(p1, p2)
        call assert_approx(mid%x, 0.5d0, "midpoint 3D x")
        call assert_approx(mid%y, 1.0d0, "midpoint 3D y")
        call assert_approx(mid%z, 1.0d0, "midpoint 3D z")
        
        ! Test vector operations
        v1 = make_point3d(1.0d0, 0.0d0, 0.0d0)
        v2 = make_point3d(0.0d0, 1.0d0, 0.0d0)
        
        dot = vector_dot(v1, v2)
        call assert_approx(dot, 0.0d0, "dot product of perpendicular vectors")
        
        cross = vector_cross(v1, v2)
        call assert_approx(cross%x, 0.0d0, "cross x")
        call assert_approx(cross%y, 0.0d0, "cross y")
        call assert_approx(cross%z, 1.0d0, "cross z")
        
        ! Test normalize
        p1 = make_point3d(3.0d0, 0.0d0, 0.0d0)
        norm = vector_normalize(p1)
        call assert_approx(norm%x, 1.0d0, "normalize x")
        call assert_approx(norm%y, 0.0d0, "normalize y")
        call assert_approx(norm%z, 0.0d0, "normalize z")
        
        print *, "  Point 3D tests completed."
        print *, ""
    end subroutine test_point3d_operations
    
    !==========================================================================
    ! Test Line 2D Operations
    !==========================================================================
    subroutine test_line2d_operations()
        type(point2d) :: p1, p2, p3
        type(line2d) :: line
        type(segment2d) :: seg1, seg2
        real(8) :: dist
        
        print *, "Testing Line 2D Operations..."
        
        ! Test line from points
        p1 = make_point2d(0.0d0, 0.0d0)
        p2 = make_point2d(1.0d0, 1.0d0)
        line = line_from_points(p1, p2)
        
        ! Line equation: x - y = 0 (a=1, b=-1, c=0)
        call assert_approx(line%a, 1.0d0, "line coefficient a")
        call assert_approx(line%b, -1.0d0, "line coefficient b")
        call assert_approx(line%c, 0.0d0, "line coefficient c")
        
        ! Test point to line distance
        p3 = make_point2d(2.0d0, 0.0d0)
        dist = distance(p3, line)
        call assert_approx(dist, sqrt(2.0d0), "point to line distance")
        
        ! Test segment intersection
        seg1 = segment2d(make_point2d(0.0d0, 0.0d0), make_point2d(2.0d0, 2.0d0))
        seg2 = segment2d(make_point2d(0.0d0, 2.0d0), make_point2d(2.0d0, 0.0d0))
        call assert_true(segments_intersect(seg1, seg2), "segments intersect")
        
        seg2 = segment2d(make_point2d(3.0d0, 3.0d0), make_point2d(4.0d0, 4.0d0))
        call assert_true(.not. segments_intersect(seg1, seg2), "segments do not intersect")
        
        print *, "  Line 2D tests completed."
        print *, ""
    end subroutine test_line2d_operations
    
    !==========================================================================
    ! Test Triangle 2D Operations
    !==========================================================================
    subroutine test_triangle2d_operations()
        type(triangle2d) :: tri
        type(point2d) :: p1, p2, p3, centroid_pt, circum_pt, test_pt
        real(8) :: area_val, radius
        
        print *, "Testing Triangle 2D Operations..."
        
        ! Create right triangle
        p1 = make_point2d(0.0d0, 0.0d0)
        p2 = make_point2d(3.0d0, 0.0d0)
        p3 = make_point2d(0.0d0, 4.0d0)
        tri = make_triangle2d(p1, p2, p3)
        
        ! Test area (right triangle with legs 3 and 4, area = 6)
        area_val = area(tri)
        call assert_approx(area_val, 6.0d0, "triangle area")
        
        ! Test centroid
        centroid_pt = centroid(tri)
        call assert_approx(centroid_pt%x, 1.0d0, "triangle centroid x")
        call assert_approx(centroid_pt%y, 4.0d0/3.0d0, "triangle centroid y")
        
        ! Test circumradius (hypotenuse/2 = 2.5)
        radius = circumradius(tri)
        call assert_approx(radius, 2.5d0, "circumradius")
        
        ! Test point in triangle
        test_pt = make_point2d(1.0d0, 1.0d0)
        call assert_true(point_in_triangle(test_pt, tri), "point inside triangle")
        
        test_pt = make_point2d(10.0d0, 10.0d0)
        call assert_true(.not. point_in_triangle(test_pt, tri), "point outside triangle")
        
        print *, "  Triangle 2D tests completed."
        print *, ""
    end subroutine test_triangle2d_operations
    
    !==========================================================================
    ! Test Circle 2D Operations
    !==========================================================================
    subroutine test_circle2d_operations()
        type(circle2d) :: circle
        type(point2d) :: center, inside_pt, outside_pt
        type(rectangle2d) :: rect
        real(8) :: area_val, circ
        
        print *, "Testing Circle 2D Operations..."
        
        ! Create circle
        center = make_point2d(0.0d0, 0.0d0)
        circle = make_circle2d(center, 5.0d0)
        
        ! Test area (pi * r^2)
        area_val = area(circle)
        call assert_approx(area_val, PI * 25.0d0, "circle area")
        
        ! Test circumference/perimeter (2 * pi * r)
        circ = perimeter(circle)
        call assert_approx(circ, 2.0d0 * PI * 5.0d0, "circle circumference")
        
        ! Test contains point
        inside_pt = make_point2d(3.0d0, 4.0d0)  ! distance = 5, on boundary
        call assert_true(contains_point(circle, inside_pt), "point on circle boundary")
        
        outside_pt = make_point2d(6.0d0, 0.0d0)  ! distance = 6 > 5
        call assert_true(.not. contains_point(circle, outside_pt), "point outside circle")
        
        ! Test circle-rectangle intersection
        rect = make_rectangle2d(3.0d0, 0.0d0, 2.0d0, 2.0d0)
        call assert_true(intersects(circle, rect), "circle intersects rectangle")
        
        print *, "  Circle 2D tests completed."
        print *, ""
    end subroutine test_circle2d_operations
    
    !==========================================================================
    ! Test Rectangle 2D Operations
    !==========================================================================
    subroutine test_rectangle2d_operations()
        type(rectangle2d) :: rect
        type(point2d) :: inside_pt, outside_pt
        type(point2d) :: corners(4)
        real(8) :: area_val, perim
        
        print *, "Testing Rectangle 2D Operations..."
        
        ! Create rectangle
        rect = make_rectangle2d(0.0d0, 0.0d0, 4.0d0, 3.0d0)
        
        ! Test area
        area_val = area(rect)
        call assert_approx(area_val, 12.0d0, "rectangle area")
        
        ! Test perimeter
        perim = perimeter(rect)
        call assert_approx(perim, 14.0d0, "rectangle perimeter")
        
        ! Test contains point
        inside_pt = make_point2d(2.0d0, 1.5d0)
        call assert_true(contains_point(rect, inside_pt), "point inside rectangle")
        
        outside_pt = make_point2d(5.0d0, 5.0d0)
        call assert_true(.not. contains_point(rect, outside_pt), "point outside rectangle")
        
        ! Test corners
        corners = rectangle_corners(rect)
        call assert_approx(corners(1)%x, 0.0d0, "corner 1 x")
        call assert_approx(corners(1)%y, 0.0d0, "corner 1 y")
        call assert_approx(corners(3)%x, 4.0d0, "corner 3 x")
        call assert_approx(corners(3)%y, 3.0d0, "corner 3 y")
        
        print *, "  Rectangle 2D tests completed."
        print *, ""
    end subroutine test_rectangle2d_operations
    
    !==========================================================================
    ! Test Polygon 2D Operations
    !==========================================================================
    subroutine test_polygon2d_operations()
        type(point2d) :: square(4), triangle_pts(3)
        type(point2d) :: centroid_pt
        real(8) :: area_val, perim
        
        print *, "Testing Polygon 2D Operations..."
        
        ! Create square
        square(1) = make_point2d(0.0d0, 0.0d0)
        square(2) = make_point2d(2.0d0, 0.0d0)
        square(3) = make_point2d(2.0d0, 2.0d0)
        square(4) = make_point2d(0.0d0, 2.0d0)
        
        ! Test area
        area_val = area(square)
        call assert_approx(area_val, 4.0d0, "square area")
        
        ! Test perimeter
        perim = perimeter(square)
        call assert_approx(perim, 8.0d0, "square perimeter")
        
        ! Test centroid
        centroid_pt = centroid(square)
        call assert_approx(centroid_pt%x, 1.0d0, "square centroid x")
        call assert_approx(centroid_pt%y, 1.0d0, "square centroid y")
        
        ! Test convex check
        call assert_true(is_convex_polygon(square), "square is convex")
        
        ! Test triangle
        triangle_pts(1) = make_point2d(0.0d0, 0.0d0)
        triangle_pts(2) = make_point2d(3.0d0, 0.0d0)
        triangle_pts(3) = make_point2d(0.0d0, 4.0d0)
        
        area_val = area(triangle_pts)
        call assert_approx(area_val, 6.0d0, "triangle polygon area")
        
        print *, "  Polygon 2D tests completed."
        print *, ""
    end subroutine test_polygon2d_operations
    
    !==========================================================================
    ! Test Plane 3D Operations
    !==========================================================================
    subroutine test_plane3d_operations()
        type(point3d) :: p1, p2, p3, test_pt, proj_pt
        type(plane3d) :: plane
        real(8) :: dist
        
        print *, "Testing Plane 3D Operations..."
        
        ! Create plane from three points (z = 0 plane)
        p1 = make_point3d(0.0d0, 0.0d0, 0.0d0)
        p2 = make_point3d(1.0d0, 0.0d0, 0.0d0)
        p3 = make_point3d(0.0d0, 1.0d0, 0.0d0)
        plane = plane_from_three_points(p1, p2, p3)
        
        ! Test distance from point to plane
        test_pt = make_point3d(0.0d0, 0.0d0, 5.0d0)
        dist = distance(test_pt, plane)
        call assert_approx(dist, 5.0d0, "point to plane distance")
        
        ! Test projection onto plane
        proj_pt = project_point_to_plane(test_pt, plane)
        call assert_approx(proj_pt%z, 0.0d0, "projection z coordinate")
        
        print *, "  Plane 3D tests completed."
        print *, ""
    end subroutine test_plane3d_operations
    
    !==========================================================================
    ! Test Sphere 3D Operations
    !==========================================================================
    subroutine test_sphere3d_operations()
        type(sphere3d) :: sphere1, sphere2
        type(point3d) :: center, inside_pt, outside_pt
        real(8) :: vol, surf_area
        
        print *, "Testing Sphere 3D Operations..."
        
        ! Create sphere
        center = make_point3d(0.0d0, 0.0d0, 0.0d0)
        sphere1 = make_sphere3d(center, 3.0d0)
        
        ! Test volume (4/3 * pi * r^3)
        vol = volume(sphere1)
        call assert_approx(vol, (4.0d0/3.0d0) * PI * 27.0d0, "sphere volume")
        
        ! Test surface area (4 * pi * r^2)
        surf_area = surface_area(sphere1)
        call assert_approx(surf_area, 4.0d0 * PI * 9.0d0, "sphere surface area")
        
        ! Test contains point
        inside_pt = make_point3d(1.0d0, 1.0d0, 1.0d0)
        call assert_true(contains_point(sphere1, inside_pt), "point inside sphere")
        
        outside_pt = make_point3d(10.0d0, 0.0d0, 0.0d0)
        call assert_true(.not. contains_point(sphere1, outside_pt), "point outside sphere")
        
        ! Test sphere intersection
        sphere2 = make_sphere3d(make_point3d(2.0d0, 0.0d0, 0.0d0), 2.0d0)
        call assert_true(intersects(sphere1, sphere2), "spheres intersect")
        
        sphere2 = make_sphere3d(make_point3d(10.0d0, 0.0d0, 0.0d0), 2.0d0)
        call assert_true(.not. intersects(sphere1, sphere2), "spheres do not intersect")
        
        print *, "  Sphere 3D tests completed."
        print *, ""
    end subroutine test_sphere3d_operations
    
    !==========================================================================
    ! Test AABB 3D Operations
    !==========================================================================
    subroutine test_aabb3d_operations()
        type(aabb3d) :: box1, box2
        type(point3d) :: p1, p2, inside_pt, outside_pt, center_pt
        real(8) :: vol, surf_area
        
        print *, "Testing AABB 3D Operations..."
        
        ! Create AABB
        p1 = make_point3d(0.0d0, 0.0d0, 0.0d0)
        p2 = make_point3d(2.0d0, 3.0d0, 4.0d0)
        box1 = make_aabb3d(p1, p2)
        
        ! Test volume
        vol = volume(box1)
        call assert_approx(vol, 24.0d0, "AABB volume")
        
        ! Test surface area (2*(wh+hd+wd) = 2*(6+12+8) = 52)
        surf_area = surface_area(box1)
        call assert_approx(surf_area, 52.0d0, "AABB surface area")
        
        ! Test contains point
        inside_pt = make_point3d(1.0d0, 1.5d0, 2.0d0)
        call assert_true(contains_point(box1, inside_pt), "point inside AABB")
        
        outside_pt = make_point3d(5.0d0, 5.0d0, 5.0d0)
        call assert_true(.not. contains_point(box1, outside_pt), "point outside AABB")
        
        ! Test AABB intersection
        box2 = make_aabb3d(make_point3d(1.0d0, 1.0d0, 1.0d0), &
                           make_point3d(3.0d0, 4.0d0, 5.0d0))
        call assert_true(intersects(box1, box2), "AABBs intersect")
        
        box2 = make_aabb3d(make_point3d(10.0d0, 10.0d0, 10.0d0), &
                           make_point3d(12.0d0, 12.0d0, 12.0d0))
        call assert_true(.not. intersects(box1, box2), "AABBs do not intersect")
        
        ! Test center
        center_pt = aabb_center(box1)
        call assert_approx(center_pt%x, 1.0d0, "AABB center x")
        call assert_approx(center_pt%y, 1.5d0, "AABB center y")
        call assert_approx(center_pt%z, 2.0d0, "AABB center z")
        
        print *, "  AABB 3D tests completed."
        print *, ""
    end subroutine test_aabb3d_operations
    
    !==========================================================================
    ! Test Utility Functions
    !==========================================================================
    subroutine test_utility_functions()
        real(8) :: result
        
        print *, "Testing Utility Functions..."
        
        ! Test degree to radian conversion
        result = deg_to_rad(180.0d0)
        call assert_approx(result, PI, "deg to rad (180 degrees)")
        
        ! Test radian to degree conversion
        result = rad_to_deg(PI)
        call assert_approx(result, 180.0d0, "rad to deg (pi radians)")
        
        ! Test clamp
        result = clamp_value(5.0d0, 0.0d0, 10.0d0)
        call assert_approx(result, 5.0d0, "clamp (value in range)")
        
        result = clamp_value(-5.0d0, 0.0d0, 10.0d0)
        call assert_approx(result, 0.0d0, "clamp (value below min)")
        
        result = clamp_value(15.0d0, 0.0d0, 10.0d0)
        call assert_approx(result, 10.0d0, "clamp (value above max)")
        
        ! Test lerp
        result = lerp(0.0d0, 10.0d0, 0.5d0)
        call assert_approx(result, 5.0d0, "lerp (50%)")
        
        result = lerp(0.0d0, 10.0d0, 0.0d0)
        call assert_approx(result, 0.0d0, "lerp (0%)")
        
        result = lerp(0.0d0, 10.0d0, 1.0d0)
        call assert_approx(result, 10.0d0, "lerp (100%)")
        
        ! Test approx_equal (within default epsilon of 1.0d-10)
        call assert_true(approx_equal(1.0d0, 1.0d0 + 1.0d-11), "approx equal (within epsilon)")
        call assert_true(.not. approx_equal(1.0d0, 2.0d0), "approx equal (different values)")
        
        print *, "  Utility tests completed."
        print *, ""
    end subroutine test_utility_functions
    
    !==========================================================================
    ! Test Assertion Helpers
    !==========================================================================
    subroutine assert_approx(actual, expected, test_name)
        real(8), intent(in) :: actual, expected
        character(len=*), intent(in) :: test_name
        
        test_count = test_count + 1
        if (abs(actual - expected) < 1.0d-6) then
            pass_count = pass_count + 1
            write(*, '(A, A)') "    [PASS] ", test_name
        else
            write(*, '(A, A, A, F12.6, A, F12.6)') "    [FAIL] ", test_name, &
                " - Expected: ", expected, ", Got: ", actual
        end if
    end subroutine assert_approx
    
    subroutine assert_true(condition, test_name)
        logical, intent(in) :: condition
        character(len=*), intent(in) :: test_name
        
        test_count = test_count + 1
        if (condition) then
            pass_count = pass_count + 1
            write(*, '(A, A)') "    [PASS] ", test_name
        else
            write(*, '(A, A)') "    [FAIL] ", test_name
        end if
    end subroutine assert_true

end program geometry_utils_test