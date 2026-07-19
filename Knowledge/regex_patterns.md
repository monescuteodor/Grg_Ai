# Regex Patterns Complete Reference


---

# CHAPTER 1: SYNTAX

```
.        Any character (except newline)
\d       Digit [0-9]
\D       Non-digit
\w       Word character [a-zA-Z0-9_]
\W       Non-word
\s       Whitespace (space, tab, newline)
\S       Non-whitespace
^        Start of string
$        End of string
\b       Word boundary

QUANTIFIERS:
*        0 or more
+        1 or more
?        0 or 1
{3}      Exactly 3
{2,5}    Between 2 and 5
{3,}     3 or more

GROUPS:
(abc)    Capture group
(?:abc)  Non-capture group
(a|b)    a or b
(?=abc)  Lookahead (followed by abc)
(?!abc)  Negative lookahead
```


# CHAPTER 2: MOST USEFUL PATTERNS

```python
import re

# Email
re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

# Phone (international)
re.match(r'^\+?[1-9]\d{6,14}$', phone)

# URL
re.match(r'^https?://[^\s/$.?#].[^\s]*$', url)

# IPv4
re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip)

# Date (YYYY-MM-DD)
re.match(r'^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$', date)

# Password (min 8 chars, 1 upper, 1 lower, 1 digit)
re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password)

# HTML tags
re.findall(r'<(\w+)[^>]*>(.*?)</\1>', html)

# Extract numbers
re.findall(r'\d+\.?\d*', text)

# Remove extra whitespace
re.sub(r'\s+', ' ', text).strip()

# Slugify
re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

# Extract domain from URL
re.search(r'https?://([^/]+)', url).group(1)

# Validate hex color
re.match(r'^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$', color)

# Split by multiple delimiters
re.split(r'[,;\s]+', text)

# Named groups
m = re.match(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', '2026-07-18')
m.group('year')   # '2026'
m.group('month')  # '07'
```


# CHAPTER 3: JAVASCRIPT

```javascript
// Test
/^\d+$/.test('123')          // true
/^[a-z]+$/i.test('Hello')    // true (case insensitive)

// Match
'hello world'.match(/\w+/g)  // ['hello', 'world']

// Replace
'hello world'.replace(/world/, 'JS')         // 'hello JS'
'a-b-c'.replace(/-/g, '_')                   // 'a_b_c'
'John Smith'.replace(/(\w+) (\w+)/, '$2, $1') // 'Smith, John'

// Split
'a, b; c d'.split(/[,;\s]+/)  // ['a', 'b', 'c', 'd']
```