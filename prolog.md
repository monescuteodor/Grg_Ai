# Prolog Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH PROLOG


## Remarks

Prolog (Programming in Logic) is a logic programming language based on formal logic. Programs consist of facts and rules; execution is query-driven backtracking search. Prolog excels at symbolic computation, parsing, constraint solving, and AI applications.

Implementations: SWI-Prolog (most popular), GNU Prolog, SICStus Prolog, YAP.


## Hello World

```prolog
% hello.pl
:- initialization(main).

main :-
    write('Hello, World!'), nl,
    format("Hello, ~w!~n", ['Prolog']).
```

```bash
# SWI-Prolog
swipl -g "write('Hello'), nl" -t halt
swipl -s hello.pl

# Interactive
swipl
# ?- write('Hello, World!'), nl.
# Hello, World!
```


---

# CHAPTER 2: FACTS AND RULES


## Knowledge Base

```prolog
% Facts — unconditionally true
animal(dog).
animal(cat).
animal(bird).
animal(fish).

% Properties
color(dog, brown).
color(cat, orange).
color(bird, blue).

has_wings(bird).
can_swim(fish).
can_swim(dog).

% Relationships
parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).

likes(alice, bob).
likes(alice, carol).
likes(carol, dave).

% Rules — conditionally true (using :-)
% X :- Y1, Y2, ... means "X is true if Y1 AND Y2 AND ... are true"

% grandparent rule
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

% ancestor rule (recursive)
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

% pet (animal that is not a fish)
pet(X) :- animal(X), \+ X = fish.

% flies (has wings and is an animal)
flies(X) :- animal(X), has_wings(X).

% Mutual liking
friends(X, Y) :- likes(X, Y), likes(Y, X).

% Query examples:
% ?- animal(dog).          % true
% ?- animal(fox).          % false
% ?- animal(X).            % X = dog ; X = cat ; X = bird ; X = fish
% ?- grandparent(tom, Who). % Who = ann ; Who = pat
% ?- pet(X).               % X = dog ; X = cat ; X = bird
```


---

# CHAPTER 3: TERMS AND UNIFICATION


## Prolog Terms

```prolog
% Terms: atoms, numbers, variables, compound terms
atom            % atom (lowercase or quoted)
'hello world'   % atom with spaces
42              % integer
3.14            % float
X               % variable (uppercase)
_               % anonymous variable
f(x, y)         % compound term: functor f, args [x, y]
[1, 2, 3]       % list (sugar for '.'(1,'.'(2,'.'(3,[]))))

% Unification (=): makes two terms identical by binding variables
?- X = 42.           % X = 42
?- f(X, 2) = f(1, Y). % X = 1, Y = 2
?- [H|T] = [1,2,3].  % H = 1, T = [2,3]
?- X = f(X).         % fails (occurs check)

% Arithmetic (must use is/2 for evaluation)
?- X is 3 + 4.       % X = 7
?- X is 2 ** 10.     % X = 1024.0
?- X is 17 mod 5.    % X = 2
?- X is max(3, 7).   % X = 7
?- X is sqrt(16.0).  % X = 4.0
?- X is abs(-5).     % X = 5
?- X is truncate(3.7). % X = 3
?- X is floor(3.7).    % X = 3
?- X is ceiling(3.2).  % X = 4
?- X is round(3.5).    % X = 4

% Comparison
?- 3 > 2.     % true
?- 3 < 2.     % false
?- 3 >= 3.    % true
?- 3 =< 4.    % true (note: =<, not <=)
?- 3 =:= 3.0. % true (arithmetic equal)
?- 3 =\= 4.   % true (arithmetic not equal)
?- foo @< bar. % term ordering (structural)

% Structural equality / inequality
?- foo = foo.    % true
?- foo \= bar.   % true (not unifiable)
?- X == Y.       % true only if same variable or same value
?- X \== Y.      % true if not identical

% Functor and arity
?- functor(f(1,2,3), F, A).  % F = f, A = 3
?- arg(1, f(a,b,c), Arg).    % Arg = a (1-indexed)
?- T =.. [f, 1, 2, 3].      % T = f(1,2,3) (univ)
?- f(1,2,3) =.. L.           % L = [f, 1, 2, 3]
```


---

# CHAPTER 4: LISTS


## List Operations

