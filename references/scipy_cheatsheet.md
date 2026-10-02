# SciPy Quick Reference

SciPy adds tested algorithms for optimization, integration, statistics, signal processing, linear algebra, and more on top of NumPy arrays.

## Integration

```python
from scipy import integrate
import numpy as np

area, error = integrate.quad(lambda x: np.sin(x), 0, np.pi)
```

`quad` returns the estimated integral and an absolute error estimate. For sampled data, use `integrate.trapezoid(y, x=x)`.

## Optimization and roots

```python
from scipy import optimize

minimum = optimize.minimize_scalar(
    lambda x: (x - 3) ** 2 + 2,
    bounds=(-10, 10),
    method="bounded",
)
root = optimize.brentq(lambda x: x**2 - 2, 0, 2)
```

## Probability distributions

```python
from scipy import stats

normal = stats.norm(loc=0, scale=1)
normal.pdf(0)       # Density
normal.cdf(1.96)    # Cumulative probability
normal.ppf(0.975)   # Quantile
```

Common tools include `stats.describe`, `stats.ttest_ind`, `stats.pearsonr`, and `stats.linregress`.

## Signal processing

```python
from scipy import signal

filtered = signal.savgol_filter(samples, window_length=9, polyorder=2)
frequencies, power = signal.periodogram(samples, fs=sample_rate)
```

`window_length` must be an odd integer larger than `polyorder`.

## Linear algebra

```python
from scipy import linalg

solution = linalg.solve(matrix, vector)
eigenvalues, eigenvectors = linalg.eig(matrix)
```

## Interpolation

```python
from scipy.interpolate import interp1d

interpolate = interp1d(x_points, y_points, kind="linear", bounds_error=False)
values_at_new_points = interpolate(new_x)
```

## Constants and distances

```python
from scipy import constants
from scipy.spatial.distance import cdist

speed_of_light = constants.c
distances = cdist(points_a, points_b, metric="euclidean")
```

The playground includes focused examples and a custom code editor with `np`, `sp`, `integrate`, `optimize`, `stats`, `signal`, and `plt` available.