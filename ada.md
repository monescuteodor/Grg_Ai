# Ada Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH ADA


## Remarks

Ada is a statically-typed, structured, high-level programming language designed for safety-critical and real-time systems. It is standardized by ISO (Ada 83, 95, 2005, 2012, 2022). Ada is used in aerospace, defense, air traffic control, and medical devices. Ada 2012 introduced Design by Contract.

Tools: GNAT (GNU Ada Translator, part of GCC), GPS/GNAT Studio IDE, Alire (package manager).


## Hello World

```ada
-- hello.adb
with Ada.Text_IO;

procedure Hello is
begin
   Ada.Text_IO.Put_Line ("Hello, World!");
   Ada.Text_IO.Put_Line ("Hello, Ada!");
end Hello;
```

```bash
gnatmake hello.adb && ./hello
# Or with Alire:
# alr build && alr run
```


---

# CHAPTER 2: TYPES AND VARIABLES


## Type System

```ada
with Ada.Text_IO;
with Ada.Integer_Text_IO;
with Ada.Float_Text_IO;

procedure Types_Demo is
   -- Declarations must precede statements in a block

   -- Integer types
   X : Integer := 42;
   Y : Long_Integer := 1_000_000_000;
   Z : Short_Integer := 32767;

   -- Floating point
   F : Float := 3.14;
   D : Long_Float := 3.14159265358979;

   -- Boolean
   B : Boolean := True;

   -- Character and String
   C : Character := 'A';
   S : String := "Hello, World!";
   S2 : String (1 .. 5) := "Hello";   -- fixed length

   -- User-defined integer type
   type Age_Type is range 0 .. 150;
   type Percentage is range 0 .. 100;

   Age : Age_Type := 30;
   Pct : Percentage := 75;

   -- Enumeration
   type Day is (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday);
   Today : Day := Monday;

   -- Subtypes
   subtype Weekday is Day range Monday .. Friday;
   subtype Natural is Integer range 0 .. Integer'Last;
   subtype Positive is Integer range 1 .. Integer'Last;

   -- Constants
   Pi : constant Float := 3.14159;
   Max_Size : constant Integer := 100;

begin
   Ada.Text_IO.Put_Line ("X = " & Integer'Image (X));
   Ada.Text_IO.Put_Line ("F = " & Float'Image (F));
   Ada.Text_IO.Put_Line ("B = " & Boolean'Image (B));
   Ada.Text_IO.Put_Line ("C = " & C);
   Ada.Text_IO.Put_Line (S);

   -- Type attributes
   Ada.Text_IO.Put_Line (Integer'Image (Integer'First));
   Ada.Text_IO.Put_Line (Integer'Image (Integer'Last));
   Ada.Text_IO.Put_Line (Integer'Image (Integer'Size));  -- bits

   -- Enum attributes
   Ada.Text_IO.Put_Line (Day'Image (Today));
   Ada.Text_IO.Put_Line (Day'Image (Day'First));   -- Monday
   Ada.Text_IO.Put_Line (Day'Image (Day'Last));    -- Sunday
   Ada.Text_IO.Put_Line (Integer'Image (Day'Pos (Wednesday)));  -- 2
   Ada.Text_IO.Put_Line (Day'Image (Day'Val (4)));  -- Friday

end Types_Demo;
```


---

# CHAPTER 3: CONTROL FLOW


## Control Structures

```ada
with Ada.Text_IO;
use Ada.Text_IO;

procedure Control_Demo is
   X : Integer := 10;
   I : Integer;
   N : Integer := 1;
begin
   -- if/elsif/else
   if X > 0 then
      Put_Line ("positive");
   elsif X = 0 then
      Put_Line ("zero");
   else
      Put_Line ("negative");
   end if;

   -- case statement (all values must be covered)
   case X is
      when 0 =>
         Put_Line ("zero");
      when 1 .. 9 =>
         Put_Line ("single digit");
      when 10 | 20 | 30 =>
         Put_Line ("ten, twenty, or thirty");
      when others =>
         Put_Line ("something else");
   end case;

   -- for loop (range)
   for I in 1 .. 10 loop
      Put (Integer'Image (I) & " ");
   end loop;
   New_Line;

   -- for loop (reverse)
   for I in reverse 1 .. 10 loop
      Put (Integer'Image (I) & " ");
   end loop;
   New_Line;

   -- for loop over array
   declare
      Arr : array (1 .. 5) of Integer := (10, 20, 30, 40, 50);
   begin
      for Item of Arr loop          -- Ada 2012 for-of
         Put (Integer'Image (Item) & " ");
      end loop;
      New_Line;
   end;

   -- while loop
   while N < 100 loop
      N := N * 2;
   end loop;
   Put_Line ("N = " & Integer'Image (N));

   -- infinite loop with exit
   loop
      N := N - 1;
      exit when N < 50;
   end loop;

   -- Nested loop with exit (labeled)
   Outer : for I in 1 .. 5 loop
      Inner : for J in 1 .. 5 loop
         exit Outer when I * J > 15;
         Put (Integer'Image (I) & "," & Integer'Image (J) & " ");
      end loop Inner;
   end loop Outer;
   New_Line;

end Control_Demo;
```


