# Haskell Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH HASKELL


## Remarks

Haskell is a purely functional, statically typed, lazy programming language with strong type inference. It features algebraic data types, type classes, monads, and an expressive type system. Haskell is used in compilers, financial systems, and as an academic research language.

Tools: GHC (compiler), GHCi (REPL), cabal, stack (build tools), Haddock (docs).


## Hello World

```haskell
-- hello.hs
module Main where

main :: IO ()
main = do
    putStrLn "Hello, World!"
    putStrLn $ "Hello, " ++ "Haskell!"
    print 42
```

```bash
ghc hello.hs -o hello && ./hello
runghc hello.hs        # interpret
ghci                   # interactive REPL
# :load hello.hs       # load in GHCi
# main                 # run
```


---

# CHAPTER 2: TYPES AND EXPRESSIONS


## Basic Types

```haskell
-- Types
-- Int, Integer, Float, Double, Bool, Char, String

-- Variables (immutable bindings)
x :: Int
x = 42

name :: String
name = "Alice"

flag :: Bool
flag = True

ch :: Char
ch = 'A'

-- Type inference
y = 3.14           -- inferred Double
z = "hello"        -- inferred String

-- Numeric operations
2 + 3              -- 5
10 - 4             -- 6
5 * 6              -- 30
15 `div` 4         -- 3 (integer division)
15 `mod` 4         -- 3 (remainder)
15 / 4             -- 3.75 (float division)
2 ^ 10             -- 1024
abs (-5)           -- 5
sqrt 16.0          -- 4.0
floor 3.7          -- 3
ceiling 3.2        -- 4
round 3.5          -- 4

-- Boolean
True && False      -- False
True || False      -- True
not True           -- False
3 > 2              -- True
3 == 3             -- True
3 /= 4             -- True (not equal)

-- Char and String
'A'                -- Char
"Hello"            -- String = [Char]
['H','e','l','l','o']  -- same as "Hello"
head "hello"       -- 'h'
tail "hello"       -- "ello"
last "hello"       -- 'o'
init "hello"       -- "hell"
length "hello"     -- 5
"Hello" ++ " World"  -- "Hello World"
words "Hello World"  -- ["Hello","World"]
unwords ["Hello","World"]  -- "Hello World"
lines "a\nb\nc"     -- ["a","b","c"]
unlines ["a","b"]   -- "a\nb\n"
show 42             -- "42"
read "42" :: Int    -- 42

-- Tuple
t2 = (1, "hello")
t3 = (1, 2, 3)
fst (1, 2)   -- 1
snd (1, 2)   -- 2

-- Maybe
Just 42 :: Maybe Int
Nothing :: Maybe Int
```


---

# CHAPTER 3: LISTS AND LIST COMPREHENSIONS


## Lists

