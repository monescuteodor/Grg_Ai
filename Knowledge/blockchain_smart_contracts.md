Blockchain & Smart Contracts Complete Reference
CHAPTER 1: GETTING STARTED WITH BLOCKCHAIN
Remarks
Blockchain is a distributed, immutable ledger that enables trustless peer-to-peer transactions. Key concepts: consensus mechanisms (PoW, PoS), cryptographic hashing, digital signatures, smart contracts, decentralized applications (dApps). Major platforms: Bitcoin (cryptocurrency), Ethereum (smart contracts), Solana (high throughput), Polkadot (interoperability).
Tools: Python (educational implementations), Solidity (Ethereum smart contracts), Web3.py (Ethereum interaction), Hardhat/Foundry (development frameworks), Remix IDE (browser-based Solidity).
Hello Blockchain
# hello_blockchain.py
"""
Minimal blockchain implementation from scratch.
"""
import hashlib
import json
import time
from typing import List, Dict, Any

class Block:
    """A single block in the blockchain."""
    
    def __init__(self, index: int, transactions: List[Dict], previous_hash: str):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()
    
    def compute_hash(self) -> str:
        """Compute SHA-256 hash of block contents."""
        block_content = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_content.encode()).hexdigest()
    
    def __repr__(self):
        return f"Block(index={self.index}, hash={self.hash[:8]}...)"

class Blockchain:
    """Simple blockchain implementation."""
    
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict] = []
        self.difficulty = difficulty  # Number of leading zeros required
        self.mining_reward = 10.0
        
        # Create genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block."""
        genesis = Block(0, [], "0" * 64)
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)
        print(f"Genesis block created: {genesis}")
    
    def get_latest_block(self) -> Block:
        """Get the most recent block."""
        return self.chain[-1]
    
    def add_transaction(self, sender: str, recipient: str, amount: float):
        """Add a new transaction to the pending pool."""
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': time.time()
        })
    
    def mine_block(self, miner_address: str) -> Block:
        """Mine a new block with pending transactions."""
        # Add mining reward
        self.add_transaction("SYSTEM", miner_address, self.mining_reward)
        
        # Create new block
        prev_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions.copy(),
            previous_hash=prev_block.hash
        )
        
        # Proof of Work: find nonce that satisfies difficulty
        print(f"Mining block {new_block.index}...")
        while not new_block.hash.startswith('0' * self.difficulty):
            new_block.nonce += 1
            new_block.hash = new_block.compute_hash()
        
        print(f"Block mined! Nonce: {new_block.nonce}, Hash: {new_block.hash[:16]}...")
        
        # Add block to chain
        self.chain.append(new_block)
        self.pending_transactions.clear()
        
        return new_block
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            # Check hash
            if current.hash != current.compute_hash():
                print(f"Invalid hash at block {i}")
                return False
            
            # Check previous hash link
            if current.previous_hash != previous.hash:
                print(f"Broken chain at block {i}")
                return False
            
            # Check proof of work
            if not current.hash.startswith('0' * self.difficulty):
                print(f"Invalid proof of work at block {i}")
                return False
        
        return True

# Example
blockchain = Blockchain(difficulty=4)

# Add transactions
blockchain.add_transaction("Alice", "Bob", 5.0)
blockchain.add_transaction("Bob", "Charlie", 2.5)

# Mine block
block1 = blockchain.mine_block("Miner1")

# Add more transactions
blockchain.add_transaction("Charlie", "Alice", 1.0)
block2 = blockchain.mine_block("Miner1")

# Validate
print(f"\nChain valid: {blockchain.is_chain_valid()}")
print(f"Chain length: {len(blockchain.chain)}")

CHAPTER 2: CRYPTOGRAPHIC PRIMITIVES
Hash Functions
# Cryptographic hash: deterministic, fixed-size output, pre-image resistant.
# SHA-256: 256-bit output, used in Bitcoin.
# Keccak-256: used in Ethereum.

import hashlib

def sha256_hash(data: str) -> str:
    """Compute SHA-256 hash."""
    return hashlib.sha256(data.encode()).hexdigest()

def keccak256_hash(data: str) -> str:
    """Compute Keccak-256 hash (Ethereum)."""
    from Crypto.Hash import keccak
    k = keccak.new(digest_bits=256)
    k.update(data.encode())
    return k.hexdigest()

# Properties:
# 1. Deterministic: same input → same output
# 2. Fast computation
# 3. Pre-image resistant: can't reverse hash to input
# 4. Small changes → completely different hash (avalanche effect)
# 5. Collision resistant: hard to find two inputs with same hash

# Example: avalanche effect
print("Hash of 'hello':", sha256_hash("hello")[:16])
print("Hash of 'hello!':", sha256_hash("hello!")[:16])
print("Hash of 'hello.':", sha256_hash("hello.")[:16])

