# PowerShell Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH POWERSHELL


## Remarks

PowerShell is a cross-platform task automation shell and scripting language built on .NET. It uses objects (not text) as output, enabling structured data pipelines. PowerShell 7+ (cross-platform) is the current version. Windows PowerShell 5.1 ships with Windows.

Tools: `pwsh` (PowerShell 7+), `powershell` (Windows 5.1), VS Code with PowerShell extension.


## Hello World

```powershell
Write-Host "Hello, World!"
Write-Output "Hello, PowerShell!"
"Hello from the pipeline"

# Run
pwsh -File hello.ps1
pwsh -Command "Write-Host 'Hello'"
```

## Execution Policy

```powershell
Get-ExecutionPolicy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Variables

```powershell
# Variables start with $
$name = "Alice"
$age = 30
$pi = 3.14159
$flag = $true
$nothing = $null

# Type declarations
[int]$n = 42
[string]$s = "hello"
[double]$d = 3.14
[bool]$b = $true
[datetime]$dt = Get-Date
[array]$arr = 1, 2, 3

# Automatic type conversion
[int]"42"       # 42
[string]42      # "42"
[datetime]"2024-01-15"

# Special values
$true; $false; $null

# String operations
$s = "Hello, World!"
$s.Length           # 13
$s.ToUpper()
$s.ToLower()
$s.Substring(0, 5)  # "Hello"
$s.Contains("World")
$s.Replace("World","PS")
$s.Split(",")
$s.Trim()
$s.StartsWith("Hello")
$s.EndsWith("!")
$s -like "*World*"  # wildcard match
$s -match "W\w+"    # regex match
$Matches[0]         # last regex match

# String interpolation (double quotes expand variables)
$greeting = "Hello, $name!"
$greeting = "Age: $($age * 2)"   # expression

# Verbatim string (single quotes)
$path = 'C:\Users\$name'   # $ is literal

# Here-string
$here = @"
Hello, $name!
Age: $age
"@

$here2 = @'
No $interpolation here
'@
```

## Collections

```powershell
# Array
$arr = 1, 2, 3, 4, 5
$arr = @(1, 2, 3)
$arr += 6              # creates new array
$arr[0]                # 1
$arr[-1]               # last
$arr[1..3]             # slice
$arr.Count
$arr.Length
$arr -contains 3       # $true
$arr | Sort-Object
$arr | Sort-Object -Descending
$arr | Select-Object -First 3
$arr | Where-Object { $_ -gt 3 }

# ArrayList (mutable, add/remove)
$list = [System.Collections.ArrayList]::new()
$list.Add("Alice") | Out-Null
$list.Remove("Alice")
$list.Count

# Generic List (preferred)
$list = [System.Collections.Generic.List[string]]::new()
$list.Add("Alice")
$list.Contains("Alice")
$list.Remove("Alice")

# Hashtable (dictionary)
$h = @{ name = "Alice"; age = 30 }
$h["name"]          # "Alice"
$h.name             # dot notation
$h["city"] = "NYC"
$h.Remove("age")
$h.ContainsKey("name")
$h.Keys; $h.Values
$h.Count
$h.GetEnumerator()

# Ordered hashtable
$oh = [ordered]@{ a = 1; b = 2; c = 3 }
```


---

# CHAPTER 3: CONTROL FLOW


## Flow Control

```powershell
# if/elseif/else
if ($x -gt 0) {
    Write-Host "positive"
} elseif ($x -eq 0) {
    Write-Host "zero"
} else {
    Write-Host "negative"
}

# Comparison operators
-eq  -ne  -lt  -gt  -le  -ge    # numeric/type comparison
-ceq -cne -clt -cgt -cle -cge   # case-sensitive
-like   # wildcard: "hello" -like "h*"
-notlike
-match  # regex: "hello" -match "h\w+"
-notmatch
-contains   # array: @(1,2,3) -contains 2
-notcontains
-in         # 2 -in @(1,2,3)
-notin
-and  -or  -not  -xor

# switch
switch ($day) {
    "Monday"   { "Start of week" }
    "Friday"   { "End of week" }
    { $_ -match "^S" } { "Weekend" }
    default    { "Midweek" }
}

