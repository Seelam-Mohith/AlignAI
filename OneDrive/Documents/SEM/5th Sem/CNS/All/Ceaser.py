# Ceaser

def caesar_cipher_encrypt(message, shift):
    result = ""
    for ch in message:
        if ch.isupper():
            # shift uppercase characters
            result += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
        elif ch.islower():
            # shift lowercase characters
            result += chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
        else:
            # non-alphabetic characters remain same
            result += ch
    return result

def caesar_cipher_decrypt(ciphertext, shift):
    # decrypt by shifting in the opposite direction
    return caesar_cipher_encrypt(ciphertext, -shift)

def main():
    msg = input("Enter message: ")
    s = int(input("Enter shift amount (0-25): "))
    encrypted = caesar_cipher_encrypt(msg, s)
    print("Encrypted message:", encrypted)
    decrypted = caesar_cipher_decrypt(encrypted, s)
    print("Decrypted back:", decrypted)

if __name__ == "__main__":
    main()


# Vignere

def vigenere_cipher_encrypt(message, key):
    result = ""
    key = key.lower()  # Convert key to lowercase for consistency
    key_index = 0      # To keep track of which letter in the key we're using

    for ch in message:
        if ch.isalpha():  # Encrypt only letters
            shift = ord(key[key_index % len(key)]) - ord('a')  # Convert key letter to shift (0-25)
            
            if ch.isupper():
                result += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
            else:
                result += chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
            
            key_index += 1  # Move to the next letter of the key
        else:
            result += ch  # Non-letters stay unchanged

    return result


def vigenere_cipher_decrypt(ciphertext, key):
    result = ""
    key = key.lower()
    key_index = 0

    for ch in ciphertext:
        if ch.isalpha():  # Decrypt only letters
            shift = ord(key[key_index % len(key)]) - ord('a')
            
            if ch.isupper():
                result += chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))
            else:
                result += chr((ord(ch) - ord('a') - shift) % 26 + ord('a'))
            
            key_index += 1
        else:
            result += ch

    return result


def main():
    msg = input("Enter message: ")
    key = input("Enter key (letters only): ")

    encrypted = vigenere_cipher_encrypt(msg, key)
    print("Encrypted message:", encrypted)

    decrypted = vigenere_cipher_decrypt(encrypted, key)
    print("Decrypted back:", decrypted)


if __name__ == "__main__":
    main()


# Hill

import numpy as np

def hill_encrypt(msg, key_matrix):
    msg = msg.replace(" ", "").lower()
    while len(msg) % 3 != 0:  # pad to fit matrix size
        msg += 'x'
    nums = [ord(c) - 97 for c in msg]  # convert to 0-25
    nums = np.array(nums).reshape(-1, 3)
    enc = (nums @ key_matrix) % 26
    return "".join(chr(n + 97) for n in enc.flatten())


def hill_decrypt(cipher, key_matrix):
    det = int(round(np.linalg.det(key_matrix)))  # determinant
    det_inv = pow(det, -1, 26)  # modular inverse of det mod 26
    key_inv = (det_inv * np.round(det * np.linalg.inv(key_matrix)).astype(int)) % 26
    nums = [ord(c) - 97 for c in cipher]
    nums = np.array(nums).reshape(-1, 3)
    dec = (nums @ key_inv) % 26
    return "".join(chr(n + 97) for n in dec.flatten())


# === MAIN PROGRAM ===
def main():
    msg = input("Enter message: ")
    print("Enter 3x3 key matrix row-wise (9 numbers):")
    key = [int(x) for x in input().split()]
    key_matrix = np.array(key).reshape(3, 3)

    enc = hill_encrypt(msg, key_matrix)
    print("\nEncrypted:", enc)

    dec = hill_decrypt(enc, key_matrix)
    print("Decrypted back:", dec)


if __name__ == "__main__":
    main()


# Playfair

def generate_key_matrix(key):
    """Generate a 5x5 Playfair key matrix from the given key."""
    key = key.lower().replace("j", "i")  # Merge I and J
    result = ""
    for ch in key:
        if ch not in result and ch.isalpha():
            result += ch

    # Add remaining letters of alphabet
    for ch in "abcdefghijklmnopqrstuvwxyz":
        if ch not in result and ch != "j":
            result += ch

    # Convert to 5x5 matrix
    matrix = [list(result[i:i+5]) for i in range(0, 25, 5)]
    return matrix


def preprocess_message(message):
    """Prepare message for Playfair encryption (remove spaces, handle duplicates)."""
    message = message.lower().replace("j", "i")
    cleaned = ""
    for ch in message:
        if ch.isalpha():
            cleaned += ch

    # Break into digraphs and insert 'x' between double letters
    i = 0
    pairs = []
    while i < len(cleaned):
        a = cleaned[i]
        b = cleaned[i+1] if i+1 < len(cleaned) else "x"
        if a == b:
            pairs.append(a + "x")
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    return pairs


def find_position(matrix, ch):
    """Find row, column of a letter in the matrix."""
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == ch:
                return row, col


