# Python Data Science Complete Reference


---

# CHAPTER 1: NUMPY


## Remarks

NumPy is the foundation of Python's scientific computing ecosystem. It provides fast N-dimensional arrays and vectorized operations that run 10-100x faster than Python loops. Every data science library (pandas, scikit-learn, TensorFlow, PyTorch) is built on NumPy.


## Array Operations

```python
import numpy as np

# Create arrays
a = np.array([1, 2, 3, 4, 5])
zeros = np.zeros((3, 4))           # 3x4 matrix of zeros
ones = np.ones((2, 3))             # 2x3 matrix of ones
rng = np.arange(0, 10, 2)          # [0, 2, 4, 6, 8]
linspace = np.linspace(0, 1, 5)    # [0, 0.25, 0.5, 0.75, 1.0]
rand = np.random.rand(3, 3)       # 3x3 random (0 to 1)
randn = np.random.randn(1000)     # Normal distribution

# Shape and reshape
m = np.array([[1, 2, 3], [4, 5, 6]])
print(m.shape)    # (2, 3)
flat = m.reshape(-1)    # [1, 2, 3, 4, 5, 6]
col = m.reshape(6, 1)   # Column vector
t = m.T                 # Transpose: (3, 2)

# Vectorized operations (NO LOOPS!)
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

a + b          # [11, 22, 33, 44, 55]
a * b          # [10, 40, 90, 160, 250]
a ** 2         # [1, 4, 9, 16, 25]
np.sqrt(a)     # [1.0, 1.41, 1.73, 2.0, 2.24]
np.sin(a)      # Sine of each element

# 100x faster than Python loops!
# Python loop: for i in range(1000000): result[i] = a[i] * b[i]  → 500ms
# NumPy:       result = a * b                                     → 5ms

# Boolean indexing (filtering)
a = np.array([1, 5, 3, 8, 2, 9, 4])
mask = a > 4
filtered = a[mask]    # [5, 8, 9]
# Or directly:
a[a > 4]              # [5, 8, 9]
a[(a > 2) & (a < 8)]  # [5, 3, 4]

# Aggregations
a.sum()        # 32
a.mean()       # 4.57
a.std()        # 2.82
a.min()        # 1
a.max()        # 9
a.argmax()     # 5 (index of max)

# Matrix operations
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
np.dot(A, B)       # Matrix multiplication
A @ B              # Same thing (@ operator)
np.linalg.inv(A)   # Inverse
np.linalg.det(A)   # Determinant: -2
```


---

# CHAPTER 2: PANDAS


## DataFrames

```python
import pandas as pd

# Create DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve'],
    'age': [30, 25, 35, 28, 32],
    'department': ['Engineering', 'Sales', 'Engineering', 'Sales', 'Engineering'],
    'salary': [120000, 80000, 130000, 85000, 115000],
})

# Basic info
df.shape           # (5, 4)
df.dtypes          # Column types
df.describe()      # Statistics
df.head(3)         # First 3 rows
df.info()          # Summary

# Access columns
df['name']                    # Series
df[['name', 'age']]          # Multiple columns → DataFrame
df.name                       # Dot notation (same as df['name'])

# Access rows
df.iloc[0]                    # By position (first row)
df.iloc[0:3]                  # Rows 0-2
df.loc[0]                     # By label/index
df.loc[df['age'] > 30]       # Boolean indexing (filtering!)

# Filtering (most important operation!)
engineers = df[df['department'] == 'Engineering']
senior = df[(df['age'] > 28) & (df['salary'] > 100000)]
sales_or_eng = df[df['department'].isin(['Sales', 'Engineering'])]

# Sorting
df.sort_values('salary', ascending=False)
df.sort_values(['department', 'salary'], ascending=[True, False])

# Add/modify columns
df['bonus'] = df['salary'] * 0.10
df['senior'] = df['age'] > 30
df['name_upper'] = df['name'].str.upper()

# GroupBy (split-apply-combine)
df.groupby('department')['salary'].mean()
# department
# Engineering    121666.67
# Sales           82500.00

df.groupby('department').agg({
    'salary': ['mean', 'min', 'max'],
    'age': 'mean',
    'name': 'count'
})

# Pivot table
pd.pivot_table(df, values='salary', index='department',
               aggfunc=['mean', 'count'])
```


## Data Cleaning

