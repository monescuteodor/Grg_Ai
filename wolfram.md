# Wolfram Language Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH WOLFRAM LANGUAGE


## Remarks

The Wolfram Language (WL) is the programming language behind Mathematica, Wolfram Alpha, and the Wolfram Cloud. It is a symbolic, functional, and rule-based language with built-in knowledge and computation capabilities. Every expression is a symbolic term; computation is rewriting.

Tools: Wolfram Mathematica, Wolfram Engine (free), Wolfram Cloud, Wolfram Alpha, Wolfram Script.


## Hello World

```wolfram
(* Mathematica / Wolfram Language *)
Print["Hello, World!"]

(* String formatting *)
Print["Hello, ", "Wolfram", "!"]
StringJoin["Hello, ", "World", "!"]  (* "Hello, World!" *)

(* Wolfram Script (command line) *)
(* wolframscript -code 'Print["Hello, World!"]' *)
(* wolframscript -file hello.wl *)
```


---

# CHAPTER 2: EXPRESSIONS AND EVALUATION


## Everything is an Expression

```wolfram
(* All expressions have the form: Head[args...] *)
(* Even: Plus[1, 2], Times[3, 4], etc. *)

Head[1 + 2]         (* Plus *)
Head["hello"]       (* String *)
Head[{1, 2, 3}]    (* List *)
Head[Sin[x]]        (* Sin *)
FullForm[1 + 2*x]  (* Plus[1, Times[2, x]] *)

(* Variables and assignment *)
x = 42
y = Pi               (* symbolic constant *)
name = "Alice"
Clear[x, y, name]   (* clear bindings *)

(* Delayed assignment (:=) — evaluated each time *)
f[n_] := n^2 + 1
rand := RandomReal[]   (* evaluates fresh each time *)

(* Symbol attributes *)
Attributes[Plus]     (* {Flat, Listable, NumericFunction, OneIdentity, Orderless, Protected} *)
SetAttributes[myFn, Listable]  (* applies to lists automatically *)

(* Types / Predicates *)
IntegerQ[42]        (* True *)
NumberQ[3.14]       (* True *)
StringQ["hi"]       (* True *)
ListQ[{1,2,3}]     (* True *)
AtomQ[42]          (* True *)
AtomQ[f[x]]        (* False *)

(* Arithmetic *)
2 + 3               (* 5 *)
10 - 4              (* 6 *)
3 * 5               (* 15 *)
10 / 3              (* 10/3 — exact fraction! *)
10 // 3             (* alternative function call syntax *)
N[10/3]             (* 3.33333... — numerical *)
N[Pi, 50]           (* Pi to 50 digits *)
2^100               (* exact: 1267650600228229401496703205376 *)
Mod[17, 5]          (* 2 *)
Quotient[17, 5]     (* 3 *)
GCD[12, 8]          (* 4 *)
LCM[4, 6]           (* 12 *)
Factorial[10]       (* 3628800 *)
Binomial[10, 3]     (* 120 *)
Fibonacci[20]       (* 6765 *)
PrimeQ[17]          (* True *)
Prime[100]          (* 541 — 100th prime *)
```


---

# CHAPTER 3: LISTS AND FUNCTIONAL OPERATIONS


## Lists

