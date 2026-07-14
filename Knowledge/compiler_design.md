Compiler Design & Language Implementation Complete Reference
CHAPTER 1: GETTING STARTED WITH COMPILER DESIGN
Remarks
A compiler transforms source code into target code (machine code, bytecode, or another language). Phases: lexical analysis, parsing, semantic analysis, intermediate representation, optimization, code generation. Modern compilers use LLVM, GCC, or custom backends.
Tools: Python (for educational compilers), C/C++ (production), LLVM (industrial strength), ANTLR (parser generator), Flex/Bison (lexing/parsing), Rust (modern compilers).
Hello Compiler
# hello_compiler.py
"""
Minimal compiler: source → tokens → AST → x86 assembly
"""

class Token:
    def __init__(self, type, value, line=1):
        self.type = type
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"

class Lexer:
    """Tokenize simple arithmetic expressions."""
    
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
    
    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            c = self.source[self.pos]
            
            if c.isspace():
                if c == '\n':
                    self.line += 1
                self.pos += 1
                continue
            
            if c.isdigit():
                tokens.append(self._read_number())
            elif c.isalpha():
                tokens.append(self._read_identifier())
            elif c == '+':
                tokens.append(Token('PLUS', '+', self.line))
                self.pos += 1
            elif c == '-':
                tokens.append(Token('MINUS', '-', self.line))
                self.pos += 1
            elif c == '*':
                tokens.append(Token('MUL', '*', self.line))
                self.pos += 1
            elif c == '/':
                tokens.append(Token('DIV', '/', self.line))
                self.pos += 1
            elif c == '(':
                tokens.append(Token('LPAREN', '(', self.line))
                self.pos += 1
            elif c == ')':
                tokens.append(Token('RPAREN', ')', self.line))
                self.pos += 1
            else:
                raise SyntaxError(f"Unexpected character '{c}' at line {self.line}")
        
        tokens.append(Token('EOF', None, self.line))
        return tokens
    
    def _read_number(self):
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            self.pos += 1
        return Token('NUMBER', int(self.source[start:self.pos]), self.line)
    
    def _read_identifier(self):
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos].isalnum():
            self.pos += 1
        value = self.source[start:self.pos]
        return Token('IDENT', value, self.line)

# Example
source = "3 + 4 * (2 - 1)"
lexer = Lexer(source)
tokens = lexer.tokenize()
for token in tokens:
    print(token)

CHAPTER 2: LEXICAL ANALYSIS
Regular Expressions and Finite Automata
# Lexical analysis converts character stream into tokens.
# Uses regular expressions → NFA → DFA → tokenization.

import re

class RegexLexer:
    """Lexer using regular expressions."""
    
    def __init__(self, patterns):
        """
        patterns: list of (token_type, regex_pattern) tuples
        Order matters - first match wins
        """
        self.patterns = patterns
        self.compiled = [(ttype, re.compile(pattern)) for ttype, pattern in patterns]
    
    def tokenize(self, source):
        tokens = []
        pos = 0
        line = 1
        
        while pos < len(source):
            match_found = False
            
            for ttype, pattern in self.compiled:
                match = pattern.match(source, pos)
                if match:
                    value = match.group(0)
                    
                    # Skip whitespace
                    if ttype == 'SKIP':
                        line += value.count('\n')
                        pos = match.end()
                        match_found = True
                        break
                    
                    tokens.append(Token(ttype, value, line))
                    line += value.count('\n')
                    pos = match.end()
                    match_found = True
                    break
            
            if not match_found:
                raise SyntaxError(f"Unexpected character '{source[pos]}' at line {line}")
        
        tokens.append(Token('EOF', None, line))
        return tokens