---

# CHAPTER 4: SUBPROGRAMS AND PACKAGES


## Procedures, Functions, and Packages

```ada
-- Math_Utils package specification
package Math_Utils is
   function Factorial (N : Natural) return Natural;
   function Gcd (A, B : Positive) return Positive;
   function Power (Base : Float; Exp : Natural) return Float;
   procedure Swap (A, B : in out Integer);
end Math_Utils;

-- Math_Utils package body
package body Math_Utils is

   function Factorial (N : Natural) return Natural is
   begin
      if N <= 1 then
         return 1;
      else
         return N * Factorial (N - 1);
      end if;
   end Factorial;

   function Gcd (A, B : Positive) return Positive is
   begin
      if B = 0 then
         return A;
      else
         return Gcd (B, A mod B);
      end if;
   end Gcd;

   function Power (Base : Float; Exp : Natural) return Float is
      Result : Float := 1.0;
   begin
      for I in 1 .. Exp loop
         Result := Result * Base;
      end loop;
      return Result;
   end Power;

   procedure Swap (A, B : in out Integer) is
      Temp : Integer := A;
   begin
      A := B;
      B := Temp;
   end Swap;

end Math_Utils;

-- Usage
with Ada.Text_IO;
with Math_Utils;

procedure Main is
   use Ada.Text_IO;
   X : Integer := 10;
   Y : Integer := 20;
begin
   Put_Line (Natural'Image (Math_Utils.Factorial (10)));
   Put_Line (Positive'Image (Math_Utils.Gcd (48, 18)));
   Math_Utils.Swap (X, Y);
   Put_Line ("X=" & Integer'Image (X) & " Y=" & Integer'Image (Y));
end Main;
```


---

# CHAPTER 5: ARRAYS AND RECORDS


## Composite Types

```ada
with Ada.Text_IO;
use Ada.Text_IO;

procedure Composites is

   -- Arrays
   type Int_Array is array (1 .. 10) of Integer;
   type Matrix is array (1 .. 3, 1 .. 3) of Float;
   type Unbounded_Array is array (Positive range <>) of Integer;

   Arr : Int_Array := (1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
   M   : Matrix;
   Vec : Unbounded_Array (1 .. 5) := (others => 0);

   -- Array operations
   Sum : Integer := 0;

   -- Records
   type Person is record
      Name : String (1 .. 20);
      Age  : Natural;
      Score : Float;
   end record;

   -- Record with default values
   type Config is record
      Host    : String (1 .. 50) := (others => ' ');
      Port    : Natural := 8080;
      Debug   : Boolean := False;
   end record;

   Alice : Person := (Name => "Alice               ",
                      Age  => 30,
                      Score => 95.5);

   Cfg : Config;

   -- Variant record (discriminated union)
   type Shape_Kind is (Circle, Rectangle);
   type Shape (Kind : Shape_Kind) is record
      case Kind is
         when Circle =>
            Radius : Float;
         when Rectangle =>
            Width, Height : Float;
      end case;
   end record;

   C : Shape := (Kind => Circle, Radius => 5.0);
   R : Shape := (Kind => Rectangle, Width => 4.0, Height => 6.0);

begin
   -- Array access
   Put_Line (Integer'Image (Arr (1)));   -- first element
   Put_Line (Integer'Image (Arr (Arr'Last)));  -- last element
   Put_Line (Integer'Image (Arr'Length));  -- 10

   -- Array slice
   for I in 2 .. 4 loop
      Put (Integer'Image (Arr (I)) & " ");
   end loop;
   New_Line;

   -- Aggregate
   Arr := (1, 2, 3, others => 0);
   M := (others => (others => 0.0));

   -- Record access
   Put_Line (Alice.Name);
   Put_Line (Natural'Image (Alice.Age));

   -- Variant record
   case C.Kind is
      when Circle =>
         Put_Line ("Circle r=" & Float'Image (C.Radius));
      when Rectangle =>
         Put_Line ("Rectangle " & Float'Image (R.Width) &
                   "x" & Float'Image (R.Height));
   end case;

end Composites;
```


---

# CHAPTER 6: OBJECT-ORIENTED PROGRAMMING


## Tagged Types and Inheritance

