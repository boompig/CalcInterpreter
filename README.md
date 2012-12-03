CalcInterpreter
===============

A calculator interpreter written in Python.
Allows for basic math operations, variable assignment (peristent), etc.
Uses Abstract Syntax Trees (kind of).
Preserves order of operations
Has some syntactic sugar that you would expect.

= Operations =

- basic arithmetic
- exponents
- brackets
- respect for order of operations
- assign variables
- factoring (slow on purpose) 

= Parallelization = 

Possibly the most interesting feature: the interpreter performs unrelated operations in parallel. This is verifiable via the very slow factoring operation and the timing module included.

Level of parallelization should be quite high, though a large-enough expression (many operands) might cause the threading to crash the computer (not sure about this). Works by parallelizing the evaluation of each subtree (obv. subtrees are unrelated).


= Future Enhancements =

- Does not (yet) support constants, trig, etc.

- (often) ignores garbage characters and unmatched parens (can figure it out most of the time)


