# Regex Mastery Complete Reference


---

# CHAPTER 1: FUNDAMENTALS


## Remarks

Regular expressions (regex/regexp) are patterns for matching, searching, extracting, and replacing text. Every programming language supports them. Mastering regex turns hours of manual text processing into one-liners. Used everywhere: form validation, log parsing, code editors, grep, sed, web scraping, routing.

Key concepts: **Literals** (exact match), **Character classes** ([a-z]), **Quantifiers** (*, +, ?), **Anchors** (^, $), **Groups** (capture and reference), **Lookahead/Lookbehind** (match without consuming), **Backreferences** (\1), **Lazy vs Greedy**, **Named groups**, **Unicode support**.

Tools: **regex101.com** (THE best tester — shows explanations), **grep** (CLI search), **sed** (CLI replace), **awk** (CLI text processing), **re** (Python), **RegExp** (JavaScript).


## Basic Patterns

```
LITERALS:
  hello         matches "hello" exactly

CHARACTER CLASSES:
  [abc]         matches a, b, or c
  [a-z]         matches any lowercase letter
  [A-Z]         matches any uppercase letter
  [0-9]         matches any digit
  [a-zA-Z]      matches any letter
  [a-zA-Z0-9]   matches any alphanumeric
  [^abc]        matches anything EXCEPT a, b, c (negation)
  [^0-9]        matches anything except digits

SHORTHAND CLASSES:
  \d            digit [0-9]
  \D            non-digit [^0-9]
  \w            word char [a-zA-Z0-9_]
  \W            non-word char
  \s            whitespace [ \t\n\r\f\v]
  \S            non-whitespace
  .             ANY character (except newline by default)

ANCHORS:
  ^             start of string (or line with MULTILINE flag)
  $             end of string (or line with MULTILINE flag)
  \b            word boundary (between \w and \W)
  \B            non-word boundary

QUANTIFIERS:
  *             0 or more (greedy)
  +             1 or more (greedy)
  ?             0 or 1 (optional)
  {3}           exactly 3
  {2,5}         between 2 and 5
  {3,}          3 or more
  *?            0 or more (lazy — match as FEW as possible)
  +?            1 or more (lazy)
  ??            0 or 1 (lazy)

ALTERNATION:
  cat|dog       matches "cat" or "dog"
  (red|blue) car  matches "red car" or "blue car"

ESCAPING:
  \.            literal dot (not "any char")
  \*            literal asterisk
  \(            literal parenthesis
  \\            literal backslash
  Special chars needing escape: . * + ? ^ $ { } [ ] ( ) | \
```


## Python re Module

```python
import re

text = "Contact us at support@example.com or sales@example.com"

# Search (first match)
match = re.search(r'\w+@\w+\.\w+', text)
if match:
    print(match.group())           # support@example.com
    print(match.start(), match.end())  # Position

# Find all matches
emails = re.findall(r'\w+@\w+\.\w+', text)
print(emails)   # ['support@example.com', 'sales@example.com']

# Find all with groups
pairs = re.findall(r'(\w+)@(\w+\.\w+)', text)
print(pairs)    # [('support', 'example.com'), ('sales', 'example.com')]

# Finditer (lazy, returns match objects)
for match in re.finditer(r'\w+@\w+\.\w+', text):
    print(match.group(), match.span())

# Match (anchored to START of string)
if re.match(r'Contact', text):
    print("Starts with Contact")

# Fullmatch (entire string must match)
if re.fullmatch(r'\d{3}-\d{4}', '555-1234'):
    print("Valid phone")

# Sub (replace)
cleaned = re.sub(r'\d+', 'NUM', "Order 123 costs $456")
print(cleaned)   # "Order NUM costs $NUM"

# Sub with function
def double_numbers(match):
    return str(int(match.group()) * 2)

result = re.sub(r'\d+', double_numbers, "3 cats and 5 dogs")
print(result)   # "6 cats and 10 dogs"

# Split
parts = re.split(r'[,;\s]+', "one, two; three   four")
print(parts)    # ['one', 'two', 'three', 'four']

# Compile (reuse pattern for performance)
pattern = re.compile(r'\b[A-Z][a-z]+\b')
names = pattern.findall("Alice met Bob in Paris")
print(names)    # ['Alice', 'Bob', 'Paris']

# FLAGS:
# re.IGNORECASE (re.I)    — case-insensitive
# re.MULTILINE (re.M)     — ^ and $ match line boundaries
# re.DOTALL (re.S)        — . matches newline too
# re.VERBOSE (re.X)       — allow comments and whitespace in pattern

# Verbose pattern (readable complex regex)
email_pattern = re.compile(r'''
    ^                       # Start of string
    [a-zA-Z0-9._%+-]+      # Local part (before @)
    @                       # @ symbol
    [a-zA-Z0-9.-]+         # Domain name
    \.                      # Dot before TLD
    [a-zA-Z]{2,}           # TLD (com, org, io, etc.)
    $                       # End of string
''', re.VERBOSE)
```


