# Smalltalk Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH SMALLTALK


## Remarks

Smalltalk is a purely object-oriented, dynamically typed language where everything is an object, including classes, integers, and booleans. It pioneered many OOP concepts and the modern GUI/IDE. Message sending is the only way objects interact.

Implementations: Squeak, Pharo, GNU Smalltalk, VisualWorks, GemStone.


## Hello World

```smalltalk
"Pharo / Squeak"
Transcript show: 'Hello, World!'; nl.
Transcript showCrLf: 'Hello, Smalltalk!'.

"GNU Smalltalk"
Smalltalk at: #Transcript put: (FileStream stdout).
Transcript show: 'Hello, World!'; nl.
```

```bash
# GNU Smalltalk
gst hello.st

# Pharo (headless)
pharo Pharo.image eval "Transcript show: 'Hello'"
```


---

# CHAPTER 2: OBJECTS AND MESSAGES


## Message Sending

```smalltalk
"Everything is an object."
"Messages are sent to objects."

"Unary message (no arguments)"
3 factorial.         "6"
'hello' size.        "5"
'hello' reversed.    "'olleh'"
'hello' asUppercase. "'HELLO'"
3.14 truncated.      "3"
Date today.

"Binary message (one argument, symbol-like)"
3 + 4.               "7"
10 - 3.              "7"
2 * 5.               "10"
10 / 2.              "5"
10 // 3.             "3 (integer division)"
10 \\ 3.             "1 (modulo)"
10 ** 2.             "100"
'hello' , ' world'.  "'hello world' (concatenation)"
3 > 2.               "true"
3 < 2.               "false"
3 = 3.               "true"
3 ~= 4.              "true (not equal)"
3 == 3.              "true (identity)"

"Keyword message (one or more arguments)"
OrderedCollection new.
Array new: 5.
Dictionary new.
'hello world' indexOf: $o.   "5"
'Hello' copyFrom: 1 to: 3.   "'Hel'"
10 max: 20.                   "20"
3 between: 1 and: 5.          "true"
Transcript show: 'test'.

"Message precedence (highest to lowest)"
"Unary > Binary > Keyword"
2 + 3 factorial.    "2 + 6 = 8 (factorial first)"
(2 + 3) factorial.  "120"
2 + 3 * 4.          "20 (left to right, no * priority!)"

"Cascades — send multiple messages to same object"
Transcript
    show: 'Hello';
    nl;
    show: 'World';
    nl.

"OrderedCollection with cascade"
| col |
col := OrderedCollection new.
col
    add: 1;
    add: 2;
    add: 3.
```


---

# CHAPTER 3: VARIABLES AND ASSIGNMENT


## Variables

```smalltalk
"Temporary variables (local scope)"
| x y result |
x := 42.
y := 3.14.
result := x + y.
Transcript showCrLf: result printString.

"Global variables (ALL CAPS convention)"
| greeting |
greeting := 'Hello, World!'.
Smalltalk at: #MyGlobal put: 'a global'.

"Instance variables — declared in class definition"
"Class variables — shared among all instances"
"Pool variables — shared among specific classes"

"Literals"
42              "Integer"
-7              "Negative integer"
3.14            "Float"
$A              "Character"
'hello'         "String"
#symbol         "Symbol"
#(1 2 3)        "Array literal"
{1+1. 2+2. 3}   "Array constructor (dynamic)"
true false nil  "Special values"

"Strings"
| s |
s := 'Hello, World!'.
s size.                   "13"
s reversed.               "'!dlroW ,olleH'"
s asUppercase.            "'HELLO, WORLD!'"
s asLowercase.            "'hello, world!'"
s copyFrom: 1 to: 5.      "'Hello'"
s indexOf: $o.            "5"
s includesSubString: 'World'.  "true"
s replaceAll: 'World' with: 'Smalltalk'.
'Hello' , ', ' , 'World!'. "'Hello, World!'"
s printString.             "'''Hello, World!''' (with quotes)"

"Characters"
$A asciiValue.      "65"
$A isUppercase.     "true"
$a isLowercase.     "true"
$1 isDigit.         "true"
$A asLowercase.     "$a"
$a asUppercase.     "$A"

"Symbols (interned strings)"
#hello.             "'hello' (unique object)"
#hello == #hello.   "true (same object)"
```


---

# CHAPTER 4: CONTROL FLOW


## Conditionals and Loops

