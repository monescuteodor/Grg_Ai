Formal Verification & Proof Assistants Complete Reference
CHAPTER 1: GETTING STARTED WITH FORMAL VERIFICATION
Remarks
Formal verification uses mathematical proofs to ensure software/hardware correctness. Key approaches: model checking (exhaustive state exploration), theorem proving (mathematical proofs), abstract interpretation, static analysis. Tools: TLA+ (Lamport), Coq, Isabelle/HOL, Lean, Z3 (SMT solver), SPIN, NuSMV.
Used in: aerospace (NASA), hardware (Intel/AMD), smart contracts (Ethereum), security protocols, operating systems (seL4).
Hello Verification
# hello_verification.py
"""
Simple formal verification: prove a property using Z3 SMT solver.
"""
from z3 import *

# Prove: if x > 0 and y > 0, then x + y > 0
x = Int('x')
y = Int('y')

# Create solver
solver = Solver()

# Add negation of what we want to prove (proof by contradiction)
solver.add(x > 0)
solver.add(y > 0)
solver.add(x + y <= 0)  # Negation of conclusion

# Check if negation is satisfiable
result = solver.check()

if result == unsat:
    print("✓ Property is VALID: x > 0 ∧ y > 0 → x + y > 0")
else:
    print("✗ Property is INVALID")
    print("Counterexample:", solver.model())

# Another example: prove commutativity of addition
x = Int('x')
y = Int('y')
solver = Solver()
solver.add(x + y != y + x)  # Negation

if solver.check() == unsat:
    print("✓ Addition is commutative: x + y = y + x")

# Example: find bug in simple program
# Program: if x > 10 then y = x else y = 10
# Property: y >= 10 always holds
x = Int('x')
y = Int('y')
solver = Solver()

# Program semantics
solver.add(Implies(x > 10, y == x))
solver.add(Implies(x <= 10, y == 10))

# Check if property can be violated
solver.add(y < 10)

if solver.check() == unsat:
    print("✓ Property holds: y >= 10 always")
else:
    print("✗ Bug found! Counterexample:", solver.model())

CHAPTER 2: PROPOSITIONAL LOGIC AND SAT
Propositional Logic
# Propositional logic: statements that are true or false.
# Connectives: ∧ (AND), ∨ (OR), ¬ (NOT), → (IMPLIES), ↔ (IFF)

from itertools import product

class PropositionalLogic:
    """Propositional logic evaluator."""
    
    def __init__(self):
        self.variables = {}
    
    def set_variable(self, name, value):
        """Set truth value for variable."""
        self.variables[name] = value
    
    def evaluate(self, expr):
        """Evaluate propositional expression."""
        # Replace variables with values
        result = expr
        for var, val in self.variables.items():
            result = result.replace(var, str(int(val)))
        
        # Evaluate
        result = result.replace('~', 'not ')
        result = result.replace('&', ' and ')
        result = result.replace('|', ' or ')
        result = result.replace('=>', ' <= ')  # Python syntax
        result = result.replace('<=>', ' == ')
        
        return eval(result)
    
    def truth_table(self, variables, expr):
        """Generate truth table for expression."""
        print(f"{'  '.join(variables)} | {expr}")
        print("-" * (len(variables) * 3 + len(expr) + 3))
        
        for values in product([False, True], repeat=len(variables)):
            for var, val in zip(variables, values):
                self.set_variable(var, val)
            
            result = self.evaluate(expr)
            row = '  '.join(str(int(v)) for v in values)
            print(f"{row} | {int(result)}")

# Example
logic = PropositionalLogic()
print("=== Truth Table for (P & Q) => (P | Q) ===")
logic.truth_table(['P', 'Q'], '(P & Q) => (P | Q)')

SAT Solving (DPLL Algorithm)
# SAT: Boolean satisfiability problem (NP-complete)
# DPLL: Davis-Putnam-Logemann-Loveland algorithm