---

# CHAPTER 2: GROUPS AND REFERENCES


## Capturing Groups

```python
# Parentheses create CAPTURING groups

# Extract parts
match = re.search(r'(\d{4})-(\d{2})-(\d{2})', '2026-06-10')
if match:
    print(match.group(0))    # '2026-06-10' (full match)
    print(match.group(1))    # '2026' (first group)
    print(match.group(2))    # '06' (second group)
    print(match.group(3))    # '10' (third group)
    print(match.groups())    # ('2026', '06', '10')


# NAMED GROUPS (?P<name>...)
match = re.search(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', '2026-06-10')
if match:
    print(match.group('year'))     # '2026'
    print(match.group('month'))    # '06'
    print(match.groupdict())       # {'year': '2026', 'month': '06', 'day': '10'}


# NON-CAPTURING groups (?:...)
# Groups for structure, but doesn't capture
emails = re.findall(r'\w+@(?:gmail|yahoo|outlook)\.com', text)
# (?:gmail|yahoo|outlook) groups alternation but doesn't capture


# BACKREFERENCES \1, \2 or (?P=name)
# Match repeated words
re.search(r'\b(\w+)\s+\1\b', 'the the cat')
# \1 refers to first group's match ("the" matches "the")

# Named backreference
re.search(r'\b(?P<word>\w+)\s+(?P=word)\b', 'the the cat')

# Find HTML tags with matching close
re.findall(r'<(\w+)>.*?</\1>', '<b>bold</b> <i>italic</i>')
# \1 ensures closing tag matches opening tag


# CONDITIONAL replacement with groups
# Reformat dates: 06/10/2026 → 2026-06-10
result = re.sub(r'(\d{2})/(\d{2})/(\d{4})', r'\3-\1-\2', '06/10/2026')
print(result)   # '2026-06-10'

# Named group in replacement
result = re.sub(
    r'(?P<month>\d{2})/(?P<day>\d{2})/(?P<year>\d{4})',
    r'\g<year>-\g<month>-\g<day>',
    '06/10/2026'
)
```


---

# CHAPTER 3: LOOKAHEAD AND LOOKBEHIND


## Zero-Width Assertions