```wolfram
(* Lists — fundamental data structure *)
list = {1, 2, 3, 4, 5}
{1, 2, 3, 4, 5}

Length[list]           (* 5 *)
First[list]            (* 1 *)
Last[list]             (* 5 *)
Rest[list]             (* {2, 3, 4, 5} *)
Most[list]             (* {1, 2, 3, 4} *)
list[[1]]              (* 1 — 1-indexed! *)
list[[2;;4]]           (* {2, 3, 4} — span *)
list[[-1]]             (* 5 — last element *)

(* Create lists *)
Range[5]               (* {1, 2, 3, 4, 5} *)
Range[0, 10, 2]        (* {0, 2, 4, 6, 8, 10} *)
Table[i^2, {i, 1, 10}] (* {1, 4, 9, 16, 25, 36, 49, 64, 81, 100} *)
Array[#^2 &, 10]       (* same using pure function *)
ConstantArray[0, 5]    (* {0, 0, 0, 0, 0} *)
RandomReal[{0,1}, 10]  (* 10 random reals *)

(* Modify lists *)
Append[list, 6]        (* {1, 2, 3, 4, 5, 6} — non-destructive *)
Prepend[list, 0]       (* {0, 1, 2, 3, 4, 5} *)
Insert[list, 99, 3]   (* {1, 2, 99, 3, 4, 5} *)
Delete[list, 3]        (* {1, 2, 4, 5} *)
ReplacePart[list, 3 -> 99] (* {1, 2, 99, 4, 5} *)
Join[{1,2}, {3,4}, {5}]    (* {1, 2, 3, 4, 5} *)
Flatten[{{1,2},{3,{4,5}}}] (* {1, 2, 3, 4, 5} *)
Reverse[list]              (* {5, 4, 3, 2, 1} *)
Sort[{3,1,4,1,5}]         (* {1, 1, 3, 4, 5} *)
Sort[list, Greater]        (* descending *)
SortBy[words, StringLength]
Union[{1,2,2,3,3}]         (* {1, 2, 3} — unique+sorted *)
Intersection[{1,2,3},{2,3,4}] (* {2, 3} *)
Complement[{1,2,3,4},{2,4}]   (* {1, 3} *)
Tally[{1,2,2,3,3,3}]       (* {{1,1},{2,2},{3,3}} *)

(* Functional operations *)
Map[f, {1,2,3}]             (* {f[1], f[2], f[3]} *)
Map[#^2 &, {1,2,3}]         (* {1, 4, 9} *)
{1,2,3,4,5} /@ (# * 2 &)   (* {2, 4, 6, 8, 10} — shorthand Map *)
Select[Range[10], EvenQ]    (* {2, 4, 6, 8, 10} *)
Cases[{1,"a",2,"b",3}, _Integer] (* {1, 2, 3} *)
Pick[list, {True,False,True,False,True}] (* {1, 3, 5} *)
Fold[Plus, 0, {1,2,3,4,5}] (* 15 *)
FoldList[Plus, 0, {1,2,3}] (* {0, 1, 3, 6} *)
Apply[Plus, list]           (* 15 = Plus @@ list *)
Apply[Plus, {{1,2},{3,4}}, 1] (* {3, 7} — apply at level 1 *)
Total[list]                 (* 15 *)
Times @@ list               (* 120 — product *)
MapAt[#^2 &, list, {{1},{3}}] (* square elements 1 and 3 *)
MapThread[f, {{1,2,3},{a,b,c}}] (* {f[1,a],f[2,b],f[3,c]} *)
MapIndexed[{#1, First@#2} &, list] (* {val,idx} pairs *)
```


---

# CHAPTER 4: PATTERNS AND RULES


## Pattern Matching

```wolfram
(* Patterns *)
_ (* any single expression (blank) *)
__ (* any sequence of 1+ expressions *)
___ (* any sequence of 0+ expressions *)
_h (* any expression with head h *)
x_ (* any expression, bound to x *)
x_Integer (* any integer, bound to x *)
x_ /; x > 0 (* any positive number *)

(* Matching *)
MatchQ[3, _Integer]    (* True *)
MatchQ[{1,2,3}, {__Integer}] (* True *)
MatchQ[f[x,y], f[_,_]] (* True *)

(* Replace / ReplaceAll *)
x^2 + y /. x -> 3              (* 9 + y *)
x^2 + y /. {x -> 3, y -> 1}   (* 10 *)
x^2 + x + 1 /. x^n_ -> a^n    (* a^2 + a + 1 — replace pattern *)
{1,2,3,4,5} /. n_ /; n > 3 -> 0  (* {1,2,3,0,0} *)

(* Replace repeatedly *)
{1,2,3} //. x:{a___,b_,c_,d___} /; b > c :> {a,c,b,d}  (* sort! *)

(* Rules as data *)
rules = {a -> 1, b -> 2, c -> 3}
a + b + c /. rules   (* 6 *)

(* Function definitions use patterns *)
f[0] = 1
f[n_Integer /; n > 0] := n * f[n-1]
f[5]   (* 120 *)

(* Multiple definitions *)
g[x_, y_] := x + y
g[x_, y_, z_] := x + y + z

(* _ default values *)
h[x_, y_:0] := x + y   (* y defaults to 0 *)
h[3]        (* 3 *)
h[3, 4]     (* 7 *)
```


---

# CHAPTER 5: CALCULUS AND ALGEBRA


## Symbolic Mathematics

