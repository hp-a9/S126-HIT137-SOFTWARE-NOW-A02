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
    pass

def encrypt_file(shift1, shift2):
    pass

def decrypt_file(shift1, shift2):
    pass

def verify_decryption():
    pass

def main():
    pass

if __name__ == "__main__":
    main()