Merkle Trees
# Merkle tree: hash tree for efficient data verification.
# Used in blockchain to verify transactions in a block.

class MerkleNode:
    """Node in a Merkle tree."""
    
    def __init__(self, data: str = None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.hash = self.compute_hash()
    
    def compute_hash(self) -> str:
        if self.left is None and self.right is None:
            # Leaf node
            return sha256_hash(self.data)
        else:
            # Internal node
            combined = self.left.hash + self.right.hash
            return sha256_hash(combined)

class MerkleTree:
    """Merkle tree implementation."""
    
    def __init__(self, transactions: List[str]):
        self.transactions = transactions
        self.root = self.build_tree(transactions)
    
    def build_tree(self, data: List[str]) -> MerkleNode:
        """Build Merkle tree from data."""
        if len(data) == 0:
            return None
        
        # Create leaf nodes
        nodes = [MerkleNode(d) for d in data]
        
        # Build tree bottom-up
        while len(nodes) > 1:
            # If odd number, duplicate last node
            if len(nodes) % 2 == 1:
                nodes.append(nodes[-1])
            
            next_level = []
            for i in range(0, len(nodes), 2):
                parent = MerkleNode(left=nodes[i], right=nodes[i+1])
                next_level.append(parent)
            
            nodes = next_level
        
        return nodes[0]
    
    def get_root_hash(self) -> str:
        """Get Merkle root hash."""
        return self.root.hash if self.root else ""
    
    def verify_transaction(self, transaction: str, proof: List[str]) -> bool:
        """Verify transaction is in tree using Merkle proof."""
        current_hash = sha256_hash(transaction)
        
        for sibling_hash in proof:
            # Combine hashes (order matters)
            combined = current_hash + sibling_hash
            current_hash = sha256_hash(combined)
        
        return current_hash == self.get_root_hash()

# Example
transactions = ["tx1", "tx2", "tx3", "tx4"]
tree = MerkleTree(transactions)
print(f"\nMerkle root: {tree.get_root_hash()[:16]}...")

Digital Signatures (ECDSA)
# ECDSA: Elliptic Curve Digital Signature Algorithm.
# Used in Bitcoin/Ethereum for transaction signing.

from ecdsa import SigningKey, SECP256k1, VerifyingKey

def generate_keypair():
    """Generate ECDSA keypair."""
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    return private_key, public_key

def sign_message(private_key: SigningKey, message: str) -> bytes:
    """Sign a message with private key."""
    signature = private_key.sign(message.encode())
    return signature

def verify_signature(public_key: VerifyingKey, message: str, signature: bytes) -> bool:
    """Verify signature with public key."""
    try:
        return public_key.verify(signature, message.encode())
    except:
        return False

# Example
private_key, public_key = generate_keypair()
message = "Transfer 10 BTC to Alice"
signature = sign_message(private_key, message)

print(f"\nMessage: {message}")
print(f"Signature: {signature.hex()[:32]}...")
print(f"Verified: {verify_signature(public_key, message, signature)}")

CHAPTER 3: CONSENSUS MECHANISMS
Proof of Work (PoW)
# PoW: miners compete to solve computational puzzle.
# Puzzle: find nonce such that hash(block + nonce) starts with N zeros.
# Difficulty adjusts to maintain block time (~10 min for Bitcoin).

class ProofOfWork:
    """Proof of Work consensus."""
    
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
    
    def mine(self, block_data: str) -> tuple[int, str]:
        """Find nonce that satisfies difficulty."""
        nonce = 0
        target = '0' * self.difficulty
        
        while True:
            data = f"{block_data}{nonce}"
            hash_result = sha256_hash(data)
            
            if hash_result.startswith(target):
                return nonce, hash_result
            
            nonce += 1
            
            # Progress indicator
            if nonce % 100000 == 0:
                print(f"  Mining... nonce={nonce}")

# Example
pow = ProofOfWork(difficulty=4)
block_data = "block1:tx1,tx2,tx3"
nonce, hash_result = pow.mine(block_data)
print(f"\nMined! Nonce: {nonce}, Hash: {hash_result[:16]}...")

Proof of Stake (PoS)
# PoS: validators stake cryptocurrency to participate in consensus.
# Validators chosen based on stake size, age, randomization.
# More energy-efficient than PoW.

import random

class Validator:
    """PoS validator."""
    
    def __init__(self, address: str, stake: float):
        self.address = address
        self.stake = stake
        self.is_slashed = False

class ProofOfStake:
    """Proof of Stake consensus."""
    
    def __init__(self):
        self.validators: List[Validator] = []
        self.total_stake = 0.0
    
    def register_validator(self, address: str, stake: float):
        """Register a new validator."""
        validator = Validator(address, stake)
        self.validators.append(validator)
        self.total_stake += stake
        print(f"Validator registered: {address} (stake: {stake})")
    
    def select_proposer(self) -> Validator:
        """Select block proposer based on stake."""
        if not self.validators:
            return None
        
        # Weighted random selection
        rand_val = random.uniform(0, self.total_stake)
        cumulative = 0.0
        
        for validator in self.validators:
            if validator.is_slashed:
                continue
            cumulative += validator.stake
            if cumulative >= rand_val:
                return validator
        
        return self.validators[0]
    
    def slash_validator(self, address: str, amount: float):
        """Penalize malicious validator."""
        for validator in self.validators:
            if validator.address == address:
                validator.stake -= amount
                self.total_stake -= amount
                if validator.stake <= 0:
                    validator.is_slashed = True
                print(f"Validator {address} slashed: -{amount}")
                break

# Example
pos = ProofOfStake()
pos.register_validator("validator1", 1000.0)
pos.register_validator("validator2", 500.0)
pos.register_validator("validator3", 2000.0)

proposer = pos.select_proposer()
print(f"\nSelected proposer: {proposer.address} (stake: {proposer.stake})")

CHAPTER 4: ETHEREUM VIRTUAL MACHINE (EVM)
EVM Basics
# EVM: stack-based virtual machine for executing smart contracts.
# Gas: unit of computation cost (prevents infinite loops).
# Opcodes: low-level instructions (ADD, MUL, SSTORE, etc.).

class EVM:
    """Simplified Ethereum Virtual Machine."""
    
    def __init__(self):
        self.stack: List[int] = []
        self.storage: Dict[str, int] = {}
        self.memory: bytearray = bytearray(1024)
        self.gas = 1000000
        self.pc = 0  # Program counter
    
    def consume_gas(self, amount: int):
        """Consume gas for operation."""
        if self.gas < amount:
            raise Exception("Out of gas")
        self.gas -= amount
    
    def push(self, value: int):
        """Push value onto stack."""
        self.consume_gas(3)
        self.stack.append(value)
    
    def pop(self) -> int:
        """Pop value from stack."""
        self.consume_gas(2)
        if not self.stack:
            raise Exception("Stack underflow")
        return self.stack.pop()
    
    def add(self):
        """Add top two stack values."""
        self.consume_gas(3)
        a = self.pop()
        b = self.pop()
        self.push(a + b)
    
    def mul(self):
        """Multiply top two stack values."""
        self.consume_gas(5)
        a = self.pop()
        b = self.pop()
        self.push(a * b)
    
    def sub(self):
        """Subtract top two stack values."""
        self.consume_gas(3)
        a = self.pop()
        b = self.pop()
        self.push(b - a)  # Note: b - a (stack order)
    
    def sstore(self, key: str, value: int):
        """Store value in storage."""
        self.consume_gas(20000)  # Expensive operation
        self.storage[key] = value
    
    def sload(self, key: str) -> int:
        """Load value from storage."""
        self.consume_gas(200)
        return self.storage.get(key, 0)
    
    def execute(self, bytecode: List[str]):
        """Execute EVM bytecode."""
        self.pc = 0
        
        while self.pc < len(bytecode):
            opcode = bytecode[self.pc]
            
            if opcode == 'PUSH':
                value = int(bytecode[self.pc + 1])
                self.push(value)
                self.pc += 2
            
            elif opcode == 'ADD':
                self.add()
                self.pc += 1
            
            elif opcode == 'MUL':
                self.mul()
                self.pc += 1
            
            elif opcode == 'SUB':
                self.sub()
                self.pc += 1
            
            elif opcode == 'SSTORE':
                key = bytecode[self.pc + 1]
                value = self.pop()
                self.sstore(key, value)
                self.pc += 2
            
            elif opcode == 'SLOAD':
                key = bytecode[self.pc + 1]
                value = self.sload(key)
                self.push(value)
                self.pc += 2
            
            elif opcode == 'STOP':
                break
            
            else:
                raise Exception(f"Unknown opcode: {opcode}")
        
        return self.stack[-1] if self.stack else None

# Example: Execute "x = 5 + 3"
evm = EVM()
bytecode = ['PUSH', '5', 'PUSH', '3', 'ADD', 'SSTORE', 'x', 'STOP']
result = evm.execute(bytecode)
print(f"\nEVM result: {result}")
print(f"Storage: {evm.storage}")
print(f"Gas remaining: {evm.gas}")

Gas Calculation
# Gas costs (approximate):
# - Arithmetic operations: 3-5 gas
# - Storage operations: 200-20000 gas
# - Contract creation: 32000 gas
# - Transaction: 21000 gas (base cost)

# Example: estimate gas for simple transfer
def estimate_transfer_gas():
    """Estimate gas for ETH transfer."""
    base_cost = 21000  # Base transaction cost
    data_cost = 0  # No data in simple transfer
    return base_cost + data_cost

gas_estimate = estimate_transfer_gas()
print(f"\nGas estimate for transfer: {gas_estimate}")

CHAPTER 5: SMART CONTRACTS (SOLIDITY)
Basic Solidity Contract
// SimpleStorage.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    // State variable (stored on blockchain)
    uint256 private storedValue;
    
    // Event (emitted when value changes)
    event ValueChanged(uint256 newValue, address changedBy);
    
    // Constructor (called once on deployment)
    constructor(uint256 initialValue) {
        storedValue = initialValue;
    }
    
    // Function to set value
    function set(uint256 newValue) public {
        storedValue = newValue;
        emit ValueChanged(newValue, msg.sender);
    }
    
    // Function to get value (view = read-only, no gas cost)
    function get() public view returns (uint256) {
        return storedValue;
    }
}