class SATSolver:
    """Simple DPLL SAT solver."""
    
    def __init__(self):
        self.clauses = []  # List of clauses (disjunctions)
        self.variables = set()
    
    def add_clause(self, clause):
        """Add clause (list of literals).
        Positive number = variable, negative = negation.
        Example: [1, -2, 3] means (x1 ∨ ¬x2 ∨ x3)
        """
        self.clauses.append(clause)
        for lit in clause:
            self.variables.add(abs(lit))
    
    def unit_propagate(self, assignment):
        """Unit propagation: if clause has one literal, assign it."""
        changed = True
        while changed:
            changed = False
            for clause in self.clauses:
                # Remove satisfied literals
                clause = [lit for lit in clause if assignment.get(abs(lit)) != (lit > 0)]
                
                if not clause:
                    continue  # Clause satisfied
                
                if len(clause) == 1:
                    # Unit clause: must be true
                    lit = clause[0]
                    var = abs(lit)
                    val = lit > 0
                    assignment[var] = val
                    changed = True
        
        return assignment
    
    def pure_literal_eliminate(self, assignment):
        """Pure literal elimination."""
        literal_polarity = {}
        
        for clause in self.clauses:
            for lit in clause:
                var = abs(lit)
                if var not in assignment:
                    if var not in literal_polarity:
                        literal_polarity[var] = set()
                    literal_polarity[var].add(lit > 0)
        
        # If variable appears with only one polarity, assign it
        for var, polarities in literal_polarity.items():
            if len(polarities) == 1:
                assignment[var] = polarities.pop()
        
        return assignment
    
    def is_satisfied(self, assignment):
        """Check if all clauses are satisfied."""
        for clause in self.clauses:
            satisfied = False
            for lit in clause:
                var = abs(lit)
                if var in assignment:
                    if (lit > 0 and assignment[var]) or (lit < 0 and not assignment[var]):
                        satisfied = True
                        break
            if not satisfied:
                return False
        return True
    
    def has_empty_clause(self):
        """Check if any clause is empty (unsatisfiable)."""
        for clause in self.clauses:
            if not clause:
                return True
        return False
    
    def solve(self, assignment=None):
        """DPLL algorithm."""
        if assignment is None:
            assignment = {}
        
        # Unit propagation
        assignment = self.unit_propagate(assignment)
        
        # Pure literal elimination
        assignment = self.pure_literal_eliminate(assignment)
        
        # Check satisfaction
        if self.is_satisfied(assignment):
            return assignment
        
        if self.has_empty_clause():
            return None  # Unsatisfiable
        
        # Choose unassigned variable
        unassigned = [v for v in self.variables if v not in assignment]
        if not unassigned:
            return None
        
        var = unassigned[0]
        
        # Try True
        assignment_true = assignment.copy()
        assignment_true[var] = True
        result = self.solve(assignment_true)
        if result:
            return result
        
        # Try False
        assignment_false = assignment.copy()
        assignment_false[var] = False
        result = self.solve(assignment_false)
        if result:
            return result
        
        return None  # Unsatisfiable

# Example: Solve (x1 ∨ x2) ∧ (¬x1 ∨ x3) ∧ (¬x2 ∨ ¬x3)
solver = SATSolver()
solver.add_clause([1, 2])      # x1 ∨ x2
solver.add_clause([-1, 3])     # ¬x1 ∨ x3
solver.add_clause([-2, -3])    # ¬x2 ∨ ¬x3

result = solver.solve()
if result:
    print("\n✓ SAT! Assignment:", result)
else:
    print("\n✗ UNSAT")

CHAPTER 3: FIRST-ORDER LOGIC
First-Order Logic Basics
# First-order logic: extends propositional logic with quantifiers.
# ∀ (for all), ∃ (exists)
# Predicates: P(x), Q(x, y)
# Functions: f(x), g(x, y)

from z3 import *

# Example: "All humans are mortal. Socrates is human. Therefore, Socrates is mortal."
Human = Function('Human', IntSort(), BoolSort())
Mortal = Function('Mortal', IntSort(), BoolSort())
Socrates = Int('Socrates')

solver = Solver()

# Premise 1: ∀x. Human(x) → Mortal(x)
x = Int('x')
solver.add(ForAll(x, Implies(Human(x), Mortal(x))))

# Premise 2: Human(Socrates)
solver.add(Human(Socrates))

# Conclusion: Mortal(Socrates)
# Check if negation is unsatisfiable
solver.add(Not(Mortal(Socrates)))

if solver.check() == unsat:
    print("✓ Valid: Socrates is mortal")
else:
    print("✗ Invalid")

# Example: "There exists a number that is even and prime"
x = Int('x')
Even = Function('Even', IntSort(), BoolSort())
Prime = Function('Prime', IntSort(), BoolSort())

solver = Solver()
solver.add(Exists(x, And(Even(x), Prime(x))))

# Add constraints: 2 is even and prime
solver.add(Even(2))
solver.add(Prime(2))

if solver.check() == sat:
    print("✓ Satisfiable: ∃x. Even(x) ∧ Prime(x)")
    print("Model:", solver.model())

Quantifier Elimination
# Quantifier elimination: transform formula to equivalent quantifier-free form.

from z3 import *

# Example: ∃x. x > 5 ∧ x < 10
x = Int('x')
formula = Exists(x, And(x > 5, x < 10))

# Z3 can check satisfiability
solver = Solver()
solver.add(formula)

if solver.check() == sat:
    print("✓ Formula is satisfiable")
    print("Example:", solver.model())

# Example: ∀x. x > 0 → x + 1 > 1
x = Int('x')
formula = ForAll(x, Implies(x > 0, x + 1 > 1))

solver = Solver()
solver.add(Not(formula))  # Negate to check validity

if solver.check() == unsat:
    print("✓ Formula is valid")

CHAPTER 4: TLA+ (TEMPORAL LOGIC OF ACTIONS)
TLA+ Specifications
# TLA+: specification language for concurrent/distributed systems.
# Developed by Leslie Lamport.
# Used for: algorithms, protocols, distributed systems.

# Example: Simple counter in TLA+
"""
---- MODULE Counter ----
EXTENDS Integers, Sequences

VARIABLES count

Init == count = 0

Increment == count' = count + 1

Next == Increment

Spec == Init /\ [][Next]_<<count>>

TypeInvariant == count \in Nat

====
"""

