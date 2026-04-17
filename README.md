### q2.py (Tokenizer)

**Responsibilities:**

* Breaks the input expression into tokens
* Identifies numbers, operators (`+`, `-`, `*`, `/`), and parentheses
* Outputs a list of tokens for the parser

**Key Feature:**

* Ensures unary negation is treated as a separate operator

---

### parser_refactored.py (Parser + Evaluator)

**Responsibilities:**

* Implements recursive descent parsing
* Handles operator precedence using separate functions
* Builds a parse tree representation of the expression
* Evaluates the expression and returns the computed result

**Supports:**

* Binary operators (`+`, `-`, `*`, `/`)
* Unary negation
* Parentheses (including nested)
* Implicit multiplication
