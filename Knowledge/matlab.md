# MATLAB Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH MATLAB


## Remarks

MATLAB (Matrix Laboratory) is a high-level language and interactive environment for numerical computation, visualization, and programming. It excels at matrix operations, signal processing, control systems, and scientific computing. GNU Octave is a free, mostly compatible alternative.

Tools: MATLAB IDE, Live Scripts (.mlx), Simulink, toolboxes.


## Hello World

```matlab
% hello.m
disp('Hello, World!')
fprintf('Hello, %s!\n', 'MATLAB')

% Run: type hello in MATLAB prompt, or:
% >> run('hello.m')
```

## Basic Interface

```matlab
% Workspace
whos         % list variables
clear        % clear all
clear x y    % clear specific
clc          % clear command window
close all    % close all figures

% Getting help
help sin
doc sin
lookfor 'fast fourier'

% Semicolon suppresses output
x = 42;      % no output
y = 42       % displays y = 42
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Variables

```matlab
% Scalars
x = 42;
y = 3.14;
z = 2 + 3i;        % complex
b = true;           % logical

% Basic operations
2 + 3, 10 - 4, 5 * 6, 15 / 4   % 5, 6, 30, 3.75
2 ^ 10                            % 1024
mod(17, 5)                        % 2
abs(-5)                           % 5
sqrt(16)                          % 4
floor(3.7), ceil(3.2), round(3.5) % 3, 4, 4

% Type functions
class(x)          % 'double'
isa(x, 'double')  % 1 (true)
isnumeric(x)      % 1
islogical(b)      % 1
ischar('hello')   % 1

% Constants
pi, exp(1), Inf, -Inf, NaN

% Strings (char arrays) and string type
s1 = 'Hello';          % char array
s2 = "Hello";          % string (newer)
s1(1)                  % 'H'
length(s1)             % 5
numel(s1)              % 5
upper(s1)              % 'HELLO'
lower(s1)              % 'hello'
strtrim(s1)            % trim whitespace
strsplit('a,b,c', ',') % {'a','b','c'}
strjoin({'a','b'}, '-') % 'a-b'
strfind(s1, 'ell')     % 2 (index)
strrep(s1,'l','L')     % 'HeLLo'
sprintf('%.2f', pi)    % '3.14'
num2str(42)            % '42'
str2num('42')          % 42
str2double('3.14')     % 3.14
strcmp(s1, 'Hello')    % 1
```


---

# CHAPTER 3: MATRICES AND ARRAYS


## Matrix Operations

```matlab
% Create vectors
row_vec = [1 2 3 4 5];       % row vector
col_vec = [1; 2; 3; 4; 5];  % column vector
range   = 1:5;                % [1 2 3 4 5]
step    = 0:0.5:2;           % [0 0.5 1 1.5 2]
linspace(0, 1, 5)            % [0 0.25 0.5 0.75 1]

% Create matrices
A = [1 2 3; 4 5 6; 7 8 9];  % 3x3 matrix
B = zeros(3, 3);             % 3x3 zeros
C = ones(2, 4);              % 2x4 ones
D = eye(3);                  % 3x3 identity
E = rand(3, 3);              % 3x3 random [0,1]
F = randn(3, 3);             % 3x3 normal(0,1)

% Size and shape
size(A)         % [3 3]
size(A, 1)      % 3 (rows)
size(A, 2)      % 3 (cols)
length(A)       % 3 (max dimension)
numel(A)        % 9 (total elements)
ndims(A)        % 2

% Indexing (1-based!)
A(2, 3)         % row 2, col 3 = 6
A(2, :)         % entire row 2: [4 5 6]
A(:, 3)         % entire col 3: [3;6;9]
A(1:2, 2:3)    % submatrix
A(end, :)       % last row
A(end-1:end, :) % last 2 rows
A([1 3], :)    % rows 1 and 3

% Linear indexing
A(5)            % 5th element column-major: 5
A(:)            % all elements as column vector

% Matrix operations
A + B           % element-wise add
A - B
A * B           % matrix multiply
A .* B          % element-wise multiply
A ./ B          % element-wise divide
A ^ 2           % matrix power (A*A)
A .^ 2          % element-wise square
A'              % transpose
A.'             % non-conjugate transpose