```python
# Lookahead/lookbehind match a position, not characters.
# They CHECK but don't CONSUME (zero-width).

# POSITIVE LOOKAHEAD (?=...)
# Match "foo" only if followed by "bar"
re.findall(r'foo(?=bar)', 'foobar foobaz foo')
# ['foo'] — only the "foo" before "bar"

# NEGATIVE LOOKAHEAD (?!...)
# Match "foo" only if NOT followed by "bar"
re.findall(r'foo(?!bar)', 'foobar foobaz foo')
# ['foo', 'foo'] — "foo" before "baz" and standalone "foo"

# POSITIVE LOOKBEHIND (?<=...)
# Match digits only if preceded by "$"
re.findall(r'(?<=\$)\d+', 'Price: $100, €200, $300')
# ['100', '300']

# NEGATIVE LOOKBEHIND (?<!...)
# Match digits NOT preceded by "$"
re.findall(r'(?<!\$)\d+', 'Price: $100, 200, $300')
# ['00', '200', '00'] — careful! \d+ starts matching after $

# Better: match complete numbers not preceded by $
re.findall(r'(?<!\$)\b\d+\b', 'Price: $100, 200, $300')
# ['200']


# PRACTICAL EXAMPLES:

# Password validation (all conditions must be true)
password_re = re.compile(r'''
    ^
    (?=.*[a-z])        # At least one lowercase
    (?=.*[A-Z])        # At least one uppercase
    (?=.*\d)           # At least one digit
    (?=.*[@$!%*?&])    # At least one special char
    .{8,}              # At least 8 characters total
    $
''', re.VERBOSE)

password_re.match("MyP@ss1!")    # Match ✅
password_re.match("weakpass")    # None ❌ (no uppercase, digit, special)


# Add thousand separators: 1234567 → 1,234,567
re.sub(r'(?<=\d)(?=(\d{3})+$)', ',', '1234567')
# Lookbehind: position after a digit
# Lookahead: followed by groups of exactly 3 digits until end


# Extract price without currency symbol
re.findall(r'(?<=\$|€|£)\d+\.?\d*', 'Costs $19.99 or €17.50')
# ['19.99', '17.50']


# Match word NOT inside quotes
re.findall(r'(?<!")error(?!")', 'error "error" error')
# Finds standalone "error" but not the quoted one
```


---

# CHAPTER 4: ADVANCED PATTERNS


## Common Real-World Patterns

```python
# ──── EMAIL (simplified, RFC-compliant is 1000+ chars) ────
email_re = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# ──── URL ────
url_re = re.compile(r'https?://(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?')

# ──── IPv4 ────
ipv4_re = re.compile(r'^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$')

# ──── DATE (YYYY-MM-DD) ────
date_re = re.compile(r'^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$')

# ──── TIME (HH:MM:SS, 24hr) ────
time_re = re.compile(r'^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$')

# ──── HEX COLOR ────
hex_color_re = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')

# ──── SLUG ────
slug_re = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

# ──── PHONE (international) ────
phone_re = re.compile(r'^\+?[1-9]\d{1,14}$')

# ──── UUID v4 ────
uuid_re = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', re.I)

# ──── SEMANTIC VERSION ────
semver_re = re.compile(r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([\w.]+))?(?:\+([\w.]+))?$')

# ──── LOG LINE PARSING ────
log_re = re.compile(r'''
    ^
    (?P<ip>\d+\.\d+\.\d+\.\d+)\s+      # IP address
    \S+\s+\S+\s+                          # ident, authuser
    \[(?P<date>[^\]]+)\]\s+              # Date in brackets
    "(?P<method>\w+)\s+                   # HTTP method
     (?P<path>\S+)\s+                     # Request path
     (?P<proto>[^"]+)"\s+                # Protocol
    (?P<status>\d{3})\s+                 # Status code
    (?P<size>\d+|-)\s*                   # Response size
    "(?P<referer>[^"]*)"\s*              # Referer
    "(?P<ua>[^"]*)"                      # User agent
''', re.VERBOSE)

line = '192.168.1.1 - - [10/Jun/2026:14:30:00 +0300] "GET /api/users HTTP/1.1" 200 1234 "-" "Mozilla/5.0"'
match = log_re.match(line)
if match:
    print(match.groupdict())
    # {'ip': '192.168.1.1', 'date': '10/Jun/2026:14:30:00 +0300',
    #  'method': 'GET', 'path': '/api/users', ...}


# ──── EXTRACT MARKDOWN LINKS ────
md_link_re = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
links = md_link_re.findall('[Click here](https://example.com) and [docs](https://docs.com)')
# [('Click here', 'https://example.com'), ('docs', 'https://docs.com')]


# ──── CAMELCASE TO SNAKE_CASE ────
def camel_to_snake(name):
    s1 = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

camel_to_snake('camelCaseHTTPParser')   # 'camel_case_http_parser'


# ──── REMOVE HTML TAGS ────
def strip_html(html):
    return re.sub(r'<[^>]+>', '', html)

strip_html('<p>Hello <b>world</b>!</p>')   # 'Hello world!'
# WARNING: DON'T use regex to parse HTML in production!
# Use proper parser (BeautifulSoup, lxml). Regex can't handle nested tags.


# ──── VALIDATE JSON KEY ────
json_key_re = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
```