ERC-20 Token Contract
// ERC20Token.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ERC20Token {
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    uint256 public totalSupply;
    
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    
    constructor(string memory _name, string memory _symbol, uint256 _totalSupply) {
        name = _name;
        symbol = _symbol;
        totalSupply = _totalSupply * (10 ** uint256(decimals));
        balanceOf[msg.sender] = totalSupply;
    }
    
    function transfer(address to, uint256 value) public returns (bool) {
        require(balanceOf[msg.sender] >= value, "Insufficient balance");
        
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        
        emit Transfer(msg.sender, to, value);
        return true;
    }
    
    function approve(address spender, uint256 value) public returns (bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }
    
    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(balanceOf[from] >= value, "Insufficient balance");
        require(allowance[from][msg.sender] >= value, "Allowance exceeded");
        
        balanceOf[from] -= value;
        balanceOf[to] += value;
        allowance[from][msg.sender] -= value;
        
        emit Transfer(from, to, value);
        return true;
    }
}

Deploying with Web3.py
from web3 import Web3

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'))

# Check connection
print(f"Connected: {w3.is_connected()}")
print(f"Block number: {w3.eth.block_number}")

# Contract ABI and bytecode (from Solidity compilation)
contract_abi = [...]  # JSON ABI
contract_bytecode = "0x..."  # Compiled bytecode