```python
# Handle missing data
df.isnull().sum()             # Count NaN per column
df.dropna()                    # Remove rows with ANY NaN
df.dropna(subset=['name'])    # Remove only if name is NaN
df.fillna(0)                   # Replace NaN with 0
df['age'].fillna(df['age'].median(), inplace=True)

# Remove duplicates
df.drop_duplicates()
df.drop_duplicates(subset=['email'], keep='last')

# Type conversion
df['date'] = pd.to_datetime(df['date_str'])
df['price'] = df['price_str'].str.replace('$', '').astype(float)
df['category'] = df['category'].astype('category')  # Memory efficient

# String operations
df['name'].str.lower()
df['name'].str.contains('ali', case=False)
df['email'].str.split('@').str[1]    # Domain from email

# Apply custom function
df['tax'] = df['salary'].apply(lambda x: x * 0.3 if x > 100000 else x * 0.2)

# Read/write files
df = pd.read_csv('data.csv')
df = pd.read_excel('data.xlsx')
df = pd.read_json('data.json')
df.to_csv('output.csv', index=False)
df.to_excel('output.xlsx', index=False)
```


---

# CHAPTER 3: MATPLOTLIB AND VISUALIZATION


## Basic Plots

```python
import matplotlib.pyplot as plt
import numpy as np

# Line plot
x = np.linspace(0, 10, 100)
plt.figure(figsize=(10, 6))
plt.plot(x, np.sin(x), label='sin(x)', color='blue')
plt.plot(x, np.cos(x), label='cos(x)', color='red', linestyle='--')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Trigonometric Functions')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('plot.png', dpi=150, bbox_inches='tight')
plt.show()

# Bar chart
categories = ['Python', 'JavaScript', 'Rust', 'Go', 'C++']
values = [85, 78, 65, 60, 55]
plt.figure(figsize=(8, 5))
plt.bar(categories, values, color=['#3572A5', '#f1e05a', '#dea584', '#00ADD8', '#f34b7d'])
plt.ylabel('Popularity')
plt.title('Programming Languages')
plt.savefig('bar.png')

# Scatter plot
x = np.random.randn(200)
y = x * 2 + np.random.randn(200) * 0.5
plt.figure(figsize=(8, 6))
plt.scatter(x, y, alpha=0.5, c=y, cmap='viridis')
plt.colorbar(label='y value')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Scatter Plot')

# Histogram
data = np.random.randn(10000)
plt.figure(figsize=(8, 5))
plt.hist(data, bins=50, edgecolor='black', alpha=0.7)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Normal Distribution')
plt.axvline(data.mean(), color='red', linestyle='--', label=f'Mean: {data.mean():.2f}')
plt.legend()

# Subplots (multiple plots in one figure)
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title('Sine')
axes[0, 1].plot(x, np.cos(x))
axes[0, 1].set_title('Cosine')
axes[1, 0].bar(['A', 'B', 'C'], [3, 7, 5])
axes[1, 0].set_title('Bar')
axes[1, 1].hist(np.random.randn(1000), bins=30)
axes[1, 1].set_title('Histogram')
plt.tight_layout()
plt.savefig('subplots.png')
```


---

# CHAPTER 4: COMMON PITFALLS

```
PITFALL 1: Python loops on large data
  for i in range(len(df)): df['col'][i] *= 2  → 100x slower
  Fix: df['col'] *= 2 (vectorized)

PITFALL 2: SettingWithCopyWarning
  df[df['age'] > 30]['salary'] = 0  → may not modify original
  Fix: df.loc[df['age'] > 30, 'salary'] = 0

PITFALL 3: Not using .copy()
  subset = df[df['age'] > 30]  → subset is a VIEW, modifying it modifies df!
  Fix: subset = df[df['age'] > 30].copy()

PITFALL 4: Loading entire CSV into memory
  100GB CSV → MemoryError
  Fix: pd.read_csv('big.csv', chunksize=10000) or use Polars/Dask

PITFALL 5: Using .apply() when vectorized exists
  df['len'] = df['name'].apply(len)  → slow
  Fix: df['len'] = df['name'].str.len()  → vectorized, 10x faster

PITFALL 6: Not specifying dtypes on read
  All columns as object/float64 → wastes memory.
  Fix: pd.read_csv('data.csv', dtype={'id': 'int32', 'name': 'category'})

PITFALL 7: Ignoring index after operations
  After concat/merge, index has duplicates → confusing behavior.
  Fix: df.reset_index(drop=True)

PITFALL 8: plt.show() blocks execution
  Script hangs waiting for plot window to close.
  Fix: plt.savefig() instead, or use plt.ion() for interactive mode.
```