# switch on multiple values
switch ($x) {
    { $_ -lt 0 }   { "negative"; break }
    0               { "zero"; break }
    { $_ -gt 0 }   { "positive"; break }
}

# foreach
foreach ($item in $collection) {
    Write-Host $item
}

# ForEach-Object (pipeline)
1..10 | ForEach-Object { $_ * 2 }
1..10 | ForEach-Object -Begin { "Start" } -Process { $_ } -End { "Done" }

# for / while / do-while
for ($i = 0; $i -lt 10; $i++) { Write-Host $i }

$n = 0
while ($n -lt 10) { $n++ }

do { $n++ } while ($n -lt 10)

# break / continue
foreach ($i in 1..10) {
    if ($i -eq 5) { break }
    if ($i % 2 -eq 0) { continue }
    Write-Host $i
}
```


---

# CHAPTER 4: FUNCTIONS AND MODULES


## Functions

```powershell
# Basic function
function Get-Greeting {
    param(
        [string]$Name = "World",
        [int]$Times = 1
    )
    1..$Times | ForEach-Object { "Hello, $Name!" }
}

Get-Greeting -Name "Alice" -Times 3

# Advanced function (CmdletBinding)
function Invoke-Process {
    [CmdletBinding(SupportsShouldProcess)]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [string]$Path,

        [Parameter()]
        [switch]$Force,

        [ValidateSet("Info","Warning","Error")]
        [string]$Level = "Info"
    )

    begin { Write-Verbose "Starting process" }

    process {
        if ($PSCmdlet.ShouldProcess($Path, "Process")) {
            Write-Verbose "Processing: $Path"
            # do work
        }
    }

    end { Write-Verbose "Done" }
}

# Pipeline input
function Add-One {
    process { $_ + 1 }
}
1, 2, 3 | Add-One   # 2 3 4

# Filter function
filter Get-EvenNumbers { if ($_ % 2 -eq 0) { $_ } }
1..10 | Get-EvenNumbers

# Script blocks
$sq = { param($x) $x * $x }
& $sq 5              # invoke: 25
Invoke-Command -ScriptBlock $sq -ArgumentList 5

# Modules
# Save as MyModule.psm1
function Get-Hello { "Hello!" }
Export-ModuleMember -Function Get-Hello

Import-Module .\MyModule.psm1
Get-Module -ListAvailable
```


---

# CHAPTER 5: OBJECTS AND PIPELINE


## Working with Objects

```powershell
# Everything is an object
$str = "Hello"
$str | Get-Member           # show all methods/properties
$str.GetType()
$str | Get-Member -MemberType Method

# Selecting properties
Get-Process | Select-Object Name, CPU, WorkingSet
Get-Process | Select-Object -First 5
Get-Process | Select-Object -ExpandProperty Name

# Filtering
Get-Process | Where-Object { $_.CPU -gt 100 }
Get-Process | Where-Object CPU -GT 100   # simplified
Get-Service | Where-Object Status -EQ "Running"

# Sorting
Get-Process | Sort-Object CPU -Descending
Get-Process | Sort-Object -Property @{E="CPU"; D=$true}, Name

# Grouping
Get-Process | Group-Object Company
Get-Service | Group-Object Status | Select-Object Name, Count

# Measure
Get-Process | Measure-Object CPU -Sum -Average -Maximum
Get-ChildItem | Measure-Object Length -Sum

# Format
Get-Process | Format-Table Name, CPU, Id -AutoSize
Get-Service | Format-List *
Get-Process | Format-Wide Name -Column 4

# Export
Get-Process | Export-Csv processes.csv -NoTypeInformation
Get-Process | Export-Clixml processes.xml
Get-Process | ConvertTo-Json | Out-File processes.json
Import-Csv data.csv
```


---

# CHAPTER 6: FILE SYSTEM AND I/O


## File Operations

```powershell
# Navigation
Get-Location; Set-Location C:\temp; Push-Location; Pop-Location
Get-ChildItem                    # ls
Get-ChildItem -Recurse -Filter "*.txt"
Get-ChildItem *.ps1 | Select-Object Name, Length, LastWriteTime

