# PHP Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH PHP


## Remarks

PHP (PHP: Hypertext Preprocessor) is a server-side scripting language designed for web development. It runs on the server and generates HTML. PHP 8.3 is current with JIT compilation, named arguments, enums, fibers, and readonly properties.

Tools: PHP CLI, Composer (package manager), Laravel/Symfony (frameworks), PHPUnit (testing).


## Hello World

```php
<?php
echo "Hello, World!\n";
print "Hello!\n";
printf("Hello, %s!\n", "PHP");

// var_dump and print_r for debugging
var_dump(42);
print_r([1, 2, 3]);
```

```bash
php hello.php
php -r "echo 'Hello';"
php -S localhost:8080   # built-in web server
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Types

```php
<?php

// Variables start with $
$name    = "Alice";
$age     = 30;
$score   = 98.5;
$active  = true;
$nothing = null;

// Type juggling
$x = "42";
var_dump($x + 0);      // int(42)
var_dump($x + 3.14);   // float(45.14)

// Strict comparison
"1" == 1    // true (loose)
"1" === 1   // false (strict, different types)
null == false // true
null === false // false

// Type checking
is_int($age)
is_string($name)
is_array([])
is_null($nothing)
isset($x)          // is set and not null
empty($x)          // null, false, 0, "", "0", [], unset

// Type casting
(int)"42abc"      // 42
(string)42        // "42"
(float)"3.14"     // 3.14
(bool)""          // false
(array)"hello"    // ["hello"]

// PHP 8 types
$x = match(true) { true => "yes", false => "no" };

// Strings
$s = "Hello, World!";
strlen($s)              // 13
strtoupper($s)
strtolower($s)
substr($s, 0, 5)        // "Hello"
strpos($s, "World")     // 7
str_replace("World", "PHP", $s)
str_contains($s, "World")   // PHP 8
str_starts_with($s, "Hello")
str_ends_with($s, "!")
trim($s)
explode(", ", $s)       // split
implode(", ", $arr)     // join

// Heredoc
$heredoc = <<<EOT
    Hello $name
    Multiple lines
    EOT;

// Nowdoc (no interpolation)
$nowdoc = <<<'EOT'
    No $interpolation here
    EOT;

// String interpolation
$msg = "Hello, $name!";
$msg = "Hello, {$obj->name}!";
```

## Arrays

```php
<?php

// Indexed array
$arr = [1, 2, 3, 4, 5];
$arr = array(1, 2, 3);    // older syntax

$arr[] = 6;               // append
array_push($arr, 7, 8);
array_pop($arr);
array_shift($arr);        // remove first
array_unshift($arr, 0);   // prepend
count($arr);
in_array(3, $arr);
array_search(3, $arr);    // returns key
sort($arr);
rsort($arr);              // reverse sort
array_reverse($arr);
array_unique($arr);
array_slice($arr, 1, 3);  // offset, length
array_splice($arr, 1, 2); // remove 2 from index 1
array_merge($a, $b);
array_combine($keys, $values);

// Associative array (hash map)
$user = [
    "name"  => "Alice",
    "age"   => 30,
    "email" => "alice@example.com",
];

$user["city"] = "NYC";
unset($user["email"]);
array_key_exists("name", $user);
isset($user["age"]);
array_keys($user);
array_values($user);

foreach ($user as $key => $value) {
    echo "$key: $value\n";
}

// Functional operations
$doubled = array_map(fn($n) => $n * 2, $arr);
$evens   = array_filter($arr, fn($n) => $n % 2 === 0);
$total   = array_reduce($arr, fn($carry, $n) => $carry + $n, 0);
usort($arr, fn($a, $b) => $a - $b);
uksort($assoc, fn($a, $b) => strcmp($a, $b));

// Spread operator (PHP 7.4+)
$merged = [...$a, ...$b];
```


---

# CHAPTER 3: CONTROL FLOW


## Flow Control

```php
<?php

// if/elseif/else
if ($x > 0) {
    echo "positive";
} elseif ($x === 0) {
    echo "zero";
} else {
    echo "negative";
}

// Ternary and null coalescing
$label = $x > 0 ? "pos" : "non-pos";
$val   = $maybe ?? "default";       // null coalescing
$val ??= "default";                 // null coalescing assignment

// match (PHP 8, strict comparison, no fallthrough)
$result = match($day) {
    "Mon", "Tue" => "Early week",
    "Sat", "Sun" => "Weekend",
    default      => "Other",
};

