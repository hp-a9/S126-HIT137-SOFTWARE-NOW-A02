"""
PARSER MODULE (REFACTORED)
==========================
Builds a parse tree from tokens using recursive descent parsing.

Integrates with the tokenizer (q2.py) and returns:
  Input:  ["3", "+", "5", "*", "2", "END"]
  Output: ("(+ 3 (* 5 2))", position)

This module ONLY builds the tree.
Evaluation is handled separately in question2.py.
"""

from q2 import tokenize

tokens = []
position = 0


def peek():
    global position
    if position < len(tokens):
        return tokens[position]
    return 'END'


def consume(expected=None):
    global position
    current = tokens[position]
    if expected and current != expected:
        raise ValueError(f"Expected '{expected}', got '{current}'")
    position += 1
    return current


def is_number(token):
    try:
        float(token)
        return True
    except:
        return False


def normalize_number(token):
    value = float(token)
    if value.is_integer():
        return str(int(value))
    return str(value)


def parse_expression():
    """
    expression -> term ((+|-) term)*
    """
    node_tree = parse_term()

    while peek() in ('+', '-'):
        op = consume()
        right_tree = parse_term()
        node_tree = f"({op} {node_tree} {right_tree})"

    return node_tree


def parse_term():
    """
    term -> factor ((*|/) factor)*
    """
    node_tree = parse_factor()

    while peek() in ('*', '/'):
        op = consume()
        right_tree = parse_factor()
        node_tree = f"({op} {node_tree} {right_tree})"

    return node_tree


def parse_factor():
    """
    factor -> '-' factor | primary
    """
    if peek() == '-':
        consume('-')
        inner_tree = parse_factor()
        return f"(neg {inner_tree})"

    if peek() == '+':
        raise ValueError("Unary + is not supported")

    return parse_primary()


def parse_primary():
    """
    primary -> NUMBER | '(' expression ')' | implicit multiplication
    """
    node_tree = None

    if is_number(peek()):
        token = consume()
        node_tree = normalize_number(token)

    elif peek() == '(':
        consume('(')
        node_tree = parse_expression()
        consume(')')

    else:
        raise ValueError(f"Unexpected token: {peek()}")

    # implicit multiplication: 2(3), (2+3)(4+5), 2 3
    while True:
        if is_number(peek()):
            token = consume()
            next_tree = normalize_number(token)
            node_tree = f"(* {node_tree} {next_tree})"
        elif peek() == '(':
            consume('(')
            next_tree = parse_expression()
            consume(')')
            node_tree = f"(* {node_tree} {next_tree})"
        else:
            break

    return node_tree


def parse(token_list):
    """
    Args:
        token_list: list of tokens from tokenizer

    Returns:
        tuple: (tree_string, final_position)
    """
    global tokens, position
    tokens = token_list
    position = 0

    tree = parse_expression()

    if peek() != 'END':
        raise ValueError("Unexpected extra tokens after expression")

    return (tree, position)


def parse_expression_string(expression_str):
    """
    Convenience function: tokenize and parse in one call

    Returns:
        tuple: (tree_string, final_position)
    """
    tokens_list = tokenize(expression_str)
    return parse(tokens_list)


if __name__ == "__main__":
    test_cases = [
        ("5", "5"),
        ("3 + 5", "(+ 3 5)"),
        ("3 + 5 * 2", "(+ 3 (* 5 2))"),
        ("(3 + 5) * 2", "(* (+ 3 5) 2)"),
        ("-5", "(neg 5)"),
        ("--5", "(neg (neg 5))"),
        ("2(3)", "(* 2 3)"),
        ("3 * -2", "(* 3 (neg 2))"),
        ("-(3 + 4)", "(neg (+ 3 4))"),
        ("(2 + 3)(4 + 5)", "(* (+ 2 3) (+ 4 5))"),
    ]

    for expr, expected_tree in test_cases:
        try:
            tree, pos = parse_expression_string(expr)
            print(expr, "=>", tree, "| PASS" if tree == expected_tree else "| FAIL")
        except ValueError as e:
            print(expr, "=> ERROR:", e)