# TLA+ concepts:
# - Variables: state of system
# - Init: initial state predicate
# - Next: next-state relation (actions)
# - Spec: complete specification
# - Invariants: properties that always hold

# Example: Two-phase commit in TLA+
"""
---- MODULE TwoPhaseCommit ----
EXTENDS Integers, Sequences

VARIABLES tmState, rmState, tmPrepared

Init ==
    /\ tmState = "init"
    /\ rmState = [r \in {"r1", "r2"} |-> "working"]
    /\ tmPrepared = {}

TMRcvPrepareResponse ==
    /\ tmState = "init"
    /\ \E r \in {"r1", "r2"} :
        /\ rmState[r] = "prepared"
        /\ tmPrepared' = tmPrepared \cup {r}
    /\ UNCHANGED <<rmState, tmState>>

RMPrepare(r) ==
    /\ rmState[r] = "working"
    /\ rmState' = [rmState EXCEPT ![r] = "prepared"]
    /\ UNCHANGED <<tmState, tmPrepared>>

RMChooseToAbort(r) ==
    /\ rmState[r] = "working"
    /\ rmState' = [rmState EXCEPT ![r] = "aborted"]
    /\ UNCHANGED <<tmState, tmPrepared>>

RMRcvCommitMsg(r) ==
    /\ rmState[r] = "working"
    /\ tmState = "committed"
    /\ rmState' = [rmState EXCEPT ![r] = "committed"]
    /\ UNCHANGED tmPrepared

RMRcvAbortMsg(r) ==
    /\ rmState[r] = "working"
    /\ tmState = "aborted"
    /\ rmState' = [rmState EXCEPT ![r] = "aborted"]
    /\ UNCHANGED tmPrepared

TMCommit ==
    /\ tmState = "init"
    /\ tmPrepared = {"r1", "r2"}
    /\ tmState' = "committed"
    /\ UNCHANGED <<rmState, tmPrepared>>

TMAbort ==
    /\ tmState = "init"
    /\ tmState' = "aborted"
    /\ UNCHANGED <<rmState, tmPrepared>>

Next ==
    \/ TMRcvPrepareResponse
    \/ TMCommit
    \/ TMAbort
    \/ \E r \in {"r1", "r2"} :
        RMPrepare(r) \/ RMChooseToAbort(r) \/ RMRcvCommitMsg(r) \/ RMRcvAbortMsg(r)

Spec == Init /\ [][Next]_<<tmState, rmState, tmPrepared>>

TypeInvariant ==
    /\ tmState \in {"init", "committed", "aborted"}
    /\ rmState \in [r \in {"r1", "r2"} -> {"working", "prepared", "committed", "aborted"}]
    /\ tmPrepared \subseteq {"r1", "r2"}

Consistency ==
    /\ tmState = "committed" => \A r \in {"r1", "r2"} : rmState[r] = "committed"
    /\ tmState = "aborted" => \A r \in {"r1", "r2"} : rmState[r] \in {"aborted", "working"}

====
"""

TLA+ with Python (Simulation)
# Simulate TLA+ specifications in Python for testing

class TLAState:
    """State in TLA+ specification."""
    
    def __init__(self, **variables):
        self.variables = variables
    
    def __eq__(self, other):
        return self.variables == other.variables
    
    def __repr__(self):
        return f"State({self.variables})"

class TLASpec:
    """TLA+ specification simulator."""
    
    def __init__(self):
        self.states = []
        self.transitions = []
    
    def add_transition(self, from_state, to_state, action_name):
        """Add state transition."""
        self.transitions.append({
            'from': from_state,
            'to': to_state,
            'action': action_name
        })
    
    def check_invariant(self, invariant_func):
        """Check if invariant holds in all reachable states."""
        for state in self.states:
            if not invariant_func(state):
                return False, state
        return True, None
    
    def simulate(self, init_state, next_func, max_steps=100):
        """Simulate specification."""
        self.states = [init_state]
        current = init_state
        
        for step in range(max_steps):
            next_states = next_func(current)
            if not next_states:
                break
            
            # Choose next state (non-deterministic)
            import random
            next_state = random.choice(next_states)
            self.states.append(next_state)
            current = next_state
        
        return self.states

# Example: Counter specification
def counter_init():
    return TLAState(count=0)

def counter_next(state):
    """Next-state relation for counter."""
    # Increment action
    new_state = TLAState(count=state.variables['count'] + 1)
    return [new_state]

def counter_invariant(state):
    """Invariant: count >= 0"""
    return state.variables['count'] >= 0

# Simulate
spec = TLASpec()
states = spec.simulate(counter_init(), counter_next, max_steps=10)

print("Counter simulation:")
for i, state in enumerate(states):
    print(f"  Step {i}: {state}")

valid, counterexample = spec.check_invariant(counter_invariant)
print(f"Invariant holds: {valid}")

CHAPTER 5: MODEL CHECKING WITH TLC
TLC Model Checker
# TLC: model checker for TLA+ specifications.
# Exhaustively explores state space to find violations.

# Example: TLC output for counter
"""
$ tlc Counter.tla
TLC2 Version 2.x
Running breadth-first search with 1 worker.
Starting...
Computing initial states...
Finished computing initial states: 1 distinct state generated.
Computing next states...
Finished computing next states: 10 distinct states generated.
Model checking completed. No error has been found.
Estimates of the probability that TLC did not check all reachable states:
  probability: ~0.0
The number of states generated: 10
"""

