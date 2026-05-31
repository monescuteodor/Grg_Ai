# Erlang Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH ERLANG


## Remarks

Erlang is a concurrent, functional, fault-tolerant programming language designed for distributed, real-time systems. It was created by Ericsson for telecom systems. Key features include lightweight processes, message passing, hot code loading, and the OTP framework. Used in WhatsApp, RabbitMQ, and CouchDB.

Tools: erl (REPL), erlc (compiler), rebar3 (build tool), OTP framework.


## Hello World

```erlang
% hello.erl
-module(hello).
-export([main/0]).

main() ->
    io:format("Hello, World!~n"),
    io:format("Hello, ~s!~n", ["Erlang"]).
```

```bash
# Compile and run
erlc hello.erl
erl -noshell -s hello main -s init stop

# Interactive REPL
erl
# 1> io:format("Hello!~n").
# Hello!
# ok
```


---

# CHAPTER 2: TYPES AND VARIABLES


## Basic Types

```erlang
% In Erlang, variables start with uppercase
% They are immutable (single assignment)
% Terms: atoms, numbers, tuples, lists, binaries, funs, pids

% Atoms (lowercase or quoted) - compile-time constants
hello
world
'hello world'
true
false

% Numbers
42          % integer
3.14        % float
16#FF       % hex: 255
2#1010      % binary: 10
$A          % ASCII code: 65

% Tuples (fixed size, heterogeneous)
{1, 2, 3}
{ok, "result"}
{error, "not found"}
{point, 3.0, 4.0}

% Lists
[1, 2, 3, 4, 5]
[H|T] = [1,2,3]      % H=1, T=[2,3] (head|tail)
"hello"              % string = list of integers

% Binaries
<<72, 101, 108>>     % binary sequence
<<"hello">>          % binary string
<<X:8, Y:16>> = <<10, 300:16>>  % binary pattern matching

% Variables (MUST start with uppercase)
X = 42,
Name = "Alice",
Result = {ok, 42},

% Pattern matching (assignment IS matching)
{ok, Value} = {ok, 42},    % Value = 42
[First|Rest] = [1,2,3],    % First=1, Rest=[2,3]

% _ (wildcard)
{_, Important, _} = {a, 42, b},

% Comparison
1 =:= 1     % exact equality (type and value)
1 == 1.0    % loose equality (1 == 1.0 is true)
1 =/= 2     % not equal
1 /= 1.0    % not equal (loose)
1 < 2
1 > 2
1 =< 2      % less or equal (not <=)
1 >= 2

% Type checking
is_integer(42)
is_float(3.14)
is_atom(hello)
is_list([1,2,3])
is_tuple({1,2})
is_binary(<<"hi">>)
is_function(fun(X) -> X end)
is_pid(self())
```


---

# CHAPTER 3: PATTERN MATCHING AND FUNCTIONS


## Functions and Pattern Matching

```erlang
-module(examples).
-export([factorial/1, fib/1, max/2, describe/1, loop/0]).

%% Multiple clauses — pattern matching selects the clause
factorial(0) -> 1;
factorial(N) when N > 0 -> N * factorial(N - 1).

fib(0) -> 0;
fib(1) -> 1;
fib(N) -> fib(N-1) + fib(N-2).

%% Guards (when clause)
max(X, Y) when X >= Y -> X;
max(_, Y) -> Y.

%% Pattern matching on various types
describe({circle, R}) ->
    io:format("Circle with radius ~p~n", [R]);
describe({rectangle, W, H}) ->
    io:format("Rectangle ~p x ~p~n", [W, H]);
describe({triangle, B, H}) ->
    io:format("Triangle base ~p height ~p~n", [B, H]);
describe(_) ->
    io:format("Unknown shape~n").

%% Recursive list processing
sum([]) -> 0;
sum([H|T]) -> H + sum(T).

length_([]) -> 0;
length_([_|T]) -> 1 + length_(T).

map(_, []) -> [];
map(F, [H|T]) -> [F(H) | map(F, T)].

filter(_, []) -> [];
filter(Pred, [H|T]) ->
    case Pred(H) of
        true  -> [H | filter(Pred, T)];
        false -> filter(Pred, T)
    end.

foldl(_, Acc, []) -> Acc;
foldl(F, Acc, [H|T]) -> foldl(F, F(H, Acc), T).

%% Anonymous functions (funs)
Square = fun(X) -> X * X end,
Square(5),    % 25

Add = fun(X, Y) -> X + Y end,
lists:map(fun(X) -> X * 2 end, [1,2,3]),

%% Case expression
describe_number(N) ->
    case N of
        0 -> zero;
        N when N > 0 -> positive;
        _ -> negative
    end.

%% If expression
classify(X) ->
    if
        X > 100 -> big;
        X > 10  -> medium;
        true    -> small   % 'true' is the else clause
    end.

%% Receive (in a process)
loop() ->
    receive
        {hello, From} ->
            From ! world,
            loop();
        stop ->
            ok;
        Msg ->
            io:format("Got: ~p~n", [Msg]),
            loop()
    after 5000 ->
        io:format("Timeout~n"),
        loop()
    end.
```


