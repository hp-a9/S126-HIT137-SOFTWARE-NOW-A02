def shift_lowercase(ch, shift1, shift2, encrypt=True):
    if 'a' <= ch <= 'm':
        shift = shift1 * shift2
        if encrypt:
            new_offset = (ord(ch) - ord('a') + shift) % 26
        else:
            new_offset = (ord(ch) - ord('a') - shift) % 26
        return chr(ord('a') + new_offset)

    elif 'n' <= ch <= 'z':
        shift = shift1 + shift2
        if encrypt:
            new_offset = (ord(ch) - ord('a') - shift) % 26
        else:
            new_offset = (ord(ch) - ord('a') + shift) % 26
        return chr(ord('a') + new_offset)

    return ch

def shift_uppercase(ch, shift1, shift2, encrypt=True):
    if 'A' <= ch <= 'M':
        shift = shift1
        if encrypt:
            new_offset = (ord(ch) - ord('A') - shift) % 26
        else:
            new_offset = (ord(ch) - ord('A') + shift) % 26
        return chr(ord('A') + new_offset)

    elif 'N' <= ch <= 'Z':
        shift = shift2 ** 2
        if encrypt:
            new_offset = (ord(ch) - ord('A') + shift) % 26
        else:
            new_offset = (ord(ch) - ord('A') - shift) % 26
        return chr(ord('A') + new_offset)

    return ch

def transform_text(text, shift1, shift2, encrypt=True):
    result = ""

    for ch in text:
        if 'a' <= ch <= 'z':
            result += shift_lowercase(ch, shift1, shift2, encrypt)
        elif 'A' <= ch <= 'Z':
            result += shift_uppercase(ch, shift1, shift2, encrypt)
        else:
            result += ch  # keep unchanged

    return result

def encrypt_file(shift1, shift2):
    with open("raw_text.txt", "r") as file:
        original_text = file.read()

    encrypted_text = transform_text(original_text, shift1, shift2, encrypt=True)

    with open("encrypted_text.txt", "w") as file:
        file.write(encrypted_text)

def decrypt_file(shift1, shift2):
    with open("encrypted_text.txt", "r") as file:
        encrypted_text = file.read()

    decrypted_text = transform_text(encrypted_text, shift1, shift2, encrypt=False)

    with open("decrypted_text.txt", "w") as file:
        file.write(decrypted_text)

def verify_decryption():
    with open("raw_text.txt", "r") as file:
        original_text = file.read()

    with open("decrypted_text.txt", "r") as file:
        decrypted_text = file.read()

    if original_text == decrypted_text:
        print("Decryption successful: original and decrypted texts match.")
    else:
        print("Decryption failed: original and decrypted texts do not match.")

def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    encrypt_file(shift1, shift2)
    decrypt_file(shift1, shift2)
    verify_decryption()
    
if __name__ == "__main__":
    main()