# Deploy contract
account = w3.eth.account.from_key('YOUR_PRIVATE_KEY')
contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

# Build transaction
tx = contract.constructor(100).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 2000000,
    'gasPrice': w3.eth.gas_price
})

# Sign and send
signed_tx = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f"Contract deployed! TX hash: {tx_hash.hex()}")

# Wait for confirmation
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = receipt.contractAddress
print(f"Contract address: {contract_address}")

CHAPTER 6: SMART CONTRACT SECURITY
Common Vulnerabilities
# 1. Reentrancy: external call before state update
# Vulnerable:
# function withdraw() public {
#     uint256 balance = balances[msg.sender];
#     (bool success, ) = msg.sender.call{value: balance}("");
#     balances[msg.sender] = 0;  // Too late!
# }

# Fixed:
# function withdraw() public {
#     uint256 balance = balances[msg.sender];
#     balances[msg.sender] = 0;  // Update first
#     (bool success, ) = msg.sender.call{value: balance}("");
# }

# 2. Integer Overflow/Underflow (fixed in Solidity 0.8+)
# Vulnerable (pre-0.8):
# function add(uint256 a, uint256 b) public pure returns (uint256) {
#     uint256 c = a + b;  // Can overflow!
#     require(c >= a, "Overflow");
#     return c;
# }

# Fixed (0.8+):
# function add(uint256 a, uint256 b) public pure returns (uint256) {
#     return a + b;  // Automatic overflow check
# }

# 3. Access Control
# Vulnerable:
# function setOwner(address newOwner) public {
#     owner = newOwner;  // Anyone can call!
# }

# Fixed:
# function setOwner(address newOwner) public onlyOwner {
#     owner = newOwner;
# }

# modifier onlyOwner() {
#     require(msg.sender == owner, "Not owner");
#     _;
# }

Security Tools
# Static analysis:
# - Slither: static analyzer for Solidity
# - Mythril: security analysis tool
# - Securify: formal verification

# Example: Run Slither
# slither contract.sol

# Fuzzing:
# - Echidna: property-based fuzzer
# - Harvey: coverage-guided fuzzer

# Formal verification:
# - Certora Prover: formal verification
# - K Framework: semantic framework

Security Best Practices
# 1. Use latest Solidity version (0.8+)
# 2. Follow Checks-Effects-Interactions pattern
# 3. Use OpenZeppelin libraries (audited)
# 4. Implement access control (Ownable, RBAC)
# 5. Use reentrancy guards
# 6. Limit gas usage (avoid loops over dynamic arrays)
# 7. Test thoroughly (unit tests, integration tests)
# 8. Get professional audit before mainnet deployment

