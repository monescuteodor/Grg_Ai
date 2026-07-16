# R Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH R


## Remarks

R is a language and environment for statistical computing and graphics. It features extensive statistical and graphical methods, a rich package ecosystem (CRAN), and excellent data manipulation capabilities. Widely used in data science, bioinformatics, and academia.

Tools: R interpreter, RStudio IDE, tidyverse, ggplot2, data.table, Rmarkdown/Quarto.


## Hello World

```r
# hello.R
cat("Hello, World!\n")
print("Hello, R!")
message("Hello from message()")

# Run
# Rscript hello.R
# Or interactively in R/RStudio REPL
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Variables and Data Types

```r
# Assignment (use <- or =)
x <- 42
y = 3.14
name <- "Alice"
flag <- TRUE
nothing <- NULL
na_val <- NA

# Numeric (double by default)
n <- 42L          # integer (L suffix)
d <- 3.14         # double
cx <- 3 + 4i      # complex
is.integer(n)     # TRUE
is.double(d)      # TRUE
is.complex(cx)

# Type checking
class(42)        # "numeric"
class(42L)       # "integer"
class("hi")      # "character"
class(TRUE)      # "logical"
class(NULL)      # "NULL"
class(NA)        # "logical"
typeof(42)       # "double"

# Type conversion
as.integer(3.7)    # 3
as.double(5L)      # 5.0
as.character(42)   # "42"
as.logical(0)      # FALSE
as.logical(1)      # TRUE

# Special values
Inf; -Inf; NaN; NA; NULL; NA_integer_; NA_real_; NA_character_

is.na(NA)         # TRUE
is.null(NULL)     # TRUE
is.finite(Inf)    # FALSE
is.nan(NaN)       # TRUE

# String operations
s <- "Hello, World!"
nchar(s)                          # 13
toupper(s)
tolower(s)
substr(s, 1, 5)                   # "Hello"
sub("World", "R", s)              # replace first
gsub("l", "L", s)                 # replace all
grepl("World", s)                 # TRUE (regex match)
strsplit(s, ", ")                 # list of parts
paste("Hello", "World")           # "Hello World"
paste0("Hello", "World")          # "HelloWorld"
paste(1:5, collapse="-")          # "1-2-3-4-5"
sprintf("Name: %s, Age: %d", "Alice", 30)
trimws("  hello  ")               # "hello"
startsWith(s, "Hello")
endsWith(s, "!")
```


---

# CHAPTER 3: VECTORS AND LISTS


## Collections

```r
# Vector (atomic — all same type)
v <- c(1, 2, 3, 4, 5)
chars <- c("a", "b", "c")
bools <- c(TRUE, FALSE, TRUE)

# Sequences
1:10
seq(0, 1, by=0.1)
seq(0, 1, length.out=11)
rep(1:3, times=3)       # 1 2 3 1 2 3 1 2 3
rep(1:3, each=3)        # 1 1 1 2 2 2 3 3 3

# Indexing (1-based!)
v[1]            # 1
v[c(1,3,5)]     # 1 3 5
v[2:4]          # 2 3 4
v[-1]           # all except first
v[v > 3]        # logical indexing: 4 5

# Named vectors
ages <- c(Alice=30, Bob=25, Carol=35)
ages["Alice"]    # 30
ages[c("Alice","Carol")]

# Vector operations (vectorized by default)
v * 2
v + c(10, 20, 30, 40, 50)
v^2
sqrt(v)
sum(v); prod(v); cumsum(v); cumprod(v)
mean(v); median(v); var(v); sd(v)
min(v); max(v); range(v)
which(v > 3)     # indices where condition is TRUE
any(v > 4)
all(v > 0)

# List (heterogeneous)
lst <- list(name="Alice", age=30, scores=c(85, 90, 92))
lst$name          # "Alice"
lst[["name"]]     # "Alice"
lst[[3]]          # c(85, 90, 92)
lst[1]            # returns a list (single bracket)

lst$city <- "NYC"         # add element
lst[["age"]] <- NULL      # remove element

# lapply / sapply
nums <- list(1, 4, 9, 16)
lapply(nums, sqrt)          # returns list
sapply(nums, sqrt)          # returns vector: 1 2 3 4

# Matrix
m <- matrix(1:9, nrow=3, ncol=3)
m <- matrix(1:9, 3, 3, byrow=TRUE)
m[2, 3]       # row 2, col 3
m[, 2]        # column 2
m[1, ]        # row 1
t(m)          # transpose
m %*% m       # matrix multiply
det(m)
solve(m)      # inverse
eigen(m)
```


---

# CHAPTER 4: DATA FRAMES


## Data Manipulation

```r
# Create data frame
df <- data.frame(
  name  = c("Alice", "Bob", "Carol", "Dave"),
  age   = c(30, 25, 35, 28),
  city  = c("NYC", "LA", "NYC", "Chicago"),
  score = c(90, 85, 92, 88),
  stringsAsFactors = FALSE
)