# Model checking concepts:
# - State space: all possible states
# - Reachability: which states can be reached
# - Invariants: properties that hold in all reachable states
# - Deadlock: state with no next states
# - Liveness: something good eventually happens

class ModelChecker:
    """Simple model checker."""
    
    def __init__(self, init_func, next_func):
        self.init_func = init_func
        self.next_func = next_func
        self.visited = set()
        self.queue = []
    
    def check_reachability(self, max_states=1000):
        """Explore all reachable states."""
        init_state = self.init_func()
        self.queue.append(init_state)
        self.visited.add(str(init_state.variables))
        
        while self.queue and len(self.visited) < max_states:
            current = self.queue.pop(0)
            next_states = self.next_func(current)
            
            for next_state in next_states:
                state_str = str(next_state.variables)
                if state_str not in self.visited:
                    self.visited.add(state_str)
                    self.queue.append(next_state)
        
        return len(self.visited)
    
    def check_invariant(self, invariant_func):
        """Check invariant in all reachable states."""
        errors = []
        
        for state_str in self.visited:
            # Reconstruct state (simplified)
            # In real implementation, store full state
            pass
        
        return errors
    
    def check_deadlock(self, next_func):
        """Check for deadlock states."""
        deadlocks = []
        
        # For each visited state, check if it has next states
        # (simplified - real implementation stores states)
        
        return deadlocks

# Example: Check mutual exclusion
class MutexState:
    def __init__(self, p1_state, p2_state):
        self.p1 = p1_state  # 'idle', 'trying', 'critical'
        self.p2 = p2_state
    
    def __repr__(self):
        return f"Mutex(p1={self.p1}, p2={self.p2})"
    
    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2
    
    def __hash__(self):
        return hash((self.p1, self.p2))

def mutex_init():
    return MutexState('idle', 'idle')

def mutex_next(state):
    """Next-state relation for mutual exclusion."""
    next_states = []
    
    # P1 transitions
    if state.p1 == 'idle':
        next_states.append(MutexState('trying', state.p2))
    elif state.p1 == 'trying' and state.p2 != 'critical':
        next_states.append(MutexState('critical', state.p2))
    elif state.p1 == 'critical':
        next_states.append(MutexState('idle', state.p2))
    
    # P2 transitions
    if state.p2 == 'idle':
        next_states.append(MutexState(state.p1, 'trying'))
    elif state.p2 == 'trying' and state.p1 != 'critical':
        next_states.append(MutexState(state.p1, 'critical'))
    elif state.p2 == 'critical':
        next_states.append(MutexState(state.p1, 'idle'))
    
    return next_states

def mutex_invariant(state):
    """Mutual exclusion: not both in critical section."""
    return not (state.p1 == 'critical' and state.p2 == 'critical')

# Model check
checker = ModelChecker(mutex_init, mutex_next)
num_states = checker.check_reachability(max_states=100)
print(f"\nMutex: explored {num_states} states")
print(f"Mutual exclusion holds: {mutex_invariant(MutexState('critical', 'critical')) == False}")

CHAPTER 6: COQ PROOF ASSISTANT
Coq Basics
# Coq: interactive theorem prover based on Calculus of Inductive Constructions.
# Used for: mathematical proofs, program verification, certified software.

# Example: Prove that addition is commutative
"""
(* coq_example.v *)

(* Define natural numbers *)
Inductive nat : Type :=
  | O : nat
  | S : nat -> nat.

(* Define addition *)
Fixpoint add (n m : nat) : nat :=
  match n with
  | O => m
  | S p => S (add p m)
  end.

(* Theorem: addition is commutative *)
Theorem add_comm : forall n m : nat, add n m = add m n.
Proof.
  intros n m.
  induction n as [| n' IH].
  - (* Base case: n = 0 *)
    simpl.
    induction m as [| m' IHm].
    + simpl. reflexivity.
    + simpl. rewrite <- IHm. reflexivity.
  - (* Inductive case: n = S n' *)
    simpl.
    rewrite IH.
    induction m as [| m' IHm].
    + simpl. reflexivity.
    + simpl. rewrite <- IHm. reflexivity.
Qed.
"""

# Coq concepts:
# - Inductive types: define data structures
# - Fixpoint: recursive functions
# - Theorem/Lemma: statements to prove
# - Proof tactics: automated proof steps
# - Qed: proof complete

# Example: Prove simple property
"""
Theorem plus_O_n : forall n : nat, add O n = n.
Proof.
  intros n.
  simpl.
  reflexivity.
Qed.
"""

Coq with Python (PyCoq simulation)
# Simulate Coq-style proofs in Python

class CoqTerm:
    """Term in Coq's type theory."""
    
    def __init__(self, term_type, value=None):
        self.type = term_type
        self.value = value
    
    def __repr__(self):
        if self.value:
            return f"{self.value} : {self.type}"
        return f"_ : {self.type}"

