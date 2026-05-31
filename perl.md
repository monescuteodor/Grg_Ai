# Perl Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH PERL


## Remarks

Perl is a high-level, general-purpose, interpreted, dynamic programming language. It is known for its powerful text processing, regular expressions, and CPAN module ecosystem. Perl 5 is still widely used; Perl 7 (modernized 5) is in development.

Tools: perl interpreter, CPAN, cpanm (cpanminus), Carton (dependency manager).


## Hello World

```perl
#!/usr/bin/perl
use strict;
use warnings;

print "Hello, World!\n";
printf("Hello, %s!\n", "Perl");
say "Hello with newline";   # say adds \n automatically
```

```bash
perl hello.pl
perl -e "print 'Hello\n'"
perl -w -strict hello.pl   # with warnings
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Sigils and Types

```perl
use strict;
use warnings;

# Scalar ($) — single value
my $name   = "Alice";
my $age    = 30;
my $pi     = 3.14159;
my $flag   = 1;        # true (any non-zero, non-empty)
my $undef  = undef;    # undefined

# Array (@) — ordered list
my @arr    = (1, 2, 3, 4, 5);
my @words  = qw(one two three four);   # quote words

# Hash (%) — key-value pairs
my %user   = (name => "Alice", age => 30);
my %config = ("host" => "localhost", "port" => 8080);

# References (like pointers)
my $aref = \@arr;       # reference to array
my $href = \%user;      # reference to hash
my $sref = \"hello";    # reference to scalar
my $cref = sub { ... }; # anonymous sub reference

# Dereference
@$aref         # array
$$aref[0]      # element: $arr[0]
$aref->[0]     # same with arrow notation
%$href         # hash
$$href{name}   # element: $user{name}
$href->{name}  # same with arrow notation

# Anonymous references
my $aref2 = [1, 2, 3];        # anonymous array ref
my $href2 = {a => 1, b => 2}; # anonymous hash ref
my $code  = sub { print "hello\n"; };

# Scalar operations
length($name)
uc($name); lc($name); ucfirst($name); lcfirst($name)
substr($name, 0, 3)
index($name, "ic")
rindex($name, "l")
reverse($name)
sprintf("%.2f", $pi)

# String repetition
my $line = "-" x 40;        # "----...----"
my @zeros = (0) x 5;        # (0,0,0,0,0)

# Concatenation
my $full = $name . " Smith";
$full .= "!";   # append

# String comparison
"abc" eq "abc"   # true
"abc" ne "xyz"   # true
"abc" lt "bcd"   # true (lexicographic)
"abc" le "bcd"
"abc" gt "aaa"
"abc" ge "aaa"
"abc" cmp "abc"  # 0 (spaceship for strings)
1 <=> 2          # -1 (spaceship for numbers)
```


---

# CHAPTER 3: ARRAYS AND HASHES


## Collection Operations

```perl
# Array operations
my @arr = (1..10);
push @arr, 11, 12;          # add to end
my $last = pop @arr;        # remove from end
unshift @arr, 0;            # add to front
my $first = shift @arr;     # remove from front
my @slice = @arr[1..3];     # slice
my $len = scalar @arr;      # length
my $last_idx = $#arr;       # last index

# splice — insert/remove/replace
my @removed = splice(@arr, 2, 3);        # remove 3 at index 2
splice(@arr, 2, 0, 99, 100);            # insert at index 2
splice(@arr, 1, 2, 50, 60);            # replace 2 with 2

# sort
my @sorted = sort @arr;
my @num_sorted = sort { $a <=> $b } @arr;   # numeric
my @rev_sorted = sort { $b <=> $a } @arr;
my @by_length  = sort { length($a) <=> length($b) } @words;

# grep (filter)
my @evens = grep { $_ % 2 == 0 } @arr;
my @long_words = grep { length($_) > 4 } @words;

# map (transform)
my @doubled = map { $_ * 2 } @arr;
my @upper   = map { uc $_ } @words;
my @pairs   = map { [$_, $_ * $_ ] } @arr;

# join / split
my $str = join(", ", @arr);
my @parts = split(/,\s*/, $str);
my @lines = split(/\n/, $text);

