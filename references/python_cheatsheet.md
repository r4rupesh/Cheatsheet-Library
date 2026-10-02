# Python Quick Reference

## Variables and core types

```python
name = "Avery"             # str
items = ["pen", "notebook"] # list
coordinates = (3, 8)        # tuple
settings = {"theme": "light"} # dict
unique_ids = {101, 102}     # set
is_ready = True             # bool
```

## Collections and slicing

```python
items.append("folder")
first_two = items[:2]
settings.get("theme", "default")
for index, item in enumerate(items, start=1):
    print(index, item)
```

## Conditions and loops

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "Keep practicing"

squares = [number**2 for number in range(1, 6)]
```

## Functions

```python
def summarize(values, *, precision=2):
    average = sum(values) / len(values)
    return round(average, precision)
```

Use `*` to make following parameters keyword-only. Add type annotations when they make a function's inputs and output clearer.

## Exceptions

```python
try:
    number = int(user_input)
except ValueError as error:
    print(f"Enter a whole number: {error}")
else:
    print(number)
```

Catch specific exceptions and keep the `try` block limited to the operation that may fail.

## Files and paths

```python
from pathlib import Path

path = Path("data.txt")
text = path.read_text(encoding="utf-8")
Path("copy.txt").write_text(text, encoding="utf-8")
```

## Useful built-ins

```python
len(items)
sorted(items)
any(values)
all(values)
zip(names, scores)
```

## Virtual environments

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install package-name
```

The Cheatsheet tab also previews `python_cheatsheet.ipynb`; use the Playground tab to edit and run Python code.