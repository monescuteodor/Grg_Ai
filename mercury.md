# Mercury Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH MERCURY


## Remarks

Mercury is a purely declarative logic/functional programming language designed for real-world software. Created at the University of Melbourne (1995) by Zoltan Somogyi. Mercury combines Prolog-style logic programming with Haskell-style type/mode system, producing efficient compiled code. It enforces determinism modes (det, semidet, nondet, multi) at compile time.

Tools: `mmc` (Mercury compiler), `mmake` (build tool), generates C then compiles to native code.


## Hello World

```mercury
% hello.m
:- module hello.
:- interface.

:- import_module io.

:- pred main(io::di, io::uo) is det.

:- implementation.

main(!IO) :-
    io.write_string("Hello, World!\n", !IO),
    io.write_string("Hello, Mercury!\n", !IO).
```

```bash
mmc --make hello          # compile
./hello                   # run
mmc hello.m -o hello      # manual compile
```

### Program Structure

```mercury
% Every Mercury file is a module
:- module mymodule.      % module declaration

% Interface: public exports
:- interface.
:- import_module io.     % imports for interface

:- type mytype ---> value1 ; value2.  % exported type

:- pred mypred(int::in, int::out) is det.  % exported predicate

% Implementation: private details
:- implementation.
:- import_module string.  % imports for implementation

mypred(X, Y) :-
    Y = X * 2.
```


---

# CHAPTER 2: TYPES AND DATA


## Mercury Type System

```mercury
:- module types_demo.
:- interface.
:- implementation.

:- import_module int, float, string, char, bool, list.

% === BASIC TYPES ===
% int     - machine integers
% float   - double-precision floating point
% char    - Unicode character
% string  - string
% bool    - yes | no  (not true/false!)

% === ALGEBRAIC DATA TYPES ===

% Enumeration
:- type color ---> red ; green ; blue ; yellow.

% Record-like type
:- type point --->
    point(x :: int, y :: int).

% Recursive type
:- type list(T) ---> [] ; [T | list(T)].
% Built-in, shown for illustration

% Tree
:- type tree(T) --->
    empty ;
    node(tree(T), T, tree(T)).

% Maybe (option)
:- type maybe(T) --->
    yes(T) ;
    no.

% Result
:- type result(T, E) --->
    ok(T) ;
    error(E).

% === USING TYPES ===
:- pred demo is det.
demo :-
    P = point(3, 4),
    X = P ^ x,          % field access
    Y = P ^ y,
    io.format("Point: (%d, %d)\n", [i(X), i(Y)], !IO).

% Destructure
:- pred get_x(point::in, int::out) is det.
get_x(point(X, _), X).

% === TYPE PARAMETERS ===
:- type pair(A, B) ---> pair(A, B).

:- pred make_pair(A::in, B::in, pair(A, B)::out) is det.
make_pair(A, B, pair(A, B)).

% === EQUIVALENCE TYPES ===
:- type name == string.
:- type age == int.
```


---

# CHAPTER 3: MODES AND DETERMINISM


## Mercury's Unique Mode System

