# Mathematica Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH MATHEMATICA


## Remarks

Mathematica is a computational software program developed by Wolfram Research (Stephen Wolfram, 1988). It integrates symbolic computation, numerical computation, visualization, programming, and document creation. Mathematica notebooks combine code, results, text, and graphics in a single interactive document. The underlying language is the Wolfram Language.

Tools: Mathematica (commercial), Wolfram Engine (free for developers), Wolfram Cloud, Wolfram Alpha.


## Basic Usage

```mathematica
(* Cells in a Mathematica notebook *)
(* Press Shift+Enter to evaluate *)

(* Hello World *)
Print["Hello, World!"]

(* Output display — just type an expression *)
2 + 2
(* → 4 *)

3.14 * 2^10
(* → 3215.36 *)

(* Comments use (* ... *) *)

(* Last result *)
%           (* most recent output *)
%%          (* second most recent *)
%n          (* nth output line *)

(* Assignments *)
x = 5             (* assign variable *)
y := x^2          (* delayed assignment (evaluated when used) *)
Clear[x, y]       (* remove variables *)

(* Function definition *)
f[x_] := x^2 + 1
f[3]          (* → 10 *)
f[{1,2,3}]    (* → {2, 5, 10}  (auto-threads over lists) *)

(* Multi-argument *)
g[x_, y_] := x^2 + y^2
g[3, 4]     (* → 25 *)
```

```bash
# Running Mathematica from command line
math                           # interactive REPL
math -script myfile.m         # run script
wolframscript -file myfile.wl # run Wolfram Script
```


---

# CHAPTER 2: SYMBOLIC COMPUTATION


## Algebra and Calculus

```mathematica
(* === ALGEBRA === *)

(* Expand and Factor *)
Expand[(x + y)^4]
(* → x^4 + 4x^3y + 6x^2y^2 + 4xy^3 + y^4 *)

Factor[x^4 - 1]
(* → (1 + x^2)(1 - x)(1 + x) *)

Simplify[Sin[x]^2 + Cos[x]^2]
(* → 1 *)

FullSimplify[(x^2 - 1)/(x - 1)]
(* → 1 + x *)

(* Solve equations *)
Solve[x^2 - 5x + 6 == 0, x]
(* → {{x → 2}, {x → 3}} *)

Solve[{x + y == 5, x - y == 1}, {x, y}]
(* → {{x → 3, y → 2}} *)

NSolve[x^5 - x + 1 == 0, x]      (* numerical solve *)

FindRoot[Sin[x] == x/2, {x, 1}]  (* numerical root finding *)
(* → {x → 1.89549} *)

(* Reduce (general solver) *)
Reduce[x^2 < 9, x]
(* → -3 < x < 3 *)

(* === CALCULUS === *)

(* Derivatives *)
D[Sin[x], x]              (* → Cos[x] *)
D[x^3 * E^x, x]          (* → E^x (3x^2 + x^3) *)
D[f[x], {x, 3}]          (* third derivative *)
D[f[x, y], x, y]         (* partial derivative ∂²f/∂x∂y *)

(* Integrals *)
Integrate[x^2, x]             (* → x^3/3 *)
Integrate[Sin[x], {x, 0, Pi}] (* → 2  (definite integral) *)
NIntegrate[E^(-x^2), {x, -Infinity, Infinity}]  (* → 1.7725 *)

(* Series expansion *)
Series[Sin[x], {x, 0, 7}]
(* → x - x^3/6 + x^5/120 - x^7/5040 + O[x]^8 *)

Normal[%]  (* drop the O[x] term *)

(* Limits *)
Limit[Sin[x]/x, x -> 0]         (* → 1 *)
Limit[(1 + 1/n)^n, n -> Infinity] (* → E *)

(* === DIFFERENTIAL EQUATIONS === *)
DSolve[y'[x] == y[x], y[x], x]
(* → {{y[x] → E^x C[1]}} *)

DSolve[{y''[x] + y[x] == 0, y[0] == 1, y'[0] == 0}, y[x], x]
(* → {{y[x] → Cos[x]}} *)

NDSolve[{y'[x] == y[x], y[0] == 1}, y, {x, 0, 5}]  (* numerical *)
```


