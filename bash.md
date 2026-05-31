# Bash Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH BASH


## Remarks

Bash (Bourne Again SHell) is the default shell on most Linux and macOS systems. It is a command interpreter and scripting language. Bash scripts automate tasks, manage files, and glue programs together.

Shebang line: `#!/usr/bin/env bash` (portable) or `#!/bin/bash`.


## Hello World

```bash
#!/usr/bin/env bash
echo "Hello, World!"
printf "Hello, %s!\n" "Bash"

# Run
bash hello.sh
chmod +x hello.sh && ./hello.sh
```

## Script Best Practices

```bash
#!/usr/bin/env bash
set -euo pipefail   # -e: exit on error, -u: undefined vars are errors, -o pipefail: pipe errors
IFS=$'\n\t'         # safer word splitting

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Variables

```bash
# Assignment (no spaces around =)
name="Alice"
age=30
readonly PI=3.14159    # constant

# Access with $
echo "$name"
echo "${name}"          # preferred in strings/substitutions

# Unset
unset name

# Special variables
$0   # script name
$1 $2 $3  # positional arguments
$@   # all arguments (as separate words)
$*   # all arguments (as one word)
$#   # number of arguments
$?   # exit status of last command
$$   # PID of current shell
$!   # PID of last background command
$_   # last argument of previous command

# Environment variables
$HOME $PATH $USER $SHELL $PWD $OLDPWD

# Default values
name="${1:-World}"            # use "World" if $1 unset or empty
name="${1:=World}"            # assign and use "World" if unset
name="${1:?'Name required'}"  # error if unset
name="${1:+'set'}"            # use "set" if $1 is set

# String operations
s="Hello, World!"
echo "${#s}"          # length: 13
echo "${s:0:5}"       # substring: "Hello"
echo "${s: -6}"       # from end: "orld!"
echo "${s/World/Bash}" # replace first: "Hello, Bash!"
echo "${s//l/L}"      # replace all: "HeLLo, WorLd!"
echo "${s^^}"         # uppercase
echo "${s,,}"         # lowercase
echo "${s#Hello, }"   # strip prefix
echo "${s%!}"         # strip suffix

# Arrays
arr=(1 2 3 4 5)
arr+=(6 7)               # append
echo "${arr[0]}"         # 1
echo "${arr[@]}"         # all elements
echo "${#arr[@]}"        # length: 7
echo "${arr[@]:2:3}"     # slice: 3 4 5
for item in "${arr[@]}"; do echo "$item"; done

# Associative arrays (bash 4+)
declare -A map
map["name"]="Alice"
map["age"]=30
echo "${map[name]}"
echo "${!map[@]}"    # keys
echo "${map[@]}"     # values
```


---

# CHAPTER 3: CONTROL FLOW


## Conditionals

```bash
# if/elif/else
if [[ "$name" == "Alice" ]]; then
    echo "Hello, Alice!"
elif [[ "$age" -gt 18 ]]; then
    echo "You are an adult"
else
    echo "Hello, stranger!"
fi

# [[ ]] — preferred (bash extended test)
[[ -z "$var" ]]      # empty string
[[ -n "$var" ]]      # non-empty string
[[ "$a" == "$b" ]]   # string equal
[[ "$a" != "$b" ]]   # string not equal
[[ "$a" < "$b" ]]    # string less than
[[ $n -eq 42 ]]      # numeric equal
[[ $n -ne 42 ]]      # numeric not equal
[[ $n -lt 42 ]]      # less than
[[ $n -gt 42 ]]      # greater than
[[ $n -le 42 ]]      # less than or equal
[[ $n -ge 42 ]]      # greater than or equal
[[ -e "file" ]]      # file/dir exists
[[ -f "file" ]]      # regular file
[[ -d "dir" ]]       # directory
[[ -r "file" ]]      # readable
[[ -w "file" ]]      # writable
[[ -x "file" ]]      # executable
[[ -s "file" ]]      # non-empty file
[[ "$str" =~ ^[0-9]+$ ]]  # regex match

# Compound conditions
[[ $a -gt 0 && $b -gt 0 ]]
[[ $a -gt 0 || $b -gt 0 ]]
[[ ! -f "file" ]]

