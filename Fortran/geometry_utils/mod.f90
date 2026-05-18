!! AllToolkit - Fortran Geometry Utilities Module
!! Zero-dependency computational geometry functions for Fortran 90/95/2003+
!!
!! Features:
!! - 2D Geometry: points, lines, triangles, circles, polygons, rectangles
!! - 3D Geometry: points, vectors, planes, spheres, boxes
!! - Distance calculations
!! - Area and volume computations
!! - Collision/intersection detection
!! - Geometric transformations
!!
!! Author: AllToolkit Contributors
!! License: MIT

module geometry_utils
    implicit none
    
    ! Module constants
    real(8), parameter :: PI = 3.14159265358979323846d0
    real(8), parameter :: EPSILON = 1.0d-10
    
    !==========================================================================
    ! Derived Types
    !==========================================================================
    
    ! 2D Point
    type :: point2d
        real(8) :: x, y
    end type point2d
    
    ! 3D Point / Vector
    type :: point3d
        real(8) :: x, y, z
    end type point3d
    
    ! 2D Line (ax + by + c = 0)
    type :: line2d
        real(8) :: a, b, c
    end type line2d
    
    ! 2D Line Segment
    type :: segment2d
        type(point2d) :: p1, p2
    end type segment2d
    
    ! 2D Circle
    type :: circle2d
        type(point2d) :: center
        real(8) :: radius
    end type circle2d
    
    ! 2D Triangle
    type :: triangle2d
        type(point2d) :: p1, p2, p3
    end type triangle2d
    
    ! 2D Rectangle
    type :: rectangle2d
        real(8) :: x, y, width, height
    end type rectangle2d
    
    ! 3D Plane (ax + by + cz + d = 0)
    type :: plane3d
        real(8) :: a, b, c, d
    end type plane3d
    
    ! 3D Sphere
    type :: sphere3d
        type(point3d) :: center
        real(8) :: radius
    end type sphere3d
    
    ! 3D Box (Axis-Aligned Bounding Box)
    type :: aabb3d
        type(point3d) :: min_pt, max_pt
    end type aabb3d
    
    !==========================================================================
    ! Interfaces for generic functions
    !==========================================================================
    
    interface distance
        module procedure distance_point2d
        module procedure distance_point3d
        module procedure distance_point_to_line2d
        module procedure distance_point_to_segment2d
        module procedure distance_point_to_plane3d
    end interface
    
    interface midpoint
        module procedure midpoint_point2d
        module procedure midpoint_point3d
    end interface
    
    interface area
        module procedure area_triangle2d
        module procedure area_circle2d
        module procedure area_rectangle2d
        module procedure area_polygon2d
    end interface
    
    interface perimeter
        module procedure perimeter_circle2d
        module procedure perimeter_rectangle2d
        module procedure perimeter_polygon2d
    end interface
    
    interface volume
        module procedure volume_sphere3d
        module procedure volume_aabb3d
    end interface
    
    interface surface_area
        module procedure surface_area_sphere3d
        module procedure surface_area_aabb3d
    end interface
    
    interface centroid
        module procedure centroid_triangle2d
        module procedure centroid_polygon2d
    end interface
    
    interface contains_point
        module procedure circle_contains_point
        module procedure rectangle_contains_point
        module procedure aabb_contains_point
        module procedure sphere_contains_point
    end interface
    
    interface intersects
        module procedure segments_intersect
        module procedure circle_rectangle_intersect
        module procedure aabb_intersect
        module procedure sphere_intersect
    end interface
    