# Example: Secure contract
// SecureContract.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SecureContract is ReentrancyGuard, Ownable {
    mapping(address => uint256) private balances;
    
    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);
    
    function deposit() public payable {
        require(msg.value > 0, "Must send ETH");
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }
    
    function withdraw(uint256 amount) public nonReentrant {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // Checks-Effects-Interactions pattern
        balances[msg.sender] -= amount;  // Effect
        (bool success, ) = msg.sender.call{value: amount}("");  // Interaction
        require(success, "Transfer failed");
        
        emit Withdrawal(msg.sender, amount);
    }
    
    function emergencyWithdraw() public onlyOwner {
        // Emergency function for owner
        payable(owner()).transfer(address(this).balance);
    }
}

CHAPTER 7: DECENTRALIZED FINANCE (DeFi)
Automated Market Makers (AMM)
# AMM: constant product formula (x * y = k)
# Used in Uniswap, SushiSwap for decentralized trading.

class AMM:
    """Constant product AMM (Uniswap V2 style)."""
    
    def __init__(self, reserve_x: float, reserve_y: float):
        self.reserve_x = reserve_x  # e.g., ETH
        self.reserve_y = reserve_y  # e.g., USDC
        self.k = reserve_x * reserve_y  # Constant product
        self.total_lp_tokens = 0.0
        self.lp_balances: Dict[str, float] = {}
    
    def get_price(self) -> float:
        """Get current price of X in terms of Y."""
        return self.reserve_y / self.reserve_x
    
    def add_liquidity(self, user: str, amount_x: float, amount_y: float) -> float:
        """Add liquidity and receive LP tokens."""
        # Calculate LP tokens to mint
        if self.total_lp_tokens == 0:
            # First liquidity provider
            lp_tokens = (amount_x * amount_y) ** 0.5
        else:
            # Proportional to existing liquidity
            lp_tokens = min(
                amount_x * self.total_lp_tokens / self.reserve_x,
                amount_y * self.total_lp_tokens / self.reserve_y
            )
        
        # Update reserves
        self.reserve_x += amount_x
        self.reserve_y += amount_y
        self.k = self.reserve_x * self.reserve_y
        
        # Update LP balances
        self.lp_balances[user] = self.lp_balances.get(user, 0) + lp_tokens
        self.total_lp_tokens += lp_tokens
        
        print(f"{user} added liquidity: {amount_x} X, {amount_y} Y → {lp_tokens:.2f} LP tokens")
        return lp_tokens
    
    def remove_liquidity(self, user: str, lp_tokens: float) -> tuple[float, float]:
        """Remove liquidity and receive tokens."""
        if self.lp_balances.get(user, 0) < lp_tokens:
            raise Exception("Insufficient LP tokens")
        
        # Calculate tokens to return
        share = lp_tokens / self.total_lp_tokens
        amount_x = self.reserve_x * share
        amount_y = self.reserve_y * share
        
        # Update reserves
        self.reserve_x -= amount_x
        self.reserve_y -= amount_y
        self.k = self.reserve_x * self.reserve_y
        
        # Update LP balances
        self.lp_balances[user] -= lp_tokens
        self.total_lp_tokens -= lp_tokens
        
        print(f"{user} removed liquidity: {lp_tokens:.2f} LP → {amount_x:.4f} X, {amount_y:.4f} Y")
        return amount_x, amount_y
    
    def swap_x_for_y(self, amount_x_in: float, user: str) -> float:
        """Swap X for Y (with 0.3% fee)."""
        # Apply fee (0.3%)
        amount_x_with_fee = amount_x_in * 0.997
        
        # Calculate output using constant product formula
        # (reserve_x + amount_x_with_fee) * (reserve_y - amount_y_out) = k
        amount_y_out = self.reserve_y - (self.k / (self.reserve_x + amount_x_with_fee))
        
        # Update reserves
        self.reserve_x += amount_x_in
        self.reserve_y -= amount_y_out
        self.k = self.reserve_x * self.reserve_y
        
        print(f"{user} swapped {amount_x_in:.4f} X → {amount_y_out:.4f} Y")
        return amount_y_out
    
    def swap_y_for_x(self, amount_y_in: float, user: str) -> float:
        """Swap Y for X (with 0.3% fee)."""
        amount_y_with_fee = amount_y_in * 0.997
        amount_x_out = self.reserve_x - (self.k / (self.reserve_y + amount_y_with_fee))
        
        self.reserve_y += amount_y_in
        self.reserve_x -= amount_x_out
        self.k = self.reserve_x * self.reserve_y
        
        print(f"{user} swapped {amount_y_in:.4f} Y → {amount_x_out:.4f} X")
        return amount_x_out

# Example
amm = AMM(reserve_x=10.0, reserve_y=20000.0)  # 10 ETH, 20000 USDC
print(f"\nInitial price: 1 ETH = {amm.get_price():.2f} USDC")