# case
case "$day" in
    Mon|Tue|Wed|Thu|Fri)
        echo "Weekday" ;;
    Sat|Sun)
        echo "Weekend" ;;
    *)
        echo "Unknown" ;;
esac

# Ternary-like
result=$( [[ $x -gt 0 ]] && echo "pos" || echo "non-pos" )
```

## Loops

```bash
# for
for i in 1 2 3 4 5; do echo "$i"; done
for i in {1..10}; do echo "$i"; done
for i in {1..10..2}; do echo "$i"; done   # step 2
for (( i=0; i<10; i++ )); do echo "$i"; done

# for with glob
for file in *.txt; do
    echo "Processing: $file"
done

# for over array
for item in "${arr[@]}"; do
    echo "$item"
done

# for over command output
for line in $(cat file.txt); do echo "$line"; done
while IFS= read -r line; do echo "$line"; done < file.txt  # safer

# while
while [[ $n -gt 0 ]]; do
    echo "$n"
    ((n--))
done

# until
until [[ $n -ge 10 ]]; do
    ((n++))
done

# break / continue
for i in {1..10}; do
    [[ $i -eq 5 ]] && break
    [[ $i -eq 3 ]] && continue
    echo "$i"
done
```


---

# CHAPTER 4: FUNCTIONS


## Functions

```bash
# Function definition
greet() {
    local name="${1:-World}"   # local variable
    echo "Hello, $name!"
}

greet "Alice"
greet          # uses default

# Return value (exit code 0-255)
is_even() {
    [[ $(( $1 % 2 )) -eq 0 ]]
}
is_even 4 && echo "even" || echo "odd"

# Return string (use echo/printf)
get_extension() {
    echo "${1##*.}"
}
ext=$(get_extension "file.txt")

# Multiple outputs
parse_name() {
    local full="$1"
    echo "${full%% *}"   # first
    echo "${full#* }"    # last
}
read -r first last < <(parse_name "Alice Smith")

# Recursive
factorial() {
    [[ $1 -le 1 ]] && echo 1 && return
    echo $(( $1 * $(factorial $(( $1 - 1 ))) ))
}

# Error handling in functions
require_file() {
    if [[ ! -f "$1" ]]; then
        echo "ERROR: File not found: $1" >&2
        return 1
    fi
}
```


---

# CHAPTER 5: INPUT/OUTPUT AND REDIRECTION


## I/O

```bash
# Read input
read -p "Enter name: " name
read -s -p "Password: " password; echo
read -a arr -p "Enter values: "   # read into array
read -r line < file.txt           # read first line
read -t 10 -p "Timeout in 10s: " input  # with timeout

# Here string
cat <<< "Hello, World!"

# Heredoc
cat <<'EOF'
Line 1
Line 2 with $no_interpolation
EOF

cat <<EOF
Hello, $name!
Today is $(date)
EOF

# Redirection
command > output.txt         # stdout to file (overwrite)
command >> output.txt        # stdout to file (append)
command 2> error.txt         # stderr to file
command 2>&1                 # stderr to stdout
command &> all.txt           # stdout+stderr to file
command < input.txt          # stdin from file
command 2>/dev/null          # discard stderr

# Pipe
ls -l | grep "\.txt$" | sort | head -10

# Process substitution
diff <(ls dir1) <(ls dir2)
while IFS= read -r line; do
    echo ">> $line"
done < <(grep "error" logfile.txt)

# tee (write to file and stdout)
command | tee output.txt
command | tee -a output.txt   # append

# printf
printf "%-20s %5d\n" "Name" 42
printf "%08.2f\n" 3.14
```


---

# CHAPTER 6: STRING PROCESSING


## Text Tools

```bash
# grep
grep "pattern" file.txt
grep -i "PATTERN" file.txt     # case-insensitive
grep -r "pattern" dir/         # recursive
grep -l "pattern" *.txt        # filenames only
grep -n "pattern" file.txt     # line numbers
grep -v "pattern" file.txt     # invert (non-matching)
grep -c "pattern" file.txt     # count
grep -E "regex+" file.txt      # extended regex
grep -o "matched" file.txt     # only matching part
grep -A 3 -B 2 "pattern" file  # context lines

