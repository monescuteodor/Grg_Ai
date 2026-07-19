# Testing Patterns Complete Reference


---

# CHAPTER 1: PYTHON (PYTEST)

```python
import pytest

def test_addition():
    assert 1 + 1 == 2

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

@pytest.mark.parametrize("n,expected", [(1,1),(2,4),(3,9)])
def test_square(n, expected):
    assert n ** 2 == expected

@pytest.fixture
def users():
    return [{"name": "Alice"}, {"name": "Bob"}]

def test_count(users):
    assert len(users) == 2

from unittest.mock import patch
def test_api():
    with patch('requests.get') as mock:
        mock.return_value.json.return_value = {"name": "Alice"}
        result = fetch_user(1)
        assert result["name"] == "Alice"
```


# CHAPTER 2: JAVASCRIPT (JEST)

```javascript
test('adds numbers', () => { expect(1 + 2).toBe(3); });
test('throws error', () => { expect(() => divide(1,0)).toThrow(); });
test('async fetch', async () => {
    const user = await fetchUser(1);
    expect(user.name).toBe('Alice');
});
const callback = jest.fn();
processItems([1,2], callback);
expect(callback).toHaveBeenCalledTimes(2);

describe('Calculator', () => {
    test('add', () => expect(add(1,2)).toBe(3));
    test('subtract', () => expect(sub(5,3)).toBe(2));
});
```


# CHAPTER 3: TESTING TYPES

```
UNIT:        One function, mocked deps, fast
INTEGRATION: Multiple components, real DB, medium
E2E:         Full browser flow, slow but real
```