def playfair_encrypt(message, key):
    matrix = generate_key_matrix(key)
    pairs = preprocess_message(message)
    result = ""

    for a, b in pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:  # Same row → shift right
            result += matrix[row1][(col1 + 1) % 5]
            result += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:  # Same column → shift down
            result += matrix[(row1 + 1) % 5][col1]
            result += matrix[(row2 + 1) % 5][col2]
        else:  # Rectangle → swap columns
            result += matrix[row1][col2]
            result += matrix[row2][col1]

    return result


def playfair_decrypt(ciphertext, key):
    matrix = generate_key_matrix(key)
    result = ""

    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:  # Same row → shift left
            result += matrix[row1][(col1 - 1) % 5]
            result += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:  # Same column → shift up
            result += matrix[(row1 - 1) % 5][col1]
            result += matrix[(row2 - 1) % 5][col2]
        else:  # Rectangle → swap columns
            result += matrix[row1][col2]
            result += matrix[row2][col1]

    return result


def main():
    message = input("Enter message: ")
    key = input("Enter key: ")

    encrypted = playfair_encrypt(message, key)
    print("Encrypted message:", encrypted)

    decrypted = playfair_decrypt(encrypted, key)
    print("Decrypted back:", decrypted)


if __name__ == "__main__":
    main()


#Rail

def rail_fence_encrypt(msg, rails):
    msg = msg.replace(" ", "").lower()
    fence = [""] * rails
    rail, step = 0, 1
    for ch in msg:
        fence[rail] += ch
        rail += step
        if rail == 0 or rail == rails - 1:
            step *= -1
    return "".join(fence)


def rail_fence_decrypt(cipher, rails):
    pattern, rail, step = [], 0, 1
    for _ in cipher:
        pattern.append(rail)
        rail += step
        if rail == 0 or rail == rails - 1:
            step *= -1

    rail_counts = [pattern.count(r) for r in range(rails)]
    rails_data, i = [], 0
    for count in rail_counts:
        rails_data.append(list(cipher[i:i+count]))
        i += count

    res = ""
    positions = [0] * rails
    for r in pattern:
        res += rails_data[r][positions[r]]
        positions[r] += 1
    return res


# === MAIN PROGRAM ===
def main():
    msg = input("Enter message: ")
    rails = int(input("Enter number of rails: "))
    
    encrypted = rail_fence_encrypt(msg, rails)
    print("\nEncrypted message:", encrypted)
    
    decrypted = rail_fence_decrypt(encrypted, rails)
    print("Decrypted back:", decrypted)

if __name__ == "__main__":
    main()

# Row

def row_trans_encrypt(msg, key):
    msg = msg.replace(" ", "").lower()
    klen = len(key)
    while len(msg) % klen:  # pad if needed
        msg += "x"

    rows = [msg[i:i+klen] for i in range(0, len(msg), klen)]
    order = sorted(range(klen), key=lambda i: key[i])  # column order
    return "".join("".join(row[i] for row in rows) for i in order)


def row_trans_decrypt(cipher, key):
    klen = len(key)
    rows = len(cipher) // klen
    order = sorted(range(klen), key=lambda i: key[i])

    # split ciphertext into columns by order
    cols = {}
    idx = 0
    for i in order:
        cols[i] = cipher[idx:idx+rows]
        idx += rows

    # rebuild plaintext row by row
    return "".join("".join(cols[i][r] for i in range(klen)) for r in range(rows))


# === MAIN PROGRAM ===
def main():
    msg = input("Enter message: ")
    key = input("Enter key (letters only): ")
    
    encrypted = row_trans_encrypt(msg, key)
    print("\nEncrypted message:", encrypted)
    
    decrypted = row_trans_decrypt(encrypted, key)
    print("Decrypted back:", decrypted)

if __name__ == "__main__":
    main()


#DES

from Cryptodome.Cipher import DES

# take user key (DES requires 8 bytes)
key = input("Enter DES key (8 chars): ").encode("utf-8")
if len(key) != 8:
    # force 8-byte key by padding/trimming
    key = key.ljust(8, b' ')[:8]

# take message
msg = input("Enter a message: ")
msg += ' ' * (-len(msg) % 8)   # pad to multiple of 8 bytes

# create DES cipher (ECB mode)
des = DES.new(key, DES.MODE_ECB)

# encrypt
enc = des.encrypt(msg.encode())
print("Encrypted (Hex):", enc.hex())

# decrypt
dec = des.decrypt(enc).decode().rstrip()
print("Decrypted:", dec)

#AES

from Cryptodome.Cipher import AES

# take user key (AES requires 16, 24, or 32 bytes)
key = input("Enter AES key (16/24/32 chars): ").encode("utf-8")
if len(key) not in (16, 24, 32):
    # force 16-byte key by padding/trimming
    key = key.ljust(16, b' ')[:16]

# take message
msg = input("Enter a message: ")
msg = msg + ' ' * (-len(msg) % 16)   # pad to multiple of 16 bytes

# create AES cipher (ECB mode)
aes = AES.new(key, AES.MODE_ECB)

# encrypt
enc = aes.encrypt(msg.encode())
print("Encrypted (Hex):", enc.hex())

# decrypt
dec = aes.decrypt(enc).decode().rstrip()
print("Decrypted:", dec)