```mercury
:- module modes_demo.
:- interface.
:- import_module io.
:- implementation.
:- import_module int, list.

% === MODE DECLARATIONS ===
% in    - input (must be ground when called)
% out   - output (must be unbound when called, ground after)
% di    - destructive input (for IO state)
% uo    - unique output (for IO state)
% in(unique)  - unique input

% === DETERMINISM ANNOTATIONS ===
% det      - exactly one solution
% semidet  - zero or one solution
% nondet   - zero or more solutions
% multi    - one or more solutions
% cc_nondet - committed choice nondet (no backtracking)
% cc_multi  - committed choice multi

% det example
:- pred add(int::in, int::in, int::out) is det.
add(X, Y, Z) :-
    Z = X + Y.

% semidet example (may fail)
:- pred safe_divide(int::in, int::in, int::out) is semidet.
safe_divide(X, Y, Z) :-
    Y \= 0,            % fail if Y is zero
    Z = X / Y.

% nondet example (multiple solutions)
:- pred member(T, list(T)) is nondet.
% (built-in list.member is nondet)

% multi example (always at least one)
:- pred nonempty_member(T::out, list(T)::in) is multi.
nonempty_member(X, [X | _]).
nonempty_member(X, [_ | Xs]) :-
    nonempty_member(X, Xs).

% === MULTIPLE MODES ===
% Same predicate with different modes
:- pred append(list(T), list(T), list(T)).
:- mode append(in, in, out) is det.
:- mode append(out, out, in) is nondet.   % splits list
:- mode append(in, out, in) is semidet.

append([], Ys, Ys).
append([X|Xs], Ys, [X|Zs]) :-
    append(Xs, Ys, Zs).

% === IO STATE THREADING ===
% IO is pure through unique state threading
:- pred main(io::di, io::uo) is det.
main(!IO) :-
    io.write_string("Enter a number: ", !IO),
    io.read_term(Res, !IO),
    (
        Res = ok(term.functor(term.integer(_, N), [], _)),
        io.format("Double: %d\n", [i(N * 2)], !IO)
    ;
        Res = error(_, _),
        io.write_string("Invalid input\n", !IO)
    ;
        Res = eof,
        io.write_string("EOF\n", !IO)
    ).
```


---

# CHAPTER 4: PREDICATES AND FUNCTIONS


## Defining Logic and Functions

```mercury
:- module predicates.
:- interface.
:- implementation.
:- import_module int, float, list, string, math.

% === FUNCTIONS ===
% Functions are predicates with last arg as return value
:- func square(int) = int.
square(N) = N * N.

:- func factorial(int) = int.
factorial(N) = (N =< 1 -> 1 ; N * factorial(N - 1)).

% Function with pattern matching
:- func fib(int) = int.
fib(0) = 0.
fib(1) = 1.
fib(N) = fib(N-1) + fib(N-2) :- N > 1.

% Higher-order functions
:- func apply(func(T, U), T) = U.
apply(F, X) = F(X).

:- func compose(func(U, V), func(T, U), T) = V.
compose(F, G, X) = F(G(X)).

% === PREDICATES ===
% Predicates can succeed, fail, or have multiple solutions
:- pred between(int::in, int::in, int::out) is nondet.
between(Lo, Hi, X) :-
    Lo =< Hi,
    (
        X = Lo
    ;
        between(Lo + 1, Hi, X)
    ).

% Recursive predicate
:- pred sum_list(list(int)::in, int::out) is det.
sum_list([], 0).
sum_list([X|Xs], Sum) :-
    sum_list(Xs, Rest),
    Sum = X + Rest.

% === AGGREGATION ===
:- import_module solutions.

% Collect all solutions
:- pred all_between(int::in, int::in, list(int)::out) is det.
all_between(Lo, Hi, Xs) :-
    solutions(between(Lo, Hi), Xs).

% === IF-THEN-ELSE ===
:- pred classify(int::in, string::out) is det.
classify(N, Class) :-
    ( N > 0 ->
        Class = "positive"
    ; N < 0 ->
        Class = "negative"
    ;
        Class = "zero"
    ).

% === LAMBDA (anonymous predicate) ===
:- import_module higher_order.
% Using lambda expressions (Mercury extension):
% P = (pred(X::in, Y::out) is det :- Y = X * 2)
```


---

# CHAPTER 5: LISTS AND COLLECTIONS


## List Operations