# Define token patterns
PATTERNS = [
    ('SKIP', r'\s+'),
    ('NUMBER', r'\d+(\.\d+)?'),
    ('IDENT', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MUL', r'\*'),
    ('DIV', r'/'),
    ('ASSIGN', r'='),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('SEMI', r';'),
]

lexer = RegexLexer(PATTERNS)
source = """
x = 42;
y = x + 3.14;
"""
tokens = lexer.tokenize(source)
for token in tokens:
    if token.type != 'EOF':
        print(token)

DFA Implementation
# Deterministic Finite Automaton for token recognition

class DFA:
    """DFA for recognizing identifiers and numbers."""
    
    def __init__(self):
        # States: 0=start, 1=in_ident, 2=in_number, 3=in_float
        self.transitions = {
            0: {'alpha': 1, 'digit': 2},
            1: {'alpha': 1, 'digit': 1, '_': 1},
            2: {'digit': 2, '.': 3},
            3: {'digit': 3},
        }
        self.accept_states = {1: 'IDENT', 2: 'NUMBER', 3: 'FLOAT'}
    
    def recognize(self, input_str):
        state = 0
        for char in input_str:
            if char.isalpha() or char == '_':
                char_type = 'alpha'
            elif char.isdigit():
                char_type = 'digit'
            elif char == '.':
                char_type = '.'
            else:
                return None
            
            if char_type in self.transitions[state]:
                state = self.transitions[state][char_type]
            else:
                return None
        
        return self.accept_states.get(state)

dfa = DFA()
print("Recognize 'hello':", dfa.recognize("hello"))  # IDENT
print("Recognize '123':", dfa.recognize("123"))      # NUMBER
print("Recognize '3.14':", dfa.recognize("3.14"))    # FLOAT
print("Recognize 'x_42':", dfa.recognize("x_42"))    # IDENT

CHAPTER 3: PARSING
Recursive Descent Parser
# Recursive descent: top-down parser, one function per grammar rule.
# Grammar (arithmetic expressions):
#   expr   → term (('+' | '-') term)*
#   term   → factor (('*' | '/') factor)*
#   factor → NUMBER | '(' expr ')'

class ASTNode:
    """Base class for AST nodes."""
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"Number({self.value})"

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"BinOp({self.left} {self.op} {self.right})"

class Parser:
    """Recursive descent parser."""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current(self):
        return self.tokens[self.pos]
    
    def consume(self, expected_type):
        token = self.current()
        if token.type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token.type} at line {token.line}")
        self.pos += 1
        return token
    
    def parse(self):
        ast = self.expr()
        if self.current().type != 'EOF':
            raise SyntaxError(f"Unexpected token {self.current()}")
        return ast
    
    def expr(self):
        """expr → term (('+' | '-') term)*"""
        node = self.term()
        
        while self.current().type in ('PLUS', 'MINUS'):
            op = self.current()
            self.pos += 1
            right = self.term()
            node = BinOpNode(node, op.type, right)
        
        return node
    
    def term(self):
        """term → factor (('*' | '/') factor)*"""
        node = self.factor()
        
        while self.current().type in ('MUL', 'DIV'):
            op = self.current()
            self.pos += 1
            right = self.factor()
            node = BinOpNode(node, op.type, right)
        
        return node
    
    def factor(self):
        """factor → NUMBER | '(' expr ')'"""
        token = self.current()
        
        if token.type == 'NUMBER':
            self.pos += 1
            return NumberNode(token.value)
        
        if token.type == 'LPAREN':
            self.pos += 1
            node = self.expr()
            self.consume('RPAREN')
            return node
        
        raise SyntaxError(f"Expected number or '(', got {token.type}")

# Example
source = "3 + 4 * (2 - 1)"
lexer = Lexer(source)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
print("AST:", ast)

LL(1) Parsing Table
# LL(1): Left-to-right, Leftmost derivation, 1 token lookahead.
# Requires grammar to be LL(1): no left recursion, no ambiguity.

class LL1Parser:
    """LL(1) parser using parsing table."""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        
        # Parsing table for expression grammar
        # Non-terminals: E, T, F
        # Terminals: NUMBER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN
        self.table = {
            ('E', 'NUMBER'): ['T', 'Ep'],
            ('E', 'LPAREN'): ['T', 'Ep'],
            ('Ep', 'PLUS'): ['+', 'T', 'Ep'],
            ('Ep', 'MINUS'): ['-', 'T', 'Ep'],
            ('Ep', 'RPAREN'): [],
            ('Ep', 'EOF'): [],
            ('T', 'NUMBER'): ['F', 'Tp'],
            ('T', 'LPAREN'): ['F', 'Tp'],
            ('Tp', 'MUL'): ['*', 'F', 'Tp'],
            ('Tp', 'DIV'): ['/', 'F', 'Tp'],
            ('Tp', 'PLUS'): [],
            ('Tp', 'MINUS'): [],
            ('Tp', 'RPAREN'): [],
            ('Tp', 'EOF'): [],
            ('F', 'NUMBER'): ['NUMBER'],
            ('F', 'LPAREN'): ['(', 'E', ')'],
        }
    
    def parse(self):
        stack = ['$', 'E']
        tokens = self.tokens + [Token('$', None)]
        idx = 0
        
        while stack:
            top = stack[-1]
            token = tokens[idx]
            
            if top == token.type:
                stack.pop()
                idx += 1
            elif top == '$':
                if token.type == '$':
                    return True
                else:
                    raise SyntaxError("Parse error")
            elif (top, token.type) in self.table:
                stack.pop()
                production = self.table[(top, token.type)]
                stack.extend(reversed(production))
            else:
                raise SyntaxError(f"No production for ({top}, {token.type})")
        
        return True