contains

    !==========================================================================
    ! Point 2D Operations
    !==========================================================================
    
    !> Calculate distance between two 2D points
    function distance_point2d(p1, p2) result(res)
        type(point2d), intent(in) :: p1, p2
        real(8) :: res
        res = sqrt((p2%x - p1%x)**2 + (p2%y - p1%y)**2)
    end function distance_point2d
    
    !> Calculate midpoint between two 2D points
    function midpoint_point2d(p1, p2) result(res)
        type(point2d), intent(in) :: p1, p2
        type(point2d) :: res
        res%x = (p1%x + p2%x) / 2.0d0
        res%y = (p1%y + p2%y) / 2.0d0
    end function midpoint_point2d
    
    !> Create a 2D point
    function make_point2d(x, y) result(res)
        real(8), intent(in) :: x, y
        type(point2d) :: res
        res%x = x
        res%y = y
    end function make_point2d
    
    !> Translate a 2D point by dx, dy
    function translate_point2d(p, dx, dy) result(res)
        type(point2d), intent(in) :: p
        real(8), intent(in) :: dx, dy
        type(point2d) :: res
        res%x = p%x + dx
        res%y = p%y + dy
    end function translate_point2d
    
    !> Rotate a 2D point around origin by angle (radians)
    function rotate_point2d(p, angle) result(res)
        type(point2d), intent(in) :: p
        real(8), intent(in) :: angle
        type(point2d) :: res
        real(8) :: c, s
        c = cos(angle)
        s = sin(angle)
        res%x = p%x * c - p%y * s
        res%y = p%x * s + p%y * c
    end function rotate_point2d
    
    !> Scale a 2D point by factor
    function scale_point2d(p, factor) result(res)
        type(point2d), intent(in) :: p
        real(8), intent(in) :: factor
        type(point2d) :: res
        res%x = p%x * factor
        res%y = p%y * factor
    end function scale_point2d
    
    !==========================================================================
    ! Point 3D / Vector Operations
    !==========================================================================
    
    !> Calculate distance between two 3D points
    function distance_point3d(p1, p2) result(res)
        type(point3d), intent(in) :: p1, p2
        real(8) :: res
        res = sqrt((p2%x - p1%x)**2 + (p2%y - p1%y)**2 + (p2%z - p1%z)**2)
    end function distance_point3d
    
    !> Calculate midpoint between two 3D points
    function midpoint_point3d(p1, p2) result(res)
        type(point3d), intent(in) :: p1, p2
        type(point3d) :: res
        res%x = (p1%x + p2%x) / 2.0d0
        res%y = (p1%y + p2%y) / 2.0d0
        res%z = (p1%z + p2%z) / 2.0d0
    end function midpoint_point3d
    
    !> Create a 3D point
    function make_point3d(x, y, z) result(res)
        real(8), intent(in) :: x, y, z
        type(point3d) :: res
        res%x = x
        res%y = y
        res%z = z
    end function make_point3d
    
    !> Vector addition (3D)
    function vector_add(v1, v2) result(res)
        type(point3d), intent(in) :: v1, v2
        type(point3d) :: res
        res%x = v1%x + v2%x
        res%y = v1%y + v2%y
        res%z = v1%z + v2%z
    end function vector_add
    
    !> Vector subtraction (3D)
    function vector_sub(v1, v2) result(res)
        type(point3d), intent(in) :: v1, v2
        type(point3d) :: res
        res%x = v1%x - v2%x
        res%y = v1%y - v2%y
        res%z = v1%z - v2%z
    end function vector_sub
    
    !> Vector dot product (3D)
    function vector_dot(v1, v2) result(res)
        type(point3d), intent(in) :: v1, v2
        real(8) :: res
        res = v1%x * v2%x + v1%y * v2%y + v1%z * v2%z
    end function vector_dot
    
    !> Vector cross product (3D)
    function vector_cross(v1, v2) result(res)
        type(point3d), intent(in) :: v1, v2
        type(point3d) :: res
        res%x = v1%y * v2%z - v1%z * v2%y
        res%y = v1%z * v2%x - v1%x * v2%z
        res%z = v1%x * v2%y - v1%y * v2%x
    end function vector_cross
    
    !> Vector magnitude (3D)
    function vector_magnitude(v) result(res)
        type(point3d), intent(in) :: v
        real(8) :: res
        res = sqrt(v%x**2 + v%y**2 + v%z**2)
    end function vector_magnitude
    
    !> Vector normalize (3D)
    function vector_normalize(v) result(res)
        type(point3d), intent(in) :: v
        type(point3d) :: res
        real(8) :: mag
        mag = vector_magnitude(v)
        if (mag > EPSILON) then
            res%x = v%x / mag
            res%y = v%y / mag
            res%z = v%z / mag
        else
            res = make_point3d(0.0d0, 0.0d0, 0.0d0)
        end if
    end function vector_normalize
    
    !> Scale vector by factor
    function vector_scale(v, factor) result(res)
        type(point3d), intent(in) :: v
        real(8), intent(in) :: factor
        type(point3d) :: res
        res%x = v%x * factor
        res%y = v%y * factor
        res%z = v%z * factor
    end function vector_scale
    
    !==========================================================================
    ! Line 2D Operations
    !==========================================================================
    
    !> Create a line from two points (ax + by + c = 0)
    function line_from_points(p1, p2) result(res)
        type(point2d), intent(in) :: p1, p2
        type(line2d) :: res
        res%a = p2%y - p1%y
        res%b = p1%x - p2%x
        res%c = p2%x * p1%y - p1%x * p2%y
    end function line_from_points
    
    !> Distance from point to line (2D)
    function distance_point_to_line2d(p, line) result(res)
        type(point2d), intent(in) :: p
        type(line2d), intent(in) :: line
        real(8) :: res, denom
        denom = sqrt(line%a**2 + line%b**2)
        if (denom > EPSILON) then
            res = abs(line%a * p%x + line%b * p%y + line%c) / denom
        else
            res = 0.0d0
        end if
    end function distance_point_to_line2d
    
    !> Distance from point to line segment (2D)
    function distance_point_to_segment2d(p, seg) result(res)
        type(point2d), intent(in) :: p
        type(segment2d), intent(in) :: seg
        real(8) :: res
        real(8) :: dx, dy, t, closest_x, closest_y, seg_len_sq
        
        dx = seg%p2%x - seg%p1%x
        dy = seg%p2%y - seg%p1%y
        seg_len_sq = dx**2 + dy**2
        
        if (seg_len_sq < EPSILON) then
            ! Segment is a point
            res = distance_point2d(p, seg%p1)
            return
        end if
        
        ! Parameter t for projection onto line
        t = ((p%x - seg%p1%x) * dx + (p%y - seg%p1%y) * dy) / seg_len_sq
        t = max(0.0d0, min(1.0d0, t))
        
        closest_x = seg%p1%x + t * dx
        closest_y = seg%p1%y + t * dy
        
        res = sqrt((p%x - closest_x)**2 + (p%y - closest_y)**2)
    end function distance_point_to_segment2d
    
    !> Check if two line segments intersect
    function segments_intersect(seg1, seg2) result(res)
        type(segment2d), intent(in) :: seg1, seg2
        logical :: res
        real(8) :: d1, d2, d3, d4
        
        d1 = cross_product_2d(seg2%p1, seg2%p2, seg1%p1)
        d2 = cross_product_2d(seg2%p1, seg2%p2, seg1%p2)
        d3 = cross_product_2d(seg1%p1, seg1%p2, seg2%p1)
        d4 = cross_product_2d(seg1%p1, seg1%p2, seg2%p2)
        
        if (((d1 > 0.0d0 .and. d2 < 0.0d0) .or. (d1 < 0.0d0 .and. d2 > 0.0d0)) .and. &
            ((d3 > 0.0d0 .and. d4 < 0.0d0) .or. (d3 < 0.0d0 .and. d4 > 0.0d0))) then
            res = .true.
        else
            res = .false.
        end if
    end function segments_intersect
    
    !> 2D cross product helper (for CCW tests)
    function cross_product_2d(o, a, b) result(res)
        type(point2d), intent(in) :: o, a, b
        real(8) :: res
        res = (a%x - o%x) * (b%y - o%y) - (a%y - o%y) * (b%x - o%x)
    end function cross_product_2d
    
    !==========================================================================
    ! Triangle 2D Operations
    !==========================================================================
    
    !> Create a triangle from three points
    function make_triangle2d(p1, p2, p3) result(res)
        type(point2d), intent(in) :: p1, p2, p3
        type(triangle2d) :: res
        res%p1 = p1
        res%p2 = p2
        res%p3 = p3
    end function make_triangle2d
    
    !> Calculate area of triangle (2D)
    function area_triangle2d(tri) result(res)
        type(triangle2d), intent(in) :: tri
        real(8) :: res
        res = abs((tri%p2%x - tri%p1%x) * (tri%p3%y - tri%p1%y) - &
                  (tri%p3%x - tri%p1%x) * (tri%p2%y - tri%p1%y)) / 2.0d0
    end function area_triangle2d
    
    !> Calculate centroid of triangle (2D)
    function centroid_triangle2d(tri) result(res)
        type(triangle2d), intent(in) :: tri
        type(point2d) :: res
        res%x = (tri%p1%x + tri%p2%x + tri%p3%x) / 3.0d0
        res%y = (tri%p1%y + tri%p2%y + tri%p3%y) / 3.0d0
    end function centroid_triangle2d
    
    !> Calculate circumcenter of triangle (2D)
    function circumcenter(tri) result(res)
        type(triangle2d), intent(in) :: tri
        type(point2d) :: res
        real(8) :: d, ax, ay, bx, by, cx, cy
        
        ax = tri%p1%x
        ay = tri%p1%y
        bx = tri%p2%x
        by = tri%p2%y
        cx = tri%p3%x
        cy = tri%p3%y
        
        d = 2.0d0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        
        if (abs(d) < EPSILON) then
            res%x = 0.0d0
            res%y = 0.0d0
            return
        end if
        
        res%x = ((ax**2 + ay**2) * (by - cy) + &
                 (bx**2 + by**2) * (cy - ay) + &
                 (cx**2 + cy**2) * (ay - by)) / d
        res%y = ((ax**2 + ay**2) * (cx - bx) + &
                 (bx**2 + by**2) * (ax - cx) + &
                 (cx**2 + cy**2) * (bx - ax)) / d
    end function circumcenter
    
    !> Calculate circumradius of triangle (2D)
    function circumradius(tri) result(res)
        type(triangle2d), intent(in) :: tri
        real(8) :: res
        real(8) :: a, b, c, s, area_val
        
        a = distance_point2d(tri%p2, tri%p3)
        b = distance_point2d(tri%p1, tri%p3)
        c = distance_point2d(tri%p1, tri%p2)
        area_val = area_triangle2d(tri)
        
        if (area_val < EPSILON) then
            res = 0.0d0
        else
            res = (a * b * c) / (4.0d0 * area_val)
        end if
    end function circumradius
    
    !> Check if point is inside triangle
    function point_in_triangle(p, tri) result(res)
        type(point2d), intent(in) :: p
        type(triangle2d), intent(in) :: tri
        logical :: res
        real(8) :: d1, d2, d3
        logical :: has_neg, has_pos
        
        d1 = cross_product_2d(tri%p1, tri%p2, p)
        d2 = cross_product_2d(tri%p2, tri%p3, p)
        d3 = cross_product_2d(tri%p3, tri%p1, p)
        
        has_neg = (d1 < 0.0d0) .or. (d2 < 0.0d0) .or. (d3 < 0.0d0)
        has_pos = (d1 > 0.0d0) .or. (d2 > 0.0d0) .or. (d3 > 0.0d0)
        
        res = .not. (has_neg .and. has_pos)
    end function point_in_triangle
    
    !==========================================================================
    ! Circle 2D Operations
    !==========================================================================
    
    !> Create a circle from center and radius
    function make_circle2d(center, radius) result(res)
        type(point2d), intent(in) :: center
        real(8), intent(in) :: radius
        type(circle2d) :: res
        res%center = center
        res%radius = radius
    end function make_circle2d
    
    !> Calculate area of circle (2D)
    function area_circle2d(circle) result(res)
        type(circle2d), intent(in) :: circle
        real(8) :: res
        res = PI * circle%radius**2
    end function area_circle2d
    
    !> Calculate circumference of circle (2D)
    function perimeter_circle2d(circle) result(res)
        type(circle2d), intent(in) :: circle
        real(8) :: res
        res = 2.0d0 * PI * circle%radius
    end function perimeter_circle2d
    
    !> Check if circle contains a point
    function circle_contains_point(circle, p) result(res)
        type(circle2d), intent(in) :: circle
        type(point2d), intent(in) :: p
        logical :: res
        res = distance_point2d(circle%center, p) <= circle%radius
    end function circle_contains_point
    
    !> Check if circle intersects with rectangle
    function circle_rectangle_intersect(circle, rect) result(res)
        type(circle2d), intent(in) :: circle
        type(rectangle2d), intent(in) :: rect
        logical :: res
        real(8) :: closest_x, closest_y, dist_sq
        
        closest_x = max(rect%x, min(circle%center%x, rect%x + rect%width))
        closest_y = max(rect%y, min(circle%center%y, rect%y + rect%height))
        
        dist_sq = (circle%center%x - closest_x)**2 + (circle%center%y - closest_y)**2
        res = dist_sq <= circle%radius**2
    end function circle_rectangle_intersect
    
    !> Circle from three points
    function circle_from_three_points(p1, p2, p3) result(res)
        type(point2d), intent(in) :: p1, p2, p3
        type(circle2d) :: res
        real(8) :: ax, ay, bx, by, cx, cy, d, ux, uy, vx, vy, w
        
        ax = p1%x; ay = p1%y
        bx = p2%x; by = p2%y
        cx = p3%x; cy = p3%y
        
        d = 2.0d0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        
        if (abs(d) < EPSILON) then
            res%center = make_point2d(0.0d0, 0.0d0)
            res%radius = 0.0d0
            return
        end if
        
        ux = (ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)
        uy = (ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)
        
        res%center%x = ux / d
        res%center%y = uy / d
        res%radius = distance_point2d(res%center, p1)
    end function circle_from_three_points
    
    !==========================================================================
    ! Rectangle 2D Operations
    !==========================================================================
    
    !> Create a rectangle from position and size
    function make_rectangle2d(x, y, width, height) result(res)
        real(8), intent(in) :: x, y, width, height
        type(rectangle2d) :: res
        res%x = x
        res%y = y
        res%width = width
        res%height = height
    end function make_rectangle2d
    
    !> Calculate area of rectangle (2D)
    function area_rectangle2d(rect) result(res)
        type(rectangle2d), intent(in) :: rect
        real(8) :: res
        res = rect%width * rect%height
    end function area_rectangle2d
    
    !> Calculate perimeter of rectangle (2D)
    function perimeter_rectangle2d(rect) result(res)
        type(rectangle2d), intent(in) :: rect
        real(8) :: res
        res = 2.0d0 * (rect%width + rect%height)
    end function perimeter_rectangle2d
    
    !> Check if rectangle contains a point
    function rectangle_contains_point(rect, p) result(res)
        type(rectangle2d), intent(in) :: rect
        type(point2d), intent(in) :: p
        logical :: res
        res = (p%x >= rect%x .and. p%x <= rect%x + rect%width .and. &
               p%y >= rect%y .and. p%y <= rect%y + rect%height)
    end function rectangle_contains_point
    
    !> Get bounding box corners
    function rectangle_corners(rect) result(corners)
        type(rectangle2d), intent(in) :: rect
        type(point2d) :: corners(4)
        
        corners(1) = make_point2d(rect%x, rect%y)                              ! Bottom-left
        corners(2) = make_point2d(rect%x + rect%width, rect%y)                 ! Bottom-right
        corners(3) = make_point2d(rect%x + rect%width, rect%y + rect%height)   ! Top-right
        corners(4) = make_point2d(rect%x, rect%y + rect%height)                 ! Top-left
    end function rectangle_corners
    
    !==========================================================================
    ! Polygon 2D Operations
    !==========================================================================
    
    !> Calculate area of polygon using Shoelace formula (2D)
    function area_polygon2d(points) result(res)
        type(point2d), intent(in) :: points(:)
        real(8) :: res
        integer :: n, i
        
        n = size(points)
        if (n < 3) then
            res = 0.0d0
            return
        end if
        
        res = 0.0d0
        do i = 1, n
            res = res + points(i)%x * points(modulo(i, n) + 1)%y
            res = res - points(modulo(i, n) + 1)%x * points(i)%y
        end do
        res = abs(res) / 2.0d0
    end function area_polygon2d
    
    !> Calculate perimeter of polygon (2D)
    function perimeter_polygon2d(points) result(res)
        type(point2d), intent(in) :: points(:)
        real(8) :: res
        integer :: n, i
        
        n = size(points)
        if (n < 2) then
            res = 0.0d0
            return
        end if
        
        res = 0.0d0
        do i = 1, n
            res = res + distance_point2d(points(i), points(modulo(i, n) + 1))
        end do
    end function perimeter_polygon2d
    
    !> Calculate centroid of polygon (2D)
    function centroid_polygon2d(points) result(res)
        type(point2d), intent(in) :: points(:)
        type(point2d) :: res
        integer :: n, i
        real(8) :: area_val, cross
        
        n = size(points)
        if (n < 3) then
            res = make_point2d(0.0d0, 0.0d0)
            return
        end if
        
        area_val = 0.0d0
        res%x = 0.0d0
        res%y = 0.0d0
        
        do i = 1, n
            cross = points(i)%x * points(modulo(i, n) + 1)%y - &
                    points(modulo(i, n) + 1)%x * points(i)%y
            area_val = area_val + cross
            res%x = res%x + (points(i)%x + points(modulo(i, n) + 1)%x) * cross
            res%y = res%y + (points(i)%y + points(modulo(i, n) + 1)%y) * cross
        end do
        
        area_val = area_val / 2.0d0
        if (abs(area_val) > EPSILON) then
            res%x = res%x / (6.0d0 * area_val)
            res%y = res%y / (6.0d0 * area_val)
        end if
    end function centroid_polygon2d
    
    !> Check if polygon is convex
    function is_convex_polygon(points) result(res)
        type(point2d), intent(in) :: points(:)
        logical :: res
        integer :: n, i
        real(8) :: cross, prev_cross
        
        n = size(points)
        if (n < 3) then
            res = .false.
            return
        end if
        
        prev_cross = 0.0d0
        do i = 1, n
            cross = cross_product_2d(points(i), &
                                     points(modulo(i, n) + 1), &
                                     points(modulo(i+1, n) + 1))
            if (abs(cross) > EPSILON) then
                if (prev_cross * cross < 0.0d0) then
                    res = .false.
                    return
                end if
                prev_cross = cross
            end if
        end do
        res = .true.
    end function is_convex_polygon
    
    !==========================================================================
    ! Plane 3D Operations
    !==========================================================================
    
    !> Create a plane from point and normal
    function plane_from_point_normal(point, normal) result(res)
        type(point3d), intent(in) :: point, normal
        type(plane3d) :: res
        type(point3d) :: n
        n = vector_normalize(normal)
        res%a = n%x
        res%b = n%y
        res%c = n%z
        res%d = -(res%a * point%x + res%b * point%y + res%c * point%z)
    end function plane_from_point_normal
    
    !> Create a plane from three points
    function plane_from_three_points(p1, p2, p3) result(res)
        type(point3d), intent(in) :: p1, p2, p3
        type(plane3d) :: res
        type(point3d) :: v1, v2, normal
        
        v1 = vector_sub(p2, p1)
        v2 = vector_sub(p3, p1)
        normal = vector_cross(v1, v2)
        res = plane_from_point_normal(p1, normal)
    end function plane_from_three_points
    
    !> Distance from point to plane (3D)
    function distance_point_to_plane3d(p, plane) result(res)
        type(point3d), intent(in) :: p
        type(plane3d), intent(in) :: plane
        real(8) :: res, denom
        
        denom = sqrt(plane%a**2 + plane%b**2 + plane%c**2)
        if (denom > EPSILON) then
            res = abs(plane%a * p%x + plane%b * p%y + plane%c * p%z + plane%d) / denom
        else
            res = 0.0d0
        end if
    end function distance_point_to_plane3d
    
    !> Project point onto plane
    function project_point_to_plane(p, plane) result(res)
        type(point3d), intent(in) :: p
        type(plane3d), intent(in) :: plane
        type(point3d) :: res
        real(8) :: dist, denom
        
        denom = plane%a**2 + plane%b**2 + plane%c**2
        if (abs(denom) < EPSILON) then
            res = p
            return
        end if
        
        dist = (plane%a * p%x + plane%b * p%y + plane%c * p%z + plane%d) / denom
        res%x = p%x - plane%a * dist
        res%y = p%y - plane%b * dist
        res%z = p%z - plane%c * dist
    end function project_point_to_plane
    
    !==========================================================================
    ! Sphere 3D Operations
    !==========================================================================
    
    !> Create a sphere from center and radius
    function make_sphere3d(center, radius) result(res)
        type(point3d), intent(in) :: center
        real(8), intent(in) :: radius
        type(sphere3d) :: res
        res%center = center
        res%radius = radius
    end function make_sphere3d
    
    !> Calculate volume of sphere (3D)
    function volume_sphere3d(sphere) result(res)
        type(sphere3d), intent(in) :: sphere
        real(8) :: res
        res = (4.0d0 / 3.0d0) * PI * sphere%radius**3
    end function volume_sphere3d
    
    !> Calculate surface area of sphere (3D)
    function surface_area_sphere3d(sphere) result(res)
        type(sphere3d), intent(in) :: sphere
        real(8) :: res
        res = 4.0d0 * PI * sphere%radius**2
    end function surface_area_sphere3d
    
    !> Check if sphere contains a point
    function sphere_contains_point(sphere, p) result(res)
        type(sphere3d), intent(in) :: sphere
        type(point3d), intent(in) :: p
        logical :: res
        res = distance_point3d(sphere%center, p) <= sphere%radius
    end function sphere_contains_point
    
    !> Check if two spheres intersect
    function sphere_intersect(s1, s2) result(res)
        type(sphere3d), intent(in) :: s1, s2
        logical :: res
        real(8) :: dist
        dist = distance_point3d(s1%center, s2%center)
        res = dist <= (s1%radius + s2%radius)
    end function sphere_intersect
    
    !==========================================================================
    ! AABB 3D (Axis-Aligned Bounding Box) Operations
    !==========================================================================
    
    !> Create an AABB from two corner points
    function make_aabb3d(p1, p2) result(res)
        type(point3d), intent(in) :: p1, p2
        type(aabb3d) :: res
        
        res%min_pt%x = min(p1%x, p2%x)
        res%min_pt%y = min(p1%y, p2%y)
        res%min_pt%z = min(p1%z, p2%z)
        res%max_pt%x = max(p1%x, p2%x)
        res%max_pt%y = max(p1%y, p2%y)
        res%max_pt%z = max(p1%z, p2%z)
    end function make_aabb3d
    
    !> Calculate volume of AABB (3D)
    function volume_aabb3d(box) result(res)
        type(aabb3d), intent(in) :: box
        real(8) :: res
        res = (box%max_pt%x - box%min_pt%x) * &
              (box%max_pt%y - box%min_pt%y) * &
              (box%max_pt%z - box%min_pt%z)
    end function volume_aabb3d
    
    !> Calculate surface area of AABB (3D)
    function surface_area_aabb3d(box) result(res)
        type(aabb3d), intent(in) :: box
        real(8) :: res
        real(8) :: w, h, d
        
        w = box%max_pt%x - box%min_pt%x
        h = box%max_pt%y - box%min_pt%y
        d = box%max_pt%z - box%min_pt%z
        
        res = 2.0d0 * (w*h + h*d + d*w)
    end function surface_area_aabb3d
    
    !> Check if AABB contains a point
    function aabb_contains_point(box, p) result(res)
        type(aabb3d), intent(in) :: box
        type(point3d), intent(in) :: p
        logical :: res
        
        res = (p%x >= box%min_pt%x .and. p%x <= box%max_pt%x .and. &
               p%y >= box%min_pt%y .and. p%y <= box%max_pt%y .and. &
               p%z >= box%min_pt%z .and. p%z <= box%max_pt%z)
    end function aabb_contains_point
    
    !> Check if two AABBs intersect
    function aabb_intersect(box1, box2) result(res)
        type(aabb3d), intent(in) :: box1, box2
        logical :: res
        
        res = (box1%min_pt%x <= box2%max_pt%x .and. box1%max_pt%x >= box2%min_pt%x) .and. &
              (box1%min_pt%y <= box2%max_pt%y .and. box1%max_pt%y >= box2%min_pt%y) .and. &
              (box1%min_pt%z <= box2%max_pt%z .and. box1%max_pt%z >= box2%min_pt%z)
    end function aabb_intersect
    
    !> Get center of AABB
    function aabb_center(box) result(res)
        type(aabb3d), intent(in) :: box
        type(point3d) :: res
        
        res%x = (box%min_pt%x + box%max_pt%x) / 2.0d0
        res%y = (box%min_pt%y + box%max_pt%y) / 2.0d0
        res%z = (box%min_pt%z + box%max_pt%z) / 2.0d0
    end function aabb_center
    
    !==========================================================================
    ! Utility Functions
    !==========================================================================
    
    !> Convert degrees to radians
    function deg_to_rad(degrees) result(res)
        real(8), intent(in) :: degrees
        real(8) :: res
        res = degrees * PI / 180.0d0
    end function deg_to_rad
    
    !> Convert radians to degrees
    function rad_to_deg(radians) result(res)
        real(8), intent(in) :: radians
        real(8) :: res
        res = radians * 180.0d0 / PI
    end function rad_to_deg
    
    !> Clamp value between min and max
    function clamp_value(value, min_val, max_val) result(res)
        real(8), intent(in) :: value, min_val, max_val
        real(8) :: res
        res = max(min_val, min(max_val, value))
    end function clamp_value
    
    !> Linear interpolation between two values
    function lerp(a, b, t) result(res)
        real(8), intent(in) :: a, b, t
        real(8) :: res
        res = a + t * (b - a)
    end function lerp
    
    !> Check if two values are approximately equal
    function approx_equal(a, b, tol) result(res)
        real(8), intent(in) :: a, b
        real(8), intent(in), optional :: tol
        logical :: res
        real(8) :: tolerance
        
        if (present(tol)) then
            tolerance = tol
        else
            tolerance = EPSILON
        end if
        
        res = abs(a - b) < tolerance
    end function approx_equal
    
end module geometry_utils