# Add liquidity
amm.add_liquidity("Alice", 5.0, 10000.0)
print(f"Price after adding liquidity: 1 ETH = {amm.get_price():.2f} USDC")

# Swap
amm.swap_x_for_y(1.0, "Bob")
print(f"Price after swap: 1 ETH = {amm.get_price():.2f} USDC")

Lending Protocols
# Lending: users deposit collateral, borrow assets.
# Over-collateralization required (e.g., 150% collateral ratio).
# Interest rates determined by supply/demand.

class LendingPool:
    """Simple lending pool (Aave/Compound style)."""
    
    def __init__(self):
        self.total_deposits: Dict[str, float] = {}  # asset -> total deposited
        self.total_borrows: Dict[str, float] = {}   # asset -> total borrowed
        self.user_deposits: Dict[str, Dict[str, float]] = {}  # user -> asset -> amount
        self.user_borrows: Dict[str, Dict[str, float]] = {}   # user -> asset -> amount
        self.collateral_factors: Dict[str, float] = {
            'ETH': 0.75,  # Can borrow 75% of ETH value
            'USDC': 0.80
        }
        self.interest_rates: Dict[str, float] = {
            'ETH': 0.05,  # 5% APR
            'USDC': 0.08  # 8% APR
        }
    
    def deposit(self, user: str, asset: str, amount: float):
        """Deposit asset as collateral."""
        if user not in self.user_deposits:
            self.user_deposits[user] = {}
        
        self.user_deposits[user][asset] = self.user_deposits[user].get(asset, 0) + amount
        self.total_deposits[asset] = self.total_deposits.get(asset, 0) + amount
        
        print(f"{user} deposited {amount} {asset}")
    
    def borrow(self, user: str, asset: str, amount: float, collateral_value_usd: float):
        """Borrow asset against collateral."""
        # Check collateralization
        max_borrow = collateral_value_usd * self.collateral_factors.get(asset, 0.75)
        
        if amount > max_borrow:
            raise Exception(f"Insufficient collateral. Max borrow: {max_borrow}")
        
        if user not in self.user_borrows:
            self.user_borrows[user] = {}
        
        self.user_borrows[user][asset] = self.user_borrows[user].get(asset, 0) + amount
        self.total_borrows[asset] = self.total_borrows.get(asset, 0) + amount
        
        print(f"{user} borrowed {amount} {asset}")
    
    def get_health_factor(self, user: str, collateral_value_usd: float) -> float:
        """Calculate health factor (>1 = safe, <1 = liquidatable)."""
        total_borrow_usd = 0.0
        
        for asset, amount in self.user_borrows.get(user, {}).items():
            # Simplified: assume 1:1 USD value for demo
            total_borrow_usd += amount
        
        if total_borrow_usd == 0:
            return float('inf')
        
        # Health factor = collateral / (borrow * collateral_factor)
        avg_collateral_factor = 0.75
        return collateral_value_usd / (total_borrow_usd * avg_collateral_factor)

# Example
lending = LendingPool()
lending.deposit("Alice", "ETH", 10.0)
lending.borrow("Alice", "USDC", 15000.0, collateral_value_usd=20000.0)

health = lending.get_health_factor("Alice", collateral_value_usd=20000.0)
print(f"\nAlice's health factor: {health:.2f}")

CHAPTER 8: LAYER 2 SCALING
Optimistic Rollups
# Optimistic Rollups: execute transactions off-chain, post to L1.
# Assume transactions are valid (optimistic), challenge period for disputes.
# Used in: Optimism, Arbitrum.

class OptimisticRollup:
    """Simplified optimistic rollup."""
    
    def __init__(self):
        self.state: Dict[str, float] = {}  # account -> balance
        self.transaction_batch: List[Dict] = []
        self.state_roots: List[str] = []
        self.challenge_period = 7 * 24 * 3600  # 7 days
    
    def execute_transaction(self, tx: Dict):
        """Execute transaction off-chain."""
        sender = tx['from']
        recipient = tx['to']
        amount = tx['amount']
        
        if self.state.get(sender, 0) < amount:
            raise Exception("Insufficient balance")
        
        self.state[sender] -= amount
        self.state[recipient] = self.state.get(recipient, 0) + amount
        
        self.transaction_batch.append(tx)
        print(f"Executed: {sender} → {recipient}: {amount}")
    
    def submit_batch_to_l1(self):
        """Submit transaction batch to L1 with state root."""
        # Compute state root (simplified)
        state_root = sha256_hash(json.dumps(self.state, sort_keys=True))
        self.state_roots.append(state_root)
        
        print(f"\nSubmitted batch to L1:")
        print(f"  Transactions: {len(self.transaction_batch)}")
        print(f"  State root: {state_root[:16]}...")
        print(f"  Challenge period: {self.challenge_period / 86400} days")
        
        self.transaction_batch.clear()
    
    def challenge_state_root(self, batch_index: int, proof: str):
        """Challenge invalid state root (fraud proof)."""
        print(f"\nChallenging state root at batch {batch_index}")
        print(f"  Proof: {proof[:32]}...")
        # In reality: re-execute transactions and prove incorrect state
        return True