---

# CHAPTER 3: LISTS AND FUNCTIONAL PROGRAMMING


## Working with Lists

```mathematica
(* === CREATING LISTS === *)
{1, 2, 3, 4, 5}                   (* literal list *)
Range[5]                           (* {1, 2, 3, 4, 5} *)
Range[2, 10, 2]                    (* {2, 4, 6, 8, 10} *)
Table[i^2, {i, 1, 5}]             (* {1, 4, 9, 16, 25} *)
Table[{i, j}, {i, 2}, {j, 3}]    (* 2x3 nested list *)
ConstantArray[0, {3, 3}]          (* 3x3 zero matrix *)
RandomReal[{0, 1}, 10]            (* 10 random reals *)

(* === LIST OPERATIONS === *)
lst = {3, 1, 4, 1, 5, 9, 2, 6};
Length[lst]           (* 8 *)
First[lst]            (* 3 *)
Last[lst]             (* 6 *)
Rest[lst]             (* {1, 4, 1, 5, 9, 2, 6} *)
Most[lst]             (* {3, 1, 4, 1, 5, 9, 2} *)
lst[[3]]              (* 4  (1-indexed) *)
lst[[2;;5]]           (* {1, 4, 1, 5}  (span) *)
lst[[-1]]             (* 6  (last element) *)
Take[lst, 3]          (* {3, 1, 4} *)
Drop[lst, -2]         (* {3, 1, 4, 1, 5, 9} *)

Append[lst, 7]        (* {3, 1, 4, 1, 5, 9, 2, 6, 7} *)
Prepend[lst, 0]       (* {0, 3, 1, 4, 1, 5, 9, 2, 6} *)
Join[{1,2}, {3,4}]    (* {1, 2, 3, 4} *)
Flatten[{1, {2, 3}, {4, {5}}}]  (* {1, 2, 3, 4, 5} *)

Sort[lst]             (* {1, 1, 2, 3, 4, 5, 6, 9} *)
Reverse[lst]          (* {6, 2, 9, 5, 1, 4, 1, 3} *)
Union[lst]            (* {1, 2, 3, 4, 5, 6, 9} (sorted unique) *)

(* === FUNCTIONAL OPERATIONS === *)
Map[f, {1, 2, 3}]              (* {f[1], f[2], f[3]} *)
Map[#^2 &, {1, 2, 3}]         (* {1, 4, 9}  (pure function) *)
{1, 2, 3}^2                   (* {1, 4, 9}  (auto-thread) *)

Select[{1,2,3,4,5,6}, EvenQ]  (* {2, 4, 6} *)
Select[lst, # > 4 &]           (* {5, 9, 6} *)

Fold[Plus, 0, {1,2,3,4,5}]    (* 15  (foldl) *)
FoldList[Plus, 0, {1,2,3,4,5}] (* {0,1,3,6,10,15} running sum *)
Total[lst]                     (* 31 *)
Times @@ {1,2,3,4,5}          (* 120  (Apply at level 0) *)
Plus @@ {1,2,3,4,5}           (* 15 *)

(* Cases — select by pattern *)
Cases[{1, "a", 2, "b", 3}, _Integer]  (* {1, 2, 3} *)
Cases[{f[1], g[2], f[3]}, f[x_] :> x] (* {1, 3} *)

(* Thread — zip *)
Thread[f[{1,2,3}, {4,5,6}]]  (* {f[1,4], f[2,5], f[3,6]} *)
Transpose[{{1,2},{3,4},{5,6}}]  (* {{1,3,5},{2,4,6}} *)
```


---

# CHAPTER 4: MATRICES AND LINEAR ALGEBRA


## Matrix Operations

