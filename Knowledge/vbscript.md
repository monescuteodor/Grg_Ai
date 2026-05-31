# VBScript Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH VBSCRIPT


## Remarks

VBScript (Visual Basic Scripting Edition) is a scripting language modeled on Visual Basic, developed by Microsoft. It is used primarily in Windows Script Host (WSH), Internet Explorer (legacy), and Classic ASP web pages. VBScript is dynamically typed and uses the Variant data type for all variables.

Tools: Windows Script Host (cscript.exe, wscript.exe), Classic ASP, Internet Explorer (legacy).


## Hello World

```vbscript
' hello.vbs
WScript.Echo "Hello, World!"
MsgBox "Hello from VBScript!"

' Run with:
' cscript hello.vbs    (console output)
' wscript hello.vbs    (GUI dialog)
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Variables and Data Types

```vbscript
Option Explicit   ' require variable declarations

' Variable declaration
Dim name
Dim age
Dim pi
Dim flag

' Assignment
name = "Alice"
age = 30
pi = 3.14159
flag = True

' VBScript uses Variant — one type for everything
' VarType() returns subtype
Dim x
x = 42
WScript.Echo VarType(x)       ' 2 (vbInteger or vbLong)
x = "hello"
WScript.Echo VarType(x)       ' 8 (vbString)
x = True
WScript.Echo VarType(x)       ' 11 (vbBoolean)
x = 3.14
WScript.Echo VarType(x)       ' 5 (vbDouble)

' Type constants
' vbEmpty=0, vbNull=1, vbInteger=2, vbLong=3, vbSingle=4
' vbDouble=5, vbString=8, vbBoolean=11, vbDate=7, vbObject=9

' String operations
Dim s
s = "Hello, World!"
WScript.Echo Len(s)           ' 13
WScript.Echo UCase(s)
WScript.Echo LCase(s)
WScript.Echo Left(s, 5)       ' Hello
WScript.Echo Right(s, 6)      ' World!
WScript.Echo Mid(s, 8, 5)     ' World
WScript.Echo InStr(s, "World") ' 8
WScript.Echo Replace(s, "World", "VBScript")
WScript.Echo Trim("  hello  ")
WScript.Echo LTrim("  hello")
WScript.Echo RTrim("hello  ")

' Type conversion
Dim n
n = CInt("42")
n = CDbl("3.14")
n = CStr(42)
n = CBool(1)
n = CDate("2024-01-15")

' Numeric functions
WScript.Echo Abs(-5)
WScript.Echo Int(3.7)     ' 3 (floor)
WScript.Echo Fix(3.7)     ' 3 (truncate toward zero)
WScript.Echo Round(3.567, 2)  ' 3.57
WScript.Echo Sqr(16)      ' 4
WScript.Echo Rnd()        ' random 0..1

' String formatting
WScript.Echo FormatNumber(3.14159, 2)   ' 3.14
WScript.Echo FormatCurrency(9.99)
WScript.Echo FormatDate(Now(), vbShortDate)
```


---

# CHAPTER 3: CONTROL FLOW


## Flow Control

```vbscript
Option Explicit
Dim x, i, day, score

x = 10

' If / ElseIf / Else
If x > 0 Then
    WScript.Echo "positive"
ElseIf x = 0 Then
    WScript.Echo "zero"
Else
    WScript.Echo "negative"
End If

' Single-line If
If x > 0 Then WScript.Echo "pos"

' Select Case
day = "Monday"
Select Case day
    Case "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
        WScript.Echo "Weekday"
    Case "Saturday", "Sunday"
        WScript.Echo "Weekend"
    Case Else
        WScript.Echo "Unknown"
End Select

' Select Case with range (Is keyword)
score = 85
Select Case score
    Case Is >= 90
        WScript.Echo "A"
    Case Is >= 80
        WScript.Echo "B"
    Case Is >= 70
        WScript.Echo "C"
    Case Else
        WScript.Echo "F"
End Select

' For...Next
For i = 1 To 10
    WScript.Echo i
Next

' For...Next with Step
For i = 0 To 10 Step 2
    WScript.Echo i
Next

' For...Next backwards
For i = 10 To 1 Step -1
    WScript.Echo i
Next

' For Each (works on collections and arrays)
Dim arr
arr = Array("apple", "banana", "cherry")
Dim item
For Each item In arr
    WScript.Echo item
Next

' While...Wend
Dim n
n = 1
While n < 100
    n = n * 2
Wend
WScript.Echo n

' Do While...Loop
Dim count
count = 0
Do While count < 5
    count = count + 1
Loop

' Do Until...Loop
Do Until count = 10
    count = count + 1
Loop

' Do...Loop While
Do
    count = count - 1
Loop While count > 5

' Exit For / Exit Do
For i = 1 To 10
    If i = 5 Then Exit For
    WScript.Echo i
Next
```


---

# CHAPTER 4: PROCEDURES AND FUNCTIONS


## Subs and Functions

```vbscript
Option Explicit