# File operations
New-Item -ItemType File "file.txt"
New-Item -ItemType Directory "mydir"
Copy-Item "src.txt" "dst.txt"
Copy-Item "srcdir" "dstdir" -Recurse
Move-Item "old.txt" "new.txt"
Remove-Item "file.txt"
Remove-Item "dir" -Recurse -Force
Rename-Item "old.txt" "new.txt"
Test-Path "file.txt"

# Read/Write
Get-Content "file.txt"                    # array of lines
Get-Content "file.txt" -Raw              # one string
Get-Content "file.txt" -Tail 10          # last 10 lines
Set-Content "file.txt" "Hello, World!"   # overwrite
Add-Content "file.txt" "New line"        # append
Out-File "file.txt" -Encoding utf8       # from pipeline

"line1","line2" | Out-File "file.txt"
Get-Content "file.txt" | Select-String "pattern"

# JSON
$json = Get-Content "data.json" -Raw | ConvertFrom-Json
$json.name
$obj | ConvertTo-Json -Depth 5 | Set-Content "out.json"

# CSV
Import-Csv "data.csv"
Export-Csv "out.csv" -NoTypeInformation

# Path operations
Split-Path "C:\temp\file.txt" -Leaf       # file.txt
Split-Path "C:\temp\file.txt" -Parent     # C:\temp
[System.IO.Path]::GetExtension("file.txt") # .txt
Join-Path "C:\temp" "subdir" "file.txt"
Resolve-Path "."
```


---

# CHAPTER 7: ERROR HANDLING


## Exceptions and Error Handling

```powershell
# Try/Catch/Finally
try {
    $result = 1 / 0
    Get-Item "nonexistent.txt" -ErrorAction Stop
} catch [System.DivideByZeroException] {
    Write-Host "Math error: $_"
} catch [System.IO.FileNotFoundException] {
    Write-Host "File not found: $_"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
    Write-Host "Type: $($_.Exception.GetType().Name)"
} finally {
    Write-Host "Cleanup"
}

# Error handling preferences
$ErrorActionPreference = "Stop"       # Stop on all errors
Get-Item "file.txt" -ErrorAction Stop
Get-Item "file.txt" -ErrorAction SilentlyContinue
Get-Item "file.txt" -ErrorAction Continue   # default

# Check for errors
if (-not (Get-Item "file.txt" -ErrorAction SilentlyContinue)) {
    Write-Host "File not found"
}

# $Error automatic variable
$Error[0]              # last error
$Error.Clear()

# Throw
throw "Custom error message"
throw [System.ArgumentException]::new("Invalid argument")

# Write-Error (non-terminating)
Write-Error "Warning: something went wrong"
```


---

# CHAPTER 8: REMOTING AND JOBS


## Remote Execution and Background Jobs

```powershell
# Background jobs
$job = Start-Job { Get-Process }
$job2 = Start-Job -ScriptBlock { param($n) $n * 2 } -ArgumentList 5

Get-Job
Wait-Job $job
Receive-Job $job -AutoRemoveJob

# Job state
$job.State    # Running, Completed, Failed, Stopped

# Foreach-Object -Parallel (PowerShell 7+)
1..10 | ForEach-Object -Parallel {
    Start-Sleep 1
    "Done: $_"
} -ThrottleLimit 5

# Remoting
Enable-PSRemoting
Invoke-Command -ComputerName Server01 { Get-Service }
$session = New-PSSession -ComputerName Server01
Invoke-Command -Session $session { Get-Process }
Enter-PSSession -ComputerName Server01    # interactive
Remove-PSSession $session

# Scheduled jobs
Register-ScheduledJob -Name "DailyReport" -ScriptBlock { Write-Log "Running" } -Trigger (New-JobTrigger -Daily -At "8am")

# WMI / CIM
Get-CimInstance Win32_OperatingSystem
Get-CimInstance Win32_LogicalDisk | Where-Object DriveType -EQ 3
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine="notepad.exe"}

# Registry
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion"
Set-ItemProperty "HKCU:\SOFTWARE\MyApp" -Name "Setting" -Value "Value"
New-Item "HKCU:\SOFTWARE\MyApp" -Force
```