// switch
switch ($day) {
    case "Mon":
    case "Tue":
        echo "Weekday"; break;
    default:
        echo "Other";
}

// for
for ($i = 0; $i < 10; $i++) {
    echo $i;
}

// foreach
foreach ($arr as $value) { echo $value; }
foreach ($hash as $key => $value) { echo "$key=$value"; }

// while / do-while
while ($n > 0) $n--;
do { $n++; } while ($n < 10);

// list() / [] destructuring
[$a, $b] = [1, 2];
[, $second] = [1, 2, 3];
["name" => $name, "age" => $age] = $user;

// list() in foreach
foreach ($matrix as [$x, $y]) { echo "$x,$y\n"; }
```


---

# CHAPTER 4: FUNCTIONS


## Functions

```php
<?php

// Basic function
function add(int $a, int $b): int {
    return $a + $b;
}

// Default arguments
function greet(string $name, string $prefix = "Hello"): string {
    return "$prefix, $name!";
}

// Variadic
function sum(int ...$nums): int {
    return array_sum($nums);
}
sum(1, 2, 3, 4, 5);

// Type declarations (PHP 7+)
function divide(float $a, float $b): float|false {
    return $b !== 0.0 ? $a / $b : false;
}

// Return type: void, mixed, never, union, nullable
function log(?string $msg): void { echo $msg ?? "null"; }

// Named arguments (PHP 8)
str_pad(string: "Hello", length: 10, pad_string: "*", pad_type: STR_PAD_LEFT);

// Closures / anonymous functions
$square = function(int $n): int { return $n * $n; };
$add    = fn(int $a, int $b): int => $a + $b;   // arrow function

// Capture variables
$offset = 10;
$addOffset = function(int $n) use ($offset): int { return $n + $offset; };
$addOffsetRef = function(int $n) use (&$offset): int { return $n + $offset; };

// First-class callable syntax (PHP 8.1)
$fn = strlen(...);
$fn("hello");   // 5

// Higher-order
$nums = range(1, 10);
array_map(fn($n) => $n ** 2, $nums);
array_filter($nums, fn($n) => $n % 2 === 0);

// Recursive
function factorial(int $n): int {
    return $n <= 1 ? 1 : $n * factorial($n - 1);
}
```


---

# CHAPTER 5: OBJECT-ORIENTED PROGRAMMING


## Classes

```php
<?php

class Animal {
    private static int $count = 0;

    public function __construct(
        private string $name,           // constructor promotion (PHP 8)
        protected string $sound,
        public readonly int $id = 0,    // readonly property
    ) {
        self::$count++;
    }

    public function getName(): string { return $this->name; }

    public function speak(): string {
        return "{$this->name} says {$this->sound}";
    }

    public static function getCount(): int { return self::$count; }

    public function __toString(): string { return "Animal({$this->name})"; }

    public function __clone() { self::$count++; }
}

class Dog extends Animal {
    public function __construct(string $name, private string $breed) {
        parent::__construct($name, "Woof");
    }

    public function speak(): string { return parent::speak() . "!"; }
    public function getBreed(): string { return $this->breed; }
}

// Interface
interface Flyable {
    public function fly(): void;
    public function land(): void;
}

// Abstract class
abstract class Shape {
    abstract public function area(): float;
    abstract public function perimeter(): float;

    public function describe(): void {
        printf("Area=%.2f, Perimeter=%.2f\n", $this->area(), $this->perimeter());
    }
}

// Trait (mixin)
trait Loggable {
    private array $logs = [];

    public function log(string $msg): void {
        $this->logs[] = date("Y-m-d H:i:s") . " - $msg";
    }

    public function getLogs(): array { return $this->logs; }
}

class Service {
    use Loggable;

    public function process(): void {
        $this->log("Processing started");
    }
}

// Enum (PHP 8.1)
enum Status: string {
    case Active   = "active";
    case Inactive = "inactive";
    case Pending  = "pending";

    public function label(): string {
        return match($this) {
            Status::Active   => "Active User",
            Status::Inactive => "Inactive User",
            Status::Pending  => "Pending Approval",
        };
    }
}

$s = Status::Active;
$s->value;   // "active"
$s->name;    // "Active"
Status::from("active");         // Status::Active
Status::tryFrom("invalid");     // null
```


---

# CHAPTER 6: ERROR HANDLING AND EXCEPTIONS


## Exceptions

```php
<?php

