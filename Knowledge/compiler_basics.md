# Compiler and Interpreter Basics Complete Reference


---

# CHAPTER 1: HOW PROGRAMMING LANGUAGES WORK


## Remarks

Every programming language is transformed from human-readable source code into something a computer can execute. Understanding this pipeline demystifies programming, enables you to build domain-specific languages (DSLs), write better code (knowing what the compiler does), and debug complex issues. Even if you never build a compiler, knowing lexing, parsing, and ASTs is invaluable for code analysis tools, linters, formatters, and template engines.

Key concepts: **Lexing/Tokenizing** (text → tokens), **Parsing** (tokens → AST), **AST** (Abstract Syntax Tree), **Semantic analysis** (type checking, scope resolution), **Code generation** (AST → target code), **Interpreters** (execute AST directly), **Compilers** (translate to machine code), **Transpilers** (translate to another language), **JIT** (Just-In-Time compilation), **Bytecode** (intermediate representation).


## Compilation Pipeline

```
SOURCE CODE:  "let x = 2 + 3 * 4;"

     │
     ▼
LEXER (Tokenizer):
  Breaks text into tokens.
  → [LET, IDENT("x"), EQUALS, INT(2), PLUS, INT(3), STAR, INT(4), SEMICOLON]

     │
     ▼
PARSER:
  Builds tree structure respecting grammar rules.
  → AST:
        LetStatement
        ├── name: "x"
        └── value: BinaryExpr(+)
                   ├── left: Int(2)
                   └── right: BinaryExpr(*)
                              ├── left: Int(3)
                              └── right: Int(4)

     │
     ▼
SEMANTIC ANALYSIS:
  Type checking, scope resolution, constant folding.
  → "3 * 4 = 12" (constant fold) → BinaryExpr(+, Int(2), Int(12))

     │
     ▼
CODE GENERATION (compiler):
  AST → machine code / bytecode / another language
  → x86: mov eax, 14; mov [rbp-4], eax
  → Bytecode: PUSH 14; STORE x
  → JavaScript: var x = 2 + 3 * 4;  (transpiler)

OR INTERPRETATION (interpreter):
  Walk AST and execute directly.
  → x = 14 (stored in environment)

TYPES OF LANGUAGE IMPLEMENTATIONS:
  Compiled:     C, C++, Rust, Go → machine code (fast execution)
  Interpreted:  Python, Ruby, PHP → execute AST/bytecode (slower)
  JIT-compiled: Java, C#, JavaScript → bytecode → JIT to machine code
  Transpiled:   TypeScript→JS, Kotlin→JVM bytecode, Dart→JS
```


---

# CHAPTER 2: LEXER (TOKENIZER)


## Building a Lexer

```python
# Lexer: convert source string into list of tokens

from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    # Literals
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    IDENT = auto()
    
    # Keywords
    LET = auto()
    IF = auto()
    ELSE = auto()
    FN = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    ASSIGN = auto()
    EQ = auto()         # ==
    NEQ = auto()        # !=
    LT = auto()
    GT = auto()
    LTE = auto()        # <=
    GTE = auto()        # >=
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    SEMICOLON = auto()
    
    # Special
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

KEYWORDS = {
    "let": TokenType.LET,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "fn": TokenType.FN,
    "return": TokenType.RETURN,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
}

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def tokenize(self) -> list[Token]:
        while self.pos < len(self.source):
            char = self.source[self.pos]

            # Skip whitespace
            if char in ' \t\r':
                self.advance()
            elif char == '\n':
                self.line += 1
                self.column = 0
                self.advance()

            # Numbers
            elif char.isdigit():
                self.read_number()

            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.read_identifier()

            # Strings
            elif char == '"':
                self.read_string()

            # Two-character operators
            elif char == '=' and self.peek() == '=':
                self.add_token(TokenType.EQ, '==')
                self.advance()
                self.advance()
            elif char == '!' and self.peek() == '=':
                self.add_token(TokenType.NEQ, '!=')
                self.advance()
                self.advance()
            elif char == '<' and self.peek() == '=':
                self.add_token(TokenType.LTE, '<=')
                self.advance()
                self.advance()
            elif char == '>' and self.peek() == '=':
                self.add_token(TokenType.GTE, '>=')
                self.advance()
                self.advance()

            # Single-character tokens
            elif char == '+': self.add_token(TokenType.PLUS, char); self.advance()
            elif char == '-': self.add_token(TokenType.MINUS, char); self.advance()
            elif char == '*': self.add_token(TokenType.STAR, char); self.advance()
            elif char == '/': self.add_token(TokenType.SLASH, char); self.advance()
            elif char == '=': self.add_token(TokenType.ASSIGN, char); self.advance()
            elif char == '<': self.add_token(TokenType.LT, char); self.advance()
            elif char == '>': self.add_token(TokenType.GT, char); self.advance()
            elif char == '(': self.add_token(TokenType.LPAREN, char); self.advance()
            elif char == ')': self.add_token(TokenType.RPAREN, char); self.advance()
            elif char == '{': self.add_token(TokenType.LBRACE, char); self.advance()
            elif char == '}': self.add_token(TokenType.RBRACE, char); self.advance()
            elif char == ',': self.add_token(TokenType.COMMA, char); self.advance()
            elif char == ';': self.add_token(TokenType.SEMICOLON, char); self.advance()

            else:
                raise SyntaxError(f"Unexpected character '{char}' at line {self.line}")

        self.add_token(TokenType.EOF, '')
        return self.tokens

    def advance(self):
        self.pos += 1
        self.column += 1

    def peek(self):
        if self.pos + 1 < len(self.source):
            return self.source[self.pos + 1]
        return '\0'

    def add_token(self, type, value):
        self.tokens.append(Token(type, value, self.line, self.column))

    def read_number(self):
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            self.advance()
        if self.pos < len(self.source) and self.source[self.pos] == '.':
            self.advance()
            while self.pos < len(self.source) and self.source[self.pos].isdigit():
                self.advance()
            self.add_token(TokenType.FLOAT, self.source[start:self.pos])
        else:
            self.add_token(TokenType.INT, self.source[start:self.pos])

    def read_identifier(self):
        start = self.pos
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            self.advance()
        word = self.source[start:self.pos]
        token_type = KEYWORDS.get(word, TokenType.IDENT)
        self.add_token(token_type, word)

    def read_string(self):
        self.advance()   # Skip opening "
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            if self.source[self.pos] == '\n':
                self.line += 1
            self.advance()
        value = self.source[start:self.pos]
        self.advance()   # Skip closing "
        self.add_token(TokenType.STRING, value)


# Usage
tokens = Lexer('let x = 2 + 3 * 4;').tokenize()
for t in tokens:
    print(f"{t.type.name:10} {t.value!r}")

# Output:
# LET        'let'
# IDENT      'x'
# ASSIGN     '='
# INT        '2'
# PLUS       '+'
# INT        '3'
# STAR       '*'
# INT        '4'
# SEMICOLON  ';'
# EOF        ''
```


