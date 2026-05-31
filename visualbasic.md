# Visual Basic Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH VISUAL BASIC


## Remarks

Visual Basic (VB.NET) is a type-safe, object-oriented language on the .NET platform. It features natural English-like syntax, strong IDE integration with Visual Studio, and full access to the .NET ecosystem. VB.NET and C# are largely interchangeable on .NET.

Tools: Visual Studio, dotnet CLI, Visual Studio Code with VB extension.


## Hello World

```vb
' HelloWorld.vb
Module Program
    Sub Main(args As String())
        Console.WriteLine("Hello, World!")
        Console.WriteLine("Hello, {0}!", "Visual Basic")
    End Sub
End Module
```

```bash
dotnet new console --language VB -o HelloApp
cd HelloApp
dotnet run
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Variables and Data Types

```vb
Module TypesDemo
    Sub Main()
        ' Basic types
        Dim name As String = "Alice"
        Dim age As Integer = 30
        Dim pi As Double = 3.14159
        Dim flag As Boolean = True
        Dim ch As Char = "A"c
        Dim big As Long = 9_000_000_000L
        Dim dec As Decimal = 19.99D
        Dim single_ As Single = 3.14F

        ' Type inference with Dim ... = ...
        Dim inferred = "inferred string"   ' String
        Dim inferredNum = 42               ' Integer

        ' Nothing (null equivalent)
        Dim obj As Object = Nothing

        ' Nullable types
        Dim nullInt As Integer? = Nothing
        If nullInt.HasValue Then
            Console.WriteLine(nullInt.Value)
        End If

        ' Constants
        Const MaxItems As Integer = 100
        Const Pi As Double = 3.14159

        ' String operations
        Dim s As String = "Hello, World!"
        Console.WriteLine(s.Length)         ' 13
        Console.WriteLine(s.ToUpper())
        Console.WriteLine(s.ToLower())
        Console.WriteLine(s.Substring(0, 5))  ' Hello
        Console.WriteLine(s.Contains("World"))
        Console.WriteLine(s.Replace("World", "VB"))
        Console.WriteLine(s.Trim())
        Console.WriteLine(s.Split(",").Length)

        ' String interpolation
        Dim greeting = $"Hello, {name}! You are {age} years old."
        Console.WriteLine(greeting)

        ' Type conversions
        Dim n As Integer = CInt("42")
        Dim d As Double = CDbl("3.14")
        Dim str As String = CStr(42)
        Dim bool_ As Boolean = CBool(1)

        ' Integer.Parse / TryParse
        Dim parsed As Integer
        If Integer.TryParse("123", parsed) Then
            Console.WriteLine(parsed)
        End If
    End Sub
End Module
```


---

# CHAPTER 3: CONTROL FLOW


## Flow Control

```vb
Module ControlFlow
    Sub Main()
        Dim x As Integer = 10

        ' If / ElseIf / Else
        If x > 0 Then
            Console.WriteLine("positive")
        ElseIf x = 0 Then
            Console.WriteLine("zero")
        Else
            Console.WriteLine("negative")
        End If

        ' Single-line If
        If x > 0 Then Console.WriteLine("pos")

        ' IIf (inline if — always evaluates both)
        Dim label = IIf(x > 0, "positive", "non-positive")

        ' Select Case
        Dim day = "Monday"
        Select Case day
            Case "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
                Console.WriteLine("Weekday")
            Case "Saturday", "Sunday"
                Console.WriteLine("Weekend")
            Case Else
                Console.WriteLine("Unknown")
        End Select

        ' Select Case with ranges
        Dim score = 85
        Select Case score
            Case 90 To 100
                Console.WriteLine("A")
            Case 80 To 89
                Console.WriteLine("B")
            Case 70 To 79
                Console.WriteLine("C")
            Case Else
                Console.WriteLine("F")
        End Select

        ' For...Next
        For i As Integer = 1 To 10
            Console.Write(i & " ")
        Next
        Console.WriteLine()

        ' For...Next with Step
        For i As Integer = 0 To 10 Step 2
            Console.Write(i & " ")
        Next

        ' For Each
        Dim fruits() = {"apple", "banana", "cherry"}
        For Each fruit In fruits
            Console.WriteLine(fruit)
        Next

        ' While
        Dim n = 1
        While n < 100
            n *= 2
        End While

        ' Do...Loop
        Dim count = 0
        Do While count < 5
            count += 1
        Loop

        Do Until count = 10
            count += 1
        Loop

        Do
            count -= 1
        Loop While count > 5

        ' Exit and Continue
        For i As Integer = 1 To 10
            If i = 5 Then Exit For
            If i Mod 2 = 0 Then Continue For
            Console.Write(i & " ")
        Next
    End Sub
