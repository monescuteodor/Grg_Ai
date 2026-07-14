# Shell Scripting and Bash Complete Reference


---

# CHAPTER 1: BASH FUNDAMENTALS


## Remarks

Shell scripting automates repetitive tasks, deploys applications, processes log files, and manages servers. Every developer needs basic Bash skills — it's the universal interface to Unix/Linux systems. Bash is available on Linux, macOS, Windows (WSL/Git Bash), and cloud servers.

Key concepts: **Variables**, **Conditionals** (if/elif/else), **Loops** (for, while), **Functions**, **Pipes and redirection**, **Exit codes**, **Command substitution**, **String manipulation**, **Arrays**, **Regular expressions** (grep/sed/awk).


## Variables and Data Types

```bash
#!/bin/bash

# Variables (no spaces around =!)
name="Alice"
age=30
readonly PI=3.14159  # Constant

# Use variables with $
echo "Hello, $name! You are $age years old."
echo "Pi is ${PI}"  # Braces for clarity

# Command substitution (capture command output)
current_date=$(date +%Y-%m-%d)
file_count=$(ls *.py 2>/dev/null | wc -l)
echo "Today: $current_date, Python files: $file_count"

# Arithmetic
count=$((5 + 3))
result=$((age * 2))
((count++))          # Increment
((count += 10))      # Add 10

# String operations
str="Hello World"
echo ${#str}              # Length: 11
echo ${str:0:5}           # Substring: Hello
echo ${str,,}             # Lowercase: hello world
echo ${str^^}             # Uppercase: HELLO WORLD
echo ${str/World/Bash}    # Replace: Hello Bash
echo ${str% *}            # Remove last word: Hello
echo ${str#* }            # Remove first word: World

# Default values
echo ${UNDEFINED_VAR:-"default"}   # Use default if unset
echo ${UNDEFINED_VAR:="default"}   # Set AND use default if unset

# Arrays
fruits=("apple" "banana" "cherry" "date")
echo ${fruits[0]}         # apple
echo ${fruits[@]}         # All elements
echo ${#fruits[@]}        # Length: 4
fruits+=("elderberry")    # Append

for fruit in "${fruits[@]}"; do
    echo "Fruit: $fruit"
done

# Associative arrays (dictionaries, Bash 4+)
declare -A colors
colors[red]="#FF0000"
colors[green]="#00FF00"
colors[blue]="#0000FF"
echo ${colors[red]}       # #FF0000
```


## Conditionals

```bash
# if/elif/else
if [[ $age -gt 18 ]]; then
    echo "Adult"
elif [[ $age -gt 12 ]]; then
    echo "Teenager"
else
    echo "Child"
fi

# String comparisons (use == inside [[ ]])
if [[ "$name" == "Alice" ]]; then echo "Hi Alice!"; fi
if [[ "$name" != "Bob" ]]; then echo "Not Bob"; fi
if [[ -z "$var" ]]; then echo "Empty or unset"; fi
if [[ -n "$var" ]]; then echo "Not empty"; fi

# Numeric comparisons
# -eq (equal), -ne (not equal), -gt (greater), -lt (less)
# -ge (greater/equal), -le (less/equal)
if [[ $count -eq 0 ]]; then echo "Zero"; fi

# File tests
if [[ -f "config.txt" ]]; then echo "File exists"; fi
if [[ -d "src" ]]; then echo "Directory exists"; fi
if [[ -r "file.txt" ]]; then echo "Readable"; fi
if [[ -w "file.txt" ]]; then echo "Writable"; fi
if [[ -x "script.sh" ]]; then echo "Executable"; fi
if [[ ! -f "missing.txt" ]]; then echo "Doesn't exist"; fi

# Logical operators
if [[ $a -gt 0 && $b -gt 0 ]]; then echo "Both positive"; fi
if [[ $a -gt 0 || $b -gt 0 ]]; then echo "At least one positive"; fi

# Case statement (switch)
case "$command" in
    start)  echo "Starting...";;
    stop)   echo "Stopping...";;
    restart)
        echo "Restarting..."
        stop_service
        start_service
        ;;
    *)      echo "Usage: $0 {start|stop|restart}";;
esac
```


## Loops

```bash
# For loop
for i in 1 2 3 4 5; do
    echo "Number: $i"
done

# C-style for
for ((i=0; i<10; i++)); do
    echo "Index: $i"
done

# Iterate over files
for file in *.py; do
    echo "Python file: $file"
    wc -l "$file"
done

# Iterate over command output
for user in $(cat users.txt); do
    echo "Processing: $user"
done

# While loop
count=0
while [[ $count -lt 5 ]]; do
    echo "Count: $count"
    ((count++))
done

# Read file line by line (safe, handles spaces)
while IFS= read -r line; do
    echo "Line: $line"
done < "input.txt"

# Infinite loop with break
while true; do
    read -p "Enter command (quit to exit): " cmd
    if [[ "$cmd" == "quit" ]]; then
        break
    fi
    echo "Running: $cmd"
done
```


## Functions