```mathematica
(* === MATRIX CREATION === *)
m = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
MatrixForm[m]         (* display as grid *)
Dimensions[m]         (* {3, 3} *)
m[[2, 3]]             (* 6  (row 2, col 3) *)
m[[All, 2]]           (* {2, 5, 8}  (column 2) *)
m[[1;;2, 2;;3]]       (* submatrix *)

(* === MATRIX ARITHMETIC === *)
m + m                          (* element-wise add *)
2 m                            (* scalar multiply *)
m . m                          (* matrix multiply (dot) *)
m^2                            (* element-wise square *)
MatrixPower[m, 3]              (* matrix cubed: m.m.m *)

(* === LINEAR ALGEBRA === *)
Det[m]                (* determinant *)
Inverse[m]            (* inverse *)
Transpose[m]          (* transpose *)
Tr[m]                 (* trace *)

(* Solve Ax = b *)
A = {{2, 1}, {1, 3}};
b = {5, 10};
LinearSolve[A, b]     (* → {1, 3} *)

(* Eigenvalues and eigenvectors *)
Eigenvalues[{{1,2},{2,1}}]        (* → {3, -1} *)
Eigenvectors[{{1,2},{2,1}}]       (* → {{1,1},{-1,1}} *)
{vals, vecs} = Eigensystem[m];

(* Singular Value Decomposition *)
SingularValueDecomposition[m]     (* {U, Sigma, V} *)

(* Null space, row reduction *)
NullSpace[m]
RowReduce[m]
MatrixRank[m]

(* Norms *)
Norm[{3, 4}]              (* 5  (Euclidean norm) *)
Norm[m, "Frobenius"]      (* Frobenius norm *)

(* Special matrices *)
IdentityMatrix[4]
DiagonalMatrix[{1, 2, 3}]
Table[KroneckerDelta[i, j], {i, 3}, {j, 3}]
```


---

# CHAPTER 5: GRAPHICS AND VISUALIZATION


## Plotting and 3D Graphics

```mathematica
(* === 2D PLOTS === *)
Plot[Sin[x], {x, 0, 2 Pi}]

Plot[{Sin[x], Cos[x]}, {x, 0, 2 Pi},
    PlotLegends -> {"Sin", "Cos"},
    PlotStyle -> {Red, Blue},
    AxesLabel -> {"x", "y"},
    PlotLabel -> "Trigonometric Functions"]

(* Parametric *)
ParametricPlot[{Cos[t], Sin[t]}, {t, 0, 2Pi}]

(* Polar *)
PolarPlot[1 + Cos[theta], {theta, 0, 2Pi}]

(* Data *)
ListPlot[{1, 4, 9, 16, 25}]
ListLinePlot[{1, 4, 9, 16, 25}]

(* Contour *)
ContourPlot[Sin[x]*Cos[y], {x, -Pi, Pi}, {y, -Pi, Pi}]
DensityPlot[Sin[x]*Cos[y], {x, -Pi, Pi}, {y, -Pi, Pi}]

(* === 3D PLOTS === *)
Plot3D[Sin[x*y], {x, -Pi, Pi}, {y, -Pi, Pi}]
ParametricPlot3D[{Sin[t], Cos[t], t/5}, {t, 0, 4Pi}]
ContourPlot3D[x^2 + y^2 + z^2 == 4, {x,-3,3}, {y,-3,3}, {z,-3,3}]
SphericalPlot3D[1, {theta, 0, Pi}, {phi, 0, 2Pi}]

(* === STATISTICAL GRAPHICS === *)
BarChart[{3, 7, 2, 8, 5}]
Histogram[RandomVariate[NormalDistribution[], 1000]]
BoxWhiskerChart[{{1,2,3,4,5}, {3,4,5,6,7}}]
SmoothHistogram[RandomVariate[NormalDistribution[], 1000]]

(* === GRAPHICS PRIMITIVES === *)
Graphics[{
    Red, Disk[{0, 0}, 1],
    Blue, Rectangle[{-2, -2}, {-1, -1}],
    Green, Line[{{0,0}, {2, 1}, {3, -1}}],
    Text["Label", {1, 1}]
}]

(* === MANIPULATE (interactive) === *)
Manipulate[
    Plot[Sin[a x + b], {x, 0, 2Pi}],
    {a, 1, 5},
    {b, 0, Pi}
]

(* === ANIMATE === *)
Animate[
    Plot[Sin[x + t], {x, 0, 2Pi}],
    {t, 0, 2Pi}
]

(* === EXPORT === *)
Export["plot.png", Plot[Sin[x], {x, 0, 2Pi}]]
Export["data.csv", {{1, 2}, {3, 4}}]
Export["image.pdf", Graphics[...]]
```