```wolfram
(* Calculus *)
D[Sin[x], x]              (* Cos[x] *)
D[x^3 + 2x^2 - x, x]    (* 3x^2 + 4x - 1 *)
D[f[x], {x, 2}]          (* f''[x] — second derivative *)
D[x*y^2 + z, y]          (* 2xy — partial derivative *)

Integrate[x^2, x]          (* x^3/3 *)
Integrate[Sin[x], {x, 0, Pi}]  (* 2 *)
Integrate[Exp[-x^2], {x, -Infinity, Infinity}]  (* Sqrt[Pi] *)

Limit[Sin[x]/x, x -> 0]   (* 1 *)
Limit[(1 + 1/n)^n, n -> Infinity]  (* E *)

Series[Sin[x], {x, 0, 7}]  (* Taylor series up to x^7 *)
Series[1/(1-x), {x, 0, 5}] (* geometric series *)

Sum[n^2, {n, 1, 10}]      (* 385 *)
Sum[1/n^2, {n, 1, Infinity}]  (* Pi^2/6 — Euler *)
Product[n, {n, 1, 10}]    (* 3628800 *)

(* Algebra *)
Expand[(x + y)^3]
Factor[x^3 - 3x^2 + 3x - 1]   (* (x-1)^3 *)
Simplify[(x^2 - 1)/(x - 1)]    (* 1 + x *)
FullSimplify[expression]
Together[(1/x + 1/y)]           (* (x+y)/(xy) *)
Apart[(x^2+1)/(x*(x-1))]       (* partial fractions *)
Cancel[(x^2-1)/(x+1)]          (* x-1 *)

(* Solving equations *)
Solve[x^2 - 5x + 6 == 0, x]    (* {{x->2},{x->3}} *)
NSolve[x^3 - x - 2 == 0, x]    (* numerical solutions *)
Reduce[x^2 < 9, x]              (* -3 < x < 3 *)
FindRoot[Cos[x] == x, {x, 0.5}]  (* {x -> 0.739085} *)

(* Systems of equations *)
Solve[{x + y == 5, x - y == 1}, {x, y}]  (* {{x->3, y->2}} *)

(* Differential equations *)
DSolve[y'[x] == y[x], y, x]   (* {{y->C[1]*E^x}} *)
DSolve[{y'[x] == -2*y[x], y[0] == 1}, y, x]  (* {{y->E^(-2x)}} *)
NDSolve[{y'[x] == -2*y[x], y[0] == 1}, y, {x, 0, 5}]
```


---

# CHAPTER 6: GRAPHICS


## Visualization

```wolfram
(* 2D plotting *)
Plot[Sin[x], {x, 0, 2Pi}]
Plot[{Sin[x], Cos[x]}, {x, 0, 2Pi}]
Plot[Sin[x], {x, 0, 2Pi},
    PlotStyle -> {Thick, Blue},
    AxesLabel -> {"x", "sin(x)"},
    PlotLabel -> "Sine Wave"]

(* Parametric *)
ParametricPlot[{Sin[t], Cos[t]}, {t, 0, 2Pi}]
ParametricPlot[{t*Cos[t], t*Sin[t]}, {t, 0, 4Pi}]  (* spiral *)

(* Discrete data *)
ListPlot[{1, 4, 9, 16, 25}]
ListLinePlot[{1, 4, 9, 16, 25}]
ListLogPlot[Range[10]]

(* 3D plotting *)
Plot3D[Sin[x*y], {x, -Pi, Pi}, {y, -Pi, Pi}]
Plot3D[Sin[x]*Cos[y], {x, -Pi, Pi}, {y, -Pi, Pi},
    ColorFunction -> "Rainbow",
    PlotPoints -> 50]

ContourPlot[x^2 + y^2, {x, -2, 2}, {y, -2, 2}]
DensityPlot[Sin[x]*Sin[y], {x, -Pi, Pi}, {y, -Pi, Pi}]

(* Bar, pie, histogram *)
BarChart[{3, 1, 4, 1, 5, 9}]
PieChart[{30, 25, 45}]
Histogram[RandomReal[{0, 1}, 1000]]

(* 3D data *)
ListPlot3D[Table[Sin[i] + Cos[j], {i, 0, 2Pi, Pi/10}, {j, 0, 2Pi, Pi/10}]]

(* Show multiple graphics *)
Show[Plot[Sin[x], {x, 0, 2Pi}], Plot[Cos[x], {x, 0, 2Pi}]]

(* Export *)
Export["plot.png", Plot[Sin[x], {x, 0, 2Pi}]]
Export["plot.pdf", plot]
```


---

