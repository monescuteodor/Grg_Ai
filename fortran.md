# Fortran Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH FORTRAN


## Remarks

Fortran (Formula Translation) is the oldest high-level programming language, created in 1957. It remains dominant in scientific computing, numerical analysis, weather forecasting, and HPC. Modern Fortran (2003/2008/2018) is a full-featured OOP language with excellent array operations and parallel computing support.

Standards: Fortran 77, 90, 95, 2003, 2008, 2018.
Tools: gfortran (GCC), ifort (Intel), nvfortran (NVIDIA), flang (LLVM).


## Hello World

```fortran
! hello.f90
program hello
    implicit none
    print *, "Hello, World!"
    write(*, '(A)') "Hello, Fortran!"
    write(*, '(A, A, A)') "Hello, ", "modern ", "Fortran!"
end program hello
```

```bash
gfortran hello.f90 -o hello && ./hello
gfortran -O2 -o hello hello.f90
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Intrinsic Types

```fortran
program types_demo
    implicit none

    ! Integer kinds
    integer :: i           ! default integer
    integer(kind=1) :: i8  ! 8-bit
    integer(kind=2) :: i16 ! 16-bit
    integer(kind=4) :: i32 ! 32-bit
    integer(kind=8) :: i64 ! 64-bit

    ! Real kinds
    real :: r              ! single precision (~7 digits)
    real(kind=8) :: d      ! double precision (~15 digits)
    double precision :: dp ! same as real(8)
    real(kind=16) :: quad  ! quad precision (gfortran extension)

    ! Complex
    complex :: z
    complex(kind=8) :: dz

    ! Logical
    logical :: flag

    ! Character
    character(len=20) :: name
    character :: single_char

    ! Constants (parameters)
    integer, parameter :: N = 100
    real, parameter :: PI = 3.14159265358979_8  ! _8 = double

    ! Assignments
    i = 42
    d = 3.14159265358979d0   ! d0 or D0 = double
    r = 3.14
    z = (3.0, 4.0)           ! real + imaginary parts
    flag = .true.             ! .TRUE. or .FALSE.
    name = "Alice"
    name = 'Bob'

    ! Print
    print *, i, d, flag, name

    ! Arithmetic
    print *, 10 / 3          ! 3 (integer division!)
    print *, 10.0 / 3.0      ! 3.333...
    print *, 10 ** 3         ! 1000
    print *, mod(17, 5)      ! 2
    print *, abs(-5)         ! 5
    print *, sqrt(16.0)      ! 4.0
    print *, sin(0.0), cos(0.0)
    print *, exp(1.0), log(exp(1.0))
    print *, max(3, 7, 2), min(3, 7, 2)
    print *, floor(3.7), ceiling(3.2), nint(3.5)

    ! Type conversion
    print *, real(42)        ! 42.0
    print *, int(3.7)        ! 3
    print *, dble(3.14)      ! 3.14 as double

end program types_demo
```


---

# CHAPTER 3: ARRAYS


## Array Operations

```fortran
program array_demo
    implicit none

    ! 1D array
    integer, dimension(5) :: arr = [1, 2, 3, 4, 5]
    integer :: v(10)   ! uninitialized
    real :: x(100)

    ! 2D array
    real :: mat(3, 3)
    real :: grid(100, 100)

    ! Array literal
    arr = [10, 20, 30, 40, 50]

    ! Access (1-indexed!)
    print *, arr(1)      ! 10
    print *, arr(5)      ! 50

    ! Slices
    print *, arr(2:4)    ! 20 30 40
    print *, arr(1:5:2)  ! 10 30 50 (every 2nd)
    print *, arr(:3)     ! 10 20 30
    print *, arr(3:)     ! 30 40 50
    print *, arr(::-1)   ! 50 40 30 20 10 (reversed)

    ! Whole-array operations (vectorized!)
    arr = arr * 2        ! element-wise multiply
    arr = arr + 100      ! element-wise add
    print *, arr

    ! Array intrinsics
    print *, size(arr)       ! 5
    print *, size(mat, 1)    ! 3 (first dimension)
    print *, shape(arr)      ! [5]
    print *, shape(mat)      ! [3, 3]
    print *, lbound(arr, 1)  ! 1 (lower bound)
    print *, ubound(arr, 1)  ! 5 (upper bound)

    ! Mathematical intrinsics (work on whole arrays)
    x = [(real(i), i=1,100)]   ! implied do loop: 1.0 to 100.0
    print *, sum(x)            ! 5050.0
    print *, product(arr)      ! product of all elements
    print *, maxval(arr), minval(arr)
    print *, maxloc(arr), minloc(arr)  ! index of max/min
    print *, dot_product([1,2,3], [4,5,6])   ! 32

    ! Matrix operations
    mat = reshape([1,2,3,4,5,6,7,8,9], [3,3])
    print *, matmul(mat, mat)  ! matrix multiply
    print *, transpose(mat)    ! transpose

    ! Element-wise functions
    x = sin(x) + cos(x)   ! applied element-wise
    x = where(x > 0, x, -x)  ! element-wise abs

    ! Allocatable arrays
    real, allocatable :: dynamic(:)
    allocate(dynamic(100))
    dynamic = 0.0
    deallocate(dynamic)

    ! 2D allocatable
    real, allocatable :: m(:,:)
    allocate(m(3, 4))
    m = 0.0
    m(2, 3) = 42.0
    deallocate(m)