---

# CHAPTER 6: PROGRAMMING


## Mathematica Programming

```mathematica
(* === CONDITIONALS === *)
If[3 > 2, "yes", "no"]       (* → "yes" *)
If[x > 0, x, -x]             (* absolute value *)
Which[x < 0, "negative", x == 0, "zero", True, "positive"]
Switch[x, 1, "one", 2, "two", _, "other"]

(* === LOOPS === *)
(* For loop *)
For[i = 1, i <= 5, i++,
    Print[i]
]

(* While loop *)
n = 1;
While[n < 100, n = n * 2];
n  (* → 128 *)

(* Do loop *)
Do[Print[i^2], {i, 5}]

(* Functional (preferred) *)
Table[i^2, {i, 1, 5}]
Array[#^2 &, 5]
NestList[# * 2 &, 1, 7]    (* {1,2,4,8,16,32,64,128} *)

(* === PATTERNS AND RULES === *)
rule = x^2 -> "squared";
x^2 /. rule              (* → "squared" *)

rules = {x -> 3, y -> 4};
x^2 + y^2 /. rules       (* → 25 *)

(* Replace all occurrences *)
expr = f[a, f[b, c]];
expr //. f[x_, y_] -> {x, y}

(* Pattern matching *)
MatchQ[{1, 2, 3}, {__Integer}]  (* True *)
MatchQ[f[x, y], f[_, _]]        (* True *)

(* === MODULES AND BLOCKS === *)
Module[{x, y},
    x = 3; y = 4;
    Sqrt[x^2 + y^2]
]  (* → 5; x,y local *)

Block[{x = 3, y = 4},
    x + y
]  (* → 7; x,y temporarily set *)

With[{x = 3, y = 4},
    x^2 + y^2
]  (* → 25; x,y substituted symbolically *)

(* === PURE FUNCTIONS === *)
#^2 &                    (* pure function: argument^2 *)
(#1 + #2) &              (* two arguments *)
Function[x, x^2]         (* explicit form *)
Function[{x, y}, x + y]

Map[#^2 &, {1,2,3}]      (* {1,4,9} *)
Select[Range[10], OddQ]  (* {1,3,5,7,9} *)
Sort[{3,1,4}, # < #2 &]  (* wait: use Sort[lst, f[#1,#2]&] *)
```


---

# CHAPTER 7: STATISTICS AND PROBABILITY


## Statistical Analysis

```mathematica
(* === DESCRIPTIVE STATISTICS === *)
data = {2, 4, 4, 4, 5, 5, 7, 9};
Mean[data]                (* 5 *)
Median[data]              (* 4.5 *)
Variance[data]            (* 4 *)
StandardDeviation[data]   (* 2 *)
Skewness[data]
Kurtosis[data]
Min[data]; Max[data]
Quantile[data, {0.25, 0.5, 0.75}]  (* quartiles *)

(* Dataset summary *)
data2 = RandomVariate[NormalDistribution[0, 1], 1000];
{Mean[data2], StandardDeviation[data2]}

(* === DISTRIBUTIONS === *)
dist = NormalDistribution[0, 1]
PDF[dist, 0]              (* 0.3989... density at 0 *)
CDF[dist, 1.96]           (* 0.975... cumulative probability *)
InverseCDF[dist, 0.975]   (* 1.96   quantile *)

RandomVariate[dist, 10]   (* 10 random samples *)

(* Common distributions *)
BinomialDistribution[n, p]
PoissonDistribution[lambda]
ExponentialDistribution[lambda]
UniformDistribution[{a, b}]
TDistribution[k]
ChiSquareDistribution[k]

(* Fit distribution *)
fitted = FindDistributionParameters[data, NormalDistribution[mu, sigma]]
EstimatedDistribution[data, NormalDistribution[mu, sigma]]

(* === HYPOTHESIS TESTING === *)
MeanTest[data, 5]               (* t-test: H0: mean = 5 *)
LocationTest[data1, data2]      (* two-sample t-test *)
VarianceTest[data]              (* chi-square test for variance *)
FisherHypergeometricDistribution

(* === LINEAR REGRESSION === *)
x = {1, 2, 3, 4, 5};
y = {2.1, 3.9, 6.2, 7.8, 10.1};

lm = LinearModelFit[Transpose[{x, y}], {1, x}, x]
lm["ParameterTable"]
lm["RSquared"]
lm[3.5]               (* predict at x=3.5 *)

(* Non-linear fit *)
nlm = NonlinearModelFit[data, a * E^(b * x), {a, b}, x]
```