End Module
```


---

# CHAPTER 4: ARRAYS AND COLLECTIONS


## Arrays and Collections

```vb
Imports System.Collections.Generic

Module CollectionsDemo
    Sub Main()
        ' Array declaration
        Dim arr(4) As Integer        ' 5 elements (0..4)
        Dim arr2() As Integer = {1, 2, 3, 4, 5}
        Dim matrix(,) As Integer = {{1, 2}, {3, 4}, {5, 6}}

        ' Array operations
        arr2(0) = 10
        Console.WriteLine(arr2.Length)     ' 5
        Console.WriteLine(arr2(arr2.Length - 1))  ' last element
        Array.Sort(arr2)
        Array.Reverse(arr2)

        ' Multi-dimensional
        Console.WriteLine(matrix(1, 0))   ' 3
        Console.WriteLine(matrix.GetLength(0))  ' rows: 3
        Console.WriteLine(matrix.GetLength(1))  ' cols: 2

        ' Jagged array
        Dim jagged()() As Integer = {
            New Integer() {1, 2},
            New Integer() {3, 4, 5},
            New Integer() {6}
        }

        ' List(Of T)
        Dim list As New List(Of String)
        list.Add("Alice")
        list.Add("Bob")
        list.Add("Carol")
        list.Remove("Bob")
        list.Insert(0, "Zero")
        Console.WriteLine(list.Count)
        Console.WriteLine(list.Contains("Alice"))
        list.Sort()

        For Each item In list
            Console.WriteLine(item)
        Next

        ' Dictionary(Of K, V)
        Dim dict As New Dictionary(Of String, Integer)
        dict("Alice") = 30
        dict("Bob") = 25
        dict.Add("Carol", 35)
        dict.Remove("Bob")

        If dict.ContainsKey("Alice") Then
            Console.WriteLine(dict("Alice"))
        End If

        For Each kvp In dict
            Console.WriteLine($"{kvp.Key}: {kvp.Value}")
        Next

        ' HashSet(Of T)
        Dim set_ As New HashSet(Of Integer)
        set_.Add(1) : set_.Add(2) : set_.Add(3) : set_.Add(2)
        Console.WriteLine(set_.Count)  ' 3

        ' Queue and Stack
        Dim queue As New Queue(Of String)
        queue.Enqueue("first")
        queue.Enqueue("second")
        Console.WriteLine(queue.Dequeue())  ' first

        Dim stack As New Stack(Of Integer)
        stack.Push(1) : stack.Push(2) : stack.Push(3)
        Console.WriteLine(stack.Pop())  ' 3
    End Sub
End Module
```


---

# CHAPTER 5: PROCEDURES AND FUNCTIONS


## Subs and Functions

```vb
Module ProcedureDemo

    ' Sub — no return value
    Sub Greet(name As String, Optional greeting As String = "Hello")
        Console.WriteLine($"{greeting}, {name}!")
    End Sub

    ' Function — returns value
    Function Add(a As Integer, b As Integer) As Integer
        Return a + b
    End Function

    ' ByRef (pass by reference)
    Sub Swap(ByRef a As Integer, ByRef b As Integer)
        Dim temp = a
        a = b
        b = temp
    End Sub

    ' Params (variable arguments)
    Function Sum(ParamArray nums() As Integer) As Integer
        Dim total = 0
        For Each n In nums
            total += n
        Next
        Return total
    End Function

    ' Function overloading
    Function Max(a As Integer, b As Integer) As Integer
        Return If(a > b, a, b)
    End Function

    Function Max(a As Double, b As Double) As Double
        Return If(a > b, a, b)
    End Function

    ' Lambda expressions
    Dim square As Func(Of Integer, Integer) = Function(x) x * x
    Dim isEven As Func(Of Integer, Boolean) = Function(x) x Mod 2 = 0
    Dim greetLambda As Action(Of String) = Sub(name) Console.WriteLine($"Hi {name}")

    Sub Main()
        Greet("Alice")
        Greet("Bob", "Hi")

        Console.WriteLine(Add(3, 4))   ' 7

        Dim x = 10, y = 20
        Swap(x, y)
        Console.WriteLine($"x={x}, y={y}")   ' x=20, y=10

        Console.WriteLine(Sum(1, 2, 3, 4, 5))  ' 15

        ' Lambda usage
        Console.WriteLine(square(5))    ' 25
        Console.WriteLine(isEven(4))    ' True
        greetLambda("Carol")

        ' LINQ with lambdas
        Dim numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
        Dim evens = numbers.Where(Function(n) n Mod 2 = 0).ToArray()
        Dim doubled = numbers.Select(Function(n) n * 2).ToArray()
        Dim total = numbers.Sum()
        Console.WriteLine($"Evens: {String.Join(", ", evens)}")
    End Sub