---

# CHAPTER 4: LISTS AND STDLIB


## Lists and Standard Library

```erlang
%% lists module (most important stdlib module)
lists:append([1,2], [3,4])           % [1,2,3,4]
lists:append([[1,2],[3,4],[5,6]])     % [1,2,3,4,5,6]
lists:reverse([1,2,3,4,5])           % [5,4,3,2,1]
lists:length([1,2,3])                % 3
lists:nth(2, [a,b,c])               % b (1-indexed)
lists:last([1,2,3])                  % 3
lists:member(3, [1,2,3,4])          % true
lists:delete(3, [1,2,3,4])          % [1,2,4]
lists:flatten([[1,2],[3,[4,5]]])     % [1,2,3,4,5]
lists:zip([1,2,3], [a,b,c])         % [{1,a},{2,b},{3,c}]
lists:unzip([{1,a},{2,b}])          % {[1,2],[a,b]}
lists:sort([3,1,4,1,5,9,2,6])       % [1,1,2,3,4,5,6,9]
lists:sort(fun(A,B) -> A > B end, [3,1,4])  % desc
lists:keysort(2, [{a,3},{b,1},{c,2}])  % by second element
lists:map(fun(X) -> X*2 end, [1,2,3])  % [2,4,6]
lists:filter(fun(X) -> X rem 2 =:= 0 end, [1,2,3,4])  % [2,4]
lists:foldl(fun(X,A) -> X+A end, 0, [1,2,3,4,5])      % 15
lists:foldr(fun(X,A) -> [X*2|A] end, [], [1,2,3])      % [2,4,6]
lists:sum([1,2,3,4,5])              % 15
lists:max([3,1,4,1,5])              % 5
lists:min([3,1,4,1,5])              % 1
lists:any(fun(X) -> X > 3 end, [1,2,3,4])   % true
lists:all(fun(X) -> X > 0 end, [1,2,3,4])   % true
lists:partition(fun(X) -> X rem 2 =:= 0 end, [1,2,3,4])  % {[2,4],[1,3]}
lists:flatten([1,[2,[3,4]],5])      % [1,2,3,4,5]
lists:seq(1, 10)                    % [1,2,3,4,5,6,7,8,9,10]
lists:seq(1, 10, 2)                 % [1,3,5,7,9]
lists:sublist([1,2,3,4,5], 2, 3)   % [2,3,4]
lists:splitwith(fun(X) -> X<3 end, [1,2,3,4])  % {[1,2],[3,4]}
lists:takewhile(fun(X) -> X<3 end, [1,2,3,4])  % [1,2]
lists:dropwhile(fun(X) -> X<3 end, [1,2,3,4])  % [3,4]

%% String (list of chars) operations
string:len("hello")                 % 5
string:concat("Hello", " World")
string:sub_string("Hello", 1, 3)   % "Hel"
string:to_upper("hello")
string:to_lower("HELLO")
string:tokens("a,b,c", ",")        % ["a","b","c"]
string:join(["a","b","c"], ", ")

%% io_lib for formatting
io_lib:format("~p + ~p = ~p", [1, 2, 3])
integer_to_list(42)    % "42"
list_to_integer("42")  % 42
float_to_list(3.14)
list_to_float("3.14")
atom_to_list(hello)    % "hello"
list_to_atom("hello")  % hello
```


---

# CHAPTER 5: PROCESSES AND CONCURRENCY


## Lightweight Processes

```erlang
-module(concurrency).
-export([start/0, worker/1, counter/1]).

%% Spawn a process
start() ->
    Pid = spawn(fun worker_fun/0),
    Pid ! {self(), hello},
    receive
        Reply -> io:format("Got: ~p~n", [Reply])
    after 1000 ->
        io:format("Timeout~n")
    end.

worker_fun() ->
    receive
        {From, hello} ->
            From ! world;
        _ ->
            ok
    end.

%% Process with state (via recursion)
counter(N) ->
    receive
        increment ->
            counter(N + 1);
        {get, From} ->
            From ! N,
            counter(N);
        reset ->
            counter(0);
        stop ->
            ok
    end.

%% Start counter
start_counter() ->
    Pid = spawn(?MODULE, counter, [0]),
    Pid ! increment,
    Pid ! increment,
    Pid ! increment,
    Pid ! {get, self()},
    receive
        N -> io:format("Count: ~p~n", [N])
    end,
    Pid ! stop.

%% Register a process by name
register(my_counter, spawn(?MODULE, counter, [0])),
my_counter ! increment,

%% Monitor processes
{Pid, Ref} = spawn_monitor(fun worker_fun/0),
receive
    {'DOWN', Ref, process, Pid, Reason} ->
        io:format("Process died: ~p~n", [Reason])
end,

%% Link processes (crash propagates)
spawn_link(fun() -> exit(reason) end),

%% Process info
self()         % current PID
is_pid(Pid)
Pid ! message  % send message
process_info(self(), message_queue_len)
```


---

# CHAPTER 6: OTP AND GENSERVER


## OTP Framework

