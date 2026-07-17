# Blockchain and Web3 Complete Reference


---

# CHAPTER 1: BLOCKCHAIN FUNDAMENTALS


## Remarks

A blockchain is a distributed, immutable ledger. Each block contains transactions, a hash of the previous block, and a timestamp. Once written, data cannot be altered without changing all subsequent blocks. Used for cryptocurrencies, smart contracts, supply chain tracking, and decentralized applications.


## How Blockchain Works

```
BLOCK STRUCTURE:
  ┌──────────────────────────────┐
  │ Block #42                    │
  │ Timestamp: 2026-07-16 10:00  │
  │ Previous Hash: 0x8a3f...     │
  │ Transactions:                │
  │   Alice → Bob: 5 tokens      │
  │   Carol → Dave: 2 tokens     │
  │ Nonce: 73829                 │
  │ Hash: 0x00003b7f...          │
  └──────────────────────────────┘
         │
         ▼
  ┌──────────────────────────────┐
  │ Block #43                    │
  │ Previous Hash: 0x00003b7f   │ ← Links to Block #42
  │ ...                          │
  └──────────────────────────────┘

CHAIN: Block 1 → Block 2 → Block 3 → ... → Block N
Changing Block 2 → changes its hash → breaks Block 3's previous_hash
→ must recalculate ALL subsequent blocks → practically impossible
```


## Simple Blockchain in Python

```python
import hashlib
import json
import time

class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine(self, difficulty=4):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash


class Blockchain:
    def __init__(self):
        self.chain = [self._create_genesis()]
        self.difficulty = 4
        self.pending = []

    def _create_genesis(self):
        return Block(0, [], "0")

    def add_transaction(self, sender, receiver, amount):
        self.pending.append({"sender": sender, "receiver": receiver, "amount": amount})

    def mine_pending(self, miner_address):
        block = Block(len(self.chain), self.pending, self.chain[-1].hash)
        block.mine(self.difficulty)
        self.chain.append(block)
        self.pending = [{"sender": "network", "receiver": miner_address, "amount": 1}]
        return block

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True


# Usage
bc = Blockchain()
bc.add_transaction("Alice", "Bob", 5)
bc.add_transaction("Bob", "Carol", 2)
block = bc.mine_pending("miner1")
print(f"Block mined: {block.hash}")
print(f"Chain valid: {bc.is_valid()}")
```


## Smart Contracts (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleToken {
    string public name = "GrgToken";
    string public symbol = "GRG";
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(uint256 _initialSupply) {
        totalSupply = _initialSupply;
        balanceOf[msg.sender] = _initialSupply;
    }

    function transfer(address _to, uint256 _amount) public returns (bool) {
        require(balanceOf[msg.sender] >= _amount, "Not enough tokens");
        balanceOf[msg.sender] -= _amount;
        balanceOf[_to] += _amount;
        emit Transfer(msg.sender, _to, _amount);
        return true;
    }
}
```


---

# CHAPTER 2: COMMON PITFALLS

```
PITFALL 1: Blockchain for everything
  Most apps don't need blockchain. Use a database.
  Use blockchain only when: no trusted central authority + need immutable record.

PITFALL 2: Private keys in code
  Exposed private key → all funds stolen instantly.
  Fix: use environment variables, hardware wallets, key management services.

PITFALL 3: Smart contract bugs
  Once deployed, smart contracts can't be changed. Bugs = permanent.
  Fix: audit, test extensively, use upgradeable proxy patterns.

PITFALL 4: Ignoring gas costs
  Complex smart contract → expensive to run ($50+ per transaction).
  Fix: optimize storage, minimize on-chain operations.
```