# Access
df$name               # column as vector
df[["age"]]           # same
df[1, ]               # first row
df[, 2]               # second column
df[1:2, c("name","age")]  # subset rows and cols

# Modify
df$bonus <- df$score * 0.1   # add column
df$age[df$name == "Bob"] <- 26   # update

# Filter rows
df[df$age > 28, ]
df[df$city == "NYC" & df$score > 89, ]
subset(df, age > 28 & city == "NYC")

# Summary statistics
summary(df)
nrow(df); ncol(df)
dim(df)
head(df, 3); tail(df, 3)
str(df)
colnames(df); rownames(df)

# Sort
df[order(df$age), ]
df[order(df$score, decreasing=TRUE), ]

# Aggregate
aggregate(score ~ city, data=df, FUN=mean)

# tapply
tapply(df$score, df$city, mean)

# Read/Write CSV
# df <- read.csv("data.csv", stringsAsFactors=FALSE)
# write.csv(df, "output.csv", row.names=FALSE)

# Table (frequency count)
table(df$city)
table(df$city, df$age > 28)

# Factor (categorical)
df$city <- factor(df$city)
levels(df$city)
nlevels(df$city)
```


---

# CHAPTER 5: CONTROL FLOW AND FUNCTIONS


## Functions and Control

```r
# if/else
x <- 10
if (x > 0) {
  cat("positive\n")
} else if (x == 0) {
  cat("zero\n")
} else {
  cat("negative\n")
}

# ifelse (vectorized)
x <- c(-2, 0, 3, -1, 5)
ifelse(x > 0, "pos", "non-pos")

# switch
day <- "Monday"
result <- switch(day,
  Monday    = "Start of week",
  Friday    = "End of week",
  Saturday  = ,
  Sunday    = "Weekend",
  "Unknown"    # default
)

# for loop
for (i in 1:10) {
  cat(i, " ")
}

for (item in c("a", "b", "c")) {
  cat(item, "\n")
}

# while loop
n <- 1
while (n < 100) {
  n <- n * 2
}

# repeat with break
repeat {
  n <- n - 1
  if (n <= 10) break
}

# next (continue)
for (i in 1:10) {
  if (i %% 2 == 0) next
  cat(i, " ")
}

# Functions
add <- function(a, b) {
  a + b    # last expression is return value
}

# Default arguments
greet <- function(name, greeting = "Hello") {
  cat(sprintf("%s, %s!\n", greeting, name))
}
greet("Alice")
greet("Bob", "Hi")

# ... (variadic)
my_sum <- function(...) {
  args <- c(...)
  sum(args)
}
my_sum(1, 2, 3, 4, 5)

# Return multiple values (as list)
minmax <- function(v) {
  list(min=min(v), max=max(v))
}
result <- minmax(c(3,1,4,1,5,9))
result$min; result$max

# Closures
make_adder <- function(n) {
  function(x) x + n
}
add5 <- make_adder(5)
add5(10)   # 15

# Anonymous functions
(function(x) x^2)(5)    # 25
\(x) x^2               # R 4.1+ shorthand lambda

# Apply family
sapply(1:10, function(x) x^2)
lapply(1:5, function(x) x * 10)
vapply(1:5, function(x) x^2, numeric(1))
mapply(function(x, y) x + y, 1:3, 4:6)
Map(function(x,y) x+y, 1:3, 4:6)
Reduce("+", 1:10)               # 55
Filter(function(x) x > 3, 1:6) # 4 5 6
```


---

# CHAPTER 6: STATISTICS AND MODELING


## Statistical Analysis

```r
# Distributions
dnorm(0)              # N(0,1) density at 0
pnorm(1.96)           # CDF: P(Z <= 1.96) ≈ 0.975
qnorm(0.975)          # quantile: 1.96
rnorm(100)            # 100 random N(0,1) values
rnorm(100, mean=5, sd=2)

dbinom(3, size=10, prob=0.5)   # binomial PMF
pbinom(3, 10, 0.5)
rbinom(100, 10, 0.5)

dpois(5, lambda=3)   # Poisson
runif(100, 0, 10)    # uniform
rexp(100, rate=2)    # exponential

# t-test
x <- rnorm(30, mean=5, sd=1)
y <- rnorm(30, mean=6, sd=1)
t.test(x, y)
t.test(x, mu=5)         # one-sample

# Linear regression
set.seed(42)
x <- 1:100
y <- 2*x + rnorm(100, 0, 10)
model <- lm(y ~ x)
summary(model)
coef(model)
fitted(model)
residuals(model)
predict(model, newdata=data.frame(x=c(101, 102)))
confint(model)

# Multiple regression
df2 <- data.frame(y=y, x1=x, x2=runif(100))
model2 <- lm(y ~ x1 + x2, data=df2)
summary(model2)