```erlang
%% gen_server — generic server behavior
-module(my_server).
-behaviour(gen_server).

-export([start_link/0, get/0, put/2, delete/1]).
-export([init/1, handle_call/3, handle_cast/2, handle_info/2, terminate/2]).

%% Client API
start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

get() ->
    gen_server:call(?MODULE, get_all).

put(Key, Value) ->
    gen_server:cast(?MODULE, {put, Key, Value}).

delete(Key) ->
    gen_server:call(?MODULE, {delete, Key}).

%% Server callbacks
init([]) ->
    {ok, #{}}.   % initial state: empty map

handle_call(get_all, _From, State) ->
    {reply, State, State};
handle_call({delete, Key}, _From, State) ->
    NewState = maps:remove(Key, State),
    {reply, ok, NewState}.

handle_cast({put, Key, Value}, State) ->
    NewState = maps:put(Key, Value, State),
    {noreply, NewState}.

handle_info(_Info, State) ->
    {noreply, State}.

terminate(_Reason, _State) ->
    ok.

%% supervisor — restart strategy
-module(my_sup).
-behaviour(supervisor).
-export([start_link/0, init/1]).

start_link() ->
    supervisor:start_link({local, ?MODULE}, ?MODULE, []).

init([]) ->
    ChildSpec = #{
        id      => my_server,
        start   => {my_server, start_link, []},
        restart => permanent,
        type    => worker,
        modules => [my_server]
    },
    {ok, {#{strategy => one_for_one, intensity => 5, period => 10},
          [ChildSpec]}}.
```


---

# CHAPTER 7: MAPS AND RECORDS


## Data Structures

```erlang
%% Maps (Erlang 17+)
M = #{name => "Alice", age => 30, city => "NYC"},
maps:get(name, M),          % "Alice"
maps:get(missing, M, default),  % default
maps:put(city, "LA", M),   % new map
maps:remove(age, M),
maps:is_key(name, M),       % true
maps:keys(M),               % [age, city, name]
maps:values(M),
maps:size(M),               % 3
maps:to_list(M),
maps:from_list([{a,1},{b,2}]),

%% Map pattern matching
#{name := Name, age := Age} = M,
io:format("~s is ~p~n", [Name, Age]),

%% Map update (!)
M2 = M#{age => 31},
M3 = M#{age := 31},   % := only for existing keys

%% Merge
maps:merge(M, #{email => "alice@example.com"}),

%% Map operations
maps:map(fun(K, V) -> {K, V} end, M),
maps:filter(fun(K, _V) -> K =/= age end, M),
maps:fold(fun(K, V, Acc) -> [{K,V}|Acc] end, [], M),

%% Records (compile-time named tuple)
-record(person, {name, age=0, city="Unknown"}).

P = #person{name="Alice", age=30},
P#person.name,          % "Alice"
P#person{age=31},       % update
is_record(P, person),   % true

%% Record pattern matching
greet(#person{name=Name, age=Age}) ->
    io:format("Hello ~s, age ~p~n", [Name, Age]).

%% ETS (Erlang Term Storage) — in-memory tables
Tab = ets:new(my_table, [set, public, named_table]),
ets:insert(Tab, {key1, "value1"}),
ets:insert(Tab, {key2, "value2"}),
ets:lookup(Tab, key1),      % [{key1,"value1"}]
ets:delete(Tab, key1),
ets:match(Tab, {key2, '$1'}),   % [["value2"]]
ets:tab2list(Tab),
ets:select(Tab, [{{'$1','$2'}, [], ['$$']}]),
```


---

# CHAPTER 8: ERROR HANDLING AND DISTRIBUTION


## Fault Tolerance

```erlang
%% try/catch
try
    1 / 0
catch
    error:badarith ->
        io:format("Division by zero~n");
    error:Error ->
        io:format("Error: ~p~n", [Error]);
    throw:Thrown ->
        io:format("Thrown: ~p~n", [Thrown]);
    exit:Reason ->
        io:format("Exit: ~p~n", [Reason])
after
    io:format("Cleanup~n")
end,

%% Throw (non-error exception)
safe_div(_, 0) -> throw(division_by_zero);
safe_div(X, Y) -> X / Y.

%% Error types
error(my_error),       % raise error
throw(my_value),       % throw non-error
exit(my_reason),       % terminate process

%% catch expression
Result = catch (1 / 0),  % Result = {'EXIT',{badarith,[...]}}

%% Distribution (multi-node)
% Start nodes:
% erl -name node1@localhost -setcookie secret
% erl -name node2@localhost -setcookie secret

% Connect nodes
net_kernel:connect_node('node2@localhost'),
nodes(),   % list connected nodes

% Spawn on remote node
Pid = spawn('node2@localhost', fun() -> io:format("Hello from remote~n") end),

% Send to remote process
{my_server, 'node2@localhost'} ! hello,

%% Hot code loading
code:load_file(my_module),
code:soft_purge(my_module),
code:purge(my_module),

%% Application behavior
-module(my_app).
-behaviour(application).
-export([start/2, stop/1]).

start(_Type, _Args) ->
    my_sup:start_link().

stop(_State) ->
    ok.
```