```mercury
:- module lists_demo.
:- interface.
:- implementation.
:- import_module list, int, string, io.

:- pred list_examples is det.
list_examples :-
    % Create
    Xs = [1, 2, 3, 4, 5],
    [H|T] = Xs,          % head and tail
    
    % Standard predicates
    list.length(Xs, Len),
    list.append([1,2], [3,4], Combined),
    list.reverse(Xs, Rev),
    
    % Higher-order
    list.map(double, Xs, Doubled),
    list.filter(is_even, Xs, Evens),
    list.foldl(add, Xs, 0, Total),
    list.foldl(max_of, Xs, 0, MaxVal),
    
    io.format("Length: %d\n", [i(Len)], !IO),
    io.format("Head: %d\n", [i(H)], !IO),
    io.format("Total: %d\n", [i(Total)], !IO).

:- pred double(int::in, int::out) is det.
double(X, X * 2).

:- pred is_even(int::in) is semidet.
is_even(X) :- X mod 2 = 0.

:- pred add(int::in, int::in, int::out) is det.
add(X, Acc, Acc + X).

:- pred max_of(int::in, int::in, int::out) is det.
max_of(X, Acc, Max) :- Max = max(X, Acc).

% === SORTING ===
:- pred sort_demo is det.
sort_demo :-
    Xs = [3, 1, 4, 1, 5, 9, 2, 6],
    list.sort(Xs, Sorted),          % removes duplicates
    list.msort(Xs, Msorted),        % keeps duplicates
    io.write(Sorted, !IO), io.nl(!IO),
    io.write(Msorted, !IO), io.nl(!IO).

% === LIST COMPREHENSION PATTERN ===
% Using foldl/map/filter:
:- func squares_of_evens(list(int)) = list(int).
squares_of_evens(Xs) = Ys :-
    list.filter(is_even, Xs, Evens),
    list.map(square, Evens, Ys).

:- func square(int) = int.
square(X) = X * X.
```


---

# CHAPTER 6: EXCEPTIONS AND IO


## Error Handling and I/O

```mercury
:- module io_demo.
:- interface.
:- import_module io.
:- pred main(io::di, io::uo) is det.
:- implementation.
:- import_module string, int, exception.

% === BASIC IO ===
main(!IO) :-
    % Output
    io.write_string("Hello!\n", !IO),
    io.print_line("Also hello!", !IO),
    io.format("Number: %d, Float: %f\n", [i(42), f(3.14)], !IO),
    
    % Input
    io.read_line_as_string(LineRes, !IO),
    (
        LineRes = ok(Line),
        Trimmed = string.strip(Line),
        io.format("You said: %s\n", [s(Trimmed)], !IO)
    ;
        LineRes = error(Error),
        io.format("Error: %s\n", [s(io.error_message(Error))], !IO)
    ;
        LineRes = eof,
        io.write_string("EOF\n", !IO)
    ).

% === FILE I/O ===
:- pred read_file(string::in, string::out, io::di, io::uo) is det.
read_file(Filename, Contents, !IO) :-
    io.open_input(Filename, OpenRes, !IO),
    (
        OpenRes = ok(Stream),
        io.read_file_as_string(Stream, ReadRes, !IO),
        io.close_input(Stream, !IO),
        (
            ReadRes = ok(Contents)
        ;
            ReadRes = error(_, Error),
            Contents = "Error: " ++ io.error_message(Error)
        )
    ;
        OpenRes = error(Error),
        Contents = "Cannot open: " ++ io.error_message(Error)
    ).

% === EXCEPTIONS ===
:- pred safe_op(int::in, int::in, int::out, io::di, io::uo) is det.
safe_op(X, Y, Result, !IO) :-
    ( try []
        ( Y = 0 -> throw(divide_by_zero) ; true ),
        Result0 = X / Y
    then
        Result = Result0
    catch divide_by_zero ->
        io.write_string("Division by zero!\n", !IO),
        Result = 0
    ).

:- type my_error ---> divide_by_zero ; invalid_input(string).
```


---

# CHAPTER 7: MODULES AND TYPE CLASSES


## Mercury Module System