```haskell
-- List operations
lst = [1, 2, 3, 4, 5]

head lst        -- 1
tail lst        -- [2,3,4,5]
last lst        -- 5
init lst        -- [1,2,3,4]
length lst      -- 5
null lst        -- False
null []         -- True
reverse lst     -- [5,4,3,2,1]
lst !! 2        -- 3 (0-indexed)

-- Adding elements
1 : [2,3,4]    -- [1,2,3,4] (prepend)
[1,2] ++ [3,4] -- [1,2,3,4] (append)

-- Searching
elem 3 lst      -- True
notElem 9 lst   -- True
filter (>3) lst -- [4,5]
takeWhile (<4) lst  -- [1,2,3]
dropWhile (<4) lst  -- [4,5]

-- Transforming
map (*2) lst         -- [2,4,6,8,10]
map show lst         -- ["1","2","3","4","5"]
zip [1,2,3] ["a","b","c"]  -- [(1,"a"),(2,"b"),(3,"c")]
zipWith (+) [1,2,3] [4,5,6] -- [5,7,9]
unzip [(1,"a"),(2,"b")]     -- ([1,2],["a","b"])
concat [[1,2],[3,4],[5]]    -- [1,2,3,4,5]
concatMap (\x -> [x,x*2]) [1,2,3]  -- [1,2,2,4,3,6]

-- Folding
foldl (+) 0 [1..5]     -- 15 (left fold)
foldr (:) [] [1,2,3]   -- [1,2,3]
foldl1 (+) [1..5]      -- 15 (no initial value)
foldr1 max [3,1,4,1,5] -- 5

-- Range
[1..10]          -- [1,2,3,4,5,6,7,8,9,10]
[1,3..10]        -- [1,3,5,7,9]
[10,8..1]        -- [10,8,6,4,2]
take 5 [1..]     -- [1,2,3,4,5] (infinite list!)
take 5 (cycle [1,2,3])  -- [1,2,3,1,2]
take 5 (repeat 42)      -- [42,42,42,42,42]
take 5 (iterate (*2) 1) -- [1,2,4,8,16]

-- List comprehensions
[x^2 | x <- [1..10]]                     -- [1,4,9,16,25,36,49,64,81,100]
[x | x <- [1..20], even x]               -- [2,4,6,8,10,12,14,16,18,20]
[(x,y) | x <- [1..3], y <- [1..3], x/=y] -- all pairs where x≠y
[x*y | x <- [2,4..10], y <- [2,4..10], x*y < 50]

-- Sorting and grouping
import Data.List (sort, group, nub, permutations, subsequences)
sort [3,1,4,1,5,9]     -- [1,1,3,4,5,9]
nub [1,2,2,3,3,4]      -- [1,2,3,4] (remove dups)
group [1,1,2,3,3,3]    -- [[1,1],[2],[3,3,3]]
sum [1..100]            -- 5050
product [1..5]          -- 120
maximum [3,1,4,1,5]     -- 5
minimum [3,1,4,1,5]     -- 1
and [True, True, True]  -- True
or  [False, False, True] -- True
any even [1,3,5,6]      -- True
all odd  [1,3,5,7]      -- True
```


---

# CHAPTER 4: FUNCTIONS


## Functions and Higher-Order Programming

```haskell
-- Function definition
add :: Int -> Int -> Int
add x y = x + y

-- Pattern matching
factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- Guards
bmi :: Double -> String
bmi x
    | x < 18.5 = "Underweight"
    | x < 25.0 = "Normal"
    | x < 30.0 = "Overweight"
    | otherwise = "Obese"

-- Where clause
circleArea :: Double -> Double
circleArea r = pi * r * r
    where pi = 3.14159

-- Let expression
cylinderVol :: Double -> Double -> Double
cylinderVol r h =
    let baseArea = pi * r * r
        pi = 3.14159
    in baseArea * h

-- Lambda (anonymous function)
(\x -> x * x) 5        -- 25
(\x y -> x + y) 3 4    -- 7
map (\x -> x^2) [1..5] -- [1,4,9,16,25]

-- Currying (all functions are curried)
add 3      -- returns a function (Int -> Int)
add 3 4    -- 7
map (add 3) [1..5]  -- [4,5,6,7,8]

-- Function composition (.)
(not . even) 3      -- True
(map (*2) . filter even) [1..10]  -- [4,8,12,16,20]

-- Application ($) — avoids parentheses
negate (abs (-5))  -- same as:
negate $ abs (-5)  -- 5

-- flip
flip div 3 9   -- same as div 9 3 = 3

-- const, id
map (const 0) [1..5]   -- [0,0,0,0,0]
map id [1..5]           -- [1,2,3,4,5]

-- Sections (partial application with operators)
(2^) 10     -- 1024
(^2) 5      -- 25
(10-) 3     -- 7
(`div` 2) 10  -- 5

-- until (iterate while condition)
until (>100) (*2) 1   -- 128

-- zipWith
zipWith (*) [1,2,3] [4,5,6]  -- [4,10,18]
```


---

# CHAPTER 5: ALGEBRAIC DATA TYPES AND TYPE CLASSES


## Types and Type Classes

