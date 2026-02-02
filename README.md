# Argumentation Framework Solver

> Master IAD Project - Knowledge Representation and Reasoning  
> Academic Year 2025-2026

**[Français](README.fr.md)** | **English**

## Overview

This project implements a solver for Argumentation Systems (AS). It computes and verifies different types of extensions according to preferred (PR) and stable (ST) semantics.

An argumentation framework is defined as **F = ⟨A, R⟩** where:
- **A** is a set of abstract arguments
- **R ⊆ A × A** is the attack relation between arguments

**For more detailed information, please refer to the [detailed report](rapport.pdf).**

## Supported Problems

The program solves the following 6 problems:

| Problem | Semantics | Description |
|---------|-----------|-------------|
| **VE-PR** | Preferred | Verify if S is a preferred extension |
| **DC-PR** | Preferred | Credulous acceptance of an argument |
| **DS-PR** | Preferred | Skeptical acceptance of an argument |
| **VE-ST** | Stable | Verify if S is a stable extension |
| **DC-ST** | Stable | Credulous acceptance of an argument |
| **DS-ST** | Stable | Skeptical acceptance of an argument |

## Installation

### Prerequisites

- Python 3.8 or higher
- No external dependencies required (standard library only)

### Installation Verification

```bash
python3 --version
```

## Usage

### General Syntax

```bash
python3 program.py -p <PROBLEM> -f <FILE> -a <ARGUMENTS>
```

### Parameters

- **-p**: Problem type (`VE-PR`, `DC-PR`, `DS-PR`, `VE-ST`, `DC-ST`, `DS-ST`)
- **-f**: Path to the `.apx` file containing the argumentation framework
- **-a**: Query arguments
  - For VE-* problems: comma-separated list (e.g., `a,c,d`)
  - For DC-* and DS-* problems: single argument (e.g., `b`)

### Usage Examples

Assuming `af.txt` contains an AF with A = {a,b,c,d} and R = {(a,b), (b,c), (b,d)}:

```bash
# Verify if {a,c,d} is a preferred extension
python3 program.py -p VE-PR -f af.txt -a a,c,d
# Output: YES

# Check credulous acceptance of 'b' (preferred semantics)
python3 program.py -p DC-PR -f af.txt -a b
# Output: NO

# Check skeptical acceptance of 'a' (preferred semantics)
python3 program.py -p DS-PR -f af.txt -a a
# Output: YES

# Verify if {a,c,d} is a stable extension
python3 program.py -p VE-ST -f af.txt -a a,c,d
# Output: YES
```

## Project Structure

```
Argumentation-Project/
├── README.md                
├── README.fr.md             # French documentation
├── program.py               # Main entry point
├── src/
│   ├── __init__.py
│   ├── cli.py              # Command-line argument handling
│   ├── apx_parser.py       # Parser for .apx files
│   ├── systeme_argumentation.py  # Argumentation system class
│   ├── semantics.py        # Semantics algorithms
│   └── queries.py          # Query resolution
└── Fichiers-tests/         # Test files
    ├── test_af1.apx
    ├── test_af1_pr.txt
    ├── test_af1_st.txt
    └── ...
```

## APX File Format

The `.apx` files follow this format:

```
arg(argument_name).
att(source_argument,target_argument).
```

### Format Rules

- Each argument must be declared with `arg()` before being used in an attack
- No spaces in lines
- Argument names can contain letters, numbers, and `_` (except `arg` and `att` which are reserved)

### Example

```
arg(a).
arg(b).
arg(c).
arg(d).
att(a,b).
att(b,c).
att(b,d).
```

This example represents the following graph:
```
a → b → c
    ↓
    d
```

## Running Tests

The `Fichiers-tests/` directory contains several test cases:

```bash
# Test with provided files
python3 program.py -p VE-PR -f Fichiers-tests/test_af1.apx -a a,c,d
python3 program.py -p DC-ST -f Fichiers-tests/test_af2.apx -a b
```

## Implementation Details

### Preferred Extensions

The solver uses a backtracking algorithm to compute all conflict-free, admissible sets, and then identifies maximal admissible sets (preferred extensions).

### Stable Extensions

A stable extension is computed by finding conflict-free sets that attack all arguments outside the set.

### Query Resolution

- **VE (Verification)**: Checks if the given set is an extension under the specified semantics
- **DC (Credulous)**: Returns YES if the argument appears in at least one extension
- **DS (Skeptical)**: Returns YES if the argument appears in all extensions

## Author

[@thmsgo18](https://github.com/thmsgo18) - Thomas Gourmelen