End Module
```


---

# CHAPTER 6: OBJECT-ORIENTED PROGRAMMING


## Classes and Inheritance

```vb
' Animal.vb
Public Class Animal
    Private _name As String
    Private _sound As String

    Public Property Name As String
        Get
            Return _name
        End Get
        Set(value As String)
            _name = value
        End Set
    End Property

    Public Property Age As Integer

    Public ReadOnly Property IsAdult As Boolean
        Get
            Return Age >= 1
        End Get
    End Property

    Public Sub New(name As String, sound As String)
        _name = name
        _sound = sound
    End Sub

    Public Overridable Function Speak() As String
        Return $"{_name} says {_sound}"
    End Function

    Public Overrides Function ToString() As String
        Return $"Animal({_name})"
    End Function
End Class

Public Class Dog
    Inherits Animal

    Public Property Breed As String

    Public Sub New(name As String, breed As String)
        MyBase.New(name, "Woof")
        Breed = breed
    End Sub

    Public Overrides Function Speak() As String
        Return MyBase.Speak() & "!"
    End Function

    Public Function Fetch() As String
        Return $"{Name} fetches!"
    End Function
End Class

' Interface
Public Interface IPrintable
    Sub PrintDescription()
    Function PrettyDescription() As String
End Interface

' MustInherit (abstract)
Public MustInherit Class Shape
    Public MustOverride ReadOnly Property Area As Double
    Public MustOverride ReadOnly Property Perimeter As Double

    Public Sub PrintInfo()
        Console.WriteLine($"Area: {Area:F2}, Perimeter: {Perimeter:F2}")
    End Sub
End Class

Public Class Circle
    Inherits Shape
    Private _radius As Double

    Public Sub New(radius As Double)
        _radius = radius
    End Sub

    Public Overrides ReadOnly Property Area As Double
        Get
            Return Math.PI * _radius * _radius
        End Get
    End Property

    Public Overrides ReadOnly Property Perimeter As Double
        Get
            Return 2 * Math.PI * _radius
        End Get
    End Property
End Class

Module OOPDemo
    Sub Main()
        Dim dog As New Dog("Rex", "Labrador")
        Console.WriteLine(dog.Speak())   ' Rex says Woof!
        Console.WriteLine(dog.Fetch())

        Dim c As New Circle(5.0)
        c.PrintInfo()

        ' Polymorphism
        Dim animals As Animal() = {
            New Animal("Cat", "Meow"),
            New Dog("Rex", "Lab")
        }
        For Each a In animals
            Console.WriteLine(a.Speak())
        Next
    End Sub
End Module
```


---

# CHAPTER 7: ERROR HANDLING AND FILE I/O


## Exceptions and Files

```vb
Imports System.IO

