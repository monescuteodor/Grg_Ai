# GNU Octave Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH OCTAVE


## Remarks

GNU Octave is a free, open-source numerical computation language largely compatible with MATLAB. It provides powerful matrix operations, a rich set of mathematical functions, and can run most MATLAB scripts without modification. Widely used in academia and scientific computing.

Tools: octave CLI, Octave GUI, Octave Online, Jupyter with the Octave kernel.


## Hello World

```octave
% hello.m
disp('Hello, World!')
fprintf('Hello, %s!\n', 'Octave')
printf('Hello from printf!\n')

% Run:
% octave hello.m
% octave --no-gui hello.m
% octave-cli hello.m
```

```octave
% Interactive session
% >> disp("Hello!")
% Hello!
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Variables and Data Types

```octave
% Scalars
x = 42
y = 3.14
z = 2 + 3i          % complex number
b = true             % logical
b2 = false

% Semicolons suppress output
x = 42;    % no output
y = 42     % displays y = 42

% Workspace
whos         % list variables with types
clear x y    % clear specific variables
clear        % clear all

% Type checking
class(x)        % 'double'
isnumeric(x)    % 1 (true)
isinteger(x)    % 0 (false — 42 is double!)
islogical(b)    % 1
ischar('hi')    % 1

% Integer types
n = int8(127)
n = int16(1000)
n = int32(100000)
n = int64(1e10)
n = uint8(255)
n = uint32(4294967295)

% Logical operations
true & false    % AND
true | false    % OR
~true           % NOT
true && false   % short-circuit AND
true || false   % short-circuit OR
xor(true, false)

% Strings (character arrays)
s = 'Hello, World!';
length(s)          % 13
numel(s)           % 13
upper(s)           % 'HELLO, WORLD!'
lower(s)           % 'hello, world!'
strtrim(s)         % trim whitespace
s(1)               % 'H' (1-indexed)
s(1:5)             % 'Hello'
strcat('Hello', ' World')  % 'Hello World'
[s, ' more']               % concatenate
strsplit('a,b,c', ',')    % {'a','b','c'}
strjoin({'a','b'}, '-')   % 'a-b'
strrep(s, 'World', 'Octave')
strfind(s, 'World')        % 8 (position)
sprintf('%.2f', pi)        % '3.14'
num2str(42)                % '42'
str2num('42')              % 42
str2double('3.14')         % 3.14
strcmp(s, 'Hello')         % 0 (false)
strcmpi(s, 'hello')        % case-insensitive compare
```


---

# CHAPTER 3: MATRICES AND ARRAYS


## Matrix Operations

```octave
% Row vector
row = [1 2 3 4 5];
row = [1, 2, 3, 4, 5];   % commas optional

% Column vector
col = [1; 2; 3; 4; 5];

% Ranges
r1 = 1:5;           % [1 2 3 4 5]
r2 = 0:0.5:2;       % [0 0.5 1.0 1.5 2.0]
r3 = linspace(0, 1, 5);  % [0 0.25 0.5 0.75 1]

% Matrix (rows separated by ;)
A = [1 2 3; 4 5 6; 7 8 9];   % 3x3
B = zeros(3, 4);               % 3x4 zeros
C = ones(2, 3);                % 2x3 ones
D = eye(3);                    % 3x3 identity
E = rand(3, 3);                % uniform random [0,1]
F = randn(3, 3);               % normal random

% Size and shape
size(A)         % [3, 3]
size(A, 1)      % 3 (rows)
size(A, 2)      % 3 (cols)
length(A)       % 3 (max dim)
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

% Linear indexing (column-major order)
A(5)            % 5th element
A(:)            % all as column vector

% Modify elements
A(1, 1) = 99;
A(:, 2) = 0;    % set column to zero

% Matrix arithmetic
A + B           % element-wise (if same size)
A - B
A * B           % matrix multiply
A .* B          % element-wise multiply
A ./ B          % element-wise divide
A .^ 2          % element-wise square
A ^ 2           % matrix power (A*A)
A'              % conjugate transpose
A.'             % non-conjugate transpose
-A              % negate

% Linear algebra
det(A)
inv(A)          % matrix inverse
rank(A)
trace(A)        % sum of diagonal
norm(A)         % Frobenius norm
norm(v)         % vector 2-norm
eig(A)          % eigenvalues
[V, D] = eig(A) % eigenvectors and values
[U, S, V] = svd(A)     % SVD
A \ b           % solve Ax = b (backslash operator)

