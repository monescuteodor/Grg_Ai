# Logtalk Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH LOGTALK


## Remarks

Logtalk is an object-oriented logic programming language that extends and builds on top of Prolog. Created by Paulo Moura in 1998, it supports encapsulation, inheritance, polymorphism, and component-based programming while maintaining Prolog compatibility. Logtalk runs on top of any standard Prolog system.

Tools: SWI-Prolog + Logtalk, GNU Prolog + Logtalk, SICStus Prolog + Logtalk. Install via `logtalk_install`.


## Hello World

```logtalk
% hello.lgt
:- object(hello).
    :- initialization(main).
    
    main :-
        write('Hello, World!'), nl,
        write('Hello, Logtalk!'), nl.

:- end_object.
```

```bash
# Run with SWI-Prolog backend:
swilgt -g "logtalk_load('hello')" -t halt

# Or use the logtalk_tester utility
logtalk_tester -p swi

# Interactive:
swilgt   # starts SWI-Prolog + Logtalk
?- logtalk_load('hello').
```

### Setting Up

```bash
# Install Logtalk (Linux/Mac)
brew install logtalk              # macOS Homebrew
# Or download from logtalk.org

# Environment variable
export LOGTALKHOME=/usr/local/share/logtalk
export LOGTALKUSER=$HOME/logtalk

# Integration scripts
swilgt    # SWI-Prolog + Logtalk
gplgt     # GNU Prolog + Logtalk
sicstuslgt # SICStus + Logtalk
```


---

# CHAPTER 2: OBJECTS


## Basic Object-Oriented Programming

```logtalk
% === BASIC OBJECT ===
:- object(animal).

    :- public([
        name/1,
        sound/1,
        speak/0
    ]).
    
    name(animal).
    sound('...').
    
    speak :-
        ::name(N),        % :: sends message to self
        ::sound(S),
        format("~w says ~w~n", [N, S]).

:- end_object.


% === EXTENDING OBJECTS (prototype-based) ===
:- object(dog, extends(animal)).

    name(dog).
    sound(woof).
    
    % Add new method
    :- public(fetch/1).
    fetch(Item) :-
        format("~w fetches the ~w!~n", [dog, Item]).

:- end_object.

:- object(cat, extends(animal)).

    name(cat).
    sound(meow).

:- end_object.


% === SENDING MESSAGES ===
:- initialization(run_animals).

run_animals :-
    animal::speak,    % message to object
    dog::speak,
    cat::speak,
    dog::fetch(ball).


% === OBJECT WITH STATE (using dynamic predicates) ===
:- object(counter).

    :- public([increment/0, decrement/0, value/1, reset/0]).
    
    :- private(count/1).
    :- dynamic(count/1).
    
    count(0).    % initial state
    
    value(N) :-
        ::count(N).
    
    increment :-
        ::retract(count(N)),
        N1 is N + 1,
        ::assert(count(N1)).
    
    decrement :-
        ::retract(count(N)),
        N1 is max(0, N - 1),
        ::assert(count(N1)).
    
    reset :-
        ::retract(count(_)),
        ::assert(count(0)).

:- end_object.
```


---

# CHAPTER 3: INHERITANCE


## Class-Based Inheritance

```logtalk
% === CLASSES (vs prototypes) ===
% Classes use 'instantiates' and 'extends' for metaclass hierarchy

% Abstract base class
:- object(shape, abstract).

    :- public([area/1, perimeter/1, describe/0]).
    
    describe :-
        ::area(A),
        ::perimeter(P),
        format("Area: ~f, Perimeter: ~f~n", [A, P]).

:- end_object.


% Concrete subclass
:- object(circle, extends(shape)).

    :- public(radius/1).
    :- private(radius_/1).
    :- dynamic(radius_/1).
    
    radius_(5.0).    % default radius
    
    radius(R) :- ::radius_(R).
    
    area(A) :-
        ::radius_(R),
        A is pi * R * R.
    
    perimeter(P) :-
        ::radius_(R),
        P is 2 * pi * R.

:- end_object.


:- object(rectangle, extends(shape)).

    :- public([width/1, height/1]).
    :- private([width_/1, height_/1]).
    :- dynamic([width_/1, height_/1]).
    
    width_(4.0).
    height_(6.0).
    
    width(W)  :- ::width_(W).
    height(H) :- ::height_(H).
    
    area(A) :-
        ::width_(W), ::height_(H),
        A is W * H.
    
    perimeter(P) :-
        ::width_(W), ::height_(H),
        P is 2 * (W + H).

:- end_object.


% === MULTIPLE INHERITANCE ===
:- object(colored_circle, extends([circle, colored])).
    % Inherits from both circle and colored
:- end_object.


% === USING SUPER ===
:- object(verbose_animal, extends(animal)).

    speak :-
        write('About to speak: '),
        ^^speak.    % ^^ calls inherited (super) method

:- end_object.
```