Module ErrorAndIO
    Sub Main()
        ' Try/Catch/Finally
        Try
            Dim result = 10 / 0
        Catch ex As DivideByZeroException
            Console.WriteLine($"Math error: {ex.Message}")
        Catch ex As Exception
            Console.WriteLine($"Error: {ex.Message}")
        Finally
            Console.WriteLine("Cleanup always runs")
        End Try

        ' Custom exception
        Try
            Throw New ArgumentException("Invalid argument", "paramName")
        Catch ex As ArgumentException
            Console.WriteLine($"{ex.Message}, Param: {ex.ParamName}")
        End Try

        ' File operations
        Dim path = "test.txt"

        ' Write to file
        File.WriteAllText(path, "Hello, World!" & Environment.NewLine)
        File.AppendAllText(path, "Second line" & Environment.NewLine)

        ' Read file
        Dim content = File.ReadAllText(path)
        Console.WriteLine(content)

        Dim lines() = File.ReadAllLines(path)
        For Each line In lines
            Console.WriteLine(line)
        Next

        ' StreamReader/Writer
        Using writer As New StreamWriter(path, append:=True)
            writer.WriteLine("StreamWriter line")
        End Using

        Using reader As New StreamReader(path)
            Dim line = reader.ReadLine()
            While line IsNot Nothing
                Console.WriteLine(line)
                line = reader.ReadLine()
            End While
        End Using

        ' File/Directory checks
        If File.Exists(path) Then
            Console.WriteLine($"File size: {New FileInfo(path).Length} bytes")
        End If

        If Not Directory.Exists("mydir") Then
            Directory.CreateDirectory("mydir")
        End If

        ' Cleanup
        File.Delete(path)

        ' Path operations
        Dim fullPath = Path.Combine("C:\Users", "Alice", "file.txt")
        Console.WriteLine(Path.GetFileName(fullPath))    ' file.txt
        Console.WriteLine(Path.GetExtension(fullPath))   ' .txt
        Console.WriteLine(Path.GetDirectoryName(fullPath))
    End Sub
End Module
```


---

# CHAPTER 8: LINQ AND ADVANCED FEATURES


## LINQ and Modern VB

```vb
Imports System.Linq

Module AdvancedDemo
    Class Person
        Public Property Name As String
        Public Property Age As Integer
        Public Property City As String
    End Class

    Sub Main()
        Dim people As New List(Of Person) From {
            New Person With {.Name = "Alice", .Age = 30, .City = "NYC"},
            New Person With {.Name = "Bob",   .Age = 25, .City = "LA"},
            New Person With {.Name = "Carol", .Age = 35, .City = "NYC"},
            New Person With {.Name = "Dave",  .Age = 28, .City = "Chicago"}
        }

        ' LINQ Query Syntax
        Dim nycPeople = From p In people
                        Where p.City = "NYC"
                        Order By p.Age
                        Select p.Name

        For Each name In nycPeople
            Console.WriteLine(name)
        Next

        ' LINQ Method Syntax
        Dim avgAge = people.Average(Function(p) p.Age)
        Dim oldest = people.OrderByDescending(Function(p) p.Age).First()
        Dim grouped = people.GroupBy(Function(p) p.City)

        Console.WriteLine($"Average age: {avgAge}")
        Console.WriteLine($"Oldest: {oldest.Name}")

        For Each group In grouped
            Console.WriteLine($"City: {group.Key}")
            For Each p In group
                Console.WriteLine($"  {p.Name}")
            Next
        Next

        ' LINQ on arrays
        Dim numbers = Enumerable.Range(1, 20).ToArray()
        Dim evens = numbers.Where(Function(n) n Mod 2 = 0)
        Dim sum = numbers.Sum()
        Dim top5 = numbers.OrderByDescending(Function(n) n).Take(5)

        ' Anonymous types
        Dim nameAge = From p In people
                      Select New With {p.Name, p.Age}

        ' String operations with LINQ
        Dim words = "Hello World Foo Bar".Split(" ")
        Dim long_words = words.Where(Function(w) w.Length > 3).ToArray()
        Console.WriteLine(String.Join(", ", long_words))

        ' Attributes (similar to C# attributes)
        ' Using With initializer
        Dim p1 As New Person With {.Name = "Eve", .Age = 22, .City = "NYC"}

        ' Tuple (ValueTuple)
        Dim t As (Integer, String) = (42, "hello")
        Console.WriteLine(t.Item1)
        Console.WriteLine(t.Item2)

        Dim named = (Count:=5, Name:="Alice")
        Console.WriteLine(named.Count)
        Console.WriteLine(named.Name)
    End Sub

End Module
```
