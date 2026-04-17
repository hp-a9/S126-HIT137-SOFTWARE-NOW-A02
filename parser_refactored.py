"""
PARSER MODULE (REFACTORED)
==========================
Builds a parse tree from tokens and computes the value using recursive descent parsing.

Integrates with the tokenizer (q2.py) and returns the required format:
  Input:  ["3", "+", "5", "*", "2", "END"]
  Output: ("(+ 3 (* 5 2))", 13.0, 5)
"""

# Import the tokenizer
from q2 import tokenize

# ============================================================================
# GLOBAL STATE
# ============================================================================

tokens = []
position = 0


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def peek():
    """Return current token without consuming it"""
    global position
    if position < len(tokens):
        return tokens[position]
    return 'END'


def consume(expected=None):
    """Consume current token and move forward"""
    global position
    current = tokens[position]
    if expected and current != expected:
        raise ValueError(f"Expected '{expected}', got '{current}'")
    position += 1
    return current


def is_number(token):
    """Check if token is a number"""
    try:
        float(token)
        return True
    except:
        return False


# ============================================================================
# PARSER FUNCTIONS - Build tree and compute value
# ============================================================================

def parse_expression():
    """
    expression -> term ((+|-) term)*
    Handles addition and subtraction (lowest precedence)
    
    Returns: (tree_string, numeric_value)
    """
    node_tree, node_val = parse_term()
    
    while peek() in ('+', '-'):
        op = consume()
        right_tree, right_val = parse_term()
        
        # Compute value
        if op == '+':
            node_val = node_val + right_val
        else:  # op == '-'
            node_val = node_val - right_val
        
        # Build tree string
        node_tree = f"({op} {node_tree} {right_tree})"
    
    return (node_tree, node_val)


def parse_term():
    """
    term -> factor ((*|/) factor)*
    Handles multiplication and division (medium precedence)
    
    Returns: (tree_string, numeric_value)
    """
    node_tree, node_val = parse_factor()
    
    while peek() in ('*', '/'):
        op = consume()
        right_tree, right_val = parse_factor()
        
        # Compute value
        if op == '*':
            node_val = node_val * right_val
        else:  # op == '/'
            if right_val == 0:
                raise ValueError("Division by zero")
            node_val = node_val / right_val
        
        # Build tree string
        node_tree = f"({op} {node_tree} {right_tree})"
    
    return (node_tree, node_val)


def parse_factor():
    """
    factor -> '-' factor | primary
    Handles unary negation
    
    Returns: (tree_string, numeric_value)
    """
    # Unary negation
    if peek() == '-':
        consume('-')
        inner_tree, inner_val = parse_factor()
        # Apply negation
        inner_val = -inner_val
        tree = f"(neg {inner_tree})"
        return (tree, inner_val)
    
    # Reject unary +
    if peek() == '+':
        raise ValueError("Unary + is not supported")
    
    return parse_primary()


def parse_primary():
    """
    primary -> NUMBER | '(' expression ')' | implicit multiplication
    Handles numbers, parentheses, and implicit multiplication
    
    Returns: (tree_string, numeric_value)
    """
    node_tree = None
    node_val = None
    
    # Case 1: Number
    if is_number(peek()):
        token = consume()
        node_tree = token
        node_val = float(token)
    
    # Case 2: Parenthesized expression
    elif peek() == '(':
        consume('(')
        node_tree, node_val = parse_expression()
        consume(')')
    
    else:
        raise ValueError(f"Unexpected token: {peek()}")
    
    # ===== IMPLICIT MULTIPLICATION =====
    # If next token starts a primary (number or paren), treat as multiplication
    while peek() not in ('END', ')', '+', '-', '*', '/'):
        next_tree = None
        next_val = None
        
        # Next primary is a number
        if is_number(peek()):
            token = consume()
            next_tree = token
            next_val = float(token)
        
        # Next primary is a parenthesized expression
        elif peek() == '(':
            consume('(')
            next_tree, next_val = parse_expression()
            consume(')')
        
        else:
            break
        
        # Combine with implicit multiplication
        node_val = node_val * next_val
        node_tree = f"(* {node_tree} {next_tree})"
    
    return (node_tree, node_val)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def parse(token_list):
    """
    Main parsing function
    
    Args:
        token_list: List of tokens from tokenizer
        
    Returns:
        tuple: (tree_string, numeric_value, final_position)
        
    Raises:
        ValueError: If there are syntax errors
    """
    global tokens, position
    tokens = token_list
    position = 0
    
    try:
        tree, value = parse_expression()
        
        # Verify we've consumed all tokens
        if peek() != 'END':
            raise ValueError("Unexpected extra tokens after expression")
        
        return (tree, value, position)
    
    except ValueError as e:
        # Return error for assignment format
        raise e


# ============================================================================
# CONVENIENCE FUNCTION - Parse from string
# ============================================================================

def parse_expression_string(expression_str):
    """
    Convenience function: tokenize and parse in one call
    
    Args:
        expression_str: Mathematical expression as string
        
    Returns:
        tuple: (tree_string, numeric_value, final_position)
    """
    try:
        tokens_list = tokenize(expression_str)
        return parse(tokens_list)
    except ValueError as e:
        raise e


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PARSER TESTING")
    print("=" * 70)
    
    test_cases = [
        ("5", "5", 5.0),
        ("3 + 5", "(+ 3 5)", 8.0),
        ("3 + 5 * 2", "(+ 3 (* 5 2))", 13.0),
        ("(3 + 5) * 2", "(* (+ 3 5) 2)", 16.0),
        ("-5", "(neg 5)", -5.0),
        ("--5", "(neg (neg 5))", 5.0),
        ("2(3)", "(* 2 3)", 6.0),
        ("3 * -2", "(* 3 (neg 2))", -6.0),
        ("-(3 + 4)", "(neg (+ 3 4))", -7.0),
        ("(2 + 3)(4 + 5)", "(* (+ 2 3) (+ 4 5))", 45.0),
    ]
    
    print("\nTEST CASES:")
    print("-" * 70)
    
    passed = 0
    failed = 0
    
    for expr, expected_tree, expected_val in test_cases:
        print(f"\nInput: {expr!r}")
        try:
            tree, val, pos = parse_expression_string(expr)
            print(f"Tree:  {tree}")
            print(f"Value: {val}")
            
            # Check if results match
            if tree == expected_tree and abs(val - expected_val) < 0.0001:
                print("PASS")
                passed += 1
            else:
                print(f"FAIL")
                print(f"   Expected tree: {expected_tree}")
                print(f"   Expected val:  {expected_val}")
                failed += 1
        
        except ValueError as e:
            print(f"ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)
    
    # ===== ERROR CASES =====
    print("\nERROR CASES:")
    print("-" * 70)
    
    error_cases = [
        ("(3 + 5", "Missing closing parenthesis"),
        ("3 )", "Unexpected closing parenthesis"),
        ("+5", "Unary plus not supported"),
        ("3 +", "Unexpected end of expression"),
    ]
    
    for expr, description in error_cases:
        print(f"\nInput: {expr!r}")
        print(f"Expected: {description}")
        try:
            tree, val, pos = parse_expression_string(expr)
            print(f"FAIL - Should have raised error but got: {tree}")
        except ValueError as e:
            print(f"PASS - Got error: {e}")