```prolog
% Built-in list predicates
:- use_module(library(lists)).

% member/2 — check membership or enumerate
?- member(X, [1, 2, 3]).  % X = 1 ; X = 2 ; X = 3

% length/2
?- length([1,2,3], N).    % N = 3
?- length(L, 3).          % L = [_,_,_]

% append/3
?- append([1,2], [3,4], L).   % L = [1,2,3,4]
?- append(X, Y, [1,2,3]).     % enumerate splits

% last/2
?- last([1,2,3], X).    % X = 3

% reverse/2
?- reverse([1,2,3], X). % X = [3,2,1]

% nth0 / nth1 (0-indexed / 1-indexed)
?- nth0(0, [a,b,c], X). % X = a
?- nth1(1, [a,b,c], X). % X = a

% msort / sort
?- msort([3,1,4,1,5], S). % S = [1,1,3,4,5]
?- sort([3,1,4,1,5], S).  % S = [1,3,4,5] (removes dups)

% sum_list / max_list / min_list
?- sum_list([1,2,3,4,5], S).   % S = 15
?- max_list([3,1,4,1,5], M).   % M = 5
?- min_list([3,1,4,1,5], M).   % M = 1

% numlist
?- numlist(1, 5, L).    % L = [1,2,3,4,5]

% flatten
?- flatten([1,[2,[3,4]],5], F). % F = [1,2,3,4,5]

% Custom list predicates
my_length([], 0).
my_length([_|T], N) :-
    my_length(T, N1),
    N is N1 + 1.

my_append([], L, L).
my_append([H|T], L, [H|R]) :- my_append(T, L, R).

my_member(X, [X|_]).
my_member(X, [_|T]) :- my_member(X, T).

my_reverse([], []).
my_reverse([H|T], R) :-
    my_reverse(T, RT),
    append(RT, [H], R).

% Accumulator pattern (efficient reverse)
rev(L, R) :- rev(L, [], R).
rev([], Acc, Acc).
rev([H|T], Acc, R) :- rev(T, [H|Acc], R).

% Map equivalent
maplist(_, []).
maplist(P, [H|T]) :- call(P, H), maplist(P, T).
maplist(_, [], []).
maplist(P, [H|T], [RH|RT]) :- call(P, H, RH), maplist(P, T, RT).

% Filter equivalent
include(_, [], []).
include(P, [H|T], R) :-
    (call(P, H) -> R = [H|RT] ; R = RT),
    include(P, T, RT).
```


---

# CHAPTER 5: CONTROL FLOW AND CUT


## Control Predicates

```prolog
% Conjunction (AND) with comma
hot_weather :-
    temperature(T),
    T > 30,
    sunny.

% Disjunction (OR) with semicolon
transport(X, Y) :-
    (drive(X, Y) ; train(X, Y) ; fly(X, Y)).

% Negation as failure (\+)
non_member(X, L) :- \+ member(X, L).

adult(X) :- person(X), \+ child(X).

% if-then-else (-> ;)
classify(X, Class) :-
    (X > 0 -> Class = positive
    ; X < 0 -> Class = negative
    ; Class = zero).

% Cut (!) — prune the search tree
% Commits to choices made before the cut
max(X, Y, X) :- X >= Y, !.
max(_, Y, Y).

% Without cut, max would backtrack unnecessarily
first_match(X, [X|_]) :- !.
first_match(X, [_|T]) :- first_match(X, T).

% once/1 — get only first solution
?- once(member(X, [1,2,3])).  % X = 1

% findall / bagof / setof — collect solutions
?- findall(X, member(X, [1,2,3]), L).   % L = [1,2,3]

% findall with transformation
?- findall(X-Y, (member(X,[1,2,3]), Y is X*X), Pairs).
% Pairs = [1-1, 2-4, 3-9]

% bagof fails if no solutions; findall returns []
?- bagof(X, member(X, [1,2,3]), L).    % L = [1,2,3]
?- setof(X, member(X, [3,1,2,1]), L).  % L = [1,2,3] (sorted, unique)

% aggregate (SWI-Prolog)
?- aggregate_all(count, member(_, [a,b,c]), N).  % N = 3
?- aggregate_all(sum(X), member(X,[1,2,3,4,5]), S). % S = 15

% forall
?- forall(member(X, [2,4,6]), 0 =:= X mod 2).  % true (all even)

% between
?- between(1, 5, X).   % X = 1 ; 2 ; 3 ; 4 ; 5
```


---

# CHAPTER 6: ARITHMETIC AND STRINGS


## Numeric and String Operations