---

# CHAPTER 4: CATEGORIES AND PROTOCOLS


## Mixins and Interfaces

```logtalk
% === PROTOCOL (interface) ===
:- protocol(printable).

    :- public([
        print/0,
        to_string/1
    ]).

:- end_protocol.


:- protocol(comparable).

    :- public([
        less_than/1,
        greater_than/1,
        equal_to/1
    ]).

:- end_protocol.


% === CATEGORY (mixin/trait) ===
% Categories provide reusable code without being standalone objects
:- category(logging).

    :- public([log/1, log_error/1]).
    
    log(Msg) :-
        get_time(T),
        format("[~f] INFO: ~w~n", [T, Msg]).
    
    log_error(Msg) :-
        get_time(T),
        format("[~f] ERROR: ~w~n", [T, Msg]).

:- end_category.


:- category(serializable).

    :- public([serialize/1, deserialize/2]).
    
    serialize(JSON) :-
        % default serialization
        term_to_atom(This, JSON).

:- end_category.


% === OBJECT IMPLEMENTING PROTOCOL AND USING CATEGORY ===
:- object(person,
    implements([printable, comparable]),
    imports([logging, serializable])).

    :- public([name/1, age/1]).
    :- private([name_/1, age_/1]).
    
    name_('Alice').
    age_(30).
    
    name(N) :- ::name_(N).
    age(A)  :- ::age_(A).
    
    % Implement protocol methods
    print :-
        ::name(N), ::age(A),
        format("Person(~w, ~w)~n", [N, A]).
    
    to_string(S) :-
        ::name(N), ::age(A),
        format(atom(S), "~w (~w)", [N, A]).
    
    less_than(Other) :-
        ::age(A1),
        Other::age(A2),
        A1 < A2.
    
    greater_than(Other) :-
        Other::less_than(This).
    
    equal_to(Other) :-
        ::name(N),
        Other::name(N).

:- end_object.
```


---

# CHAPTER 5: PARAMETRIC OBJECTS


## Generic Programming

```logtalk
% === PARAMETRIC OBJECTS ===
% Objects can be parameterized

:- object(pair(First, Second)).

    :- public([
        first/1,
        second/1,
        swap/1,
        map/3
    ]).
    
    first(First).
    second(Second).
    
    swap(pair(Second, First)).
    
    map(F, G, pair(NF, NS)) :-
        call(F, First, NF),
        call(G, Second, NS).

:- end_object.


% Use:
% ?- pair(1, hello)::first(X).
% X = 1
% ?- pair(1, hello)::swap(P).
% P = pair(hello, 1)


% === PARAMETRIC LIST ===
:- object(typed_list(Type)).

    :- public([
        add/2,
        contains/1,
        size/1
    ]).
    
    :- private(items_/1).
    :- dynamic(items_/1).
    
    items_([]).
    
    add(Item, typed_list(Type)) :-
        call(Type, Item),     % type check
        ::retract(items_(L)),
        ::assert(items_([Item|L])).
    
    contains(Item) :-
        ::items_(L),
        member(Item, L).
    
    size(N) :-
        ::items_(L),
        length(L, N).

:- end_object.


% === LAMBDA OBJECTS ===
% Using library(lambda) for higher-order

:- meta_predicate maplist(1, ?).

% Calling meta-predicates safely:
:- object(functional).

    :- public([map/3, filter/3, fold/4]).
    
    map(_, [], []).
    map(Closure, [H|T], [NH|NT]) :-
        call(Closure, H, NH),
        map(Closure, T, NT).
    
    filter(_, [], []).
    filter(Pred, [H|T], Result) :-
        (call(Pred, H) -> Result = [H|R] ; Result = R),
        filter(Pred, T, R).
    
    fold(_, Acc, [], Acc).
    fold(F, Acc, [H|T], Result) :-
        call(F, H, Acc, NAcc),
        fold(F, NAcc, T, Result).

:- end_object.
```


---

# CHAPTER 6: EVENTS AND MONITORS


## Event-Driven Programming

