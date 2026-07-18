# Coding Interview Problems and Solutions


---

# CHAPTER 1: ARRAY PROBLEMS


## Two Sum

```python
# Given nums and target, return indices of two numbers that add up to target
# O(n) time, O(n) space

def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
    return []

# two_sum([2, 7, 11, 15], 9)  →  [0, 1]
```


## Best Time to Buy and Sell Stock

```python
# Find max profit from one buy and one sell
# O(n) time, O(1) space

def max_profit(prices):
    min_price = float('inf')
    profit = 0
    for price in prices:
        min_price = min(min_price, price)
        profit = max(profit, price - min_price)
    return profit

# max_profit([7,1,5,3,6,4])  →  5 (buy at 1, sell at 6)
```


## Maximum Subarray (Kadane's Algorithm)

```python
def max_subarray(nums):
    current = best = nums[0]
    for n in nums[1:]:
        current = max(n, current + n)
        best = max(best, current)
    return best

# max_subarray([-2,1,-3,4,-1,2,1,-5,4])  →  6 ([4,-1,2,1])
```


## Merge Intervals

```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

# merge_intervals([[1,3],[2,6],[8,10],[15,18]])  →  [[1,6],[8,10],[15,18]]
```


---

# CHAPTER 2: STRING PROBLEMS


## Valid Palindrome

```python
def is_palindrome(s):
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

# is_palindrome("A man, a plan, a canal: Panama")  →  True
```


## Longest Substring Without Repeating Characters

```python
def length_of_longest_substring(s):
    seen = {}
    start = 0
    max_len = 0
    for i, c in enumerate(s):
        if c in seen and seen[c] >= start:
            start = seen[c] + 1
        seen[c] = i
        max_len = max(max_len, i - start + 1)
    return max_len

# length_of_longest_substring("abcabcbb")  →  3 ("abc")
```


## Valid Anagram

```python
from collections import Counter

def is_anagram(s, t):
    return Counter(s) == Counter(t)

# is_anagram("anagram", "nagaram")  →  True
```


---

# CHAPTER 3: LINKED LIST & TREE PROBLEMS


## Reverse Linked List

```python
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev
```


## Binary Tree Level Order Traversal (BFS)

```python
from collections import deque

def level_order(root):
    if not root: return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```


## Valid BST

```python
def is_valid_bst(node, min_val=float('-inf'), max_val=float('inf')):
    if not node: return True
    if node.val <= min_val or node.val >= max_val: return False
    return (is_valid_bst(node.left, min_val, node.val) and
            is_valid_bst(node.right, node.val, max_val))
```


---

# CHAPTER 4: DYNAMIC PROGRAMMING


## Fibonacci (Bottom-Up)

```python
def fib(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```


## Climbing Stairs

```python
def climb_stairs(n):
    if n <= 2: return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b
```


## Coin Change

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

# coin_change([1, 5, 10, 25], 30)  →  2 (25 + 5)
```


## Longest Common Subsequence

```python
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```