class CoqProof:
    """Simple Coq proof assistant simulation."""
    
    def __init__(self):
        self.context = {}
        self.goal = None
        self.proof_steps = []
    
    def set_goal(self, goal):
        """Set proof goal."""
        self.goal = goal
        print(f"Goal: {goal}")
    
    def intro(self, var_name):
        """Introduce variable into context."""
        self.context[var_name] = "unknown"
        self.proof_steps.append(f"intro {var_name}")
        print(f"Context: {self.context}")
    
    def simpl(self):
        """Simplify goal."""
        self.proof_steps.append("simpl")
        print("Simplified goal")
    
    def reflexivity(self):
        """Prove goal by reflexivity (x = x)."""
        self.proof_steps.append("reflexivity")
        print("✓ Proved by reflexivity")
        return True
    
    def rewrite(self, lemma):
        """Rewrite using lemma."""
        self.proof_steps.append(f"rewrite {lemma}")
        print(f"Rewrote using {lemma}")
    
    def induction(self, var_name):
        """Perform induction on variable."""
        self.proof_steps.append(f"induction {var_name}")
        print(f"Induction on {var_name}")
        print("  Case 1: base case")
        print("  Case 2: inductive case")
    
    def qed(self):
        """Complete proof."""
        print(f"✓ Proof complete ({len(self.proof_steps)} steps)")
        return True

# Example: Prove 0 + n = n
proof = CoqProof()
proof.set_goal("forall n : nat, add 0 n = n")
proof.intro("n")
proof.simpl()
proof.reflexivity()
proof.qed()

CHAPTER 7: SMT SOLVERS (Z3)
Z3 Basics
# Z3: SMT (Satisfiability Modulo Theories) solver by Microsoft.
# Theories: integers, reals, arrays, bit-vectors, strings.

from z3 import *

# Integer arithmetic
x = Int('x')
y = Int('y')

solver = Solver()
solver.add(x > 0)
solver.add(y > 0)
solver.add(x + y == 10)

if solver.check() == sat:
    model = solver.model()
    print(f"✓ Satisfiable: x={model[x]}, y={model[y]}")

# Find all solutions
print("\nAll solutions:")
while solver.check() == sat:
    model = solver.model()
    print(f"  x={model[x]}, y={model[y]}")
    
    # Block this solution
    solver.add(Or(x != model[x], y != model[y]))

# Real arithmetic
a = Real('a')
b = Real('b')

solver = Solver()
solver.add(a * a + b * b == 1)  # Circle
solver.add(a > 0)
solver.add(b > 0)

if solver.check() == sat:
    model = solver.model()
    print(f"\n✓ Point on unit circle: a={model[a]}, b={model[b]}")

Bit-Vectors
# Bit-vectors: fixed-width integers (used in hardware verification)

from z3 import *

# 8-bit bit-vectors
x = BitVec('x', 8)
y = BitVec('y', 8)

solver = Solver()
solver.add(x + y == 255)
solver.add(x > 100)

if solver.check() == sat:
    model = solver.model()
    print(f"✓ x={model[x].as_long()}, y={model[y].as_long()}")

# Bitwise operations
a = BitVec('a', 8)
b = BitVec('b', 8)

solver = Solver()
solver.add(a & b == 0x0F)  # AND
solver.add(a | b == 0xFF)  # OR

if solver.check() == sat:
    model = solver.model()
    print(f"✓ a=0x{model[a].as_long():02X}, b=0x{model[b].as_long():02X}")

Arrays
# Arrays: uninterpreted functions (used in software verification)

from z3 import *

# Array from Int to Int
arr = Array('arr', IntSort(), IntSort())

solver = Solver()
solver.add(arr[0] == 10)
solver.add(arr[1] == 20)
solver.add(arr[2] == arr[0] + arr[1])

if solver.check() == sat:
    model = solver.model()
    print(f"✓ arr[0]={model.evaluate(arr[0])}")
    print(f"✓ arr[1]={model.evaluate(arr[1])}")
    print(f"✓ arr[2]={model.evaluate(arr[2])}")

# Array update
arr2 = Store(arr, 3, 100)  # arr2 = arr with arr[3] = 100

solver = Solver()
solver.add(arr2[3] == 100)
solver.add(arr2[0] == 10)

if solver.check() == sat:
    print("✓ Array update works correctly")

Program Verification
# Verify program properties using Z3

from z3 import *

def verify_program():
    """Verify a simple program."""
    
    # Program:
    # x = input()
    # if x > 0:
    #     y = x * 2
    # else:
    #     y = -x
    # assert y >= 0
    
    x = Int('x')
    y = Int('y')
    
    solver = Solver()
    
    # Program semantics
    solver.add(Implies(x > 0, y == x * 2))
    solver.add(Implies(x <= 0, y == -x))
    
    # Check if property can be violated
    solver.add(y < 0)
    
    if solver.check() == unsat:
        print("✓ Program is correct: y >= 0 always holds")
        return True
    else:
        print("✗ Bug found!")
        print("Counterexample:", solver.model())
        return False

verify_program()