# sed (stream editor)
sed 's/foo/bar/' file.txt          # replace first per line
sed 's/foo/bar/g' file.txt         # replace all
sed 's/foo/bar/gi' file.txt        # case-insensitive
sed -i.bak 's/foo/bar/g' file.txt  # in-place with backup
sed -n '5,10p' file.txt            # print lines 5-10
sed '/^#/d' file.txt               # delete comment lines
sed 's/[[:space:]]*$//' file.txt   # strip trailing whitespace

# awk
awk '{print $1}' file.txt              # first field
awk -F: '{print $1,$3}' /etc/passwd   # custom delimiter
awk '{sum += $1} END {print sum}' file.txt
awk 'NR==5' file.txt                  # print 5th line
awk '$3 > 100 {print $1, $3}' data.txt
awk '/pattern/{count++} END{print count}' file.txt

# cut
cut -d: -f1,3 /etc/passwd    # fields 1 and 3, colon delimited
cut -c1-10 file.txt           # characters 1-10

# sort / uniq / wc
sort file.txt
sort -n file.txt              # numeric sort
sort -rn file.txt             # reverse numeric
sort -k2 -t, file.csv         # sort by 2nd field, comma sep
sort -u file.txt              # unique sort
uniq file.txt                 # remove consecutive duplicates
uniq -c file.txt              # count occurrences
sort file.txt | uniq -d       # show duplicates
wc -l file.txt                # line count
wc -w file.txt                # word count
```


---

# CHAPTER 7: FILE OPERATIONS


## Files and Directories

```bash
# Navigation
pwd; cd /path; cd -; cd ~

# Listing
ls -la    # long, all
ls -lh    # human-readable sizes
ls -lt    # sort by time
ls -lS    # sort by size

# File operations
cp src dst
cp -r srcdir dstdir           # recursive
cp -a srcdir dstdir           # archive (preserve metadata)
mv old new
rm file
rm -rf dir                    # force recursive (dangerous!)
ln -s target link             # symlink
ln target link                # hard link

# Find
find . -name "*.txt"
find . -type f -newer ref.txt
find . -size +10M
find . -mtime -7              # modified in last 7 days
find . -name "*.log" -delete  # find and delete
find . -name "*.sh" -exec chmod +x {} \;

# Permissions
chmod 755 script.sh
chmod +x script.sh
chmod u+rw,g+r,o-rwx file
chown user:group file
chown -R user dir/

# xargs
find . -name "*.txt" | xargs grep "pattern"
find . -name "*.txt" | xargs -I{} cp {} backup/

# Disk usage
du -sh dir/        # directory size
df -h              # filesystem usage
```


---

# CHAPTER 8: ADVANCED BASH


## Advanced Features

```bash
# Error handling
set -euo pipefail
trap 'echo "Error on line $LINENO"; exit 1' ERR
trap 'cleanup' EXIT INT TERM

cleanup() {
    echo "Cleaning up..."
    rm -f /tmp/tempfile
}

# Subshells
(cd /tmp && ls)   # cd is local to subshell
result=$(command) # command substitution

# Arithmetic
((n++))
((n += 5))
n=$(( n * 2 ))
echo $(( 10 / 3 ))  # integer: 3
echo $(( 10 % 3 ))  # modulo: 1

# bc for floats
echo "scale=4; 22/7" | bc

# Parallel execution
for i in {1..5}; do
    sleep 1 &
done
wait   # wait for all background jobs

# Signals
kill -SIGTERM $pid
kill -9 $pid       # SIGKILL (unblockable)

# getopts (argument parsing)
while getopts "f:n:vh" opt; do
    case $opt in
        f) file="$OPTARG" ;;
        n) num="$OPTARG" ;;
        v) verbose=true ;;
        h) usage; exit 0 ;;
        *) usage; exit 1 ;;
    esac
done

# mapfile / readarray
mapfile -t lines < file.txt
echo "${lines[0]}"

# Process management
sleep 100 &
bg_pid=$!
wait $bg_pid
echo "Exit status: $?"

jobs -l      # list background jobs
fg %1        # bring job 1 to foreground
bg %1        # send job 1 to background
disown %1    # detach from shell
```