```ada
-- animal.ads (specification)
package Animals is

   -- Tagged type (base class)
   type Animal is tagged record
      Name  : String (1 .. 20);
      Sound : String (1 .. 20);
      Age   : Natural := 0;
   end record;

   -- Primitive operations (methods)
   function Speak (A : Animal) return String;
   procedure Birthday (A : in out Animal);
   function Is_Adult (A : Animal) return Boolean;
   procedure Print_Info (A : Animal);

   -- Derived type (inheritance)
   type Dog is new Animal with record
      Breed : String (1 .. 30);
   end record;

   overriding function Speak (D : Dog) return String;
   function Fetch (D : Dog) return String;

   -- Abstract type
   type Shape is abstract tagged null record;
   function Area (S : Shape) return Float is abstract;
   function Perimeter (S : Shape) return Float is abstract;

   type Circle is new Shape with record
      Radius : Float;
   end record;

   overriding function Area (C : Circle) return Float;
   overriding function Perimeter (C : Circle) return Float;

end Animals;

-- animal.adb (body)
package body Animals is

   function Speak (A : Animal) return String is
   begin
      return A.Name (1 .. 5) & " says " & A.Sound (1 .. 4);
   end Speak;

   procedure Birthday (A : in out Animal) is
   begin
      A.Age := A.Age + 1;
   end Birthday;

   function Is_Adult (A : Animal) return Boolean is
   begin
      return A.Age >= 1;
   end Is_Adult;

   overriding function Speak (D : Dog) return String is
   begin
      return Speak (Animal (D)) & "!";   -- call parent
   end Speak;

   function Fetch (D : Dog) return String is
   begin
      return D.Name (1 .. 3) & " fetches!";
   end Fetch;

   overriding function Area (C : Circle) return Float is
   begin
      return 3.14159 * C.Radius ** 2;
   end Area;

   overriding function Perimeter (C : Circle) return Float is
   begin
      return 2.0 * 3.14159 * C.Radius;
   end Perimeter;

end Animals;
```


---

# CHAPTER 7: EXCEPTION HANDLING


## Exceptions

```ada
with Ada.Text_IO;
use Ada.Text_IO;
with Ada.Exceptions;

procedure Exception_Demo is

   -- Define custom exceptions
   Validation_Error : exception;
   Connection_Error : exception;

   procedure Validate_Age (Age : Integer) is
   begin
      if Age < 0 or Age > 150 then
         raise Validation_Error with
               "Age must be between 0 and 150, got: " & Integer'Image (Age);
      end if;
   end Validate_Age;

   function Safe_Divide (X, Y : Integer) return Integer is
   begin
      if Y = 0 then
         raise Constraint_Error with "Division by zero";
      end if;
      return X / Y;
   end Safe_Divide;

begin
   -- Basic exception handling
   begin
      Validate_Age (-5);
   exception
      when Validation_Error =>
         Put_Line ("Caught validation error");
      when Constraint_Error =>
         Put_Line ("Caught constraint error");
   end;

   -- With exception information
   begin
      Validate_Age (200);
   exception
      when E : Validation_Error =>
         Put_Line ("Error: " & Ada.Exceptions.Exception_Message (E));
         Put_Line ("Name: " & Ada.Exceptions.Exception_Name (E));
   end;

   -- Reraise
   begin
      begin
         raise Connection_Error with "Server unreachable";
      exception
         when Connection_Error =>
            Put_Line ("Logging connection error...");
            raise;   -- reraise
      end;
   exception
      when E : others =>
         Put_Line ("Outer: " & Ada.Exceptions.Exception_Message (E));
   end;

   -- Predefined exceptions
   -- Constraint_Error: type range, array bounds, null access
   -- Program_Error: logic errors (uninitialized, wrong mode)
   -- Storage_Error: out of memory
   -- Tasking_Error: task errors

end Exception_Demo;
```


---

# CHAPTER 8: TASKING AND CONCURRENCY


## Ada Tasking

```ada
with Ada.Text_IO;
use Ada.Text_IO;

procedure Tasking_Demo is

   -- Task type
   task type Worker is
      entry Start (ID : Positive);
      entry Get_Result (R : out Integer);
   end Worker;

   task body Worker is
      Worker_ID : Positive;
      Result    : Integer := 0;
   begin
      accept Start (ID : Positive) do
         Worker_ID := ID;
      end Start;

      -- Do work
      for I in 1 .. 100 loop
         Result := Result + I;
      end loop;

      Put_Line ("Worker " & Positive'Image (Worker_ID) & " done.");

      accept Get_Result (R : out Integer) do
         R := Result;
      end Get_Result;
   end Worker;

   W1, W2 : Worker;
   R1, R2 : Integer;

   -- Protected type (synchronized data)
   protected type Counter is
      procedure Increment;
      function Value return Natural;
   private
      Count : Natural := 0;
   end Counter;

   protected body Counter is
      procedure Increment is
      begin
         Count := Count + 1;
      end Increment;

      function Value return Natural is
      begin
         return Count;
      end Value;
   end Counter;

   Shared_Counter : Counter;

begin
   -- Start workers
   W1.Start (1);
   W2.Start (2);

   -- Get results (rendezvous)
   W1.Get_Result (R1);
   W2.Get_Result (R2);

   Put_Line ("R1 = " & Integer'Image (R1));
   Put_Line ("R2 = " & Integer'Image (R2));

   -- Protected object
   Shared_Counter.Increment;
   Shared_Counter.Increment;
   Put_Line ("Counter = " & Natural'Image (Shared_Counter.Value));

   -- Select statement (non-deterministic receive)
   -- select
   --    W1.Get_Result (R1) =>
   --       Put_Line ("Got R1");
   --    or
   --    W2.Get_Result (R2) =>
   --       Put_Line ("Got R2");
   --    or
   --    delay 5.0 =>
   --       Put_Line ("Timeout");
   -- end select;

end Tasking_Demo;
```
