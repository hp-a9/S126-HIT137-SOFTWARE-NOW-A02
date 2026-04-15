"""
TOKENIZER MODULE
================
Converts a mathematical expression string into a list of tokens.

Example:
  Input:  "3 + 5 * (2 - 1)"
  Output: ["3", "+", "5", "*", "(", "2", "-", "1", ")", "END"]
"""

def tokenize(expression: str) -> list:
    """
    Converts a mathematical expression string into a list of tokens.
    
    Args:
        expression (str): The mathematical expression to tokenize
        
    Returns:
        list: A list of token strings, ending with "END"
        
    Raises:
        ValueError: If an invalid character is encountered
    """
    
    tokens = []
    position = 0
    
    # Keep processing until we reach the end of the string
    while position < len(expression):
        #  STEP 1: Skip whitespace
        # Skip spaces, tabs, and newlines
        if expression[position] in ' \t\n':
            position += 1
            continue
        
        current_char = expression[position]
        
        # === STEP 2: Check if it's a number =====
        # Numbers can be: 3, 15, 3.14, 0.5
        if current_char.isdigit():
            number_str = ""
            has_decimal = False
            
            # Keep reading characters while they're digits or a decimal point
            while position < len(expression):
                char = expression[position]
                
                # If it's a digit, add it to the number
                if char.isdigit():
                    number_str += char
                    position += 1
                
                # If it's a decimal point
                elif char == '.':
                    # Check if we already have a decimal point
                    if has_decimal:
                        # ERROR: Multiple decimal points (e.g., 3.1.4)
                        raise ValueError(f"Invalid number: multiple decimal points in '{number_str}{char}...'")
                    
                    # Check if there's a digit after the decimal
                    if position + 1 >= len(expression) or not expression[position + 1].isdigit():
                        # ERROR: No digit after decimal (e.g., 3. or 3.+)
                        raise ValueError(f"Invalid number: decimal point must be followed by a digit")
                    
                    has_decimal = True
                    number_str += char
                    position += 1
                
                # If it's anything else, stop reading the number
                else:
                    break
            
            # Add the complete number token
            tokens.append(number_str)
        
        # ===== STEP 3: Check if it's an operator =====
        # Valid operators: +, -, *, /
        elif current_char in '+-*/':
            tokens.append(current_char)
            position += 1
        
        # ===== STEP 4: Check if it's a left parenthesis =====
        elif current_char == '(':
            tokens.append('(')
            position += 1
        
        # ===== STEP 5: Check if it's a right parenthesis =====
        elif current_char == ')':
            tokens.append(')')
            position += 1
        
        # ===== STEP 6: Invalid character =====
        # If we get here, it's not a valid character
        else:
            raise ValueError(f"Invalid character: '{current_char}' at position {position}")
    
    # Add the END token to mark the end of input
    tokens.append('END')
    
    return tokens

# TESTING THE TOKENIZER
# ============================================================================
 
if __name__ == "__main__":
    print("=" * 70)
    print("TOKENIZER - MATHEMATICAL EXPRESSION PARSER")
    print("=" * 70)
    
    # =========== SECTION 1: AUTOMATED TEST CASES ===========
    print("\n" + "=" * 70)
    print("SECTION 1: AUTOMATED TEST CASES")
    print("=" * 70)
    
    test_cases = [
        "3 + 5",
        "10 - 2 * 3",
        "(2 + 3) * 4",
        "-5",
        "-(3 + 4)",
        "2(3 + 4)",
        "3 * -2",
        "--5",
        "8 / 2",
        "(10 + 5) / 3",
        "3.14 + 2.86",
        "3 @ 5",  # Invalid character
        "3. + 5",  # Invalid decimal
        "3.1.4",   # Multiple decimals
    ]
    
    for test in test_cases:
        print(f"\nInput:  {test!r}")
        try:
            result = tokenize(test)
            print(f"Output: {result}")
        except ValueError as e:
            print(f"ERROR:  {e}")





#  # =========== SECTION 2: INTERACTIVE USER INPUT ===========
# print("\n" + "=" * 70)
# print("SECTION 2: INTERACTIVE USER INPUT")
# print("=" * 70)
# print("\nEnter mathematical expressions to tokenize.")
# print("Type 'quit' or 'exit' to stop.\n")

# while True:
#     try:
#         # Get user input
#         user_input = input("Enter expression: ").strip()
        
#         # Check if user wants to exit
#         if user_input.lower() in ['quit', 'exit', 'q']:
#             print("\n" + "=" * 70)
#             print("Program successfully terminated...")
#             print("=" * 70)
#             break
        
#         # Skip empty input
#         if not user_input:
#             print("Please enter a non-empty expression.\n")
#             continue
        
#         # Tokenize the input
#         tokens = tokenize(user_input)
        
#         # Display results
#         print(f"\nTokenization successful!")
#         print(f"Tokens: {tokens}")
        
#         # Display tokens in a more readable format
#         print(f"Formatted: ", end="")
#         for token in tokens:
#             if token == "END":
#                 print(f"[END]", end="")
#             elif token in '+-*/()':
#                 print(f"[OP:{token}]", end=" ")
#             elif token in '()':
#                 if token == '(':
#                     print(f"[LPAREN]", end=" ")
#                 else:
#                     print(f"[RPAREN]", end=" ")
#             else:
#                 # It's a number
#                 print(f"[NUM:{token}]", end=" ")
#         print("\n")
        
#     except ValueError as e:
#         print(f"\nERROR: {e}\n")
#     except KeyboardInterrupt:
#         print("\n\n" + "=" * 70)
#         print("Program interrupted!")
#         print("=" * 70)
#         break
#     except Exception as e:
#         print(f"\nUnexpected error: {e}\n")