```prolog
% Arithmetic expressions
X is 2 + 3 * 4.       % 14
X is (2 + 3) * 4.     % 20
X is 2 ** 8.          % 256.0
X is 10 rem 3.        % 1
X is 10 mod 3.        % 1
X is sin(0.0).        % 0.0
X is cos(0.0).        % 1.0
X is exp(1.0).        % 2.718...
X is log(2.718).      % ~1.0
X is pi.              % 3.14159...
X is e.               % 2.71828...
X is sign(-5).        % -1
X is gcd(12, 8).      % 4

% Integer operations
X is 15 // 4.         % 3 (integer division in SWI)
X is 15 div 4.        % 3
X is 7 /\ 5.          % 5 (bitwise AND)
X is 7 \/ 5.          % 7 (bitwise OR)
X is 7 xor 5.         % 2
X is 1 << 4.          % 16 (left shift)
X is 16 >> 2.         % 4 (right shift)
X is \5.              % bitwise NOT

% String/Atom operations (SWI-Prolog)
atom_length(hello, N).          % N = 5
atom_concat(hello, world, X).   % X = helloworld
atom_concat(X, world, helloworld). % X = hello (reversible!)
sub_atom(hello, 1, 3, _, Sub).  % Sub = ell
char_code('A', C).              % C = 65
char_code(Ch, 65).              % Ch = 'A'
upcase_atom(hello, X).          % X = 'HELLO'
downcase_atom('HELLO', X).      % X = hello
atom_number('42', N).           % N = 42
number_codes(42, Codes).        % Codes = [52, 50]
number_chars(42, Chars).        % Chars = ['4','2']
atom_chars(hello, Chars).       % Chars = [h,e,l,l,o]
atom_codes(hello, Codes).
char_type('A', alpha).          % type check
char_type('1', digit(1)).

% String split/join (SWI-Prolog)
split_string("a,b,c", ",", "", Parts). % Parts = ["a","b","c"]
atomic_list_concat([a,b,c], '-', X).   % X = 'a-b-c'
atomic_list_concat(L, '-', 'a-b-c').   % L = [a,b,c] (split)

% format/write
format("~w~n", [hello]).        % hello\n
format("~a~n", [hello]).        % hello\n (atom)
format("~d~n", [42]).           % 42\n (integer)
format("~f~n", [3.14]).         % 3.140000\n
format("~e~n", [3.14]).         % 3.14e+00\n
format("~`-t~50|~n", []).       % 50 dashes
with_output_to(string(S), format("~w", [hello])). % S = "hello"
```


---

# CHAPTER 7: DEFINITE CLAUSE GRAMMARS (DCG)


## Parsing with DCG

```prolog
% DCG — Definite Clause Grammars
% --> notation automatically adds two extra args (difference lists)

% Simple grammar for sentences
sentence --> noun_phrase, verb_phrase.
noun_phrase --> det, noun.
verb_phrase --> verb, noun_phrase.
verb_phrase --> verb.

det --> [the].
det --> [a].
noun --> [cat].
noun --> [dog].
noun --> [mouse].
verb --> [chases].
verb --> [sees].

% Query
?- phrase(sentence, [the, cat, chases, a, dog]).  % true
?- phrase(sentence, S).                           % enumerate sentences

% DCG with actions (extra args)
expr(E) --> term(T), expr_rest(T, E).
expr_rest(T, E) --> [+], term(T2), { T1 is T+T2 }, expr_rest(T1, E).
expr_rest(T, T) --> [].

term(T) --> [T], { number(T) }.

?- phrase(expr(E), [3, +, 4, +, 5]).  % E = 12

% DCG for CSV parsing
csv([Row|Rows]) --> row(Row), ['\n'], csv(Rows).
csv([Row]) --> row(Row).
row([F|Fields]) --> field(F), [','], row(Fields).
row([F]) --> field(F).
field(F) --> chars(Cs), { atom_chars(F, Cs) }.
chars([C|Cs]) --> [C], { C \= (','), C \= ('\n') }, chars(Cs).
chars([]) --> [].
```


---

# CHAPTER 8: META-PREDICATES AND MODULES


## Meta-programming

```prolog
% call/N — call a goal with extra args
:- meta_predicate maplist(1, ?).
:- meta_predicate maplist(2, ?, ?).

double(X, Y) :- Y is X * 2.
?- maplist(double, [1,2,3], Doubled).  % Doubled = [2,4,6]

?- maplist(write, [a,b,c]).    % prints abc

% Lambda-like with library(yall)
?- maplist([X]>>(Y is X*2, write(Y)), [1,2,3]).

% Callable goals
Goal = write(hello),
call(Goal).

% assert / retract (dynamic KB modification)
:- dynamic fact/1.

assert(fact(1)).
assert(fact(2)).
assert(fact(3)).
asserta(fact(0)).   % add at front
assertz(fact(4)).   % add at back

?- fact(X).    % X = 0 ; 1 ; 2 ; 3 ; 4

retract(fact(2)).
retractall(fact(_)).   % remove all

% Modules (SWI-Prolog)
:- module(mymodule, [my_pred/1, my_func/2]).

my_pred(hello) :- write(hello), nl.
my_func(X, Y) :- Y is X * 2.

:- use_module(library(lists)).
:- use_module(mymodule).

% Exceptions
:- catch(
    (X is 1/0),
    error(evaluation_error(zero_divisor), _),
    write('Division by zero')
).

% throw custom exception
validate_age(Age) :-
    (Age < 0 -> throw(error(invalid_age(Age), context(validate_age/1, 'Age must be non-negative')))
    ; true).

% Meta-predicates
:- meta_predicate my_once(0).
my_once(Goal) :- call(Goal), !.

% copy_term
copy_term(f(X, X), Copy).  % Copy = f(_A, _A) — fresh variables

% numbervars
Term = f(X, g(Y, X)),
numbervars(Term, 0, End).
% Term = f(A, g(B, A)), End = 2
```