% Linear algebra
det(A)
inv(A)          % inverse
rank(A)
trace(A)
norm(A)         % Frobenius norm
norm(A, 1)      % 1-norm
norm(v)         % Euclidean norm for vectors
eig(A)          % eigenvalues
[V, D] = eig(A) % eigenvectors and values
[U, S, V] = svd(A)
A \ b           % solve Ax=b (backslash)

% Concatenation
[A, B]          % horizontal concat
[A; B]          % vertical concat
[eye(3) A; zeros(3) eye(3)]
```


---

# CHAPTER 4: CONTROL FLOW


## Flow Control

```matlab
% if/elseif/else
x = 10;
if x > 0
    disp('positive')
elseif x == 0
    disp('zero')
else
    disp('negative')
end

% for loop
for i = 1:10
    fprintf('%d ', i);
end
fprintf('\n');

for i = 1:2:10   % step of 2
    disp(i)
end

for row = A'     % iterate columns of A (transpose to iterate rows)
    disp(row)
end

% while loop
n = 1;
while n < 100
    n = n * 2;
end
disp(n)   % 128

% do-while equivalent
do_flag = true;
while do_flag
    n = input('Enter number: ');
    do_flag = (n <= 0);
end

% switch
day = 'Mon';
switch day
    case {'Mon','Tue','Wed','Thu','Fri'}
        disp('Weekday')
    case {'Sat','Sun'}
        disp('Weekend')
    otherwise
        disp('Unknown')
end

% break / continue
for i = 1:10
    if i == 5, break; end
    if mod(i,2) == 0, continue; end
    disp(i)
end

% Logical operators
true & false    % AND (element-wise)
true | false    % OR (element-wise)
~true           % NOT
true && false   % AND (short-circuit)
true || false   % OR (short-circuit)
xor(true, false)
any([0 1 0])   % true if any
all([1 1 1])   % true if all
```


---

# CHAPTER 5: FUNCTIONS


## Defining Functions

```matlab
% function_name.m (one function per file, or local functions)
function result = factorial(n)
    if n <= 1
        result = 1;
    else
        result = n * factorial(n - 1);
    end
end

% Multiple outputs
function [mn, mx] = minmax(v)
    mn = min(v);
    mx = max(v);
end
[a, b] = minmax([3 1 4 1 5 9]);

% Anonymous functions
square = @(x) x.^2;
add    = @(a, b) a + b;
compose = @(f, g) @(x) f(g(x));

% Function handles
f = @sin;
plot(0:0.01:2*pi, f(0:0.01:2*pi))

% feval
feval('sin', pi/2)   % 1

% cellfun, arrayfun, structfun
nums = {1, 4, 9, 16};
result = cellfun(@sqrt, nums)    % [1 2 3 4]

arr = 1:5;
result2 = arrayfun(@(x) x^2 + 1, arr)   % [2 5 10 17 26]

% nargin / nargout (check number of arguments)
function result = flexible(a, b, c)
    if nargin < 2, b = 1; end
    if nargin < 3, c = 0; end
    result = a * b + c;
end

% varargin / varargout
function result = sum_all(varargin)
    result = 0;
    for i = 1:nargin
        result = result + varargin{i};
    end
end
```


---

# CHAPTER 6: PLOTTING AND VISUALIZATION


## Graphics

```matlab
% 2D plot
x = 0:0.01:2*pi;
y = sin(x);
figure;
plot(x, y, 'b-', 'LineWidth', 2)
hold on
plot(x, cos(x), 'r--')
hold off
title('Trig Functions')
xlabel('x')
ylabel('y')
legend('sin(x)', 'cos(x)')
grid on
axis([0 2*pi -1.5 1.5])

% Multiple subplots
figure;
subplot(2, 2, 1); plot(x, sin(x)); title('sin')
subplot(2, 2, 2); plot(x, cos(x)); title('cos')
subplot(2, 2, 3); plot(x, tan(x)); title('tan'); ylim([-5 5])
subplot(2, 2, 4); plot(x, exp(-x)); title('exp(-x)')