```smalltalk
"Booleans respond to messages (no special syntax!)"

"if-then: ifTrue:"
(3 > 2) ifTrue: ['positive'].

"if-then-else: ifTrue:ifFalse:"
x := 10.
(x > 0)
    ifTrue: [Transcript show: 'positive']
    ifFalse: [Transcript show: 'non-positive'].

"if-else (inverted): ifFalse:ifTrue:"
(x < 0)
    ifFalse: ['not negative']
    ifTrue: ['negative'].

"Ternary-like"
| label |
label := (x > 0) ifTrue: ['pos'] ifFalse: ['non-pos'].

"Nested condition"
| grade |
grade := x >= 90
    ifTrue: ['A']
    ifFalse: [
        x >= 80
            ifTrue: ['B']
            ifFalse: ['C or lower']].

"whileTrue: / whileFalse:"
| n |
n := 1.
[n < 100] whileTrue: [n := n * 2].
Transcript showCrLf: n printString.   "128"

[n < 200] whileFalse: [n := n + 10].

"timesRepeat:"
5 timesRepeat: [Transcript showCrLf: 'hello'].

"to:do:"
1 to: 10 do: [:i | Transcript showCrLf: i printString].

"to:by:do:"
1 to: 10 by: 2 do: [:i | Transcript show: i printString; show: ' '].

10 to: 1 by: -1 do: [:i | Transcript showCrLf: i printString].

"Blocks (first-class objects)"
| b |
b := [:x :y | x + y].    "block with 2 params"
b value: 3 value: 4.      "7"

| square |
square := [:x | x * x].
square value: 5.          "25"

"Blocks can be stored, passed, returned"
| blocks |
blocks := #('hello' printString. 42. 3 + 4).   "not quite, but blocks:"
blocks := {['hello'] . [42] . [3 + 4]}.
blocks do: [:b | Transcript showCrLf: b value printString].
```


---

# CHAPTER 5: COLLECTIONS


## Collection Classes

```smalltalk
"Array (fixed size)"
| arr |
arr := #(10 20 30 40 50).
arr at: 1.          "10 (1-indexed!)"
arr size.           "5"
arr first.          "10"
arr last.           "50"
arr do: [:x | Transcript showCrLf: x printString].
arr collect: [:x | x * 2].    "#(20 40 60 80 100)"
arr select: [:x | x > 25].    "#(30 40 50)"
arr reject: [:x | x > 25].    "#(10 20)"
arr detect: [:x | x > 25].    "30 (first match)"
arr detect: [:x | x > 100] ifNone: [-1].  "-1"
arr inject: 0 into: [:sum :x | sum + x].  "150"
arr includes: 30.   "true"
arr indexOf: 30.    "3"

"Dynamic array"
| dyn |
dyn := {1+1. 2*3. 4 factorial}.  "#(2 6 24)"

"OrderedCollection (dynamic list)"
| oc |
oc := OrderedCollection new.
oc add: 'Alice'.
oc add: 'Bob'.
oc add: 'Carol'.
oc addFirst: 'Zero'.
oc addLast: 'Dave'.
oc remove: 'Bob'.
oc size.           "4"
oc first.          "'Zero'"
oc last.           "'Dave'"
oc do: [:each | Transcript showCrLf: each].
oc collect: [:x | x size].
oc select: [:x | x size > 4].
oc sortBlock: [:a :b | a < b].

"Set (unique elements)"
| set |
set := Set new.
set add: 1; add: 2; add: 3; add: 2; add: 1.
set size.          "3"
set includes: 2.   "true"

"Dictionary"
| dict |
dict := Dictionary new.
dict at: 'name' put: 'Alice'.
dict at: 'age'  put: 30.
dict at: 'name'.            "'Alice'"
dict at: 'missing' ifAbsent: ['default'].
dict includesKey: 'name'.   "true"
dict keys.                  "Set('name' 'age')"
dict values.                "Array('Alice' 30)"
dict keysAndValuesDo: [:k :v |
    Transcript show: k; show: ': '; showCrLf: v printString].
dict removeKey: 'age'.
dict size.   "1"
```


---

# CHAPTER 6: CLASSES AND INHERITANCE


## Defining Classes

