
# Encryption Program
# Task 1: Encrypt raw_text.txt using shift1 and shift2

# ============================================
# STEP 2: Create the shift_character function
# ============================================


# Encryption Program
# Task 1: Encrypt raw_text.txt using shift1 and shift2

# ============================================
# Get shift values from user input
# ============================================

print("=" * 50)
print("   ENCRYPTION PROGRAM - TASK 1")
print("=" * 50)
print()

# Prompt user for shift1
while True:
    try:
        shift1 = int(input("Enter shift1 value (a positive integer): "))
        if shift1 < 0:
            print("Error: shift1 must be a positive integer. Try again.")
            continue
        break
    except ValueError:
        print("Error: Please enter a valid integer. Try again.")

# Prompt user for shift2
while True:
    try:
        shift2 = int(input("Enter shift2 value (a positive integer): "))
        if shift2 < 0:
            print("Error: shift2 must be a positive integer. Try again.")
            continue
        break
    except ValueError:
        print("Error: Please enter a valid integer. Try again.")

print(f"\n✓ Using shift1={shift1} and shift2={shift2}")
print()

# ============================================
# STEP 2: Create the shift_character function
# ============================================

def shift_character(char, shift1, shift2):
    """
    Encrypts a single character based on the encryption rules.
    
    Rules:
    - Lowercase a-m: shift forward by (shift1 × shift2)
    - Lowercase n-z: shift backward by (shift1 + shift2)
    - Uppercase A-M: shift backward by shift1
    - Uppercase N-Z: shift forward by (shift2²)
    - Other characters: remain unchanged
    """
    
    # Check if it's a lowercase letter
    if char.islower():
        # Get position in alphabet (0-25)
        position = ord(char) - ord('a')
        
        # Check if in first half (a-m, positions 0-12)
        if char >= 'a' and char <= 'm':
            # Shift forward by (shift1 × shift2)
            shift_amount = shift1 * shift2
            new_position = (position + shift_amount) % 26
        
        # Check if in second half (n-z, positions 13-25)
        else:  # char >= 'n' and char <= 'z'
            # Shift backward by (shift1 + shift2)
            shift_amount = shift1 + shift2
            new_position = (position - shift_amount) % 26
        
        # Convert back to character
        return chr(ord('a') + new_position)
    
    # Check if it's an uppercase letter
    elif char.isupper():
        # Get position in alphabet (0-25)
        position = ord(char) - ord('A')
        
        # Check if in first half (A-M, positions 0-12)
        if char >= 'A' and char <= 'M':
            # Shift backward by shift1
            shift_amount = shift1
            new_position = (position - shift_amount) % 26
        
        # Check if in second half (N-Z, positions 13-25)
        else:  # char >= 'N' and char <= 'Z'
            # Shift forward by (shift2²)
            shift_amount = shift2 ** 2  # shift2 squared
            new_position = (position + shift_amount) % 26
        
        # Convert back to character
        return chr(ord('A') + new_position)
    
    # If it's not a letter (space, number, special char), return unchanged
    else:
        return char


# ============================================
# STEP 3: Create the encrypt_text function
# ============================================

def encrypt_text(text, shift1, shift2):
    """
    Encrypts the entire text by applying shift_character to each character.
    """
    encrypted_text = ""
    
    # Loop through each character in the text
    for char in text:
        # Apply the shift_character function and add to encrypted text
        encrypted_char = shift_character(char, shift1, shift2)
        encrypted_text += encrypted_char
    
    return encrypted_text


# ============================================
# STEP 1: Read the raw_text.txt file
# ============================================

try:
    with open('raw_text.txt', 'r') as file:
        raw_text = file.read()
    print("Successfully read raw_text.txt")
    print(f"Original text:\n{raw_text}\n")
except FileNotFoundError:
    print("Error: raw_text.txt not found!")
    exit()


# ============================================
# STEP 4: Encrypt the text
# ============================================

encrypted_text = encrypt_text(raw_text, shift1, shift2)
print(f"Encrypted text:\n{encrypted_text}\n")


# ============================================
# STEP 5: Write encrypted text to file
# ============================================

try:
    with open('encrypted_text.txt', 'w') as file:
        file.write(encrypted_text)
    print("Successfully wrote encrypted text to encrypted_text.txt")
except Exception as e:
    print(f"Error writing to file: {e}")
    exit()