```mercury
% === TYPECLASS (ad-hoc polymorphism) ===

:- module tc_demo.
:- interface.

:- typeclass printable(T) where [
    pred print_it(T::in, io::di, io::uo) is det
].

:- typeclass comparable(T) where [
    pred less_than(T::in, T::in) is semidet,
    func compare_val(T, T) = int
].

:- implementation.
:- import_module io, int, string.

% Instances for int
:- instance printable(int) where [
    print_it(N, !IO) :- io.write_int(N, !IO), io.nl(!IO)
].

:- instance comparable(int) where [
    less_than(X, Y) :- X < Y,
    compare_val(X, Y) = ( X < Y -> -1 ; X > Y -> 1 ; 0 )
].

% Instances for string
:- instance printable(string) where [
    print_it(S, !IO) :- io.write_string(S, !IO), io.nl(!IO)
].

% Generic function using typeclass
:- pred print_all(list(T)::in, io::di, io::uo) is det
    <= printable(T).
print_all([], !IO).
print_all([X|Xs], !IO) :-
    print_it(X, !IO),
    print_all(Xs, !IO).

% === MODULE IMPORTS ===
% Public interface (in .m file header):
%   :- import_module module_name.   -- imports public preds
%   :- use_module module_name.      -- qualified access only

% :- import_module list, map, set, bag, assoc_list.
% :- import_module int, float, integer, rational.
% :- import_module string, char.
% :- import_module io, stream.
% :- import_module exception, require.
% :- import_module solutions.
% :- import_module math.           -- sin/cos/sqrt/etc
```


---

# CHAPTER 8: ADVANCED MERCURY


## Performance and Advanced Features

```mercury
:- module advanced.
:- interface.
:- implementation.

:- import_module int, list, io, string, solutions.

% === ACCUMULATOR PATTERN ===
% Use accumulators for tail recursion (efficiency)

:- pred sum_acc(list(int)::in, int::in, int::out) is det.
sum_acc([], Acc, Acc).
sum_acc([X|Xs], Acc, Total) :-
    sum_acc(Xs, Acc + X, Total).

:- func list_sum(list(int)) = int.
list_sum(Xs) = Total :-
    sum_acc(Xs, 0, Total).

% === DIFFERENCE LISTS ===
% Efficient O(1) append using open-ended lists

% dl(OpenList, Hole)
:- type dl(T) == pair(list(T), list(T)).

:- func dl_empty = dl(T).
dl_empty = [] - [].

:- func dl_singleton(T) = dl(T).
dl_singleton(X) = [X|Hole] - Hole.

:- func dl_append(dl(T), dl(T)) = dl(T).
dl_append(Xs - Mid, Mid - Tail) = Xs - Tail.

:- func dl_to_list(dl(T)) = list(T).
dl_to_list(Xs - []) = Xs.

% === ALL SOLUTIONS ===
:- pred pythagorean(int::in, int::out, int::out, int::out) is nondet.
pythagorean(Max, A, B, C) :-
    between(1, Max, A),
    between(A, Max, B),
    between(B, Max, C),
    A*A + B*B = C*C.

:- pred find_pythag(int::in, io::di, io::uo) is det.
find_pythag(Max, !IO) :-
    solutions((pred(T::out) is nondet :-
        pythagorean(Max, A, B, C),
        T = A - B - C
    ), Triples),
    io.write(Triples, !IO), io.nl(!IO).

% === FOREIGN CODE (C interop) ===
:- pred c_sqrt(float::in, float::out) is det.
:- pragma foreign_proc("C",
    c_sqrt(X::in, Y::out),
    [will_not_call_mercury, promise_pure],
    "Y = sqrt(X);").

% === UNIQUE MODES (destructive update) ===
% Allows in-place mutation while preserving pure semantics
% array.set(Index, Value, !Array) -- uses unique array

:- import_module array.

:- pred array_demo is det.
array_demo :-
    array.from_list([1,2,3,4,5], A0),
    array.set(2, 99, A0, A1),         % destructive update
    array.to_list(A1, L),
    io.write(L, !IO), io.nl(!IO).     % [1,2,99,4,5]

% === MUTABLE STATE ===
:- mutable(counter, int, 0, ground, [untrailed, attach_to_io_state]).

:- pred increment_counter(io::di, io::uo) is det.
increment_counter(!IO) :-
    get_counter(N, !IO),
    set_counter(N + 1, !IO).
```