# ANOVA
groups <- factor(rep(c("A","B","C"), each=20))
values <- c(rnorm(20,5), rnorm(20,6), rnorm(20,7))
aov_result <- aov(values ~ groups)
summary(aov_result)
TukeyHSD(aov_result)

# Logistic regression
y_bin <- as.integer(y > median(y))
log_model <- glm(y_bin ~ x, family=binomial)
summary(log_model)

# Correlation
cor(x, y)
cor.test(x, y)
cor(cbind(x, y, runif(100)))
```


---

# CHAPTER 7: TIDYVERSE AND GGPLOT2


## Modern R (tidyverse)

```r
library(dplyr)
library(tidyr)
library(ggplot2)
library(readr)
library(purrr)

# dplyr verbs
df <- data.frame(
  name=c("Alice","Bob","Carol","Dave"),
  age=c(30,25,35,28),
  city=c("NYC","LA","NYC","Chicago"),
  score=c(90,85,92,88)
)

df |>
  filter(age > 26) |>
  arrange(desc(score)) |>
  select(name, score) |>
  mutate(grade = ifelse(score >= 90, "A", "B")) |>
  summarise(mean_score = mean(score))

# Group operations
df |>
  group_by(city) |>
  summarise(
    count = n(),
    avg_score = mean(score),
    max_age = max(age)
  )

# Joins
df2 <- data.frame(city=c("NYC","LA"), region=c("East","West"))
left_join(df, df2, by="city")
inner_join(df, df2, by="city")

# tidyr
# Pivot longer/wider
wide <- data.frame(name=c("Alice","Bob"), q1=c(90,80), q2=c(85,88))
long <- pivot_longer(wide, cols=c(q1,q2), names_to="quarter", values_to="score")
pivot_wider(long, names_from=quarter, values_from=score)

# ggplot2
ggplot(df, aes(x=age, y=score, color=city)) +
  geom_point(size=3) +
  geom_smooth(method="lm", se=FALSE) +
  labs(title="Score vs Age", x="Age", y="Score") +
  theme_minimal()

ggplot(df, aes(x=city, y=score, fill=city)) +
  geom_bar(stat="summary", fun=mean) +
  theme_bw()

ggplot(data.frame(x=rnorm(1000)), aes(x=x)) +
  geom_histogram(bins=30, fill="blue", alpha=0.7) +
  geom_density(aes(y=after_stat(density)*nrow(data.frame(x=rnorm(1000)))), color="red")

# purrr (functional programming)
1:10 |> map(~ .x^2)
1:10 |> map_dbl(~ .x^2)
list(1:3, 4:6) |> map(sum)
list(1:3, 4:6) |> map2(list(10,20), ~ sum(.x) + .y)
```


---

# CHAPTER 8: ADVANCED R


## Advanced Features

```r
# Environments
e <- new.env()
assign("x", 42, envir=e)
get("x", envir=e)
ls(envir=e)
environmentName(globalenv())
parent.env(e)

# S3 OOP
# Create constructor
new_animal <- function(name, sound) {
  obj <- list(name=name, sound=sound)
  class(obj) <- "Animal"
  obj
}

# Define generic methods
speak <- function(x, ...) UseMethod("speak")
speak.Animal <- function(x, ...) cat(x$name, "says", x$sound, "\n")
print.Animal <- function(x, ...) cat("Animal:", x$name, "\n")

dog <- new_animal("Rex", "Woof")
speak(dog)

# S4 OOP
setClass("Person", representation(
  name = "character",
  age  = "numeric"
))
setGeneric("greet", function(x) standardGeneric("greet"))
setMethod("greet", "Person", function(x) cat("Hello, I'm", x@name, "\n"))

alice <- new("Person", name="Alice", age=30)
greet(alice)
alice@name    # slot access

# R5 (Reference Classes)
Counter <- setRefClass("Counter",
  fields = list(count = "numeric"),
  methods = list(
    initialize = function() count <<- 0,
    increment  = function() count <<- count + 1,
    get        = function() count
  )
)
c1 <- Counter$new()
c1$increment(); c1$increment()
c1$get()   # 2

# Debugging
traceback()
browser()          # interactive debug
debug(my_function)
undebug(my_function)
trace(my_function, quote(cat("called\n")))

# Performance
system.time(sum(1:1e7))
proc.time()
Rprof()
# ... code to profile ...
Rprof(NULL)
summaryRprof()

# Rcpp (C++ integration)
# library(Rcpp)
# cppFunction('int addCpp(int x, int y) { return x + y; }')
# addCpp(3, 4)   # 7

# Parallel computing
library(parallel)
n_cores <- detectCores()
cl <- makeCluster(n_cores - 1)
parLapply(cl, 1:100, function(x) x^2)
stopCluster(cl)

mclapply(1:100, function(x) x^2, mc.cores=n_cores-1)
```