% Concatenation
[A, B]          % horizontal concatenate
[A; B]          % vertical concatenate
horzcat(A, B)
vertcat(A, B)
cat(1, A, B)    % along dim 1
cat(2, A, B)    % along dim 2

% Reshaping
reshape(A, 1, 9)   % 1x9
reshape(A, 9, 1)   % 9x1
```


---

# CHAPTER 4: CONTROL FLOW


## Flow Control

```octave
% if / elseif / else
x = 10;
if x > 0
    disp('positive')
elseif x == 0
    disp('zero')
else
    disp('negative')
end

% Ternary-like (no ternary in Octave, but ifelse() works on arrays)
y = ifelse(x > 0, 'pos', 'neg');

% for loop
for i = 1:10
    fprintf('%d ', i);
end
fprintf('\n');

for i = 1:2:10   % step 2
    disp(i)
end

for row = A'     % iterate columns of A (transpose to iterate rows)
    disp(row)
end

for item = {'apple', 'banana', 'cherry'}
    disp(item{1})
end

% while loop
n = 1;
while n < 100
    n = n * 2;
end
disp(n)   % 128

% do-while (Octave extension, not in MATLAB)
n = 0;
do
    n++;
until (n >= 5)

% break / continue
for i = 1:10
    if i == 5, break; end
    if mod(i, 2) == 0, continue; end
    fprintf('%d ', i);
end

% switch/case
day = 'Mon';
switch day
    case {'Mon','Tue','Wed','Thu','Fri'}
        disp('Weekday')
    case {'Sat','Sun'}
        disp('Weekend')
    otherwise
        disp('Unknown')
end

% try/catch
try
    x = 1 / 0;
    error('Manual error %d', 42);
catch e
    fprintf('Caught: %s\n', e.message);
    fprintf('Identifier: %s\n', e.identifier);
end
```


---

# CHAPTER 5: FUNCTIONS


## Defining Functions

```octave
% Function in a separate file: funcname.m
% Or at the end of a script (Octave extension)
% Or inside a function definition

function result = factorial(n)
    if n <= 1
        result = 1;
    else
        result = n * factorial(n - 1);
    end
end

% Multiple outputs
function [mn, mx, avg] = stats(v)
    mn = min(v);
    mx = max(v);
    avg = mean(v);
end

[a, b, c] = stats([3 1 4 1 5 9]);

% Default arguments with nargin
function result = power_val(base, exp)
    if nargin < 2
        exp = 2;   % default exponent
    end
    result = base ^ exp;
end

power_val(3)      % 9 (default exp=2)
power_val(3, 3)   % 27

% Varargs with varargin
function result = mysum(varargin)
    result = 0;
    for i = 1:nargin
        result += varargin{i};
    end
end
mysum(1, 2, 3, 4)   % 10

% Anonymous functions
square = @(x) x.^2;
add    = @(x, y) x + y;
compose = @(f, g) @(x) f(g(x));

square(5)     % 25
add(3, 4)     % 7

% Function handles
f = @sin;
fplot(f, [0, 2*pi])

% cellfun / arrayfun
nums = {1, 4, 9, 16};
results = cellfun(@sqrt, nums)      % [1 2 3 4]

arr = 1:5;
results2 = arrayfun(@(x) x^2+1, arr)  % [2 5 10 17 26]

% nargout check
function result = flexible(x)
    result = x^2;
    if nargout > 0
        % caller wants output
    end
end
```


---

# CHAPTER 6: PLOTTING


## Visualization

```octave
% 2D plot
x = 0:0.01:2*pi;
y = sin(x);
figure;
plot(x, y, 'b-', 'LineWidth', 2)
hold on
plot(x, cos(x), 'r--', 'LineWidth', 1.5)
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
figure; histogram(randn(1000,1), 30)
figure; scatter(randn(100,1), randn(100,1), 'filled')
figure; pie([30 20 50])
figure; stem(1:10, (1:10).^2)
figure; errorbar(1:5, rand(1,5), 0.1*ones(1,5))
figure; semilogy(1:10, exp(1:10))
figure; loglog(1:100, (1:100).^2)