end program array_demo
```


---

# CHAPTER 4: CONTROL FLOW


## Control Structures

```fortran
program control_demo
    implicit none
    integer :: i, j, n
    real :: x
    logical :: found

    x = 3.7

    ! if/else if/else
    if (x > 0) then
        print *, "positive"
    else if (x < 0) then
        print *, "negative"
    else
        print *, "zero"
    end if

    ! Single-line if
    if (x > 0) print *, "positive"

    ! Logical operators
    ! .and. .or. .not. .eqv. .neqv.
    if (x > 0 .and. x < 10) print *, "small positive"
    if (x < 0 .or. x > 100) print *, "out of range"
    if (.not. (x == 0)) print *, "non-zero"

    ! do loop
    do i = 1, 10
        write(*, '(I3)', advance='no') i
    end do
    print *

    ! do with step
    do i = 1, 10, 2
        print *, i
    end do

    ! do while
    n = 1
    do while (n < 100)
        n = n * 2
    end do
    print *, n   ! 128

    ! Infinite loop with exit
    do
        n = n - 1
        if (n < 50) exit
    end do

    ! cycle (continue)
    do i = 1, 10
        if (mod(i, 2) == 0) cycle
        print *, i   ! odd numbers only
    end do

    ! Nested loops with named labels
    outer: do i = 1, 5
        inner: do j = 1, 5
            if (i * j > 15) exit outer
            if (i == j) cycle inner
            print *, i, j
        end do inner
    end do outer

    ! select case
    select case (i)
        case (1)
            print *, "one"
        case (2, 3)
            print *, "two or three"
        case (4:10)
            print *, "4 to 10"
        case default
            print *, "other"
    end select

    ! select case on characters
    select case (name(1:1))
        case ('A':'M')
            print *, "first half"
        case ('N':'Z', 'a':'z')
            print *, "second half or lowercase"
        case default
            print *, "not a letter"
    end select

end program control_demo
```


---

# CHAPTER 5: SUBROUTINES AND FUNCTIONS


## Procedures

```fortran
program procedures_demo
    implicit none
    integer :: result, a, b
    real :: r, area

    ! Call subroutine
    call swap(a, b)
    call print_hello("Alice")

    ! Call function
    result = factorial(10)
    area = circle_area(5.0)
    print *, "10! =", result
    print *, "Area =", area

contains

    ! Subroutine (no return value)
    subroutine swap(x, y)
        implicit none
        integer, intent(inout) :: x, y
        integer :: temp
        temp = x
        x = y
        y = temp
    end subroutine swap

    ! Subroutine with intent
    ! intent(in)    — read-only
    ! intent(out)   — write-only (must be set)
    ! intent(inout) — read-write (default if omitted)
    subroutine print_hello(name)
        implicit none
        character(len=*), intent(in) :: name
        print *, "Hello, " // trim(name) // "!"
    end subroutine print_hello

    ! Function (returns value)
    integer function factorial(n)
        implicit none
        integer, intent(in) :: n
        integer :: i
        factorial = 1
        do i = 2, n
            factorial = factorial * i
        end do
    end function factorial

    ! Real function
    real function circle_area(radius)
        implicit none
        real, intent(in) :: radius
        real, parameter :: PI = 3.14159265
        circle_area = PI * radius**2
    end function circle_area

    ! Recursive function
    recursive integer function fib(n) result(res)
        implicit none
        integer, intent(in) :: n
        if (n <= 1) then
            res = n
        else
            res = fib(n-1) + fib(n-2)
        end if
    end function fib

    ! Array function
    function vec_sum(v) result(s)
        implicit none
        real, intent(in) :: v(:)   ! assumed-shape array
        real :: s
        s = sum(v)
    end function vec_sum

    ! Returning an array
    function linspace(a, b, n) result(v)
        implicit none
        real, intent(in) :: a, b
        integer, intent(in) :: n
        real :: v(n)
        integer :: i
        do i = 1, n
            v(i) = a + (b - a) * (i - 1) / (n - 1)
        end do
    end function linspace

end program procedures_demo
```


---

# CHAPTER 6: MODULES AND DERIVED TYPES


## Modules and OOP

```fortran
! geometry.f90
module geometry
    implicit none
    private                      ! everything private by default

    real, parameter, public :: PI = 3.14159265358979

    type, public :: Point
        real :: x, y
    end type Point

    type, public :: Circle
        type(Point) :: center
        real :: radius
    contains
        procedure :: area    => circle_area
        procedure :: perimeter => circle_perim
        procedure :: print   => circle_print
    end type Circle

    public :: distance

