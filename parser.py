"""
PARSER MODULE
=============
Builds a parse tree (AST) from a list of tokens using recursive descent parsing.

Input:
  ["3", "+", "5", "*", "(", "2", "-", "1", ")", "END"]

Output (tree example):
  ('+', '3', ('*', '5', ('-', '2', '1')))
"""

# ---------------- GLOBAL STATE ----------------
tokens = []
position = 0


# ---------------- HELPER FUNCTIONS ----------------
def peek():
    """Return current token without consuming it"""
    return tokens[position]


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


# ---------------- PARSER FUNCTIONS ----------------

# expression -> term ((+|-) term)*
def parse_expression():
    node = parse_term()

    while peek() in ('+', '-'):
        op = consume()
        right = parse_term()
        node = (op, node, right)

    return node


# term -> factor ((*|/) factor)*
def parse_term():
    node = parse_factor()

    while peek() in ('*', '/'):
        op = consume()
        right = parse_factor()
        node = (op, node, right)

    return node


# factor -> '-' factor | primary
def parse_factor():
    # Unary negation
    if peek() == '-':
        consume('-')
        return ('neg', parse_factor())

    # Reject unary +
    if peek() == '+':
        raise ValueError("Unary + is not supported")

    return parse_primary()


# primary -> NUMBER | '(' expression ')' | implicit multiplication
def parse_primary():
    node = None

    if is_number(peek()):
        node = consume()

    elif peek() == '(':
        consume('(')
        node = parse_expression()
        consume(')')

    else:
        raise ValueError(f"Unexpected token: {peek()}")

    # --------- IMPLICIT MULTIPLICATION ---------
    # If next token starts a primary, treat as multiplication
    while peek() not in ('END', ')', '+', '-', '*', '/'):
        next_node = None

        if is_number(peek()):
            next_node = consume()

        elif peek() == '(':
            consume('(')
            next_node = parse_expression()
            consume(')')

        else:
            break

        node = ('*', node, next_node)

    return node


# ---------------- MAIN ENTRY ----------------
def parse(token_list):
    global tokens, position
    tokens = token_list
    position = 0

    tree = parse_expression()

    if peek() != 'END':
        raise ValueError("Unexpected extra tokens")

    return tree