```bash
# Function definition
greet() {
    local name=$1     # Local variable (not global!)
    local greeting=${2:-"Hello"}  # Default value
    echo "$greeting, $name!"
}

greet "Alice"          # Hello, Alice!
greet "Bob" "Hi"       # Hi, Bob!

# Return values (exit code: 0=success, 1-255=error)
is_even() {
    if (( $1 % 2 == 0 )); then
        return 0  # Success = true
    else
        return 1  # Failure = false
    fi
}

if is_even 4; then
    echo "4 is even"
fi

# Capture output (for returning strings/data)
get_timestamp() {
    echo $(date +%Y%m%d_%H%M%S)
}
ts=$(get_timestamp)
echo "Timestamp: $ts"

# Error handling
die() {
    echo "ERROR: $1" >&2
    exit ${2:-1}
}

[[ -f "config.txt" ]] || die "Config file missing!" 2
```


---

# CHAPTER 2: PRACTICAL SCRIPTS


## Deployment Script

```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

PROJECT_DIR="/opt/myapp"
BACKUP_DIR="/opt/backups"
LOG_FILE="/var/log/deploy.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Deployment started ==="

# Create backup
BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S)"
log "Creating backup: $BACKUP_NAME"
cp -r "$PROJECT_DIR" "$BACKUP_DIR/$BACKUP_NAME"

# Pull latest code
log "Pulling latest code..."
cd "$PROJECT_DIR"
git pull origin main || {
    log "Git pull failed! Rolling back..."
    cp -r "$BACKUP_DIR/$BACKUP_NAME"/* "$PROJECT_DIR/"
    die "Deployment failed at git pull"
}

# Install dependencies
log "Installing dependencies..."
pip install -r requirements.txt --quiet

# Run tests
log "Running tests..."
if ! pytest tests/ --quiet; then
    log "Tests failed! Rolling back..."
    cp -r "$BACKUP_DIR/$BACKUP_NAME"/* "$PROJECT_DIR/"
    die "Deployment failed: tests did not pass"
fi

# Restart service
log "Restarting service..."
sudo systemctl restart myapp.service
sleep 3

# Health check
if curl -s http://localhost:8000/health | grep -q '"ok"'; then
    log "=== Deployment SUCCESS ==="
else
    log "Health check failed! Rolling back..."
    cp -r "$BACKUP_DIR/$BACKUP_NAME"/* "$PROJECT_DIR/"
    sudo systemctl restart myapp.service
    die "Deployment failed: health check"
fi

# Clean old backups (keep last 5)
ls -dt "$BACKUP_DIR"/backup_* | tail -n +6 | xargs rm -rf 2>/dev/null
log "Old backups cleaned."
```


## Log Analysis Script

```bash
#!/bin/bash
# Analyze web server access logs

LOG_FILE="${1:-/var/log/nginx/access.log}"

echo "=== Log Analysis: $LOG_FILE ==="
echo "Total requests: $(wc -l < "$LOG_FILE")"
echo ""

echo "--- Top 10 IPs ---"
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -10

echo ""
echo "--- HTTP Status Codes ---"
awk '{print $9}' "$LOG_FILE" | sort | uniq -c | sort -rn

echo ""
echo "--- Top 10 Requested URLs ---"
awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -10

echo ""
echo "--- Errors (4xx/5xx) ---"
awk '$9 >= 400 {print $9, $7}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -10

echo ""
echo "--- Requests per hour ---"
awk '{print $4}' "$LOG_FILE" | cut -d: -f1,2 | sort | uniq -c | sort -rn | head -24
```


---

# CHAPTER 3: COMMON PITFALLS


## Bash Pitfalls

```
PITFALL 1: Unquoted variables
  rm -rf $DIR  → if DIR is empty → rm -rf / (deletes everything!)
  Fix: always quote: rm -rf "$DIR"

PITFALL 2: Spaces around =
  name = "Alice"  → ERROR (tries to run 'name' as command)
  Fix: name="Alice" (no spaces!)

PITFALL 3: Not using set -euo pipefail
  Script continues after errors → corrupted state.
  Fix: always start with set -euo pipefail

PITFALL 4: Using [ ] instead of [[ ]]
  [ $a == $b ] fails if $a is empty or has spaces.
  Fix: [[ "$a" == "$b" ]] (modern, safe)

PITFALL 5: for file in $(ls *.txt)
  Breaks on filenames with spaces.
  Fix: for file in *.txt; do ... done

PITFALL 6: Parsing ls output
  ls output is not reliable for scripting.
  Fix: use find or globbing: for f in dir/*; do ... done

PITFALL 7: Not checking if command exists
  Calling tool that might not be installed → cryptic error.
  Fix: command -v jq >/dev/null 2>&1 || die "jq not installed"

PITFALL 8: Forgetting to make script executable
  bash: ./script.sh: Permission denied
  Fix: chmod +x script.sh

PITFALL 9: Windows line endings (CRLF)
  /bin/bash^M: bad interpreter
  Fix: dos2unix script.sh (or use LF in your editor)

PITFALL 10: Not using local in functions
  Variables leak to global scope → unexpected overwrite.
  Fix: local var="value" inside functions
```