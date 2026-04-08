# Question 1: Encryption and Decryption Program

def shift_within_group(ch, group_start, group_size, shift, forward=True):
    offset = ord(ch) - ord(group_start)
    if forward:
        new_offset = (offset + shift) % group_size
    else:
        new_offset = (offset - shift) % group_size
    return chr(ord(group_start) + new_offset)


def encrypt_char(ch, shift1, shift2):
    # Lowercase first half: a-m
    if 'a' <= ch <= 'm':
        return shift_within_group(ch, 'a', 13, shift1 * shift2, forward=True)

    # Lowercase second half: n-z
    if 'n' <= ch <= 'z':
        return shift_within_group(ch, 'n', 13, shift1 + shift2, forward=False)

    # Uppercase first half: A-M
    if 'A' <= ch <= 'M':
        return shift_within_group(ch, 'A', 13, shift1, forward=False)

    # Uppercase second half: N-Z
    if 'N' <= ch <= 'Z':
        return shift_within_group(ch, 'N', 13, shift2 ** 2, forward=True)

    # Other characters unchanged
    return ch


def decrypt_char(ch, shift1, shift2):
    # Lowercase first half: a-m
    if 'a' <= ch <= 'm':
        return shift_within_group(ch, 'a', 13, shift1 * shift2, forward=False)

    # Lowercase second half: n-z
    if 'n' <= ch <= 'z':
        return shift_within_group(ch, 'n', 13, shift1 + shift2, forward=True)

    # Uppercase first half: A-M
    if 'A' <= ch <= 'M':
        return shift_within_group(ch, 'A', 13, shift1, forward=True)

    # Uppercase second half: N-Z
    if 'N' <= ch <= 'Z':
        return shift_within_group(ch, 'N', 13, shift2 ** 2, forward=False)

    # Other characters unchanged
    return ch


def transform_text(text, shift1, shift2, encrypt=True):
    result = ""

    for ch in text:
        if encrypt:
            result += encrypt_char(ch, shift1, shift2)
        else:
            result += decrypt_char(ch, shift1, shift2)

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