% 3D plots
[X, Y] = meshgrid(-3:0.1:3, -3:0.1:3);
Z = sin(X) .* cos(Y);
figure;
surf(X, Y, Z)
colorbar
xlabel('X'); ylabel('Y'); zlabel('Z')

figure;
contour(X, Y, Z, 20)
contourf(X, Y, Z, 20)   % filled contours

figure;
mesh(X, Y, Z)

% 3D line
t = 0:0.01:4*pi;
plot3(cos(t), sin(t), t)
grid on

% Save figure
saveas(gcf, 'plot.png')
print('-dpng', '-r300', 'plot_hq.png')
print('-dpdf', 'plot.pdf')
```


---

# CHAPTER 7: FILE I/O AND DATA


## Data Operations

```octave
% Save/load .mat files
x = 1:10;
A = magic(3);
save('data.mat', 'x', 'A')     % save variables
load('data.mat')                 % load all variables
load('data.mat', 'x')           % load specific variable

% CSV
M = [1 2 3; 4 5 6; 7 8 9];
csvwrite('matrix.csv', M)
M2 = csvread('matrix.csv')

% Text file I/O
fid = fopen('data.txt', 'w');
fprintf(fid, '%d %f\n', 42, 3.14);
fclose(fid);

fid = fopen('data.txt', 'r');
while ~feof(fid)
    line = fgetl(fid);
    disp(line)
end
fclose(fid);

% Cell arrays (heterogeneous containers)
c = {1, 'hello', [1 2 3], true};
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
[s.age]    % array of all ages: [30 25]
fieldnames(s)   % {'name','age','scores'}
isfield(s, 'name')   % 1

% Statistical functions
v = [3 1 4 1 5 9 2 6];
mean(v)
median(v)
std(v)
var(v)
min(v); max(v)
sum(v); prod(v)
cumsum(v); cumprod(v)
sort(v)           % ascending
sort(v, 'descend')
unique(v)         % [1 2 3 4 5 6 9]
prctile(v, [25 50 75])   % quartiles
corrcoef(x, y)    % correlation matrix
```


---

# CHAPTER 8: ADVANCED OCTAVE


## Numerical Methods

```octave
% ODE solving
odefun = @(t, y) -2*y;   % dy/dt = -2y
[t, y] = ode45(odefun, [0 5], 1);   % solve from t=0 to 5, y(0)=1
plot(t, y)
title('Exponential Decay')

% System of ODEs (Lorenz)
sigma=10; rho=28; beta=8/3;
lorenz = @(t,s) [sigma*(s(2)-s(1)); s(1)*(rho-s(3))-s(2); s(1)*s(2)-beta*s(3)];
[t,s] = ode45(lorenz, [0 50], [1;1;1]);
plot3(s(:,1), s(:,2), s(:,3))

% Optimization
f = @(x) (x-2)^2 + sin(x);
[xmin, fmin] = fminbnd(f, 0, 5)

f2 = @(v) (v(1)-1)^2 + (v(2)-2)^2;
[x, fval] = fminsearch(f2, [0,0])

% Root finding
g = @(x) x^3 - x - 2;
root = fzero(g, 1.5)

% Numerical differentiation
x = 0:0.01:2*pi;
y = sin(x);
dy = diff(y) ./ diff(x);   % numerical derivative

% Integration
I = trapz(x, y)             % trapezoidal rule
I2 = quad(@sin, 0, pi)     % adaptive quadrature

% FFT
N = 1024; Fs = 1000;
t = (0:N-1)/Fs;
signal = sin(2*pi*50*t) + 0.5*sin(2*pi*120*t) + 0.1*randn(1,N);
X = fft(signal);
f = (0:N/2-1)*Fs/N;
plot(f, 2*abs(X(1:N/2))/N)
xlabel('Frequency (Hz)'); ylabel('Amplitude')

% Polynomial
p = [1 -3 2];   % x^2 - 3x + 2
roots(p)        % [2; 1]
polyval(p, 3)   % 2 (evaluate at x=3)
conv([1 -1], [1 -2])   % multiply polynomials: (x-1)(x-2)
deconv(p, [1 -1])      % polynomial division
polyder(p)      % derivative coefficients
polyint(p)      % integral coefficients

% Signal processing
[b, a] = butter(4, 0.1);      % Butterworth filter
y_filt = filter(b, a, signal); % apply filter
freqz(b, a)                    % frequency response plot
```
