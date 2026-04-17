"""
EVALUATOR MODULE
================

Final phase of the mathematical expression evaluator.

Workflow:
  input.txt
     ↓
  question2.py
     ↓
  output.txt

Reads expressions from input.txt and writes:
Input: ...
Tree: ...
Tokens: ...
Result: ...

(blank line between each)
"""

import os
from q2 import tokenize
from parser_refactored import parse_expression_string


def format_tokens(expression_str):
    """
    Convert tokenizer output into required token display format.
    """
    try:
        tokens = tokenize(expression_str)
        formatted_tokens = []

        for token in tokens:
            if token == "END":
                formatted_tokens.append("[END]")
            elif token == "(":
                formatted_tokens.append("[LPAREN:(]")
            elif token == ")":
                formatted_tokens.append("[RPAREN:)]")
            elif token in "+-*/":
                formatted_tokens.append(f"[OP:{token}]")
            else:
                value = float(token)
                if value.is_integer():
                    token = str(int(value))
                formatted_tokens.append(f"[NUM:{token}]")

        return " ".join(formatted_tokens)

    except ValueError:
        return "ERROR"


def parse_tree_to_nested(tree_str):
    """
    Convert tree string like:
      (+ 2 (* 3 4))
    into nested tuples like:
      ("+", 2, ("*", 3, 4))
    """
    spaced = tree_str.replace("(", " ( ").replace(")", " ) ")
    tokens = spaced.split()
    index = 0

    def parse_node():
        nonlocal index

        if tokens[index] == "(":
            index += 1
            op = tokens[index]
            index += 1

            if op == "neg":
                child = parse_node()
                if tokens[index] != ")":
                    raise ValueError("Invalid tree format")
                index += 1
                return ("neg", child)

            left = parse_node()
            right = parse_node()

            if tokens[index] != ")":
                raise ValueError("Invalid tree format")
            index += 1
            return (op, left, right)

        else:
            token = tokens[index]
            index += 1
            value = float(token)
            if value.is_integer():
                return int(value)
            return value

    return parse_node()


def evaluate_tree(node):
    """
    Evaluate nested tuple tree.
    """
    if not isinstance(node, tuple):
        return node

    op = node[0]

    if op == "neg":
        return -evaluate_tree(node[1])

    left = evaluate_tree(node[1])
    right = evaluate_tree(node[2])

    if op == "+":
        return left + right
    if op == "-":
        return left - right
    if op == "*":
        return left * right
    if op == "/":
        if right == 0:
            raise ZeroDivisionError("Division by zero")
        return left / right

    raise ValueError(f"Unknown operator: {op}")


def format_result(value):
    """
    whole number -> no decimal
    else -> 4 decimal places
    """
    if isinstance(value, str):
        return value

    if float(value).is_integer():
        return str(int(value))

    return f"{value:.4f}"


def evaluate_expression(expression_str):
    """
    Returns:
    {
        'input': ...,
        'tree': ...,
        'tokens': ...,
        'result': ...
    }
    """
    result_dict = {
        "input": expression_str,
        "tree": "ERROR",
        "tokens": "ERROR",
        "result": "ERROR"
    }

    # token formatting
    result_dict["tokens"] = format_tokens(expression_str)
    if result_dict["tokens"] == "ERROR":
        return result_dict

    # parse tree
    try:
        tree_str, pos = parse_expression_string(expression_str)
        result_dict["tree"] = tree_str
    except ValueError:
        return result_dict

    # evaluate separately so divide-by-zero keeps tree/tokens
    try:
        nested_tree = parse_tree_to_nested(tree_str)
        value = evaluate_tree(nested_tree)
        result_dict["result"] = format_result(value)
    except ZeroDivisionError:
        result_dict["result"] = "ERROR"
    except Exception:
        result_dict["tree"] = "ERROR"
        result_dict["tokens"] = "ERROR"
        result_dict["result"] = "ERROR"

    return result_dict


def evaluate_file(input_path: str) -> list[dict]:
    """
    Read input file
    Process all expressions
    Write output.txt
    Return results
    """
    input_dir = os.path.dirname(os.path.abspath(input_path))
    output_path = os.path.join(input_dir, "output.txt")

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found!")
        return []
    except IOError as e:
        print(f"Error reading input file: {e}")
        return []

    results = []

    for line in lines:
        expr = line.strip()

        if not expr:
            continue

        results.append(evaluate_expression(expr))

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            for i, result in enumerate(results):
                f.write(f"Input: {result['input']}\n")
                f.write(f"Tree: {result['tree']}\n")
                f.write(f"Tokens: {result['tokens']}\n")
                f.write(f"Result: {result['result']}\n")
                if i != len(results) - 1:
                    f.write("\n")
    except IOError as e:
        print(f"Error writing output file: {e}")

    return results


if __name__ == "__main__":
    input_file = "input.txt"

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found in current directory!")
        exit(1)

    results = evaluate_file(input_file)
    print(f"{len(results)} expression(s) processed.")