# Example
source = "3 + 4"
lexer = Lexer(source)
tokens = lexer.tokenize()
parser = LL1Parser(tokens)
print("LL(1) parse:", parser.parse())

CHAPTER 4: ABSTRACT SYNTAX TREES
AST Construction and Traversal
# AST represents program structure hierarchically.
# Used for semantic analysis, optimization, code generation.

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class VarDeclNode(ASTNode):
    def __init__(self, name, type, init_expr=None):
        self.name = name
        self.type = type
        self.init_expr = init_expr

class AssignNode(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class IfNode(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FunctionDefNode(ASTNode):
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body

class CallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ASTVisitor:
    """Visitor pattern for AST traversal."""
    
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

class ASTPrinter(ASTVisitor):
    """Print AST with indentation."""
    
    def __init__(self):
        self.indent = 0
    
    def visit_ProgramNode(self, node):
        print("Program")
        self.indent += 1
        for stmt in node.statements:
            self.visit(stmt)
        self.indent -= 1
    
    def visit_VarDeclNode(self, node):
        print("  " * self.indent + f"VarDecl: {node.name} : {node.type}")
        if node.init_expr:
            self.indent += 1
            self.visit(node.init_expr)
            self.indent -= 1
    
    def visit_AssignNode(self, node):
        print("  " * self.indent + f"Assign: {node.name}")
        self.indent += 1
        self.visit(node.expr)
        self.indent -= 1
    
    def visit_NumberNode(self, node):
        print("  " * self.indent + f"Number: {node.value}")
    
    def visit_BinOpNode(self, node):
        print("  " * self.indent + f"BinOp: {node.op}")
        self.indent += 1
        self.visit(node.left)
        self.visit(node.right)
        self.indent -= 1

# Example AST
program = ProgramNode([
    VarDeclNode('x', 'int', NumberNode(42)),
    AssignNode('y', BinOpNode(NumberNode(3), 'PLUS', NumberNode(4))),
])

printer = ASTPrinter()
printer.visit(program)

AST Transformation
# Transform AST for optimization or code generation

class ConstantFolder(ASTVisitor):
    """Fold constant expressions at compile time."""
    
    def visit_BinOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        # If both operands are constants, evaluate
        if isinstance(left, NumberNode) and isinstance(right, NumberNode):
            if node.op == 'PLUS':
                return NumberNode(left.value + right.value)
            elif node.op == 'MINUS':
                return NumberNode(left.value - right.value)
            elif node.op == 'MUL':
                return NumberNode(left.value * right.value)
            elif node.op == 'DIV':
                return NumberNode(left.value // right.value)
        
        # Otherwise, return new BinOpNode with transformed children
        return BinOpNode(left, node.op, right)
    
    def visit_NumberNode(self, node):
        return node

# Example
expr = BinOpNode(
    BinOpNode(NumberNode(2), 'PLUS', NumberNode(3)),
    'MUL',
    NumberNode(4)
)

folder = ConstantFolder()
optimized = folder.visit(expr)
print("Original:", expr)
print("Optimized:", optimized)  # Number(20)

CHAPTER 5: SEMANTIC ANALYSIS
Symbol Table
# Symbol table stores information about identifiers (variables, functions, types).

class Symbol:
    def __init__(self, name, type, kind='variable'):
        self.name = name
        self.type = type
        self.kind = kind  # 'variable', 'function', 'parameter'

class SymbolTable:
    """Scoped symbol table."""
    
    def __init__(self):
        self.scopes = [{}]  # Stack of scopes
    
    def enter_scope(self):
        self.scopes.append({})
    
    def exit_scope(self):
        self.scopes.pop()
    
    def insert(self, symbol):
        if symbol.name in self.scopes[-1]:
            raise SemanticError(f"Redefinition of '{symbol.name}'")
        self.scopes[-1][symbol.name] = symbol
    
    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

class SemanticError(Exception):
    pass

class TypeChecker(ASTVisitor):
    """Type checking and semantic analysis."""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
    
    def visit_ProgramNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)
    
    def visit_VarDeclNode(self, node):
        # Check if variable already declared
        if self.symbol_table.lookup(node.name):
            raise SemanticError(f"Variable '{node.name}' already declared")
        
        # Insert into symbol table
        self.symbol_table.insert(Symbol(node.name, node.type))
        
        # Type check initializer
        if node.init_expr:
            init_type = self.visit(node.init_expr)
            if init_type != node.type:
                raise SemanticError(f"Type mismatch: expected {node.type}, got {init_type}")
    
    def visit_AssignNode(self, node):
        # Check if variable exists
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            raise SemanticError(f"Undefined variable '{node.name}'")
        
        # Type check expression
        expr_type = self.visit(node.expr)
        if expr_type != symbol.type:
            raise SemanticError(f"Type mismatch in assignment to '{node.name}'")
    
    def visit_NumberNode(self, node):
        return 'int'
    
    def visit_BinOpNode(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        if left_type != right_type:
            raise SemanticError(f"Type mismatch in binary operation")
        
        return left_type

# Example
program = ProgramNode([
    VarDeclNode('x', 'int', NumberNode(42)),
    AssignNode('x', BinOpNode(NumberNode(3), 'PLUS', NumberNode(4))),
])

checker = TypeChecker()
try:
    checker.visit(program)
    print("Semantic analysis passed")
except SemanticError as e:
    print(f"Semantic error: {e}")

Scope Resolution
# Handle nested scopes (blocks, functions, classes)

class ScopedTypeChecker(TypeChecker):
    """Type checker with scope support."""
    
    def visit_FunctionDefNode(self, node):
        # Insert function into current scope
        func_type = f"function({', '.join(p.type for p in node.params)}) -> {node.return_type}"
        self.symbol_table.insert(Symbol(node.name, func_type, 'function'))
        
        # Enter new scope for function body
        self.symbol_table.enter_scope()
        
        # Insert parameters
        for param in node.params:
            self.symbol_table.insert(Symbol(param.name, param.type, 'parameter'))
        
        # Check body
        for stmt in node.body:
            self.visit(stmt)
        
        # Exit scope
        self.symbol_table.exit_scope()
    
    def visit_IfNode(self, node):
        # Check condition is boolean
        cond_type = self.visit(node.condition)
        if cond_type != 'bool':
            raise SemanticError("If condition must be boolean")
        
        # Check then block
        self.symbol_table.enter_scope()
        for stmt in node.then_block:
            self.visit(stmt)
        self.symbol_table.exit_scope()
        
        # Check else block
        if node.else_block:
            self.symbol_table.enter_scope()
            for stmt in node.else_block:
                self.visit(stmt)
            self.symbol_table.exit_scope()

CHAPTER 6: INTERMEDIATE REPRESENTATION
Three-Address Code
# Three-address code (TAC): each instruction has at most 3 operands.
# Form: x = y op z, x = op y, x = y, goto L, if x goto L

class TACInstruction:
    def __init__(self, op, dest=None, src1=None, src2=None):
        self.op = op
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
    
    def __repr__(self):
        if self.op in ('+', '-', '*', '/'):
            return f"{self.dest} = {self.src1} {self.op} {self.src2}"
        elif self.op == 'assign':
            return f"{self.dest} = {self.src1}"
        elif self.op == 'goto':
            return f"goto {self.dest}"
        elif self.op == 'if':
            return f"if {self.src1} goto {self.dest}"
        elif self.op == 'label':
            return f"{self.dest}:"
        elif self.op == 'param':
            return f"param {self.src1}"
        elif self.op == 'call':
            return f"{self.dest} = call {self.src1}, {self.src2}"
        elif self.op == 'return':
            return f"return {self.src1}"
        else:
            return f"{self.op} {self.dest} {self.src1} {self.src2}"

class TACGenerator(ASTVisitor):
    """Generate three-address code from AST."""
    
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"
    
    def new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"
    
    def emit(self, instruction):
        self.instructions.append(instruction)
    
    def visit_ProgramNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)
        return self.instructions
    
    def visit_VarDeclNode(self, node):
        if node.init_expr:
            temp = self.visit(node.init_expr)
            self.emit(TACInstruction('assign', node.name, temp))
    
    def visit_AssignNode(self, node):
        temp = self.visit(node.expr)
        self.emit(TACInstruction('assign', node.name, temp))
    
    def visit_NumberNode(self, node):
        return str(node.value)
    
    def visit_BinOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        temp = self.new_temp()
        self.emit(TACInstruction(node.op, temp, left, right))
        return temp
    
    def visit_IfNode(self, node):
        cond = self.visit(node.condition)
        else_label = self.new_label()
        end_label = self.new_label()
        
        self.emit(TACInstruction('if', else_label, cond))
        
        for stmt in node.then_block:
            self.visit(stmt)
        
        if node.else_block:
            self.emit(TACInstruction('goto', end_label))
            self.emit(TACInstruction('label', else_label))
            for stmt in node.else_block:
                self.visit(stmt)
            self.emit(TACInstruction('label', end_label))
        else:
            self.emit(TACInstruction('label', else_label))

# Example
program = ProgramNode([
    VarDeclNode('x', 'int', NumberNode(10)),
    AssignNode('y', BinOpNode(NumberNode(3), 'PLUS', NumberNode(4))),
])

generator = TACGenerator()
tac = generator.visit(program)
print("Three-address code:")
for instr in tac:
    print(instr)

Static Single Assignment (SSA) Form
# SSA: each variable assigned exactly once.
# Uses phi functions at control flow merge points.

class SSAVariable:
    def __init__(self, name, version):
        self.name = name
        self.version = version
    
    def __repr__(self):
        return f"{self.name}_{self.version}"

class SSAInstruction:
    def __init__(self, op, dest=None, src1=None, src2=None):
        self.op = op
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
    
    def __repr__(self):
        if self.op == 'phi':
            sources = ', '.join(f"{v} from {b}" for v, b in zip(self.src1, self.src2))
            return f"{self.dest} = φ({sources})"
        elif self.op in ('+', '-', '*', '/'):
            return f"{self.dest} = {self.src1} {self.op} {self.src2}"
        elif self.op == 'assign':
            return f"{self.dest} = {self.src1}"
        else:
            return f"{self.op} {self.dest} {self.src1} {self.src2}"

class SSABuilder:
    """Convert TAC to SSA form."""
    
    def __init__(self):
        self.version_counter = {}
        self.current_def = {}
    
    def new_version(self, var):
        if var not in self.version_counter:
            self.version_counter[var] = 0
        self.version_counter[var] += 1
        return SSAVariable(var, self.version_counter[var])
    
    def convert(self, tac_instructions):
        ssa_instructions = []
        
        for instr in tac_instructions:
            if instr.op == 'assign':
                # x = y → x_i = y_j
                dest = self.new_version(instr.dest)
                src = self.current_def.get(instr.src1, SSAVariable(instr.src1, 0))
                ssa_instructions.append(SSAInstruction('assign', dest, src))
                self.current_def[instr.dest] = dest
            
            elif instr.op in ('+', '-', '*', '/'):
                # x = y op z → x_i = y_j op z_k
                dest = self.new_version(instr.dest)
                src1 = self.current_def.get(instr.src1, SSAVariable(instr.src1, 0))
                src2 = self.current_def.get(instr.src2, SSAVariable(instr.src2, 0))
                ssa_instructions.append(SSAInstruction(instr.op, dest, src1, src2))
                self.current_def[instr.dest] = dest
        
        return ssa_instructions

# Example
tac = [
    TACInstruction('assign', 'x', '10'),
    TACInstruction('assign', 'y', '3'),
    TACInstruction('+', 'z', 'x', 'y'),
]

builder = SSABuilder()
ssa = builder.convert(tac)
print("\nSSA form:")
for instr in ssa:
    print(instr)

CHAPTER 7: CODE GENERATION
x86 Assembly Generation
# Generate x86 assembly from intermediate representation.

class X86Generator:
    """Generate x86 assembly from TAC."""
    
    def __init__(self):
        self.output = []
        self.data_section = []
        self.string_counter = 0
    
    def emit(self, instruction):
        self.output.append(instruction)
    
    def generate(self, tac_instructions):
        self.emit(".section .data")
        for data in self.data_section:
            self.emit(data)
        
        self.emit("\n.section .text")
        self.emit(".globl main")
        self.emit("main:")
        self.emit("    pushq %rbp")
        self.emit("    movq %rsp, %rbp")
        
        for instr in tac_instructions:
            self.generate_instruction(instr)
        
        self.emit("    movq $0, %rax")
        self.emit("    popq %rbp")
        self.emit("    ret")
        
        return '\n'.join(self.output)
    
    def generate_instruction(self, instr):
        if instr.op == 'assign':
            if instr.src1.isdigit():
                self.emit(f"    movq ${instr.src1}, %rax")
                self.emit(f"    movq %rax, -{self.get_offset(instr.dest)}(%rbp)")
            else:
                self.emit(f"    movq -{self.get_offset(instr.src1)}(%rbp), %rax")
                self.emit(f"    movq %rax, -{self.get_offset(instr.dest)}(%rbp)")
        
        elif instr.op in ('+', '-', '*', '/'):
            self.emit(f"    movq -{self.get_offset(instr.src1)}(%rbp), %rax")
            self.emit(f"    movq -{self.get_offset(instr.src2)}(%rbp), %rcx")
            
            if instr.op == '+':
                self.emit("    addq %rcx, %rax")
            elif instr.op == '-':
                self.emit("    subq %rcx, %rax")
            elif instr.op == '*':
                self.emit("    imulq %rcx, %rax")
            elif instr.op == '/':
                self.emit("    cqto")
                self.emit("    idivq %rcx")
            
            self.emit(f"    movq %rax, -{self.get_offset(instr.dest)}(%rbp)")
    
    def get_offset(self, var):
        # Simple stack offset allocation
        return 8  # Simplified
    
    def add_string(self, string):
        self.string_counter += 1
        label = f".LC{self.string_counter}"
        self.data_section.append(f'{label}: .string "{string}"')
        return label

# Example
tac = [
    TACInstruction('assign', 'x', '10'),
    TACInstruction('assign', 'y', '20'),
    TACInstruction('+', 'z', 'x', 'y'),
]

generator = X86Generator()
assembly = generator.generate(tac)
print("x86 Assembly:")
print(assembly)

LLVM IR Generation
# LLVM IR: platform-independent intermediate representation.

class LLVMGenerator:
    """Generate LLVM IR from TAC."""
    
    def __init__(self):
        self.output = []
        self.temp_counter = 0
        self.var_map = {}
    
    def new_temp(self):
        self.temp_counter += 1
        return f"%t{self.temp_counter}"
    
    def generate(self, tac_instructions):
        self.output.append("; ModuleID = 'example'")
        self.output.append("target triple = \"x86_64-pc-linux-gnu\"\n")
        
        self.output.append("define i32 @main() {")
        self.output.append("entry:")
        
        for instr in tac_instructions:
            self.generate_instruction(instr)
        
        self.output.append("  ret i32 0")
        self.output.append("}")
        
        return '\n'.join(self.output)
    
    def generate_instruction(self, instr):
        if instr.op == 'assign':
            if instr.src1.isdigit():
                temp = self.new_temp()
                self.output.append(f"  {temp} = add i32 0, {instr.src1}")
                self.var_map[instr.dest] = temp
            else:
                self.var_map[instr.dest] = self.var_map.get(instr.src1, f"%{instr.src1}")
        
        elif instr.op in ('+', '-', '*', '/'):
            src1 = self.var_map.get(instr.src1, f"%{instr.src1}")
            src2 = self.var_map.get(instr.src2, f"%{instr.src2}")
            temp = self.new_temp()
            
            if instr.op == '+':
                self.output.append(f"  {temp} = add i32 {src1}, {src2}")
            elif instr.op == '-':
                self.output.append(f"  {temp} = sub i32 {src1}, {src2}")
            elif instr.op == '*':
                self.output.append(f"  {temp} = mul i32 {src1}, {src2}")
            elif instr.op == '/':
                self.output.append(f"  {temp} = sdiv i32 {src1}, {src2}")
            
            self.var_map[instr.dest] = temp

# Example
tac = [
    TACInstruction('assign', 'x', '10'),
    TACInstruction('assign', 'y', '20'),
    TACInstruction('+', 'z', 'x', 'y'),
]

generator = LLVMGenerator()
llvm_ir = generator.generate(tac)
print("\nLLVM IR:")
print(llvm_ir)

CHAPTER 8: OPTIMIZATION
Constant Folding and Propagation
# Constant folding: evaluate constant expressions at compile time.
# Constant propagation: replace variables with known constant values.

class Optimizer:
    """Apply optimizations to TAC."""
    
    def __init__(self):
        self.constants = {}
    
    def optimize(self, instructions):
        optimized = []
        
        for instr in instructions:
            # Constant propagation
            if instr.op == 'assign' and instr.src1 in self.constants:
                instr.src1 = str(self.constants[instr.src1])
            
            # Constant folding
            if instr.op in ('+', '-', '*', '/'):
                if instr.src1.isdigit() and instr.src2.isdigit():
                    val1 = int(instr.src1)
                    val2 = int(instr.src2)
                    
                    if instr.op == '+':
                        result = val1 + val2
                    elif instr.op == '-':
                        result = val1 - val2
                    elif instr.op == '*':
                        result = val1 * val2
                    elif instr.op == '/':
                        result = val1 // val2
                    
                    # Replace with constant
                    instr.op = 'assign'
                    instr.src1 = str(result)
                    instr.src2 = None
                    
                    # Track constant
                    self.constants[instr.dest] = result
            
            optimized.append(instr)
        
        return optimized

# Example
tac = [
    TACInstruction('assign', 'x', '10'),
    TACInstruction('assign', 'y', '20'),
    TACInstruction('+', 'z', 'x', 'y'),
    TACInstruction('+', 'w', 'z', '5'),
]

optimizer = Optimizer()
optimized = optimizer.optimize(tac)
print("Optimized TAC:")
for instr in optimized:
    print(instr)

Dead Code Elimination
# Remove code that doesn't affect program output.

class DeadCodeEliminator:
    """Remove dead code from TAC."""
    
    def __init__(self):
        self.used_vars = set()
    
    def analyze(self, instructions):
        """Find all used variables."""
        for instr in reversed(instructions):
            if instr.dest and instr.dest in self.used_vars:
                # This instruction is used
                if instr.src1:
                    self.used_vars.add(instr.src1)
                if instr.src2:
                    self.used_vars.add(instr.src2)
            elif instr.op in ('return', 'call', 'goto', 'if'):
                # Side effects - keep
                if instr.src1:
                    self.used_vars.add(instr.src1)
                if instr.src2:
                    self.used_vars.add(instr.src2)
    
    def eliminate(self, instructions):
        self.analyze(instructions)
        
        optimized = []
        for instr in instructions:
            if instr.dest is None or instr.dest in self.used_vars:
                optimized.append(instr)
        
        return optimized

# Example
tac = [
    TACInstruction('assign', 'x', '10'),
    TACInstruction('assign', 'y', '20'),  # Dead code
    TACInstruction('+', 'z', 'x', 'x'),
    TACInstruction('return', None, 'z'),
]

eliminator = DeadCodeEliminator()
optimized = eliminator.eliminate(tac)
print("\nAfter dead code elimination:")
for instr in optimized:
    print(instr)

CHAPTER 9: RUNTIME SYSTEMS
Garbage Collection (Mark and Sweep)
# Mark and sweep: trace reachable objects, free unreachable ones.

class GCObject:
    def __init__(self, size):
        self.size = size
        self.marked = False
        self.references = []

class GarbageCollector:
    """Simple mark-and-sweep garbage collector."""
    
    def __init__(self):
        self.objects = []
        self.roots = []
    
    def allocate(self, size):
        obj = GCObject(size)
        self.objects.append(obj)
        return obj
    
    def add_root(self, obj):
        if obj not in self.roots:
            self.roots.append(obj)
    
    def remove_root(self, obj):
        if obj in self.roots:
            self.roots.remove(obj)
    
    def mark(self, obj):
        """Mark object and all reachable objects."""
        if obj.marked:
            return
        obj.marked = True
        for ref in obj.references:
            self.mark(ref)
    
    def sweep(self):
        """Free unmarked objects."""
        freed = 0
        new_objects = []
        
        for obj in self.objects:
            if obj.marked:
                obj.marked = False  # Reset for next GC
                new_objects.append(obj)
            else:
                freed += obj.size
        
        self.objects = new_objects
        return freed
    
    def collect(self):
        """Run garbage collection."""
        # Mark phase
        for root in self.roots:
            self.mark(root)
        
        # Sweep phase
        freed = self.sweep()
        return freed

# Example
gc = GarbageCollector()
obj1 = gc.allocate(100)
obj2 = gc.allocate(200)
obj3 = gc.allocate(150)

obj1.references.append(obj2)
gc.add_root(obj1)

freed = gc.collect()
print(f"Garbage collected: {freed} bytes")
print(f"Objects remaining: {len(gc.objects)}")

Memory Management
# Stack vs heap allocation, reference counting.

class MemoryManager:
    """Simple memory manager with stack and heap."""
    
    def __init__(self):
        self.stack = []
        self.heap = {}
        self.heap_counter = 0
        self.ref_counts = {}
    
    def stack_alloc(self, size):
        """Allocate on stack."""
        ptr = len(self.stack)
        self.stack.extend([0] * size)
        return ptr
    
    def stack_free(self, ptr, size):
        """Free stack memory."""
        pass  # Stack automatically freed on function return
    
    def heap_alloc(self, size):
        """Allocate on heap."""
        self.heap_counter += 1
        ptr = self.heap_counter
        self.heap[ptr] = [0] * size
        self.ref_counts[ptr] = 1
        return ptr
    
    def heap_free(self, ptr):
        """Free heap memory."""
        if ptr in self.heap:
            del self.heap[ptr]
            del self.ref_counts[ptr]
    
    def incref(self, ptr):
        """Increment reference count."""
        if ptr in self.ref_counts:
            self.ref_counts[ptr] += 1
    
    def decref(self, ptr):
        """Decrement reference count, free if zero."""
        if ptr in self.ref_counts:
            self.ref_counts[ptr] -= 1
            if self.ref_counts[ptr] == 0:
                self.heap_free(ptr)

# Example
mm = MemoryManager()
stack_ptr = mm.stack_alloc(10)
heap_ptr = mm.heap_alloc(20)
mm.incref(heap_ptr)
mm.decref(heap_ptr)

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
JIT Compilation
# Just-In-Time compilation: compile to machine code at runtime.
# Used in: Java (HotSpot), JavaScript (V8), Python (PyPy), .NET (CLR).

class JITCompiler:
    """Conceptual JIT compiler."""
    
    def __init__(self):
        self.compiled_functions = {}
        self.execution_counts = {}
    
    def interpret(self, bytecode):
        """Interpret bytecode, track execution counts."""
        func_id = id(bytecode)
        self.execution_counts[func_id] = self.execution_counts.get(func_id, 0) + 1
        
        # If hot, compile to native code
        if self.execution_counts[func_id] > 100:
            native_code = self.compile(bytecode)
            self.compiled_functions[func_id] = native_code
            return self.execute_native(native_code)
        
        return self.execute_interpreted(bytecode)
    
    def compile(self, bytecode):
        """Compile bytecode to native code."""
        # Simplified: in reality, use LLVM or similar
        return f"native_code_for_{id(bytecode)}"
    
    def execute_native(self, native_code):
        """Execute compiled native code."""
        return f"Executed {native_code}"
    
    def execute_interpreted(self, bytecode):
        """Interpret bytecode."""
        return f"Interpreted {bytecode}"

Incremental Parsing
# Parse only changed parts of source code.
# Used in: IDEs, incremental compilers.

class IncrementalParser:
    """Incremental parser for IDE support."""
    
    def __init__(self):
        self.ast = None
        self.line_map = {}
    
    def parse_full(self, source):
        """Full parse."""
        self.ast = self._do_parse(source)
        return self.ast
    
    def parse_incremental(self, source, start_line, end_line):
        """Re-parse only changed lines."""
        # Find affected AST nodes
        affected_nodes = self._find_affected_nodes(start_line, end_line)
        
        # Re-parse only affected region
        new_source = self._extract_region(source, start_line, end_line)
        new_ast = self._do_parse(new_source)
        
        # Update AST
        self._update_ast(affected_nodes, new_ast)
        
        return self.ast
    
    def _do_parse(self, source):
        """Actual parsing logic."""
        pass
    
    def _find_affected_nodes(self, start_line, end_line):
        """Find AST nodes affected by changes."""
        pass
    
    def _extract_region(self, source, start_line, end_line):
        """Extract changed region."""
        lines = source.split('\n')
        return '\n'.join(lines[start_line:end_line])
    
    def _update_ast(self, affected_nodes, new_ast):
        """Update AST with new parse results."""
        pass

Compiler Tools and Frameworks
# LLVM: Industrial-strength compiler infrastructure
# ANTLR: Parser generator for Java, C#, Python, JavaScript
# Flex/Bison: Lexical analysis and parsing (C/C++)
# Tree-sitter: Incremental parsing for editors
# Roslyn: .NET compiler platform

# LLVM Example (C++):
# #include <llvm/IR/LLVMContext.h>
# #include <llvm/IR/Module.h>
# #include <llvm/IR/IRBuilder.h>
# 
# llvm::LLVMContext context;
# llvm::Module module("example", context);
# llvm::IRBuilder<> builder(context);

# ANTLR Example (grammar file):
# grammar Expr;
# prog: stat+;
# stat: expr ';' | ID '=' expr ';';
# expr: expr ('*'|'/') expr | expr ('+'|'-') expr | INT | ID;

Recommended Reading
# - "Compilers: Principles, Techniques, and Tools" (Dragon Book) by Aho et al.
# - "Engineering a Compiler" by Cooper and Torczon
# - "Modern Compiler Implementation in ML/Java/C" by Andrew Appel
# - "Crafting Interpreters" by Robert Nystrom (free online)
# - LLVM documentation: https://llvm.org/docs/

# End of Compiler Design Reference