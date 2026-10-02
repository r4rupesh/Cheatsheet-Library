import json
from pathlib import Path

null = None

notebook_file = Path(__file__).resolve().parents[1] / "data" / "python_cheatsheet.ipynb"

# Saves the JSON object directly to disk as a valid Jupyter notebook file
with open(notebook_file, "w", encoding="utf-8") as f:
    json.dump({
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Python Cheat Sheet\n",
    "A condensed overview of Python syntax, data types, control flow, functions, classes, and built-in modules."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Getting Started\n",
    "- Start interactive shell: `$ python`\n",
    "- Quit interactive shell: `>>> exit()`\n",
    "- Run a script: `$ python my_script.py`\n",
    "- Run in interactive mode: `$ python -i my_script.py`"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Comments"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Always add a space after the #\n",
    "# Use comments to explain 'why' of your code\n",
    "\n",
    "# print(\"This code will not run.\")\n",
    "print(\"This will run.\")  # Comments are ignored by Python"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Data Types\n",
    "- Python is dynamically typed.\n",
    "- Use `None` to represent missing or optional values."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Type Investigation\n",
    "print(type(42))          # <class 'int'>\n",
    "print(type(3.14))        # <class 'float'>\n",
    "print(type(\"Hello\"))     # <class 'str'>\n",
    "print(type(True))        # <class 'bool'>\n",
    "print(type(None))        # <class 'NoneType'>\n",
    "print(isinstance(3.14, float))  # True\n",
    "print(issubclass(int, object))  # True - everything inherits from object\n",
    "\n",
    "# Type Conversion\n",
    "print(int(\"42\"))      # 42\n",
    "print(float(\"3.14\"))  # 3.14\n",
    "print(str(42))        # \"42\"\n",
    "print(bool(1))        # True\n",
    "print(list(\"abc\"))    # ['a', 'b', 'c']"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Variables & Assignment"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Basic Assignment\n",
    "name = \"Leo\"     # String\n",
    "age = 7         # Integer\n",
    "height = 5.6    # Float\n",
    "is_cat = True   # Boolean\n",
    "flaws = None    # None type\n",
    "\n",
    "# Parallel & Chained Assignments\n",
    "x, y = 10, 20   # Assign multiple values\n",
    "a = b = c = 0   # Assign same value\n",
    "\n",
    "# Augmented Assignments\n",
    "counter = 0\n",
    "counter += 1\n",
    "numbers = [1, 2, 3]\n",
    "numbers += [4, 5]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Strings"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Creating Strings\n",
    "single = 'Hello'\n",
    "double = \"World\"\n",
    "multi = \"\"\"Multiple line string\"\"\"\n",
    "\n",
    "# String Operations\n",
    "greeting = \"me\" + \"ow!\"  # \"meow!\"\n",
    "repeat = \"Meow!\" * 3    # \"Meow!Meow!Meow!\"\n",
    "length = len(\"Python\")   # 6\n",
    "\n",
    "# String Methods\n",
    "print(\"a\".upper())                 # \"A\"\n",
    "print(\"A\".lower())                 # \"a\"\n",
    "print(\" a \".strip())               # \"a\"\n",
    "print(\"abc\".replace(\"bc\", \"ha\"))   # \"aha\"\n",
    "print(\"a b\".split())               # ['a', 'b']\n",
    "print(\"-\".join([\"a\", \"b\"]))        # \"a-b\"\n",
    "\n",
    "# Indexing & Slicing\n",
    "text = \"Python\"\n",
    "print(text[0])     # \"P\" (first)\n",
    "print(text[-1])    # \"n\" (last)\n",
    "print(text[1:4])   # \"yth\" (slice)\n",
    "print(text[:3])    # \"Pyt\" (from start)\n",
    "print(text[3:])    # \"hon\" (to end)\n",
    "print(text[::2])   # \"Pto\" (every 2nd)\n",
    "print(text[::-1])  # \"nohtyP\" (reverse)\n",
    "\n",
    "# Formatting (f-strings)\n",
    "name = \"Aubrey\"\n",
    "age = 2\n",
    "print(f\"Hello, {name}!\")         # \"Hello, Aubrey!\"\n",
    "print(f\"{name} is {age} years old\") # \"Aubrey is 2 years old\"\n",
    "print(f\"Debug: {age=}\")          # \"Debug: age=2\"\n",
    "\n",
    "# Raw Strings\n",
    "print(r\"This is:\tCool.\")         # \"This is:\\tCool.\""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. Numbers & Math"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Arithmetic Operators\n",
    "print(10 + 3)   # 13\n",
    "print(10 - 3)   # 7\n",
    "print(10 * 3)   # 30\n",
    "print(10 / 3)   # 3.3333333333333335\n",
    "print(10 // 3)  # 3\n",
    "print(10 % 3)   # 1\n",
    "print(2 ** 3)   # 8\n",
    "\n",
    "# Useful Built-in Math Functions\n",
    "print(abs(-5))            # 5\n",
    "print(round(3.7))         # 4\n",
    "print(round(3.14159, 2))  # 3.14\n",
    "print(min(3, 1, 2))       # 1\n",
    "print(max(3, 1, 2))       # 3\n",
    "print(sum([1, 2, 3]))     # 6"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 7. Conditionals"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "age = 18\n",
    "has_car = True\n",
    "\n",
    "# If-Elif-Else\n",
    "if age < 13:\n",
    "    category = \"child\"\n",
    "elif age < 20:\n",
    "    category = \"teenager\"\n",
    "else:\n",
    "    category = \"adult\"\n",
    "\n",
    "# Logical Operators\n",
    "if age >= 18 and has_car:\n",
    "    print(\"Roadtrip!\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 8. Loops"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# For Loops & Range\n",
    "for i in range(3):\n",
    "    print(i)  # 0, 1, 2\n",
    "\n",
    "# Enumerate\n",
    "fruits = [\"apple\", \"banana\"]\n",
    "for i, fruit in enumerate(fruits):\n",
    "    print(f\"{i}: {fruit}\")\n",
    "\n",
    "# Loop Control (break & continue)\n",
    "for i in range(10):\n",
    "    if i == 3:\n",
    "        continue  # Skip 3\n",
    "    if i == 5:\n",
    "        break     # Exit at 5\n",
    "    print(i)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 9. Functions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Defining & Calling Functions\n",
    "def greet_person(name, age=10):\n",
    "    return f\"Hello, {name}! Age: {age}\"\n",
    "\n",
    "print(greet_person(\"Bartosz\"))\n",
    "\n",
    "# Multiple Return Values\n",
    "def get_min_max(numbers):\n",
    "    return min(numbers), max(numbers)\n",
    "\n",
    "minimum, maximum = get_min_max([1, 5, 3])\n",
    "\n",
    "# Lambda Functions\n",
    "square = lambda x: x ** 2\n",
    "print(square(5))  # 25\n",
    "\n",
    "numbers = [1, 2, 3, 4]\n",
    "squared = list(map(lambda x: x ** 2, numbers))\n",
    "evens = list(filter(lambda x: x % 2 == 0, numbers))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 10. Classes & Object-Oriented Programming"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "class Animal:\n",
    "    def __init__(self, name):\n",
    "        self.name = name\n",
    "\n",
    "    def speak(self):\n",
    "        pass\n",
    "\n",
    "# Inheritance\n",
    "class Dog(Animal):\n",
    "    species = \"Canis lupus\"  # Class Attribute\n",
    "\n",
    "    def __init__(self, name, age):\n",
    "        super().__init__(name)\n",
    "        self.age = age       # Instance Attribute\n",
    "\n",
    "    def speak(self):\n",
    "        return f\"{self.name} barks!\"\n",
    "\n",
    "my_dog = Dog(\"Frieda\", 3)\n",
    "print(my_dog.speak())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 11. Exceptions & Error Handling"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "try:\n",
    "    number = int(\"10\")\n",
    "    result = 10 / number\n",
    "except ValueError:\n",
    "    print(\"Invalid number!\")\n",
    "except ZeroDivisionError:\n",
    "    print(\"Cannot divide by zero!\")\n",
    "else:\n",
    "    print(f\"Result: {result}\")\n",
    "finally:\n",
    "    print(\"Attempt completed.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 12. Collections (Lists, Tuples, Sets, Dictionaries)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Lists\n",
    "nums = [1, 2, 3]\n",
    "nums.append(4)\n",
    "nums.remove(2)\n",
    "last = nums.pop()\n",
    "\n",
    "# Tuples & Unpacking\n",
    "point = (3, 4)\n",
    "x, y = point\n",
    "first, *rest = (1, 2, 3, 4)\n",
    "\n",
    "# Sets\n",
    "a = {1, 2, 3}\n",
    "b = {3, 4, 5}\n",
    "print(a | b)  # Union\n",
    "print(a & b)  # Intersection\n",
    "\n",
    "# Dictionaries\n",
    "pet = {\"name\": \"Leo\", \"age\": 4}\n",
    "pet[\"sound\"] = \"Purr!\"\n",
    "age = pet.get(\"age\", 0)\n",
    "print(list(pet.keys()))\n",
    "print(list(pet.values()))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 13. Comprehensions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# List Comprehension\n",
    "squares = [x ** 2 for x in range(10)]\n",
    "evens = [x for x in range(20) if x % 2 == 0]\n",
    "\n",
    "# Dictionary Comprehension\n",
    "word_lengths = {word: len(word) for word in [\"hello\", \"world\"]}\n",
    "\n",
    "# Set Comprehension\n",
    "unique_lengths = {len(word) for word in [\"who\", \"what\", \"why\"]}"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 14. File I/O"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Write File\n",
    "with open(\"output.txt\", mode=\"w\", encoding=\"utf-8\") as file:\n",
    "    file.write(\"Hello, World!\\n\")\n",
    "\n",
    "# Read File\n",
    "with open(\"output.txt\", mode=\"r\", encoding=\"utf-8\") as file:\n",
    "    content = file.read()\n",
    "    print(content)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 15. Useful Python Constructs"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from collections import Counter\n",
    "\n",
    "# Variable Swap\n",
    "a, b = 1, 2\n",
    "a, b = b, a\n",
    "\n",
    "# Flatten List of Lists\n",
    "matrix = [[1, 2], [3, 4]]\n",
    "flat = [item for sublist in matrix for item in sublist]\n",
    "\n",
    "# Remove Duplicates (Preserve Order)\n",
    "my_list = [1, 2, 2, 3, 1]\n",
    "unique = list(dict.fromkeys(my_list))\n",
    "\n",
    "# Count Occurrences\n",
    "counts = Counter(my_list)\n",
    "print(counts)"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}, f, indent=2)  # replace notebook_data with the raw JSON above