# Example
rollup = OptimisticRollup()
rollup.state = {"Alice": 1000.0, "Bob": 500.0}

rollup.execute_transaction({'from': 'Alice', 'to': 'Bob', 'amount': 100.0})
rollup.execute_transaction({'from': 'Bob', 'to': 'Charlie', 'amount': 50.0})

rollup.submit_batch_to_l1()

Zero-Knowledge Rollups (ZK-Rollups)
# ZK-Rollups: use zero-knowledge proofs to verify L2 state transitions.
# More secure than optimistic (no challenge period needed).
# Used in: zkSync, StarkNet, Polygon zkEVM.

class ZKRollup:
    """Simplified ZK-rollup."""
    
    def __init__(self):
        self.state: Dict[str, float] = {}
        self.transaction_batch: List[Dict] = []
        self.zk_proofs: List[str] = []
    
    def execute_transaction(self, tx: Dict):
        """Execute transaction off-chain."""
        sender = tx['from']
        recipient = tx['to']
        amount = tx['amount']
        
        if self.state.get(sender, 0) < amount:
            raise Exception("Insufficient balance")
        
        self.state[sender] -= amount
        self.state[recipient] = self.state.get(recipient, 0) + amount
        
        self.transaction_batch.append(tx)
    
    def generate_zk_proof(self) -> str:
        """Generate zero-knowledge proof for batch."""
        # In reality: complex cryptographic proof (SNARK/STARK)
        proof_data = json.dumps({
            'transactions': self.transaction_batch,
            'old_state': "previous_state_root",
            'new_state': sha256_hash(json.dumps(self.state, sort_keys=True))
        }, sort_keys=True)
        
        proof = sha256_hash(proof_data)  # Simplified
        self.zk_proofs.append(proof)
        
        print(f"\nGenerated ZK proof: {proof[:16]}...")
        return proof
    
    def submit_to_l1(self):
        """Submit batch and proof to L1."""
        proof = self.generate_zk_proof()
        
        print(f"Submitted to L1:")
        print(f"  Transactions: {len(self.transaction_batch)}")
        print(f"  ZK proof: {proof[:16]}...")
        print(f"  No challenge period needed!")
        
        self.transaction_batch.clear()

# Example
zk_rollup = ZKRollup()
zk_rollup.state = {"Alice": 1000.0, "Bob": 500.0}

zk_rollup.execute_transaction({'from': 'Alice', 'to': 'Bob', 'amount': 100.0})
zk_rollup.submit_to_l1()

CHAPTER 9: INTEROPERABILITY
Cross-Chain Bridges
# Bridges: transfer assets/messages between different blockchains.
# Types: lock-and-mint, liquidity networks, native interoperability.

class CrossChainBridge:
    """Simplified cross-chain bridge."""
    
    def __init__(self):
        self.locked_assets: Dict[str, Dict[str, float]] = {
            'ethereum': {},
            'polygon': {}
        }
        self.wrapped_tokens: Dict[str, Dict[str, float]] = {
            'polygon': {},  # Wrapped ETH on Polygon
            'ethereum': {}  # Wrapped MATIC on Ethereum
        }
    
    def lock_and_mint(self, from_chain: str, to_chain: str, user: str, amount: float):
        """Lock asset on source chain, mint wrapped on destination."""
        # Lock on source
        self.locked_assets[from_chain][user] = \
            self.locked_assets[from_chain].get(user, 0) + amount
        
        # Mint wrapped on destination
        wrapped_symbol = f"w{from_chain[:3].upper()}"
        self.wrapped_tokens[to_chain][user] = \
            self.wrapped_tokens[to_chain].get(user, 0) + amount
        
        print(f"Bridged {amount} from {from_chain} to {to_chain}")
        print(f"  Locked on {from_chain}: {self.locked_assets[from_chain][user]}")
        print(f"  Minted on {to_chain}: {self.wrapped_tokens[to_chain][user]} {wrapped_symbol}")
    
    def burn_and_release(self, from_chain: str, to_chain: str, user: str, amount: float):
        """Burn wrapped on source, release original on destination."""
        # Burn wrapped
        if self.wrapped_tokens[from_chain].get(user, 0) < amount:
            raise Exception("Insufficient wrapped balance")
        
        self.wrapped_tokens[from_chain][user] -= amount
        
        # Release original
        self.locked_assets[to_chain][user] -= amount
        
        print(f"Bridged back {amount} from {from_chain} to {to_chain}")

# Example
bridge = CrossChainBridge()
bridge.locked_assets['ethereum']['Alice'] = 1000.0