% Other plot types
figure;
bar([1 3 2 5 4])
histogram(randn(1000,1), 30)
scatter(randn(100,1), randn(100,1))
pie([30 20 50], {'A','B','C'})
stem(1:10, (1:10).^2)
stairs(1:5, [1 3 2 5 4])
errorbar(1:5, rand(1,5), 0.1*ones(1,5))

% 3D plots
[X, Y] = meshgrid(-3:0.1:3, -3:0.1:3);
Z = sin(X) .* cos(Y);
figure;
surf(X, Y, Z)
colorbar
shading interp
lighting phong

figure;
contour(X, Y, Z, 20)

% Save figure
saveas(gcf, 'plot.png')
print('-dpng', '-r300', 'plot_hq.png')
exportgraphics(gcf, 'plot.pdf')
```


---

# CHAPTER 7: DATA MANIPULATION


## Working with Data

```matlab
% Cell arrays (heterogeneous)
c = {1, 'hello', [1 2 3], true}
c{1}       % 1
c{2}       % 'hello'
c{3}(2)    % 2
c{end}     % true

% Struct
s.name = 'Alice';
s.age  = 30;
s.scores = [85 90 92];

s(2).name = 'Bob';
s(2).age  = 25;
[s.age]    % array of all ages

% Table (like DataFrame)
T = table({'Alice';'Bob'}, [30;25], [90;85], ...
    'VariableNames', {'Name','Age','Score'})

T.Name
T.Age
T(T.Age > 25, :)          % filter rows
T.Bonus = T.Score * 0.1   % add column
sortrows(T, 'Score', 'descend')

% Read/Write data
T2 = readtable('data.csv')
writetable(T, 'output.csv')

data = load('data.mat')
save('output.mat', 'T', 'x', 'y')

% readmatrix / writematrix
M = readmatrix('data.csv')
writematrix(M, 'output.csv')

% Statistical functions
mean(v), median(v), std(v), var(v)
min(v), max(v), sum(v), prod(v)
cumsum(v), cumprod(v)
sort(v), unique(v)
prctile(v, [25 50 75])
corrcoef(x, y)
cov(x, y)
```


---

# CHAPTER 8: ADVANCED MATLAB


## Optimization and ODE

```matlab
% fzero — find root of equation
f = @(x) x^3 - x - 2;
root = fzero(f, 1.5)   % initial guess

% fminbnd — minimize on interval
g = @(x) (x-2)^2 + sin(x);
[xmin, fmin] = fminbnd(g, 0, 5)

% fminsearch — unconstrained multivariate
h = @(v) (v(1)-1)^2 + (v(2)-2)^2;
[x, fval] = fminsearch(h, [0,0])

% ODE solvers
odefun = @(t, y) -2*y;   % dy/dt = -2y
[t, y] = ode45(odefun, [0 5], 1);  % solve from t=0 to 5, y(0)=1
plot(t, y)

% System of ODEs (Lorenz attractor)
sigma=10; rho=28; beta=8/3;
lorenz = @(t, s) [sigma*(s(2)-s(1)); s(1)*(rho-s(3))-s(2); s(1)*s(2)-beta*s(3)];
[t,s] = ode45(lorenz, [0 50], [1;1;1]);
plot3(s(:,1), s(:,2), s(:,3))

% FFT
N = 1024; Fs = 1000;
t = (0:N-1)/Fs;
x = sin(2*pi*50*t) + 0.5*sin(2*pi*120*t);
X = fft(x);
f = (0:N-1)*Fs/N;
plot(f(1:N/2), 2*abs(X(1:N/2))/N)

% Filter design
fc = 100;   % cutoff frequency (Hz)
[b,a] = butter(4, fc/(Fs/2), 'low');
filtered = filter(b, a, x);

% Symbolic math (Symbolic Math Toolbox)
syms x n
diff(sin(x^2), x)          % 2*x*cos(x^2)
int(x^2 * exp(x), x)       % symbolic integral
solve(x^2 - 5*x + 6, x)    % [2, 3]
taylor(sin(x), x, 0, 7)    % Taylor series
symsum(n^2, n, 1, inf)      % sum formula
```
