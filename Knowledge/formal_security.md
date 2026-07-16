Formal Methods for Security & Protocol Verification Complete Reference
CHAPTER 1: GETTING STARTED WITH FORMAL METHODS IN SECURITY
Remarks
Formal methods use mathematical logic to specify, develop, and verify software and hardware systems. In security, they are crucial for proving correctness of cryptographic protocols, smart contracts, and access control policies. Key approaches: Model Checking (exhaustive state exploration), Theorem Proving (interactive proof assistants), Abstract Interpretation. Tools: TLA+ (Lamport), Coq, Isabelle/HOL, ProVerif (crypto protocols), F*, Dafny, Alloy.
Tools: Python (for scripting/bridging), TLA+ Toolbox, Coq Platform, ProVerif, Z3 (SMT solver).
Hello Formal Security
(* hello_security.tla *)
----------------------------- MODULE HelloSecurity -----------------------------
EXTENDS Integers, Sequences

(* A simple specification of a secure login attempt *)
VARIABLES 
    attempts,   (* Number of failed attempts *)
    locked      (* Is the account locked? *)

Init == 
    /\ attempts = 0
    /\ locked = FALSE

Next == 
    \/ /\ ~locked
       /\ attempts' = attempts + 1
       /\ locked' = IF attempts' >= 3 THEN TRUE ELSE FALSE
    \/ /\ locked
       /\ UNCHANGED <<attempts, locked>>

Spec == Init /\ [][Next]_<<attempts, locked>>

(* Safety Property: If locked, attempts must be >= 3 *)
Safety == locked => attempts >= 3

(* Liveness Property: Eventually, if we keep trying, it locks *)
EventuallyLocked == <> (locked)
=============================================================================
(* In TLC Model Checker:
   1. Create new spec from this module.
   2. Add 'Safety' as an invariant.
   3. Run model checker.
*)

Why Formal Methods for Security?
# 1. Eliminate Ambiguity: Natural language specs are prone to interpretation errors.
# 2. Prove Correctness: Mathematically guarantee properties like secrecy, authenticity.
# 3. Find Edge Cases: Model checkers explore all possible states, including rare race conditions.
# 4. Compliance: Required for high-assurance systems (Common Criteria EAL4+).

Common Security Properties
# Confidentiality: Secret data is never revealed to unauthorized parties.
# Integrity: Data cannot be modified without detection.
# Availability: System remains operational under attack.
# Authentication: Parties are who they claim to be.
# Non-repudiation: Actions cannot be denied later.

CHAPTER 2: MODEL CHECKING WITH TLA+
Modeling Cryptographic Protocols
# We model the protocol as a state machine.
# States: Messages sent/received, keys known, nonces generated.

----------------------------- MODULE NeedhamSchroeder -----------------------------
EXTENDS Integers, FiniteSets, Sequences

CONSTANTS Agents, Keys, Nonces
ASSUME \A k \in Keys : k \notin Agents

VARIABLES 
    sentMsgs,   (* Set of messages in transit *)
    knownKeys,  (* Keys known to each agent *)
    state       (* Current step of the protocol *)

(* Helper functions *)
Encrypt(m, k) == <<"Enc", m, k>>
Decrypt(c, k) == IF c[1] = "Enc" /\ c[3] = k THEN c[2] ELSE "Fail"

Init == 
    /\ sentMsgs = {}
    /\ knownKeys = [a \in Agents |-> {"PublicKey"}]
    /\ state = "Start"

(* Simplified NS Public Key Protocol Steps *)
Step1(a, b, na) == 
    /\ state = "Start"
    /\ a # b
    /\ na \in Nonces
    /\ sentMsgs' = sentMsgs \cup {<<"A", "B", Encrypt(<<na, a>>, PublicKey(b))>}
    /\ state' = "Step1Sent"

Step2(b, a, nb) == 
    /\ state = "Step1Sent"
    /\ <<na, a>> \in Decrypt(ReceivedMsg, PrivateKey(b)) (* Simplified *)
    /\ nb \in Nonces
    /\ sentMsgs' = sentMsgs \cup {<<"B", "A", Encrypt(<<na, nb, b>>, PublicKey(a))>}
    /\ state' = "Step2Sent"

(* ... more steps ... *)

Next == 
    \/ \E a, b, na : Step1(a, b, na)
    \/ \E b, a, nb : Step2(b, a, nb)

Spec == Init /\ [][Next]_<<sentMsgs, knownKeys, state>>

(* Secrecy Invariant: Nonce na is never known to intruder *)
Secrecy == \A na \in Nonces : na \notin knownKeys["Intruder"]
=============================================================================

Detecting Man-in-the-Middle Attacks
# Lowe's Attack on Needham-Schroeder:
# Intruder intercepts message, replays it with different identity.
# TLA+ can detect this by modeling an active intruder with Dolev-Yao capabilities.