bridge.lock_and_mint('ethereum', 'polygon', 'Alice', 10.0)
bridge.burn_and_release('polygon', 'ethereum', 'Alice', 5.0)

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
NFT Standards
# ERC-721: Non-fungible tokens (unique assets)
# ERC-1155: Multi-token standard (fungible + non-fungible)

// ERC721.sol (simplified)
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ERC721 {
    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    mapping(uint256 => address) private _tokenApprovals;
    
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    
    function balanceOf(address owner) public view returns (uint256) {
        return _balances[owner];
    }
    
    function ownerOf(uint256 tokenId) public view returns (address) {
        return _owners[tokenId];
    }
    
    function transferFrom(address from, address to, uint256 tokenId) public {
        require(_owners[tokenId] == from, "Not owner");
        
        _balances[from] -= 1;
        _balances[to] += 1;
        _owners[tokenId] = to;
        
        emit Transfer(from, to, tokenId);
    }
    
    function _mint(address to, uint256 tokenId) internal {
        require(_owners[tokenId] == address(0), "Already minted");
        
        _balances[to] += 1;
        _owners[tokenId] = to;
        
        emit Transfer(address(0), to, tokenId);
    }
}

DAO (Decentralized Autonomous Organization)
# DAO: organization governed by smart contracts and token holders.
# Proposals, voting, treasury management.

class DAO:
    """Simple DAO implementation."""
    
    def __init__(self, name: str):
        self.name = name
        self.members: Dict[str, float] = {}  # address -> voting power
        self.proposals: List[Dict] = []
        self.treasury: Dict[str, float] = {}  # asset -> balance
    
    def add_member(self, address: str, voting_power: float):
        """Add member with voting power."""
        self.members[address] = voting_power
        print(f"Added member: {address} (power: {voting_power})")
    
    def create_proposal(self, proposer: str, description: str, execution_data: Dict):
        """Create new proposal."""
        proposal = {
            'id': len(self.proposals),
            'proposer': proposer,
            'description': description,
            'execution_data': execution_data,
            'votes_for': 0.0,
            'votes_against': 0.0,
            'voters': set(),
            'executed': False
        }
        self.proposals.append(proposal)
        print(f"Proposal #{proposal['id']} created: {description}")
        return proposal['id']
    
    def vote(self, proposal_id: int, voter: str, support: bool):
        """Vote on proposal."""
        if proposal_id >= len(self.proposals):
            raise Exception("Invalid proposal")
        
        proposal = self.proposals[proposal_id]
        
        if voter in proposal['voters']:
            raise Exception("Already voted")
        
        if voter not in self.members:
            raise Exception("Not a member")
        
        voting_power = self.members[voter]
        proposal['voters'].add(voter)
        
        if support:
            proposal['votes_for'] += voting_power
        else:
            proposal['votes_against'] += voting_power
        
        print(f"{voter} voted {'for' if support else 'against'} proposal #{proposal_id}")
    
    def execute_proposal(self, proposal_id: int):
        """Execute proposal if passed."""
        proposal = self.proposals[proposal_id]
        
        if proposal['executed']:
            raise Exception("Already executed")
        
        # Simple majority
        if proposal['votes_for'] > proposal['votes_against']:
            print(f"Proposal #{proposal_id} passed!")
            # Execute proposal (simplified)
            proposal['executed'] = True
        else:
            print(f"Proposal #{proposal_id} failed")

# Example
dao = DAO("TestDAO")
dao.add_member("0xAlice", 100.0)
dao.add_member("0xBob", 50.0)
dao.add_member("0xCharlie", 75.0)

proposal_id = dao.create_proposal(
    "0xAlice",
    "Send 10 ETH to Bob",
    {'action': 'transfer', 'to': '0xBob', 'amount': 10.0}
)

dao.vote(proposal_id, "0xAlice", True)
dao.vote(proposal_id, "0xBob", True)
dao.vote(proposal_id, "0xCharlie", False)

dao.execute_proposal(proposal_id)

Recommended Reading
# - "Mastering Bitcoin" by Andreas Antonopoulos
# - "Mastering Ethereum" by Andreas Antonopoulos & Gavin Wood
# - Ethereum Whitepaper: https://ethereum.org/whitepaper/
# - Bitcoin Whitepaper: https://bitcoin.org/bitcoin.pdf
# - Solidity Documentation: https://docs.soliditylang.org/
# - OpenZeppelin Contracts: https://docs.openzeppelin.com/contracts/

# Online Resources
# - Ethernaut (security challenges): https://ethernaut.openzeppelin.com/
# - CryptoZombies (Solidity tutorial): https://cryptozombies.io/
# - DeFi Pulse (DeFi analytics): https://defipulse.com/
# - Dune Analytics (blockchain data): https://dune.com/

# End of Blockchain & Smart Contracts Reference