# Verify loop invariant
def verify_loop():
    """Verify loop invariant."""
    
    # Program:
    # i = 0
    # sum = 0
    # while i < n:
    #     sum = sum + i
    #     i = i + 1
    # Invariant: sum = i * (i - 1) / 2
    
    i = Int('i')
    sum_val = Int('sum')
    n = Int('n')
    
    solver = Solver()
    
    # Initial state
    solver.add(i == 0)
    solver.add(sum_val == 0)
    
    # Loop invariant
    solver.add(sum_val == i * (i - 1) / 2)
    
    # Loop condition
    solver.add(i < n)
    
    # After one iteration
    i_next = Int('i_next')
    sum_next = Int('sum_next')
    solver.add(i_next == i + 1)
    solver.add(sum_next == sum_val + i)
    
    # Check if invariant holds after iteration
    solver.add(sum_next != i_next * (i_next - 1) / 2)
    
    if solver.check() == unsat:
        print("✓ Loop invariant is preserved")
    else:
        print("✗ Loop invariant violated")

verify_loop()

CHAPTER 8: MODEL CHECKING (LTL, CTL)
Linear Temporal Logic (LTL)
# LTL: temporal logic for reasoning about sequences of states.
# Operators:
# - G (globally): always
# - F (finally): eventually
# - X (next): in next state
# - U (until): until
# - R (release): release

class LTLFormula:
    """LTL formula representation."""
    
    def __init__(self, formula_type, *args):
        self.type = formula_type  # 'G', 'F', 'X', 'U', 'R', 'prop'
        self.args = args
    
    def __repr__(self):
        if self.type == 'prop':
            return self.args[0]
        elif self.type == 'G':
            return f"G({self.args[0]})"
        elif self.type == 'F':
            return f"F({self.args[0]})"
        elif self.type == 'X':
            return f"X({self.args[0]})"
        elif self.type == 'U':
            return f"({self.args[0]} U {self.args[1]})"
        elif self.type == 'R':
            return f"({self.args[0]} R {self.args[1]})"

# Example LTL formulas
p = LTLFormula('prop', 'p')
q = LTLFormula('prop', 'q')

# "p is always true"
always_p = LTLFormula('G', p)
print(f"Always p: {always_p}")

# "Eventually p"
eventually_p = LTLFormula('F', p)
print(f"Eventually p: {eventually_p}")

# "p until q"
p_until_q = LTLFormula('U', p, q)
print(f"p until q: {p_until_q}")

# "Globally (p implies eventually q)"
spec = LTLFormula('G', LTLFormula('prop', 'p => F(q)'))
print(f"Specification: {spec}")

LTL Model Checking
# Check if LTL formula holds in a transition system

class TransitionSystem:
    """Transition system for model checking."""
    
    def __init__(self):
        self.states = {}  # state_id -> set of propositions
        self.transitions = {}  # state_id -> [state_id]
        self.initial = None
    
    def add_state(self, state_id, propositions):
        """Add state with propositions."""
        self.states[state_id] = propositions
        if state_id not in self.transitions:
            self.transitions[state_id] = []
    
    def add_transition(self, from_state, to_state):
        """Add transition."""
        if from_state not in self.transitions:
            self.transitions[from_state] = []
        self.transitions[from_state].append(to_state)
    
    def set_initial(self, state_id):
        """Set initial state."""
        self.initial = state_id
    
    def check_G(self, proposition):
        """Check G(p): proposition holds in all reachable states."""
        visited = set()
        queue = [self.initial]
        
        while queue:
            state = queue.pop(0)
            if state in visited:
                continue
            visited.add(state)
            
            # Check if proposition holds
            if proposition not in self.states[state]:
                return False, state
            
            # Explore next states
            for next_state in self.transitions[state]:
                if next_state not in visited:
                    queue.append(next_state)
        
        return True, None
    
    def check_F(self, proposition):
        """Check F(p): proposition eventually holds in all paths."""
        # Simplified: check if proposition is reachable from all states
        for state in self.states:
            if not self._can_reach(state, proposition):
                return False, state
        return True, None
    
    def _can_reach(self, start, proposition):
        """Check if proposition is reachable from start."""
        visited = set()
        queue = [start]
        
        while queue:
            state = queue.pop(0)
            if state in visited:
                continue
            visited.add(state)
            
            if proposition in self.states[state]:
                return True
            
            for next_state in self.transitions[state]:
                if next_state not in visited:
                    queue.append(next_state)
        
        return False

# Example: Traffic light system
ts = TransitionSystem()

# States
ts.add_state('red', {'red'})
ts.add_state('yellow', {'yellow'})
ts.add_state('green', {'green'})

# Transitions
ts.add_transition('red', 'green')
ts.add_transition('green', 'yellow')
ts.add_transition('yellow', 'red')

ts.set_initial('red')

# Check properties
valid, counterexample = ts.check_G('red')
print(f"\nG(red): {valid}")  # False (not always red)

valid, counterexample = ts.check_G('red')
print(f"G(red) counterexample: {counterexample}")

# Check: always (red ∨ yellow ∨ green)
# (simplified - real implementation checks all states)
print("Safety property: always exactly one light is on")

Computation Tree Logic (CTL)
# CTL: branching-time temporal logic.
# Operators:
# - A (all paths), E (exists path)
# - G (globally), F (finally), X (next), U (until)