IntruderCapabilities == 
    /\ CanIntercept
    /\ CanModify
    /\ CanReplay
    /\ CanComposeNewMessagesFromKnownParts

(* If TLC finds a counter-example to Secrecy, it provides the trace of the attack. *)

CHAPTER 3: THEOREM PROVING WITH COQ
Verifying Smart Contracts
# Coq allows us to prove properties of code directly.
# Example: A simple vault contract that only allows the owner to withdraw.

Require Import Arith.
Require Import List.
Import ListNotations.

(* Define the state of the vault *)
Record VaultState := {
  owner : nat;
  balance : nat;
  locked : bool
}.

(* Define operations *)
Definition withdraw (vs : VaultState) (amount : nat) (caller : nat) : option VaultState :=
  if eqb caller (owner vs) then
    if leb amount (balance vs) then
      Some {| owner := owner vs; balance := balance vs - amount; locked := locked vs |}
    else None
  else None.

(* Theorem: Balance never increases on withdrawal *)
Theorem withdraw_decreases_balance :
  forall vs amount caller vs',
    withdraw vs amount caller = Some vs' ->
    balance vs' <= balance vs.
Proof.
  intros vs amount caller vs' H.
  unfold withdraw in H.
  destruct (eqb_spec caller (owner vs)) as [Heq|Hneq].
  - destruct (leb_spec amount (balance vs)) as [Hle|Hgt].
    + inversion H. reflexivity.
    + discriminate.
  - discriminate.
Qed.

(* Theorem: Only owner can withdraw *)
Theorem withdraw_only_owner :
  forall vs amount caller vs',
    withdraw vs amount caller = Some vs' ->
    caller = owner vs.
Proof.
  intros vs amount caller vs' H.
  unfold withdraw in H.
  destruct (eqb_spec caller (owner vs)) as [Heq|Hneq].
  - assumption.
  - discriminate.
Qed.

Verifying Cryptographic Implementations
# Using Coq to verify constant-time implementation of AES S-Box.
# Prevents timing side-channels.

Require Import Bool.
Require Import Arith.

(* Constant-time lookup table *)
Definition ct_lookup (table : list nat) (index : nat) : nat :=
  fold_left (fun acc x => x) (firstn index table) 0. (* Simplified *)

(* Property: Execution time does not depend on index *)
(* This requires defining a cost model in Coq, which is complex. *)
(* Instead, we prove functional correctness first. *)

CHAPTER 4: PROTOCOL VERIFICATION WITH PROVERIF
ProVerif Basics
# ProVerif is specialized for cryptographic protocols.
# Uses Pi-Calculus with extensions for crypto.

(* Simple authentication protocol *)
free c: channel.
free skey: key [private].
free pkey: key.

let processA() =
  let msg = "Hello" in
  out(c, encrypt(msg, pkey));
  in(c, x);
  let y = decrypt(x, skey) in
  event endA(y).

let processB() =
  in(c, z);
  let w = decrypt(z, skey) in
  out(c, encrypt(w, pkey));
  event endB(w).

process !processA() | !processB()

(* Query: Is the session secret? *)
query attacker(skey).
(* Query: Does B authenticate A? *)
query inj-event(endB(x)) ==> inj-event(endA(x)).

Symbolic vs Computational Models
# Symbolic (Dolev-Yao): Crypto is perfect algebra. Fast, good for logic flaws.
# Computational: Crypto is probabilistic functions. Harder, but more realistic.
# ProVerif uses symbolic model.

CHAPTER 5: ACCESS CONTROL POLICIES
Alloy for Access Control
# Alloy is great for modeling structural constraints.

sig User, Resource, Role {
  permissions: set Permission
}

sig Permission {
  action: one Action,
  resource: one Resource
}

sig Action {}

fact Policy {
  // Each user has at least one role
  all u: User | some u.permissions
  
  // No user can have both Read and Write on same resource if restricted
  no u: User, r: Resource | 
    (Read->r in u.permissions) and (Write->r in u.permissions) and Restricted[r]
}

pred ShowConflict {
  some u: User, r: Resource | 
    (Read->r in u.permissions) and (Write->r in u.permissions)
}

run ShowConflict for 5

Finding Privilege Escalation Paths
# Use Alloy to find if a user can gain higher privileges through role combinations.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Verified Compilers
# CompCert: C compiler verified in Coq.
# Ensures compiled code preserves semantics of source code.

Information Flow Control
# Jif: Java with information flow labels.
# Prevents leaks from high-security variables to low-security outputs.

Quantum Protocol Verification
# Verifying QKD (Quantum Key Distribution) protocols.
# Requires extending formal models with quantum mechanics.

Recommended Reading
# - "Specifying Systems" by Leslie Lamport
# - "Software Foundations" series by Pierce et al.
# - "Principles of Security" by Schneider
# - ProVerif Manual: https://proverif.inria.fr/
# - TLA+ Hyperproof: https://lamport.azurewebsites.net/tla/hyperproof.html

# End of Formal Methods for Security Reference