```haskell
-- Custom data types
data Color = Red | Green | Blue
    deriving (Show, Eq, Ord, Enum, Bounded)

data Shape = Circle Double
           | Rectangle Double Double
           | Triangle Double Double Double
    deriving (Show, Eq)

area :: Shape -> Double
area (Circle r)       = pi * r * r
area (Rectangle w h)  = w * h
area (Triangle a b c) = let s = (a+b+c)/2
                         in sqrt (s*(s-a)*(s-b)*(s-c))

-- Record syntax
data Person = Person
    { firstName :: String
    , lastName  :: String
    , age       :: Int
    } deriving (Show, Eq)

alice = Person { firstName="Alice", lastName="Smith", age=30 }
alice { age = 31 }   -- update (creates new record)
firstName alice      -- "Alice"

-- Parameterized types
data Maybe' a = Nothing' | Just' a
data Either' a b = Left' a | Right' b
data Tree a = Leaf | Node (Tree a) a (Tree a)

-- Newtype (single constructor, single field)
newtype Name = Name { unName :: String }
newtype Age  = Age  { unAge  :: Int }

-- Type classes
class Describable a where
    describe :: a -> String

instance Describable Person where
    describe p = firstName p ++ " " ++ lastName p ++ ", age " ++ show (age p)

instance Describable Shape where
    describe (Circle r)      = "Circle with radius " ++ show r
    describe (Rectangle w h) = "Rectangle " ++ show w ++ "x" ++ show h
    describe _               = "Some shape"

-- Common type classes
-- Eq: (==), (/=)
-- Ord: compare, (<), (>), min, max
-- Show: show (to String)
-- Read: read (from String)
-- Num: (+), (-), (*), negate, abs
-- Integral: div, mod, quot, rem
-- Floating: pi, sqrt, exp, log
-- Functor: fmap
-- Applicative: pure, (<*>)
-- Monad: (>>=), return

-- Functor instance for Tree
instance Functor Tree where
    fmap _ Leaf = Leaf
    fmap f (Node l x r) = Node (fmap f l) (f x) (fmap f r)
```


---

# CHAPTER 6: MONADS AND IO


## Monadic Programming

```haskell
-- IO monad (all effectful code)
main :: IO ()
main = do
    putStr "Enter name: "
    name <- getLine          -- bind IO String to name
    let greeting = "Hello, " ++ name ++ "!"
    putStrLn greeting
    print (length greeting)

-- Maybe monad (handle failure)
safeDivide :: Int -> Int -> Maybe Int
safeDivide _ 0 = Nothing
safeDivide x y = Just (x `div` y)

computation :: Int -> Int -> Int -> Maybe Int
computation x y z = do
    a <- safeDivide x y
    b <- safeDivide a z
    return (a + b)

-- equivalent without do:
computation' x y z =
    safeDivide x y >>= \a ->
    safeDivide a z >>= \b ->
    return (a + b)

-- Either monad (error handling)
type Error = String
parseAge :: String -> Either Error Int
parseAge s = case reads s of
    [(n, "")] -> if n >= 0 && n <= 150
                 then Right n
                 else Left "Age out of range"
    _ -> Left "Not a number"

-- List monad (non-determinism)
pairs :: [(Int,Int)]
pairs = do
    x <- [1..3]
    y <- [1..3]
    return (x, y)
-- [(1,1),(1,2),(1,3),(2,1),(2,2),...,(3,3)]

-- State monad
import Control.Monad.State

counter :: State Int ()
counter = do
    n <- get
    put (n + 1)

runCounter :: ((), Int)
runCounter = runState (do counter; counter; counter) 0
-- ((), 3)

-- IO with various operations
import System.IO
import Data.IORef

-- IORef (mutable reference in IO)
ref <- newIORef (0 :: Int)
modifyIORef ref (+1)
val <- readIORef ref
writeIORef ref 42

-- File IO
contents <- readFile "input.txt"
writeFile "output.txt" "Hello, World!\n"
appendFile "log.txt" "Log entry\n"

-- hGetLine etc
handle <- openFile "input.txt" ReadMode
line <- hGetLine handle
hClose handle
```


---

# CHAPTER 7: MODULES AND PACKAGES


## Modules and Standard Library