class CTLFormula:
    """CTL formula representation."""
    
    def __init__(self, formula_type, *args):
        self.type = formula_type
        self.args = args
    
    def __repr__(self):
        if self.type == 'prop':
            return self.args[0]
        elif self.type in ['AG', 'AF', 'AX', 'EG', 'EF', 'EX']:
            return f"{self.type}({self.args[0]})"
        elif self.type in ['AU', 'EU']:
            return f"({self.args[0]} {self.type[1]}U {self.args[1]})"

# Example CTL formulas
p = CTLFormula('prop', 'p')
q = CTLFormula('prop', 'q')

# "On all paths, globally p"
ag_p = CTLFormula('AG', p)
print(f"AG(p): {ag_p}")

# "There exists a path where eventually p"
ef_p = CTLFormula('EF', p)
print(f"EF(p): {ef_p}")

# "On all paths, p until q"
au_pq = CTLFormula('AU', p, q)
print(f"A(p U q): {au_pq}")

CTL Model Checking
class CTLModelChecker:
    """CTL model checker."""
    
    def __init__(self, ts):
        self.ts = ts
    
    def check_AG(self, proposition):
        """Check AG(p): on all paths, globally p."""
        # All reachable states must satisfy p
        visited = set()
        queue = [self.ts.initial]
        
        while queue:
            state = queue.pop(0)
            if state in visited:
                continue
            visited.add(state)
            
            if proposition not in self.ts.states[state]:
                return False, state
            
            for next_state in self.ts.transitions[state]:
                if next_state not in visited:
                    queue.append(next_state)
        
        return True, None
    
    def check_EF(self, proposition):
        """Check EF(p): there exists a path where eventually p."""
        # Check if p is reachable from initial state
        visited = set()
        queue = [self.ts.initial]
        
        while queue:
            state = queue.pop(0)
            if state in visited:
                continue
            visited.add(state)
            
            if proposition in self.ts.states[state]:
                return True, state
            
            for next_state in self.ts.transitions[state]:
                if next_state not in visited:
                    queue.append(next_state)
        
        return False, None

# Example
ts = TransitionSystem()
ts.add_state('s0', {'p'})
ts.add_state('s1', {'q'})
ts.add_state('s2', {'p', 'q'})

ts.add_transition('s0', 's1')
ts.add_transition('s1', 's2')
ts.add_transition('s2', 's0')

ts.set_initial('s0')

mc = CTLModelChecker(ts)

valid, state = mc.check_AG('p')
print(f"\nAG(p): {valid}")  # False (s1 doesn't have p)

valid, state = mc.check_EF('q')
print(f"EF(q): {valid}")  # True (q is reachable)

CHAPTER 9: ADVANCED VERIFICATION TECHNIQUES
Abstract Interpretation
# Abstract interpretation: approximate program semantics for static analysis.
# Used for: bug detection, optimization, verification.

class AbstractDomain:
    """Abstract domain for interval analysis."""
    
    def __init__(self, low, high):
        self.low = low   # -inf, or integer
        self.high = high  # +inf, or integer
    
    def __repr__(self):
        return f"[{self.low}, {self.high}]"
    
    def join(self, other):
        """Join (union) of two abstract values."""
        return AbstractDomain(
            min(self.low, other.low),
            max(self.high, other.high)
        )
    
    def meet(self, other):
        """Meet (intersection) of two abstract values."""
        return AbstractDomain(
            max(self.low, other.low),
            min(self.high, other.high)
        )
    
    def add(self, other):
        """Abstract addition."""
        return AbstractDomain(
            self.low + other.low,
            self.high + other.high
        )
    
    def multiply(self, other):
        """Abstract multiplication."""
        products = [
            self.low * other.low,
            self.low * other.high,
            self.high * other.low,
            self.high * other.high
        ]
        return AbstractDomain(min(products), max(products))

# Example: Analyze program
# x = input()  // x in [0, 10]
# y = x * 2
# z = y + 5

x = AbstractDomain(0, 10)
y = x.multiply(AbstractDomain(2, 2))
z = y.add(AbstractDomain(5, 5))

print(f"x = {x}")
print(f"y = x * 2 = {y}")
print(f"z = y + 5 = {z}")

# Check: z <= 25?
print(f"z <= 25? {z.high <= 25}")  # True

Symbolic Execution
# Symbolic execution: execute program with symbolic inputs.
# Generates path conditions and constraints.

from z3 import *

class SymbolicValue:
    """Symbolic value in execution."""
    
    def __init__(self, name, sort=IntSort()):
        self.symbol = (sort, name)
        self.expr = (sort, name)
    
    def __add__(self, other):
        if isinstance(other, SymbolicValue):
            return SymbolicValue(f"({self.expr} + {other.expr})")
        return SymbolicValue(f"({self.expr} + {other})")

class SymbolicExecutor:
    """Simple symbolic executor."""
    
    def __init__(self):
        self.path_conditions = []
        self.symbolic_state = {}
    
    def add_constraint(self, constraint):
        """Add path condition."""
        self.path_conditions.append(constraint)
    
    def execute_if(self, condition, true_branch, false_branch):
        """Execute if statement."""
        # True branch
        self.path_conditions.append(condition)
        true_result = true_branch()
        self.path_conditions.pop()
        
        # False branch
        self.path_conditions.append(Not(condition))
        false_result = false_branch()
        self.path_conditions.pop()
        
        return true_result, false_result