' Sub — no return value
Sub Greet(name)
    WScript.Echo "Hello, " & name & "!"
End Sub

' Function — returns value
Function Add(a, b)
    Add = a + b
End Function

Function Max(a, b)
    If a > b Then
        Max = a
    Else
        Max = b
    End If
End Function

' Recursive function
Function Factorial(n)
    If n <= 1 Then
        Factorial = 1
    Else
        Factorial = n * Factorial(n - 1)
    End If
End Function

' ByRef vs ByVal
Sub SwapByRef(ByRef a, ByRef b)
    Dim temp
    temp = a
    a = b
    b = temp
End Sub

Sub NoChangeByVal(ByVal x)
    x = 999  ' original unchanged
End Sub

' Arrays in functions
Function CreateArray()
    Dim arr(4)
    arr(0) = 10
    arr(1) = 20
    arr(2) = 30
    arr(3) = 40
    arr(4) = 50
    CreateArray = arr
End Function

' Main execution
Greet "Alice"
Greet("Bob")

WScript.Echo Add(3, 4)         ' 7
WScript.Echo Max(10, 20)       ' 20
WScript.Echo Factorial(5)      ' 120

Dim x, y
x = 10
y = 20
SwapByRef x, y
WScript.Echo "x=" & x & " y=" & y   ' x=20 y=10

Dim result
result = CreateArray()
WScript.Echo result(2)   ' 30
```


---

# CHAPTER 5: ARRAYS AND STRINGS


## Arrays and String Processing

```vbscript
Option Explicit

' Fixed-size array (0-based by default)
Dim arr(4)     ' 5 elements: arr(0) to arr(4)
arr(0) = "alpha"
arr(1) = "beta"
arr(2) = "gamma"

' Dynamic array
Dim dynArr()
ReDim dynArr(2)
dynArr(0) = 10
dynArr(1) = 20
dynArr(2) = 30

ReDim Preserve dynArr(4)  ' resize, keep existing data
dynArr(3) = 40
dynArr(4) = 50

' Array() function
Dim fruits
fruits = Array("apple", "banana", "cherry", "date")

' UBound / LBound
WScript.Echo UBound(fruits)   ' 3
WScript.Echo LBound(fruits)   ' 0

' Iterate
Dim i
For i = 0 To UBound(fruits)
    WScript.Echo fruits(i)
Next

' Split and Join
Dim csv
csv = "one,two,three,four"
Dim parts
parts = Split(csv, ",")
WScript.Echo parts(0)          ' one
WScript.Echo UBound(parts)     ' 3

Dim rejoined
rejoined = Join(parts, " - ")
WScript.Echo rejoined          ' one - two - three - four

' String functions
Dim s
s = "  Hello, World!  "
WScript.Echo Trim(s)
WScript.Echo Len(Trim(s))      ' 13

' Find and replace
Dim txt
txt = "The quick brown fox"
WScript.Echo InStr(txt, "quick")      ' 5
WScript.Echo Replace(txt, "quick", "slow")

' String builder pattern (concatenation)
Dim result
result = ""
For i = 1 To 5
    result = result & "Line " & i & vbCrLf
Next
WScript.Echo result

' Date/time
WScript.Echo Now()             ' current date and time
WScript.Echo Date()            ' current date
WScript.Echo Time()            ' current time
WScript.Echo Year(Now())
WScript.Echo Month(Now())
WScript.Echo Day(Now())
WScript.Echo DateDiff("d", "2024-01-01", Now())  ' days since
```


---

# CHAPTER 6: OBJECTS AND FILE SYSTEM


## COM Objects and File I/O

```vbscript
Option Explicit

' FileSystemObject
Dim fso
Set fso = CreateObject("Scripting.FileSystemObject")

' Write to file
Dim ts
Set ts = fso.CreateTextFile("test.txt", True)
ts.WriteLine "Hello, World!"
ts.WriteLine "Line 2"
ts.Close

' Read from file
Set ts = fso.OpenTextFile("test.txt", 1)  ' 1=ForReading
Dim line
Do While Not ts.AtEndOfStream
    line = ts.ReadLine()
    WScript.Echo line
Loop
ts.Close

' Append to file
Set ts = fso.OpenTextFile("test.txt", 8, True)  ' 8=ForAppending
ts.WriteLine "Appended line"
ts.Close

' File/Directory operations
If fso.FileExists("test.txt") Then
    WScript.Echo "File exists, size: " & fso.GetFile("test.txt").Size
End If

If Not fso.FolderExists("mydir") Then
    fso.CreateFolder "mydir"
End If

fso.CopyFile "test.txt", "test_copy.txt"
fso.MoveFile "test_copy.txt", "mydir\test_copy.txt"
fso.DeleteFile "test.txt"

' Path operations
WScript.Echo fso.GetFileName("C:\Users\Alice\file.txt")   ' file.txt
WScript.Echo fso.GetParentFolderName("C:\Users\Alice\file.txt")
WScript.Echo fso.GetExtensionName("file.txt")   ' txt