# CHAPTER 7: FUNCTIONAL PROGRAMMING


## Functional Patterns

```wolfram
(* Pure functions (Function or & shorthand) *)
Function[x, x^2][5]    (* 25 *)
(#^2 &)[5]             (* 25 — shorthand *)
(#1 + #2 &)[3, 4]      (* 7 — named slots *)

(* Composition *)
Composition[f, g, h][x]   (* f[g[h[x]]] *)
(f @* g @* h)[x]          (* same — @* = Composition *)

(* Repeated application *)
Nest[f, x, 3]         (* f[f[f[x]]] *)
NestList[f, x, 3]     (* {x, f[x], f[f[x]], f[f[f[x]]]} *)
NestWhile[#*2 &, 1, # < 100 &]   (* 128 — double while < 100 *)
FixedPoint[Cos, 1.0]  (* 0.739085... — iterate until stable *)
FixedPointList[Cos, 1.0]

(* Conditional / patterns *)
Piecewise[{{x^2, x < 0}, {x, x >= 0}}]   (* piecewise function *)
Which[x < 0, "neg", x == 0, "zero", True, "pos"]

(* Thread / Map variants *)
f /@ {1,2,3}           (* Map: {f[1],f[2],f[3]} *)
f @@@ {{1,2},{3,4}}    (* Apply at level 1: {f[1,2],f[3,4]} *)
{1,2,3} // f           (* Postfix: f[{1,2,3}] *)

(* Scan (like Map but for side effects) *)
Scan[Print, {1, 2, 3}]   (* prints 1, 2, 3 *)

(* Reap / Sow (collect values) *)
{result, collected} = Reap[
    Do[Sow[i^2], {i, 1, 5}]
]  (* result = Null, collected = {{1,4,9,16,25}} *)
```


---

# CHAPTER 8: ASSOCIATION, STRING, AND CONTROL


## Data and Control

```wolfram
(* Association (key-value / dictionary) *)
assoc = <|"name" -> "Alice", "age" -> 30, "city" -> "NYC"|>
assoc["name"]             (* "Alice" *)
assoc[["age"]]            (* 30 — part notation *)
KeyExistsQ[assoc, "name"] (* True *)
Keys[assoc]               (* {"name","age","city"} *)
Values[assoc]             (* {"Alice",30,"NYC"} *)
KeyTake[assoc, {"name","age"}]
KeyDrop[assoc, {"city"}]
Map[# + 1 &, <|a->1, b->2, c->3|>]  (* <|a->2,b->3,c->4|> *)
Merge[{<|a->1|>, <|a->2, b->3|>}, Total]  (* <|a->3, b->3|> *)

(* String operations *)
StringLength["hello"]              (* 5 *)
ToUpperCase["hello"]               (* "HELLO" *)
ToLowerCase["HELLO"]               (* "hello" *)
StringTake["hello world", 5]       (* "hello" *)
StringDrop["hello world", 6]       (* "world" *)
StringPart["hello", 1]             (* "h" *)
StringJoin["Hello", ", ", "World!"] (* "Hello, World!" *)
StringReplace["hello", "l" -> "L"]  (* "heLLo" *)
StringSplit["a,b,c", ","]           (* {"a","b","c"} *)
StringContainsQ["hello", "ell"]     (* True *)
StringStartsQ["hello", "he"]        (* True *)
StringMatchQ["hello", "h" ~~ __ ~~ "o"]  (* True — string pattern *)
StringCases["phone: 555-1234", DigitCharacter..]  (* {"555","1234"} *)
StringReplace["x=42", NumberString -> "N"]  (* "x=N" *)

(* Control flow *)
If[condition, t, f]
Which[c1, v1, c2, v2, True, default]
Switch[val, p1, v1, p2, v2, _, default]

Do[Print[i], {i, 1, 5}]               (* loop 1 to 5 *)
Do[Print[i], {i, 1, 10, 2}]           (* loop with step *)
Do[f[i, j], {i, 1, 3}, {j, 1, 3}]    (* nested loop *)

While[n > 0, n -= 1]
For[i = 0, i < 10, i++, Print[i]]

(* Module — local variables *)
Module[{x = 10, y = 20},
    x^2 + y^2]

(* Block — temporarily change global values *)
x = 5;
Block[{x = 100}, x^2]   (* 10000, then x is 5 again *)

(* With — substitution *)
With[{n = 42}, n^2 + n]   (* 1806 *)
```