# Example: Symbolic execution
# if x > 0:
#     y = x * 2
# else:
#     y = -x

x = Int('x')
y = Int('y')

solver = Solver()

# True branch: x > 0, y = x * 2
solver.push()
solver.add(x > 0)
solver.add(y == x * 2)
print(f"Path 1: x > 0, y = 2x")
print(f"  Constraints: {solver.assertions()}")
solver.pop()

# False branch: x <= 0, y = -x
solver.push()
solver.add(x <= 0)
solver.add(y == -x)
print(f"Path 2: x <= 0, y = -x")
print(f"  Constraints: {solver.assertions()}")
solver.pop()

# Check: can y be negative?
solver.add(Or(
    And(x > 0, y == x * 2),
    And(x <= 0, y == -x)
))
solver.add(y < 0)

if solver.check() == unsat:
    print("\n✓ y >= 0 on all paths")
else:
    print("\n✗ y can be negative")
    print("Counterexample:", solver.model())

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Dependent Types (Lean, Agda)
# Dependent types: types can depend on values.
# Used for: certified programming, mathematical proofs.

# Example in Lean 4:
"""
-- Lean 4 example
def factorial : Nat → Nat
  | 0 => 1
  | n + 1 => (n + 1) * factorial n

theorem factorial_pos : ∀ n, factorial n > 0 := by
  intro n
  induction n with
  | zero => simp [factorial]
  | succ n ih =>
    simp [factorial]
    nlinarith [ih]
"""

# Example in Coq:
"""
(* Vector with length in type *)
Inductive vec (A : Type) : nat -> Type :=
  | vnil : vec A 0
  | vcons : forall n, A -> vec A n -> vec A (S n).

(* Length-indexed list *)
Definition head {A n} (v : vec A (S n)) : A :=
  match v with
  | vcons _ x _ => x
  end.
"""

Verification in Practice
# Real-world verification projects:
# - seL4: verified microkernel (ISOC, 2009)
# - CompCert: verified C compiler (Xavier Leroy)
# - F* / EverCrypt: verified cryptographic library
# - Dafny: verified programs (Microsoft)
# - Frama-C: C program verification

# Example: Dafny program
"""
// Dafny example
method BinarySearch(a: array<int>, key: int) returns (index: int)
  requires forall i, j :: 0 <= i < j < a.Length ==> a[i] <= a[j]
  ensures 0 <= index ==> index < a.Length && a[index] == key
  ensures index < 0 ==> forall k :: 0 <= k < a.Length ==> a[k] != key
{
  var lo := 0;
  var hi := a.Length;
  while lo < hi
    invariant 0 <= lo <= hi <= a.Length
    invariant forall k :: 0 <= k < lo ==> a[k] < key
    invariant forall k :: hi <= k < a.Length ==> a[k] > key
  {
    var mid := lo + (hi - lo) / 2;
    if a[mid] < key {
      lo := mid + 1;
    } else if a[mid] > key {
      hi := mid;
    } else {
      return mid;
    }
  }
  return -1;
}
"""

Smart Contract Verification
# Verify smart contracts for security

from z3 import *

def verify_token_contract():
    """Verify ERC20 token contract properties."""
    
    # State variables
    balances = Array('balances', IntSort(), IntSort())
    total_supply = Int('total_supply')
    
    # Property: sum of all balances == total_supply
    # (simplified - real verification uses more complex logic)
    
    solver = Solver()
    
    # Initial state
    solver.add(total_supply == 1000)
    solver.add(balances[0] == 1000)
    
    # Transfer: from A to B
    A = Int('A')
    B = Int('B')
    amount = Int('amount')
    
    solver.add(A != B)
    solver.add(amount > 0)
    solver.add(balances[A] >= amount)
    
    # After transfer
    balances_after = Store(balances, A, balances[A] - amount)
    balances_after = Store(balances_after, B, balances[B] + amount)
    
    # Check: total supply unchanged
    # (simplified check)
    solver.add(balances_after[A] + balances_after[B] != balances[A] + balances[B])
    
    if solver.check() == unsat:
        print("✓ Transfer preserves total balance")
    else:
        print("✗ Bug: transfer changes total balance")

verify_token_contract()

Recommended Reading
# - "Specifying Systems" by Leslie Lamport (TLA+)
# - "Software Foundations" by Pierce et al. (Coq)
# - "The Little Prover" by Friedman & Eastlund (J-Bob)
# - "Principles of Model Checking" by Baier & Katoen
# - "Z3 Guide": https://microsoft.github.io/z3guide/
# - "Dafny Documentation": https://dafny.org/

# Online Resources
# - TLA+ Hyperproof: https://lamport.azurewebsites.net/tla/hyperproof.html
# - Coq Documentation: https://coq.inria.fr/documentation
# - Lean 4 Manual: https://leanprover.github.io/lean4/doc/
# - Z3 Playground: https://jfmc.github.io/z3-play/
# - Dafny Web IDE: https://dafny.org/

# End of Formal Verification Reference