contains

    real function circle_area(self)
        class(Circle), intent(in) :: self
        circle_area = PI * self%radius**2
    end function circle_area

    real function circle_perim(self)
        class(Circle), intent(in) :: self
        circle_perim = 2 * PI * self%radius
    end function circle_perim

    subroutine circle_print(self)
        class(Circle), intent(in) :: self
        print *, "Circle at (", self%center%x, ",", self%center%y, &
                 ") r=", self%radius
    end subroutine circle_print

    real function distance(p1, p2)
        type(Point), intent(in) :: p1, p2
        distance = sqrt((p1%x - p2%x)**2 + (p1%y - p2%y)**2)
    end function distance

end module geometry

! Usage
program use_geometry
    use geometry
    implicit none

    type(Circle) :: c
    type(Point) :: p1, p2

    c%center = Point(0.0, 0.0)
    c%radius = 5.0
    call c%print()
    print *, "Area:", c%area()
    print *, "Perimeter:", c%perimeter()

    p1 = Point(0.0, 0.0)
    p2 = Point(3.0, 4.0)
    print *, "Distance:", distance(p1, p2)   ! 5.0

end program use_geometry
```


---

# CHAPTER 7: FILE I/O


## Input and Output

```fortran
program io_demo
    implicit none
    integer :: unit_num, ios, i
    character(len=100) :: line
    real :: x, y, z

    ! Open a file
    open(unit=10, file='data.txt', status='replace', action='write', &
         iostat=ios)
    if (ios /= 0) stop "Error opening file"

    ! Write to file
    write(10, '(A)') "Hello, World!"
    write(10, '(I5, F10.4)') 42, 3.14159
    do i = 1, 5
        write(10, '(I3, F8.3)') i, real(i) * 1.5
    end do
    close(10)

    ! Open for reading
    open(unit=20, file='data.txt', status='old', action='read')
    read(20, '(A)') line
    print *, trim(line)

    read(20, *) i, x   ! free-format read
    print *, i, x

    ! Read until EOF
    do
        read(20, *, iostat=ios) x
        if (ios /= 0) exit
        print *, x
    end do
    close(20)

    ! Append to file
    open(unit=30, file='log.txt', status='unknown', position='append')
    write(30, '(A, I5)') "Run number:", 42
    close(30)

    ! Standard I/O
    write(*, '(A)', advance='no') "Enter a number: "
    read(*, *) x
    print *, "You entered:", x

    ! Formatted output
    write(*, '(I10)')  42         ! right-justified integer
    write(*, '(F12.4)') 3.14159  ! float with 4 decimals
    write(*, '(E15.6)') 1.23e-10 ! scientific notation
    write(*, '(A20)')  "hello"   ! left-padded string
    write(*, '(3I5)')  1, 2, 3   ! 3 integers each width 5
    write(*, '(*(G15.6))') (real(i), i=1,5)  ! unlimited

    ! Internal I/O (string <-> value)
    character(len=20) :: str
    write(str, '(F8.3)') 3.14159
    print *, trim(str)   ! " 3.142"

    read(str, *) x
    print *, x

end program io_demo
```


---

# CHAPTER 8: COARRAYS AND PARALLEL COMPUTING


## Modern Fortran Parallelism

```fortran
! Coarrays — Fortran 2008 parallel programming
program coarray_demo
    implicit none
    integer :: n[*]        ! coarray — each image has its own copy
    real :: x[*]
    integer :: me, num_images_val

    me = this_image()
    num_images_val = num_images()

    n = me * 10   ! each image sets its own n

    sync all      ! barrier — wait for all images

    ! Image 1 reads from all images
    if (me == 1) then
        do i = 1, num_images_val
            print *, "Image", i, "has n =", n[i]
        end do
    end if

    ! Critical section
    critical
        print *, "Image", me, "in critical section"
    end critical

    ! Coarray assignment
    if (me == 1) then
        n[2] = 999     ! put value to image 2
    end if
    sync all

    ! event_type (Fortran 2018)
    ! integer(event_kind) :: ev[*]
    ! event post(ev[me+1])   ! signal next image
    ! event wait(ev[me])     ! wait for signal

end program coarray_demo

! OpenMP (shared-memory parallelism)
program openmp_demo
    use omp_lib
    implicit none
    integer :: i, tid, nthreads
    real :: sum_val

    !$omp parallel private(tid) shared(nthreads)
    tid = omp_get_thread_num()
    nthreads = omp_get_num_threads()
    print *, "Thread", tid, "of", nthreads
    !$omp end parallel

    ! Parallel do loop
    sum_val = 0.0
    !$omp parallel do reduction(+:sum_val)
    do i = 1, 1000000
        sum_val = sum_val + real(i)
    end do
    !$omp end parallel do
    print *, "Sum:", sum_val

    ! Parallel sections
    !$omp parallel sections
    !$omp section
    call task_a()
    !$omp section
    call task_b()
    !$omp end parallel sections

end program openmp_demo
```