```haskell
-- Module definition
module Geometry
    ( Shape(..)         -- export type and constructors
    , area
    , perimeter
    ) where

-- Common imports
import Data.List (sort, nub, group, permutations, isPrefixOf, isSuffixOf, intercalate, transpose)
import Data.Char (isDigit, isAlpha, isUpper, isLower, toUpper, toLower, ord, chr)
import Data.Maybe (fromMaybe, mapMaybe, catMaybes, isJust, isNothing, fromJust, listToMaybe)
import Data.Map (Map)
import qualified Data.Map as Map
import Data.Set (Set)
import qualified Data.Set as Set
import Data.Map.Strict (Map)
import qualified Data.Map.Strict as Map

-- Map operations
m :: Map String Int
m = Map.fromList [("Alice",30),("Bob",25),("Carol",35)]
Map.lookup "Alice" m      -- Just 30
Map.insert "Dave" 28 m
Map.delete "Bob" m
Map.member "Alice" m      -- True
Map.keys m
Map.elems m
Map.map (+1) m
Map.filter (>28) m
Map.foldlWithKey (\acc k v -> acc ++ k) "" m
Map.toList m
Map.size m
Map.unionWith (+) m m
Map.intersectionWith (+) m m

-- Set operations
s :: Set Int
s = Set.fromList [1,2,3,4,5]
Set.member 3 s
Set.insert 6 s
Set.delete 1 s
Set.union s (Set.fromList [4,5,6])
Set.intersection s (Set.fromList [3,4,5,6,7])
Set.difference s (Set.fromList [3,4])
Set.toList s
Set.size s

-- Text (efficient string)
-- import qualified Data.Text as T
-- import qualified Data.Text.IO as TIO
-- t = T.pack "Hello, World!"
-- T.length t; T.toUpper t; T.splitOn ", " t

-- Data.List extras
import Data.List
sortOn length ["hello","hi","hey"]         -- ["hi","hey","hello"]
groupBy (\a b -> even a == even b) [1,3,2,4,1]  -- [[1,3],[2,4],[1]]
partition even [1..10]                     -- ([2,4,6,8,10],[1,3,5,7,9])
isPrefixOf "He" "Hello"    -- True
isSuffixOf "lo" "Hello"    -- True
intercalate ", " ["a","b","c"]  -- "a, b, c"
tails [1,2,3]              -- [[1,2,3],[2,3],[3],[]]
inits [1,2,3]              -- [[],[1],[1,2],[1,2,3]]
```


---

# CHAPTER 8: ADVANCED HASKELL


## Advanced Features

```haskell
-- Lazy evaluation
naturals :: [Int]
naturals = [1..]

fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

take 20 fibs  -- first 20 Fibonacci numbers

-- primes (Sieve of Eratosthenes)
primes :: [Int]
primes = sieve [2..]
    where sieve (p:xs) = p : sieve [x | x <- xs, x `mod` p /= 0]

-- Type families
{-# LANGUAGE TypeFamilies #-}
type family Elem (collection :: *) :: *
type instance Elem [a] = a
type instance Elem (Maybe a) = a

-- GADTs
{-# LANGUAGE GADTs #-}
data Expr a where
    Lit  :: Int  -> Expr Int
    Bool :: Bool -> Expr Bool
    Add  :: Expr Int  -> Expr Int  -> Expr Int
    If   :: Expr Bool -> Expr a    -> Expr a -> Expr a

eval :: Expr a -> a
eval (Lit n)      = n
eval (Bool b)     = b
eval (Add e1 e2)  = eval e1 + eval e2
eval (If c t f)   = if eval c then eval t else eval f

-- Lenses (with lens library)
-- import Control.Lens
-- data Point = Point { _x :: Double, _y :: Double }
-- makeLenses ''Point
-- point^.x         -- get
-- point & x .~ 5   -- set
-- point & x %~ (+1) -- modify

-- Concurrency with STM
import Control.Concurrent.STM
import Control.Concurrent

account :: TVar Int
shared :: IO ()
shared = do
    acc <- newTVarIO 1000
    let transfer amount = atomically $ do
            val <- readTVar acc
            writeTVar acc (val - amount)
    forkIO $ transfer 100
    forkIO $ transfer 200
    threadDelay 1000000
    final <- readTVarIO acc
    print final

-- QuickCheck (property testing)
-- import Test.QuickCheck
-- prop_reverse :: [Int] -> Bool
-- prop_reverse xs = reverse (reverse xs) == xs
-- quickCheck prop_reverse   -- tests 100 random cases
```