---

# CHAPTER 8: ADVANCED FEATURES


## Mathematica's Unique Capabilities

```mathematica
(* === WOLFRAM ALPHA INTEGRATION === *)
WolframAlpha["speed of light in m/s", "Result"]
WolframAlpha["population of Japan", {{"Result", 1}, "ComputableData"}]
WolframAlpha["integrate sin(x^2) from 0 to 1"]

(* === NATURAL LANGUAGE === *)
N[Pi, 50]               (* 50-digit precision *)
N[Sqrt[2], 100]
Pi + E                  (* symbolic *)

(* === BUILT-IN MATHEMATICAL FUNCTIONS === *)
Gamma[5]                (* 24 = 4! *)
Zeta[2]                 (* Pi^2/6 ≈ 1.6449 *)
BesselJ[0, x]
LegendreP[3, x]
EllipticK[k]
HypergeometricPFQ[{a}, {b}, z]
ProductLog[x]           (* Lambert W function *)

(* === GRAPH THEORY === *)
g = Graph[{1->2, 2->3, 3->4, 4->1, 1->3}];
AdjacencyMatrix[g]
GraphDiameter[g]
VertexList[g]
ShortestPath[g, 1, 4]
FindHamiltonianCycle[g]

(* === STRING OPERATIONS === *)
StringLength["Hello"]         (* 5 *)
StringJoin["Hello", " ", "World"]  (* "Hello World" *)
StringSplit["a,b,c", ","]     (* {"a","b","c"} *)
StringContainsQ["Hello", "ell"]  (* True *)
StringReplace["abc123", DigitCharacter -> "X"]  (* "abcXXX" *)
RegularExpression["\\d+"]     (* regex *)

(* === EXPORT AND IMPORT === *)
Import["data.csv"]
Import["image.png"]
Import["http://example.com/data.json"]
Export["result.xlsx", Table[{i, i^2}, {i, 10}]]
ExportString[{1,2,3}, "JSON"]

(* === PARALLEL COMPUTATION === *)
LaunchKernels[4]       (* start 4 parallel kernels *)
ParallelMap[f, bigList]
ParallelTable[f[i], {i, 1000}]
ParallelDo[Print[i], {i, 10}]

(* === DYNAMIC INTERACTIVITY === *)
DynamicModule[{x = 1},
    Column[{
        Slider[Dynamic[x], {1, 100}],
        Dynamic[x^2]
    }]
]

(* === MACHINE LEARNING === *)
classifier = Classify[
    {1 -> "odd", 2 -> "even", 3 -> "odd", 4 -> "even"}
];
classifier[7]           (* → "odd" *)

Predict[{1 -> 1, 2 -> 4, 3 -> 9, 4 -> 16}, {5, 6}]  (* → {25, 36} *)

NetChain[{LinearLayer[10], Ramp, LinearLayer[1]}]  (* neural net *)

(* === NOTEBOOK FORMATTING === *)
Style["Big Text", 24]
Style["Bold", Bold]
Style["Colored", Red]
Framed["Box around this"]
Grid[{{1,2},{3,4}}, Frame -> All]
Column[{item1, item2, item3}]
Row[{item1, item2}, " | "]
```