' WScript object
WScript.Echo WScript.ScriptName   ' script filename
WScript.Echo WScript.ScriptFullName
WScript.Sleep 1000  ' pause 1 second

' Shell object
Dim shell
Set shell = CreateObject("WScript.Shell")
shell.Run "notepad.exe", 1, False   ' open notepad
WScript.Echo shell.ExpandEnvironmentStrings("%USERPROFILE%")

' Registry access
shell.RegWrite "HKCU\SOFTWARE\MyApp\Setting", "Value", "REG_SZ"
Dim regVal
regVal = shell.RegRead("HKCU\SOFTWARE\MyApp\Setting")
WScript.Echo regVal
shell.RegDelete "HKCU\SOFTWARE\MyApp\Setting"
```


---

# CHAPTER 7: ERROR HANDLING


## Error Handling

```vbscript
Option Explicit

' On Error Resume Next — suppress errors, check Err object
On Error Resume Next

Dim x
x = 1 / 0

If Err.Number <> 0 Then
    WScript.Echo "Error " & Err.Number & ": " & Err.Description
    Err.Clear
End If

' On Error GoTo 0 — re-enable normal error handling
On Error GoTo 0

' Error handling pattern
Sub SafeDivide(a, b)
    On Error Resume Next
    Dim result
    result = a / b
    If Err.Number <> 0 Then
        WScript.Echo "Division error: " & Err.Description
        Err.Clear
        result = 0
    End If
    WScript.Echo "Result: " & result
End Sub

SafeDivide 10, 2    ' Result: 5
SafeDivide 10, 0    ' Division error: ...

' Custom error raising
Sub ValidateAge(age)
    On Error Resume Next
    If age < 0 Or age > 150 Then
        Err.Raise 1001, "ValidateAge", "Age must be between 0 and 150"
    End If
    If Err.Number <> 0 Then
        WScript.Echo "Validation error: " & Err.Description
        Err.Clear
    End If
End Sub

ValidateAge 25
ValidateAge -5

' Err object properties
' Err.Number     — error code (0 = no error)
' Err.Description — error message
' Err.Source     — source of error
' Err.Clear      — reset error
' Err.Raise      — raise custom error

' Classic ASP-style error handling
Sub ProcessData(data)
    On Error Resume Next

    ' Attempt operation
    Dim result
    result = CInt(data)

    If Err.Number = 13 Then   ' Type mismatch
        WScript.Echo "Invalid data: not a number"
        Err.Clear
    ElseIf Err.Number <> 0 Then
        WScript.Echo "Unexpected error: " & Err.Number
        Err.Clear
    Else
        WScript.Echo "Data: " & result * 2
    End If
End Sub

ProcessData "42"
ProcessData "hello"
```


---

# CHAPTER 8: WSCRIPT AND AUTOMATION


## Windows Automation

```vbscript
Option Explicit

' WScript.Arguments — command line arguments
Dim args
Set args = WScript.Arguments

If args.Count > 0 Then
    WScript.Echo "Arg 0: " & args(0)
End If

' Named arguments (/name:value)
If args.Named.Exists("output") Then
    WScript.Echo "Output: " & args.Named("output")
End If

' WshShell — run programs, access registry, environment
Dim shell
Set shell = CreateObject("WScript.Shell")

' Run synchronously (wait = True)
Dim exitCode
exitCode = shell.Run("cmd /c dir", 0, True)
WScript.Echo "Exit code: " & exitCode

' Environment variables
Dim env
Set env = shell.Environment("PROCESS")
WScript.Echo env("PATH")
WScript.Echo env("USERPROFILE")
WScript.Echo env("COMPUTERNAME")

' Popup (with timeout)
' Returns: 1=OK, 2=Cancel, 6=Yes, 7=No, -1=Timeout
Dim response
response = shell.Popup("Proceed?", 10, "Confirm", 4 + 32)
' 4=YesNo buttons, 32=Question icon

' SendKeys
shell.Run "notepad.exe", 1, False
WScript.Sleep 1000
shell.AppActivate "Notepad"
shell.SendKeys "Hello from VBScript{ENTER}"
WScript.Sleep 500
shell.SendKeys "%{F4}"  ' Alt+F4

' ADODB (database)
Dim conn
Set conn = CreateObject("ADODB.Connection")
conn.Open "Provider=Microsoft.Jet.OLEDB.4.0;Data Source=mydb.mdb"

Dim rs
Set rs = CreateObject("ADODB.Recordset")
rs.Open "SELECT * FROM Users", conn
Do While Not rs.EOF
    WScript.Echo rs.Fields("Name").Value
    rs.MoveNext
Loop
rs.Close
conn.Close

' Network object
Dim net
Set net = CreateObject("WScript.Network")
WScript.Echo net.ComputerName
WScript.Echo net.UserName
WScript.Echo net.UserDomain

' Map network drive
net.MapNetworkDrive "Z:", "\\server\share"
net.RemoveNetworkDrive "Z:"

' Cleanup
Set shell = Nothing
Set net = Nothing
```