// try/catch/finally
try {
    $result = riskyOperation();
    if ($result === false) {
        throw new RuntimeException("Operation failed", 500);
    }
} catch (InvalidArgumentException $e) {
    echo "Invalid arg: " . $e->getMessage();
} catch (RuntimeException | LogicException $e) {
    echo "Error: " . $e->getMessage();
    echo "Code: " . $e->getCode();
} catch (Throwable $e) {       // catches errors too
    echo "Fatal: " . $e->getMessage();
} finally {
    echo "Cleanup";
}

// Custom exception
class AppException extends RuntimeException {
    public function __construct(
        string $message,
        private readonly string $context = "",
        int $code = 0,
        ?\Throwable $previous = null
    ) {
        parent::__construct($message, $code, $previous);
    }

    public function getContext(): string { return $this->context; }
}

// Exception hierarchy
// Throwable
//   Error (PHP internal errors)
//     TypeError, ValueError, ...
//   Exception (application exceptions)
//     RuntimeException, LogicException, ...

// set_exception_handler
set_exception_handler(function (Throwable $e) {
    error_log($e->getMessage());
    http_response_code(500);
    echo "Internal Server Error";
});
```


---

# CHAPTER 7: DATABASE AND FILE I/O


## PDO and Files

```php
<?php

// PDO (PHP Data Objects)
$dsn = "mysql:host=localhost;dbname=mydb;charset=utf8mb4";
$pdo = new PDO($dsn, "user", "password", [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
]);

// Prepared statement (prevents SQL injection)
$stmt = $pdo->prepare("SELECT * FROM users WHERE email = ? AND active = ?");
$stmt->execute([$email, 1]);
$users = $stmt->fetchAll();

$stmt = $pdo->prepare("INSERT INTO users (name, email) VALUES (:name, :email)");
$stmt->execute([":name" => "Alice", ":email" => "alice@example.com"]);
$pdo->lastInsertId();

// Transaction
$pdo->beginTransaction();
try {
    $pdo->exec("UPDATE accounts SET balance = balance - 100 WHERE id = 1");
    $pdo->exec("UPDATE accounts SET balance = balance + 100 WHERE id = 2");
    $pdo->commit();
} catch (PDOException $e) {
    $pdo->rollBack();
    throw $e;
}

// File I/O
// Read
$content = file_get_contents("file.txt");
$lines   = file("file.txt", FILE_IGNORE_NEW_LINES);

$fp = fopen("file.txt", "r");
while (!feof($fp)) {
    $line = fgets($fp);
}
fclose($fp);

// Write
file_put_contents("out.txt", "Hello\n");
file_put_contents("out.txt", "More\n", FILE_APPEND);

$fp = fopen("out.txt", "w");
fwrite($fp, "Hello\n");
fclose($fp);

// JSON
$json = json_encode(["name" => "Alice", "age" => 30], JSON_PRETTY_PRINT);
$data = json_decode($json, associative: true);

// CSV
$fp = fopen("data.csv", "r");
$headers = fgetcsv($fp);
while ($row = fgetcsv($fp)) {
    $data[] = array_combine($headers, $row);
}
fclose($fp);
```


---

# CHAPTER 8: MODERN PHP FEATURES


## PHP 8.x Features

```php
<?php

// Nullsafe operator (?->)
$city = $user?->getAddress()?->getCity();

// Named arguments
htmlspecialchars(string: $s, encoding: "UTF-8");

// Union types
function process(int|string $id): bool|string { /* ... */ }

// Intersection types (PHP 8.1)
function accept(Iterator&Countable $collection): void { }

// Fibers (PHP 8.1 — cooperative multitasking)
$fiber = new Fiber(function(): void {
    $value = Fiber::suspend("first");
    echo "Resumed with: $value\n";
});

$result = $fiber->start();
echo $result . "\n";          // "first"
$fiber->resume("hello");      // "Resumed with: hello"

// Readonly properties and classes (PHP 8.2)
class Config {
    public function __construct(
        public readonly string $host,
        public readonly int $port,
    ) {}
}

// First-class callable syntax
$fn = $obj->method(...);
$fn = strlen(...);
$fn = Closure::fromCallable('strlen');

// Array unpacking with string keys (PHP 8.1)
$merged = [...$defaults, ...$custom];

// never return type
function throwError(string $msg): never {
    throw new Exception($msg);
}

// Disjunctive Normal Form types (PHP 8.2)
function accept2((Iterator&Countable)|null $c): void { }

// #[Attributes]
#[Route("/users", methods: ["GET", "POST"])]
class UserController {
    #[Deprecated("Use newMethod() instead")]
    public function oldMethod(): void {}
}
```