```smalltalk
"Class definition (Pharo syntax)"
Object subclass: #Animal
    instanceVariableNames: 'name sound age'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Animals'.

"Add methods to Animal (in a method browser)"
Animal class >> new: aName sound: aSound [
    | animal |
    animal := super new.
    animal setName: aName sound: aSound.
    ^animal
]

Animal >> setName: aName sound: aSound [
    name := aName.
    sound := aSound.
    age := 0.
]

Animal >> name [ ^name ]
Animal >> sound [ ^sound ]
Animal >> age [ ^age ]
Animal >> age: anAge [ age := anAge ]

Animal >> speak [
    ^name , ' says ' , sound
]

Animal >> printOn: aStream [
    aStream nextPutAll: 'Animal(' , name , ')'
]

"Subclass"
Animal subclass: #Dog
    instanceVariableNames: 'breed'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Animals'.

Dog class >> new: aName breed: aBreed [
    | dog |
    dog := super new: aName sound: 'Woof'.
    dog setBreed: aBreed.
    ^dog
]

Dog >> setBreed: aBreed [ breed := aBreed ]
Dog >> breed [ ^breed ]

Dog >> speak [
    ^super speak , '!'
]

Dog >> fetch [
    ^name , ' fetches!'
]

"Usage"
| dog |
dog := Dog new: 'Rex' breed: 'Labrador'.
Transcript showCrLf: dog speak.    "'Rex says Woof!'"
Transcript showCrLf: dog fetch.    "'Rex fetches!'"
dog isKindOf: Animal.              "true"
dog isKindOf: Dog.                 "true"
dog isMemberOf: Dog.               "true"
dog isMemberOf: Animal.            "false"
dog respondsTo: #speak.            "true"
dog class.                         "Dog"
Dog superclass.                    "Animal"
```


---

# CHAPTER 7: EXCEPTION HANDLING


## Exceptions

```smalltalk
"Signal an exception"
Error signal: 'Something went wrong'.
Error new signal: 'Custom message'.

"Custom exception class"
Error subclass: #ValidationError
    instanceVariableNames: 'field'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Errors'.

ValidationError >> field [ ^field ]
ValidationError >> field: aField [ field := aField ]

ValidationError class >> signal: msg field: aField [
    | err |
    err := self new.
    err field: aField.
    err signal: msg.
]

"Handle exceptions"
[
    Error signal: 'test error'
] on: Error do: [:e |
    Transcript showCrLf: 'Caught: ' , e messageText.
].

"Multiple handlers"
[
    self riskyOperation
] on: ZeroDivide do: [:e |
    Transcript showCrLf: 'Division by zero'.
] on: Error do: [:e |
    Transcript showCrLf: 'Other error: ' , e messageText.
].

"ensure: (finally)"
| file |
[
    file := FileStream open: 'test.txt'.
    "... use file ..."
] ensure: [
    file ifNotNil: [file close].
].

"Retry"
| attempts |
attempts := 0.
[
    attempts := attempts + 1.
    attempts < 3 ifTrue: [Error signal: 'try again'].
    Transcript showCrLf: 'Success after ' , attempts printString , ' tries'.
] on: Error do: [:e | e retry].

"Return value"
| result |
result := [
    Error signal: 'oops'.
    42
] on: Error do: [:e | -1].
"result = -1"
```


---

# CHAPTER 8: REFLECTION AND METAPROGRAMMING


## Metaprogramming

```smalltalk
"Reflection — introspect objects at runtime"

"Class info"
3 class.                      "SmallInt"
3 class name.                 "'SmallInt'"
3 class superclass.           "Integer"
SmallInt superclass.          "Integer"
Integer superclass.           "Number"
Number superclass.            "Magnitude"
Magnitude superclass.         "Object"
Object superclass.            "nil"

"Method info"
3 respondsTo: #+.             "true"
3 respondsTo: #unknownMsg.    "false"
SmallInt methodDict keys.     "all method names"
SmallInt instanceVariableNames. "all instance vars"

"Sending messages dynamically"
| selector |
selector := #+.
3 perform: selector with: 4.    "7"
3 perform: #factorial.           "6"

"doesNotUnderstand: (method_missing equivalent)"
Object >> doesNotUnderstand: aMessage [
    Transcript show: 'Unknown message: '; showCrLf: aMessage selector.
    ^nil
]

"thisContext (current execution context)"
thisContext sender.       "caller's context"
thisContext method.       "current method"
thisContext home.         "block's home context"

"Smalltalk system"
Smalltalk allClasses.       "all classes"
Smalltalk at: #Array.       "get class by name"
Smalltalk globals.          "global namespace"
Smalltalk version.          "version string"

"Class creation at runtime"
| newClass |
newClass := Object subclass: #DynamicClass
    instanceVariableNames: 'value'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'Dynamic'.

newClass compile: 'value [ ^value ]'.
newClass compile: 'value: v [ value := v ]'.
```