---

# CHAPTER 3: PARSER


## Building a Recursive Descent Parser

```python
# Parser: tokens → AST (Abstract Syntax Tree)
# Recursive descent: one function per grammar rule

# AST Node types
@dataclass
class IntLiteral:
    value: int

@dataclass
class FloatLiteral:
    value: float

@dataclass
class StringLiteral:
    value: str

@dataclass
class BoolLiteral:
    value: bool

@dataclass
class Identifier:
    name: str

@dataclass
class BinaryExpr:
    op: str
    left: any
    right: any

@dataclass
class UnaryExpr:
    op: str
    operand: any

@dataclass
class LetStatement:
    name: str
    value: any

@dataclass
class IfStatement:
    condition: any
    then_body: list
    else_body: list

@dataclass
class FnDeclaration:
    name: str
    params: list[str]
    body: list

@dataclass
class CallExpr:
    callee: any
    args: list

@dataclass
class ReturnStatement:
    value: any

@dataclass
class Program:
    statements: list


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos]

    def eat(self, expected: TokenType) -> Token:
        token = self.current()
        if token.type != expected:
            raise SyntaxError(f"Expected {expected}, got {token.type} at line {token.line}")
        self.pos += 1
        return token

    def parse(self) -> Program:
        statements = []
        while self.current().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        if self.current().type == TokenType.LET:
            return self.parse_let()
        elif self.current().type == TokenType.IF:
            return self.parse_if()
        elif self.current().type == TokenType.FN:
            return self.parse_fn()
        elif self.current().type == TokenType.RETURN:
            return self.parse_return()
        else:
            expr = self.parse_expression()
            self.eat(TokenType.SEMICOLON)
            return expr

    def parse_let(self):
        self.eat(TokenType.LET)
        name = self.eat(TokenType.IDENT).value
        self.eat(TokenType.ASSIGN)
        value = self.parse_expression()
        self.eat(TokenType.SEMICOLON)
        return LetStatement(name, value)

    # Expression parsing with PRECEDENCE
    # Uses Pratt parsing / precedence climbing
    
    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_addition()
        while self.current().type in (TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.GT):
            op = self.eat(self.current().type).value
            right = self.parse_addition()
            left = BinaryExpr(op, left, right)
        return left

    def parse_addition(self):
        left = self.parse_multiplication()
        while self.current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.eat(self.current().type).value
            right = self.parse_multiplication()
            left = BinaryExpr(op, left, right)
        return left

    def parse_multiplication(self):
        left = self.parse_primary()
        while self.current().type in (TokenType.STAR, TokenType.SLASH):
            op = self.eat(self.current().type).value
            right = self.parse_primary()
            left = BinaryExpr(op, left, right)
        return left

    def parse_primary(self):
        token = self.current()
        if token.type == TokenType.INT:
            self.pos += 1
            return IntLiteral(int(token.value))
        elif token.type == TokenType.FLOAT:
            self.pos += 1
            return FloatLiteral(float(token.value))
        elif token.type == TokenType.STRING:
            self.pos += 1
            return StringLiteral(token.value)
        elif token.type == TokenType.TRUE:
            self.pos += 1
            return BoolLiteral(True)
        elif token.type == TokenType.FALSE:
            self.pos += 1
            return BoolLiteral(False)
        elif token.type == TokenType.IDENT:
            self.pos += 1
            name = Identifier(token.value)
            if self.current().type == TokenType.LPAREN:
                return self.parse_call(name)
            return name
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return expr
        else:
            raise SyntaxError(f"Unexpected token {token.type} at line {token.line}")

    def parse_call(self, callee):
        self.eat(TokenType.LPAREN)
        args = []
        while self.current().type != TokenType.RPAREN:
            args.append(self.parse_expression())
            if self.current().type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
        self.eat(TokenType.RPAREN)
        return CallExpr(callee, args)


# Usage
source = "let x = 2 + 3 * 4;"
tokens = Lexer(source).tokenize()
ast = Parser(tokens).parse()
print(ast)
# Program(statements=[
#   LetStatement(name='x', value=BinaryExpr(op='+',
#     left=IntLiteral(2),
#     right=BinaryExpr(op='*', left=IntLiteral(3), right=IntLiteral(4))
#   ))
# ])
# Note: * has higher precedence than + (correct!)
```


