"""
EVALUATOR MODULE
================
[ IMPORTANT NOTE!!! :: The two files 'q2' and 'parser_refactored' can be found in the branch "Tokenizer" ]

This is the FINAL PHASE of the mathematical expression evaluator.

Workflow:
  input.txt (expressions to evaluate)
       ↓
  evaluator.py (reads, tokenizes, parses, evaluates)
       ↓
  output.txt (results with format specified by the lecturer)

The evaluator reads from input.txt and writes results to output.txt
in the format:
  Input: 3 + 5 * 2
  Tree: (+ 3 (* 5 2))
  Tokens: [NUM:3] [OP:+] [NUM:5] [OP:*] [NUM:2] [END]
  Result: 13
  
  (blank line between expressions)

  
"""

import os
from q2 import tokenize # get the file 'q2' from Branch "Tokenizer"
from parser_refactored import parse_expression_string # get the file 'parser_refactored' from Branch "Tokenizer"


def format_tokens(expression_str):
    """
    Tokenize expression and format tokens in the required format.
    
    Args:
        expression_str: Mathematical expression as string
        
    Returns:
        str: Formatted tokens like "[NUM:3] [OP:+] [NUM:5] [END]"
              or "ERROR" if tokenization fails
    """
    try:
        tokens = tokenize(expression_str)
        
        formatted_tokens = []
        for token in tokens:
            if token == 'END':
                formatted_tokens.append("[END]")
            elif token in '+-*/()':
                if token == '(':
                    formatted_tokens.append("[LPAREN]")
                elif token == ')':
                    formatted_tokens.append("[RPAREN]")
                else:
                    formatted_tokens.append(f"[OP:{token}]")
            else:
                # It's a number
                formatted_tokens.append(f"[NUM:{token}]")
        
        return " ".join(formatted_tokens)
    except ValueError:
        return "ERROR"


def format_result(value):
    """
    Format the numeric result according to requirements:
    - Whole numbers without decimal point (8.0 → 8)
    - Otherwise rounded to 4 decimal places
    
    Args:
        value: The numeric result (float)
        
    Returns:
        str: Formatted result (int or float)
    """
    if isinstance(value, str):  # Error case
        return value
    
    # Check if it's a whole number
    if value == int(value):
        return str(int(value))
    else:
        # Round to 4 decimal places
        return f"{value:.4f}"


def evaluate_expression(expression_str):
    """
    Evaluate a single expression and return all components.
    
    Args:
        expression_str: Mathematical expression as string
        
    Returns:
        dict: {
            'input': original expression,
            'tree': parse tree string or 'ERROR',
            'tokens': formatted tokens or 'ERROR',
            'result': numeric result or 'ERROR'
        }
    """
    result_dict = {
        'input': expression_str,
        'tree': 'ERROR',
        'tokens': 'ERROR',
        'result': 'ERROR'
    }
    
    # Get tokens and format them
    result_dict['tokens'] = format_tokens(expression_str)
    
    # Try to parse and evaluate
    try:
        tree, value, pos = parse_expression_string(expression_str)
        result_dict['tree'] = tree
        result_dict['result'] = format_result(value)
    except ValueError as e:
        # Keep error markers from above
        pass
    
    return result_dict


def evaluate_file(input_path, output_path=None):
    """
    Read expressions from input file and write results to output file.
    
    Args:
        input_path: Path to input.txt file
        output_path: Path to output.txt file (defaults to same directory as input)
        
    Returns:
        list: List of result dictionaries (one per expression)
    """
    
    # Determine output path
    if output_path is None:
        input_dir = os.path.dirname(os.path.abspath(input_path))
        output_path = os.path.join(input_dir, 'output.txt')
    
    # Read input file
    try:
        with open(input_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found!")
        return []
    except IOError as e:
        print(f"Error reading input file: {e}")
        return []
    
    # Process each expression
    results = []
    output_lines = []
    
    for i, line in enumerate(lines):
        # Skip empty lines and comments
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Skip comments (lines starting with #)
        if line.startswith('#'):
            continue
        
        print(f"Processing: {line}")
        
        # Evaluate the expression
        result = evaluate_expression(line)
        results.append(result)
        
        # Format for output file
        output_lines.append(f"Input: {result['input']}")
        output_lines.append(f"Tree: {result['tree']}")
        output_lines.append(f"Tokens: {result['tokens']}")
        output_lines.append(f"Result: {result['result']}")
        output_lines.append("")  # Blank line between expressions
    
    # Write to output file
    try:
        with open(output_path, 'w') as f:
            f.write('\n'.join(output_lines))
        print(f"\n✓ Results written to: {output_path}")
    except IOError as e:
        print(f"Error writing to output file: {e}")
        return results
    
    return results


# ============================================================================
# MAIN - Run the evaluator
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("MATHEMATICAL EXPRESSION EVALUATOR")
    print("=" * 70)
    print()
    
    # Find input.txt in the current directory or ask user
    input_file = "input.txt"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found in current directory!")
        print("Please create an input.txt file with expressions to evaluate.")
        exit(1)
    
    print(f"Reading from: {input_file}")
    print("-" * 70)
    print()
    
    # Run the evaluator
    results = evaluate_file(input_file)
    
    # Summary
    print()
    print("=" * 70)
    print(f"SUMMARY: {len(results)} expression(s) processed")
    print("=" * 70)