```logtalk
% === EVENTS ===
% Logtalk supports before/after event interceptors

:- object(logged_counter, extends(counter)).

    % Monitor all messages sent to this object
    :- use_module(logtalk, [before/3, after/3]).

:- end_object.


% === MONITOR OBJECTS ===
:- object(logger, implements(monitoring)).

    :- public([before/3, after/3]).
    
    % Called before any message send
    before(Object, Message, Sender) :-
        format("BEFORE: ~w sends ~w to ~w~n",
               [Sender, Message, Object]).
    
    % Called after any message send
    after(Object, Message, Sender) :-
        format("AFTER: ~w->~w returned to ~w~n",
               [Object, Message, Sender]).

:- end_object.


% Register monitor:
% :- define_events(after, counter, _, _, logger).
% :- define_events(before, counter, _, _, logger).


% === EVENT-BASED DESIGN PATTERN ===
:- object(observable).

    :- public([
        add_observer/1,
        remove_observer/1,
        notify/1
    ]).
    
    :- private(observers_/1).
    :- dynamic(observers_/1).
    
    observers_([]).
    
    add_observer(Obs) :-
        ::retract(observers_(L)),
        ::assert(observers_([Obs|L])).
    
    remove_observer(Obs) :-
        ::retract(observers_(L)),
        exclude(=(Obs), L, NL),
        ::assert(observers_(NL)).
    
    notify(Event) :-
        ::observers_(Obs),
        forall(member(O, Obs),
               O::update(Event, This)).

:- end_object.
```


---

# CHAPTER 7: TESTING AND DEBUGGING


## Logtalk Testing

```logtalk
% === LGTUNIT (built-in testing framework) ===
:- object(calculator_tests,
    extends(lgtunit)).

    :- info([
        version is 1.0,
        date is 2026-05-25,
        comment is 'Tests for calculator object'
    ]).
    
    % Test methods must be named test_*
    test(add_two_numbers) :-
        calculator::add(3, 4, Result),
        Result =:= 7.
    
    test(division_by_zero, error(division_by_zero, _)) :-
        calculator::divide(10, 0, _).
    
    test(factorial_zero) :-
        calculator::factorial(0, Result),
        Result =:= 1.
    
    test(factorial_five) :-
        calculator::factorial(5, Result),
        Result =:= 120.
    
    % Test with expected exception
    test(negative_factorial, error(domain_error(_, _), _)) :-
        calculator::factorial(-1, _).
    
    % Determinism test (exactly one solution)
    test(unique_result, deterministic) :-
        calculator::sqrt(4.0, R),
        R =:= 2.0.

:- end_object.


% Run tests:
% ?- lgtunit::run_test_sets([calculator_tests]).


% === DEBUGGING ===
% Enable debug mode:
% ?- set_logtalk_flag(debug, on).

% Trace messages:
% ?- trace, dog::speak.

% Spy points:
% ?- spy(animal::speak/0).

% Debug options:
% ?- logtalk_flag(unknown_entities, warning).
% ?- logtalk_flag(unknown_predicates, error).
```


---

# CHAPTER 8: ADVANCED FEATURES


## Reflection and Meta-Programming

```logtalk
% === REFLECTION ===
:- object(inspector).

    :- public([inspect/1, list_methods/1]).
    
    inspect(Object) :-
        current_object(Object),
        format("Object: ~w~n", [Object]),
        
        % List all public methods
        Object::current_predicate(F/A),
        Object::predicate_property(F/A, (public)),
        format("  ~w/~w~n", [F, A]),
        fail.
    inspect(_).
    
    list_methods(Object) :-
        findall(F/A,
            (Object::current_predicate(F/A),
             Object::predicate_property(F/A, (public))),
            Methods),
        format("Methods of ~w: ~w~n", [Object, Methods]).

:- end_object.


% === TERM EXPANSION ===
:- object(my_expander, implements(expanding)).

    % Expand terms at load time
    term_expansion(
        log_call(Head),          % input
        (Head :- write(calling(Head)), nl, Head)  % output
    ).

:- end_object.


% === META-PREDICATES ===
:- object(meta_examples).

    :- use_module(meta, [map/3, foldl/4]).
    
    :- meta_predicate maplist(1, ?).
    
    run :-
        Nums = [1, 2, 3, 4, 5],
        
        % Using Logtalk's built-in meta-predicates:
        meta::map([X, Y]>>(Y is X * 2), Nums, Doubled),
        meta::include([X]>>(X > 2), Nums, Filtered),
        meta::foldl([X, Acc, NAcc]>>(NAcc is Acc + X),
                    Nums, 0, Total),
        
        format("Doubled: ~w~n", [Doubled]),
        format("Filtered: ~w~n", [Filtered]),
        format("Total: ~w~n", [Total]).

:- end_object.


% === LIBRARY OVERVIEW ===
% Core libraries:
% - lgtunit         : unit testing framework
% - meta            : higher-order predicates  
% - pairs           : key-value pair utilities
% - sets            : set operations
% - types           : type checking predicates
% - dates           : date/time handling
% - csv             : CSV reading/writing
% - json            : JSON parsing
% - redis           : Redis client

% Load library:
% :- use_module(library(meta)).
% or:
% :- use_module(meta).
```
