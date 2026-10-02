# NumPy Quick Reference

NumPy provides fast, vectorized operations on multidimensional arrays.

## Create arrays

```python
import numpy as np

values = np.array([2, 4, 6, 8])
zeros = np.zeros((2, 3))
ones = np.ones(4)
sequence = np.arange(0, 10, 2)
points = np.linspace(0, 1, 5)
```

## Inspect and reshape

```python
values.shape
values.size
values.ndim
values.dtype
matrix = np.arange(12).reshape(3, 4)
```

## Select and filter

```python
values[0]
values[1:3]
values[values > 5]
matrix[0, :]
matrix[:, 1]
```

## Vectorized math and broadcasting

```python
values + 10
values * 2
np.sqrt(values)
np.where(values >= 5, "high", "low")
matrix + np.array([10, 20, 30, 40])
```

## Aggregations and axis

```python
values.sum()
values.mean()
values.min(), values.max()
matrix.sum(axis=0)  # Sum each column
matrix.mean(axis=1)  # Mean each row
```

## Random numbers

```python
rng = np.random.default_rng(42)
rng.integers(0, 10, size=5)
rng.normal(loc=0, scale=1, size=(3, 2))
```

## Linear algebra

```python
matrix = np.array([[2, 1], [1, 3]])
vector = np.array([5, 7])
np.linalg.solve(matrix, vector)
np.linalg.det(matrix)
```

## Combine arrays

```python
np.concatenate([values, values])
np.vstack([values, values])
np.column_stack([values, values * 10])
```

The playground provides a NumPy namespace as `np`, keeps variables between runs, and displays printed output or the final expression.