## Greedy vs Lazy vs Possessive

```python
# GREEDY (default): match as MUCH as possible
re.findall(r'<.+>', '<b>bold</b>')
# ['<b>bold</b>'] — greedy .+ eats everything between first < and LAST >

# LAZY (?): match as LITTLE as possible
re.findall(r'<.+?>', '<b>bold</b>')
# ['<b>', '</b>'] — lazy .+? stops at first >

# POSSESSIVE (+): match as much as possible, NEVER backtrack
# Python doesn't support possessive. Available in Java, Perl, PCRE.
# Prevents catastrophic backtracking.

# CATASTROPHIC BACKTRACKING:
# Pattern: (a+)+b  on input "aaaaaaaaaaaaaaac"
# Regex engine tries exponentially many ways to split a's between groups.
# Can freeze your program for minutes!
#
# FIX: avoid nested quantifiers ((a+)+), use atomic groups, or restructure.
# FIX: set timeout on regex operations.

import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Regex took too long!")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(2)   # 2 second timeout
try:
    re.match(r'(a+)+b', 'a' * 30 + 'c')
except TimeoutError:
    print("Regex timed out — likely catastrophic backtracking")
finally:
    signal.alarm(0)
```


---

# CHAPTER 5: COMMON PITFALLS


## Regex Pitfalls

```
PITFALL 1: Greedy by default
  <.+> matches "<b>bold</b>" as ONE match, not two tags.
  Fix: use lazy quantifier <.+?> or be more specific <[^>]+>.

PITFALL 2: Forgetting to escape special chars
  "file.txt" matches "fileTtxt" because . is ANY char.
  Fix: escape with \. → "file\.txt"

PITFALL 3: Catastrophic backtracking
  (a+)+ or (.*a){10} on non-matching input → exponential time.
  Fix: avoid nested quantifiers, use atomic groups, set timeouts.

PITFALL 4: Using regex to parse HTML/JSON/XML
  "<div>(<div>nested</div>)</div>" — regex can't count nesting.
  Fix: use proper parser (BeautifulSoup, JSON.parse, lxml).

PITFALL 5: Forgetting anchors
  \d+ matches "abc123def" (finds "123" inside).
  If you want ONLY digits: ^\d+$ (anchored).

PITFALL 6: Not using raw strings (Python)
  "\bword\b" — \b is interpreted as backspace!
  Fix: use raw strings r"\bword\b".

PITFALL 7: Locale-dependent character classes
  [a-z] doesn't match é, ü, ñ in some engines.
  Fix: use Unicode categories \p{L} for any letter (if supported).

PITFALL 8: Matching too much
  .* is often TOO greedy. Matches across lines, across fields.
  Fix: be specific. [^\n]* (anything except newline), [^,]* (until comma).

PITFALL 9: Not testing edge cases
  Email regex that fails on plus signs (user+tag@gmail.com).
  Fix: test with real-world data. Use regex101.com debugger.

PITFALL 10: Unreadable patterns
  ^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$
  Fix: use re.VERBOSE with comments. Or use a validation library instead.

PITFALL 11: Performance on large inputs
  Running complex regex on 100MB log file → minutes.
  Fix: use simple patterns, grep -F for literal strings, awk for structured data.

PITFALL 12: Capturing groups when not needed
  (foo|bar) creates capture group. Use (?:foo|bar) if you don't need it.
  Non-capturing is slightly faster and doesn't pollute match groups.
```