# wantarray
sub flexible {
    return wantarray ? (1, 2, 3) : 3;
}

# Hash operations
my %h = (name => "Alice", age => 30);
$h{city} = "NYC";
delete $h{age};
exists $h{name}     # true/false
defined $h{name}    # true if not undef
my @keys = keys %h;
my @vals = values %h;
my @pairs2 = each %h;    # iterate

while (my ($k, $v) = each %h) {
    print "$k => $v\n";
}

# Hash slice
my @selected = @h{qw(name city)};    # multiple values
```


---

# CHAPTER 4: CONTROL FLOW


## Flow Control

```perl
# if/elsif/else
if ($x > 0) {
    print "positive\n";
} elsif ($x == 0) {
    print "zero\n";
} else {
    print "negative\n";
}

# Postfix if/unless/while/until/for
print "positive\n" if $x > 0;
print "not zero\n" unless $x == 0;
$x++ while $x < 10;
$x-- until $x == 0;
print "$_\n" for @arr;

# Ternary
my $label = $x > 0 ? "pos" : "non-pos";

# given/when (use feature 'switch'; experimental)
# Better to use if/elsif chains

# for / foreach
for (my $i = 0; $i < 10; $i++) { print "$i\n"; }
foreach my $item (@arr) { print "$item\n"; }
for my $item (@arr) { print "$item\n"; }   # for = foreach
for (@arr) { print "$_\n"; }               # $_ default

# while / until / do-while
while ($n > 0) { $n--; }
until ($n == 0) { $n--; }
do { $n++ } while $n < 10;

# loop controls
last;       # break
next;       # continue
redo;       # restart iteration without re-checking condition

# Labels for nested loops
OUTER: for my $i (1..5) {
    for my $j (1..5) {
        next OUTER if $j == 3;
        last OUTER if $i == 4;
        print "$i,$j\n";
    }
}
```


---

# CHAPTER 5: REGULAR EXPRESSIONS


## Regex (Perl's Superpower)

```perl
# Match operator (m//)
my $str = "Hello, World! 123";

if ($str =~ /World/) {
    print "Found World\n";
}

if ($str =~ /(\w+),\s*(\w+)/) {
    print "Captured: $1, $2\n";   # Hello, World
}

# Flags
/pattern/i    # case-insensitive
/pattern/g    # global (all matches)
/pattern/m    # multiline (^ and $ match per line)
/pattern/s    # single-line (. matches \n)
/pattern/x    # extended (allow whitespace and comments)

# Global match
my @matches = ($str =~ /\d+/g);   # all digit sequences: (123)
while ($str =~ /(\w+)/g) {
    print "Found: $1\n";
}

# Substitution (s///)
(my $new = $str) =~ s/World/Perl/;
$str =~ s/\d+/NUM/g;              # replace all numbers
$str =~ s/(\w+)/uc($1)/ge;       # /e evaluates replacement