---

# CHAPTER 4: INTERPRETER


## Tree-Walking Interpreter

```python
# Interpreter: walk AST and execute

class Environment:
    """Variable scope with parent chain."""
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable: {name}")

    def set(self, name, value):
        self.vars[name] = value


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self._setup_builtins()

    def _setup_builtins(self):
        self.global_env.set("print", lambda *args: print(*args))
        self.global_env.set("len", lambda x: len(x))

    def execute(self, program: Program):
        result = None
        for stmt in program.statements:
            result = self.eval(stmt, self.global_env)
        return result

    def eval(self, node, env: Environment):
        match node:
            case IntLiteral(value=v):
                return v

            case FloatLiteral(value=v):
                return v

            case StringLiteral(value=v):
                return v

            case BoolLiteral(value=v):
                return v

            case Identifier(name=n):
                return env.get(n)

            case BinaryExpr(op=op, left=left, right=right):
                l = self.eval(left, env)
                r = self.eval(right, env)
                match op:
                    case '+': return l + r
                    case '-': return l - r
                    case '*': return l * r
                    case '/': return l / r
                    case '==': return l == r
                    case '!=': return l != r
                    case '<': return l < r
                    case '>': return l > r

            case LetStatement(name=name, value=value):
                env.set(name, self.eval(value, env))

            case CallExpr(callee=callee, args=args):
                func = self.eval(callee, env)
                evaluated_args = [self.eval(a, env) for a in args]
                if callable(func):
                    return func(*evaluated_args)
                # User-defined function
                fn_env = Environment(parent=func["closure"])
                for param, arg in zip(func["params"], evaluated_args):
                    fn_env.set(param, arg)
                return self.eval_body(func["body"], fn_env)

    def eval_body(self, statements, env):
        result = None
        for stmt in statements:
            result = self.eval(stmt, env)
        return result


# FULL EXAMPLE
source = """
let x = 2 + 3 * 4;
print(x);
"""

tokens = Lexer(source).tokenize()
ast = Parser(tokens).parse()
Interpreter().execute(ast)
# Output: 14
```


---

# CHAPTER 5: COMMON PITFALLS

```
PITFALL 1: Not handling operator precedence
  2 + 3 * 4 parsed as (2 + 3) * 4 = 20 instead of 2 + (3 * 4) = 14.
  Fix: precedence climbing in parser (separate parse functions per level).

PITFALL 2: Left recursion in recursive descent
  Rule: expr → expr + term causes infinite recursion.
  Fix: rewrite as iteration: expr → term ((+|-) term)*.

PITFALL 3: Not tracking position info
  Error says "unexpected token" but no line/column.
  Fix: every token and AST node carries source location.

PITFALL 4: Mutable global environment
  All functions share same scope → variable collision.
  Fix: environment chain (each scope has parent pointer).

PITFALL 5: No error recovery
  First syntax error → parser crashes. User fixes one error, hits next.
  Fix: synchronize at statement boundaries, collect multiple errors.

PITFALL 6: String handling
  Forgetting escape sequences (\\n, \\t, \\"), Unicode.
  Fix: handle escapes in lexer's read_string.

PITFALL 7: Whitespace sensitivity
  Accidentally treating indentation as tokens (Python does this intentionally).
  Fix: skip whitespace in lexer unless language requires it.

PITFALL 8: Testing only valid input
  Parser works on correct programs but crashes on invalid ones.
  Fix: test error cases extensively. Fuzzing helps.
```