# tr (transliterate)
(my $copy = $str) =~ tr/a-z/A-Z/;  # uppercase
$str =~ tr/aeiou//d;                 # delete vowels
my $count = ($str =~ tr/l//);        # count 'l'

# Named captures
if ($date =~ /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/) {
    print $+{year}, $+{month}, $+{day};
}

# Lookahead / lookbehind
/\d+(?=px)/   # number followed by px
/(?<=@)\w+/   # word after @
/\d+(?!px)/   # number NOT followed by px

# qr// — compiled regex
my $pattern = qr/\d{3}-\d{4}/;
if ($phone =~ $pattern) { ... }
```


---

# CHAPTER 6: SUBROUTINES AND REFERENCES


## Functions and References

```perl
# Subroutine definition
sub greet {
    my ($name, $greeting) = @_;   # @_ contains all args
    $greeting //= "Hello";        # default with //=
    return "$greeting, $name!";
}

my $msg = greet("Alice", "Hi");

# Prototypes (mostly avoid)
sub max ($$) { $_[0] > $_[1] ? $_[0] : $_[1] }

# Variable-length args
sub sum {
    my $total = 0;
    $total += $_ for @_;
    return $total;
}

# Return multiple values
sub minmax {
    my @sorted = sort { $a <=> $b } @_;
    return ($sorted[0], $sorted[-1]);
}
my ($min, $max) = minmax(3, 1, 4, 1, 5, 9);

# Closures
sub make_counter {
    my $count = 0;
    return sub { return ++$count; };
}
my $c = make_counter();
print $c->();  # 1
print $c->();  # 2

# Higher-order functions
sub apply {
    my ($func, @args) = @_;
    return $func->(@args);
}

my $double = sub { $_[0] * 2 };
print apply($double, 5);   # 10

# Complex data structures
my @matrix = ([1,2,3],[4,5,6],[7,8,9]);
print $matrix[1][2];   # 6

my %data = (
    users => [
        { name => "Alice", age => 30 },
        { name => "Bob",   age => 25 },
    ],
);
print $data{users}[0]{name};   # Alice
```


---

# CHAPTER 7: FILE I/O AND MODULES


## File Operations

```perl
use strict;
use warnings;

# Open / Read / Close
open(my $fh, '<', 'input.txt') or die "Cannot open: $!";
while (my $line = <$fh>) {
    chomp $line;   # remove newline
    print "$line\n";
}
close $fh;

# Read all lines
open(my $fh2, '<', 'input.txt') or die $!;
my @lines = <$fh2>;
close $fh2;
chomp @lines;

# Write
open(my $out, '>', 'output.txt') or die $!;
print $out "Hello, World!\n";
printf $out "Pi = %.2f\n", 3.14;
close $out;

# Append
open(my $app, '>>', 'log.txt') or die $!;
print $app time() . " - event\n";
close $app;

# File::Find
use File::Find;
find(sub {
    print "$File::Find::name\n" if /\.pl$/;
}, '.');

# Path::Tiny (modern, install from CPAN)
use Path::Tiny;
my $file = path('data.txt');
my $content = $file->slurp;
my @lines2 = $file->lines({chomp => 1});
$file->spew("new content\n");
$file->append("more\n");

# Modules
use POSIX qw(floor ceil);
use List::Util qw(sum min max first reduce any all);
use Scalar::Util qw(looks_like_number blessed reftype);
use Data::Dumper;

print Dumper(\%user);

my $total = sum @numbers;
my $minimum = min @numbers;
my $found = first { $_ > 3 } @arr;

# JSON
use JSON;
my $json_str = encode_json({ name => "Alice", age => 30 });
my $data = decode_json($json_str);

# LWP (HTTP)
use LWP::Simple;
my $content = get("https://example.com");

use LWP::UserAgent;
my $ua = LWP::UserAgent->new;
my $response = $ua->get("https://api.example.com/data");
if ($response->is_success) {
    print $response->decoded_content;
}
```


---

# CHAPTER 8: OBJECT-ORIENTED PERL


## OOP with Moose/Moo

```perl
# Classic OOP (bless)
package Animal;

sub new {
    my ($class, %args) = @_;
    my $self = {
        name  => $args{name},
        sound => $args{sound} // "...",
    };
    return bless $self, $class;
}

sub name  { $_[0]->{name} }
sub sound { $_[0]->{sound} }

sub speak {
    my $self = shift;
    return $self->name . " says " . $self->sound;
}

package Dog;
use parent 'Animal';

sub new {
    my ($class, %args) = @_;
    $args{sound} = "Woof";
    my $self = $class->SUPER::new(%args);
    $self->{breed} = $args{breed};
    return $self;
}

sub breed { $_[0]->{breed} }
sub speak { $_[0]->SUPER::speak() . "!" }

# Moo (lightweight modern OOP)
package Point;
use Moo;

has 'x' => (is => 'ro', required => 1);
has 'y' => (is => 'ro', required => 1);
has 'label' => (is => 'rw', default => "point");

sub distance {
    my ($self, $other) = @_;
    sqrt(($self->x - $other->x)**2 + ($self->y - $other->y)**2)
}

# Usage
my $dog = Dog->new(name => "Rex", breed => "Lab");
print $dog->speak, "\n";

my $p1 = Point->new(x => 3, y => 4);
my $p2 = Point->new(x => 0, y => 0);
printf "Distance: %.2f\n", $p1->distance($p2);
```
